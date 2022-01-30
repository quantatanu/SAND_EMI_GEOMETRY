/************************************************************************************************************************************************
 *                                                                                                                                              *
 *  Compile it using:                                                                                                                           *
 *                                                                                                                                              *
 *  g++ nameSomething.C `root-config --glibs` -lTreePlayer -lGeom -lEve -lEG -lRGL `root-config --cflags` -o ../DUNE_BIN/namesomething_gdml     *
 *                                                                                                                                              *
 *  Or just use the bash_alias defined compiler function "geom++":                                                                              *
 *                                                                                                                                              *
 *      geom++ nameSomething.C ../DUNE_BIN/namesomething_gdml                                                                                   *
 *                                                                                                                                              *
 *  Credit: this script has been taken from: https://github.com/gyang9/dunendggd, then modified                                                 *
 *  slightly to make it able to compile and run on the terminal.                                                                                * 
 *                                                                                                                                              *
************************************************************************************************************************************************/


#include <sstream>
#include <cassert>
#include <string>
#include <bits/stdc++.h>


//ROOT libraries
#include "TApplication.h"
#include "TString.h"
#include "TObjArray.h"
#include "TROOT.h"
#include "TGeoOpticalSurface.h"
#include "TGeoManager.h"
#include "TGLViewer.h"
#include "TPad.h"
#include "TVirtualPad.h"
#include "TSystem.h"
#include "TGeoMaterial.h"
#include "TGeoMedium.h"
#include "TGeoVolume.h"
#include "TStyle.h"
#include "TGLViewer.h"
#include "TCanvas.h"

#include "TEveLine.h"
#include "TEvePointSet.h"
#include "TEveGeoNode.h"
#include "TEveManager.h"
#include "TFile.h"


TString Ttrim(std::string input);
std::string trim(std::string input);

std::map<TString,Int_t> getMaterialKolor();
void isThereOverlap( TGeoManager *geo, Int_t checkoverlaps );
void paintingVolumes( TGeoManager *geo );
TEveLine *getEveLine();
TEvePointSet *getEvePointArgonCube(TGeoManager *geo);
TEvePointSet *getEvePointDipole(TGeoManager *geo);

int main(int argc, char *argv[])
{
    std::cout << "                                                                                   \n";
    std::cout << "###################################################################################\n";
    std::cout << "#            General GDML display program from DUNEGGD                            #\n";
    std::cout << "###################################################################################\n";
    std::cout << "                                                                                   \n";
    
    if (argc != 2){
        std::cout << "Error: a single input is accepted!\n";
        return 1;
    }
    
    if (trim(argv[1]).length() < 6 || trim(argv[1]).substr(trim(argv[1]).length() - 4) != "gdml"){
        std::cout << "Error: only a valid *.gdml file is accepted!\n";
        return 2;
    }
    
    TString filename = Ttrim(argv[1]);
    TApplication* disp = new TApplication("Geometry Display",&argc, argv);
    
    Bool_t drawbeam = kTRUE;
    Int_t checkoverlaps=0; 
    Int_t vislevel=10;

    TEveManager::Create();
    TFile::SetCacheFileDir(".");
    TGeoManager *geo2 = gEve->GetGeometry(filename);
    std::cout << "                                                                                   \n";
    if ( checkoverlaps ) isThereOverlap( geo2, checkoverlaps );
    std::cout << "                                                                                   \n";

    paintingVolumes( geo2 );

    TEveGeoTopNode* tn = new TEveGeoTopNode( geo2, geo2->GetTopNode() );
    tn->SetVisLevel(vislevel);
    gEve->AddGlobalElement(tn);
    if ( drawbeam )
    {
        TEveLine *eveline = getEveLine();
        gEve->AddGlobalElement( eveline );
    }

    TEvePointSet* markerArgonCube = getEvePointArgonCube( geo2 );
    gEve->AddGlobalElement(markerArgonCube);

    TEvePointSet* markerDipole = getEvePointDipole( geo2 );
    gEve->AddGlobalElement(markerDipole);

    std::cout << "                                                                                   \n";
    gEve->FullRedraw3D(kTRUE);
    std::cout << "                                                                                   \n";
    TGLViewer *v = gEve->GetDefaultGLViewer();
    v->GetClipSet()->SetClipType(TGLClip::EType(0));
    v->ColorSet().Background().SetColor(kMagenta+4);
    v->SetGuideState(TGLUtil::kAxesOrigin, kTRUE, kFALSE, 0);
    v->RefreshPadEditor(v);
    v->DoDraw();

    std::cout << "                                                                                   \n";
    std::cout << "###################################################################################\n";
    std::cout << "#                      Press CTRL + C to quit!                                    #\n";
    std::cout << "###################################################################################\n";
    std::cout << "                                                                                   \n";

    disp->Run();
    return 0;
}





//============================================
// getMaterialKolor
//============================================
std::map<TString,Int_t> getMaterialKolor(){
  std::map<TString,Int_t> KKolor;
  KKolor["Steel"] = kGreen;
  KKolor["Copper"] = kYellow;
  KKolor["Aluminum"] = kRed;
  KKolor["FR4"] = kGray;
  KKolor["Scintillator"] = kGray;
  return KKolor;
}

//============================================
// getKolor
//============================================
void isThereOverlap( TGeoManager *geo, Int_t checkoverlaps ){
    std::cout << "-------------------------- Checking Overlaps --------------------------------------\n";
    if ( checkoverlaps == 1 )
    {
    geo->CheckOverlaps(1e-5,"d");
    geo->PrintOverlaps();
    }
    else if ( checkoverlaps == 2 )
    {
    geo->CheckOverlaps(1e-5,"s10000000");
    geo->PrintOverlaps();
    }
    else
    std::cout << " WARNING: checkoverlaps input no defined" << "\n";
    std::cout << "-------------------------- Checking Overlaps --------------------------------------\n";
}

//============================================
// paintingVolumes
//============================================
void paintingVolumes( TGeoManager *geo ){
    Int_t PriKolor[] = {  2,  3,  4,  5,  6,  7,  8, 9, 28, 30, 38, 40, 41, 42, 46 };
    Int_t PriIndex = 0;
    std::map<TString,Int_t> materialKolor = getMaterialKolor();

    TGeoVolume *volume = NULL;
    TObjArray *volumes = geo->GetListOfVolumes();
    Int_t nvolumes = volumes->GetEntries();
    for ( int i = 0; i < nvolumes; i++ )
    {
        volume = (TGeoVolume*)volumes->At(i);
        volume->SetVisContainers(kTRUE);
        if ( TString(volume->GetName()).Contains("DetEnclosure"))
        {
            volume->SetVisibility(kFALSE);
            continue;
        }
        if ( TString(volume->GetMaterial()->GetName()).Contains("Air"))
        {
            volume->SetVisibility(kFALSE);
            continue;
        }

        if ( materialKolor[volume->GetMaterial()->GetName()] == 0 )
        {
            PriIndex = PriIndex == sizeof(PriKolor) /sizeof(PriKolor[0]) ? 0 : PriIndex + 1;
            volume->SetLineColor( PriKolor[PriIndex] );
        }
        else
        {
            volume->SetLineColor( materialKolor[volume->GetMaterial()->GetName()] );
        }

        Int_t daughters = volume->GetNdaughters();
        switch ( daughters )
        {
            case 0: volume->SetTransparency(100);
            case 1: volume->SetTransparency(80);
            case 2: volume->SetTransparency(60);
            case 3: volume->SetTransparency(40);
            default: volume->SetTransparency(20);
        }
    }
}

//============================================
// getEveLine
//============================================
TEveLine *getEveLine(){
    TEveLine* line = new TEveLine;
    line->SetMainColor(kRed);
    line->SetLineWidth(4);
    int pdg=14;
    int m1=0; int m2=0; int d1=0; int d2=0;
    double p=1.0;
    double beam_angle=0.101;
    double py=-p*sin(beam_angle);
    double pz= p*cos(beam_angle);
    double px=0;
    double vx=0;
    double vz=-762; //Front of hall at -762 in global coordinate system
    double hall_start_z_in_hall_coordinates=-15.02e2;// ~15m
    double hall_length=-2*hall_start_z_in_hall_coordinates;
    double hall_back_global=-762 + hall_length;
    double beam_entering_height=592.2 - hall_start_z_in_hall_coordinates*tan(0.101);
    double global_y0_height=335;
    double vy=beam_entering_height-global_y0_height;
    std::cout<<"Beam enters the hall at a height of "<<beam_entering_height<<" cm"<<"\n";
    std::cout<<"That is y= "<<vy<<" in the global coordinate system"<<"\n";
    int npoints=200;
    double step=hall_length/(1.0*npoints);
    for (int ipoint=0; ipoint<npoints; ipoint++)
    {
        double dz=step*ipoint;
        double dy=-dz*tan(beam_angle);
        double z=vz+dz;
        double y=vy+dy;
        std::cout << y << " " << z << "\n";
        line->SetNextPoint(0,y,z);
    }
    return line;
}
//============================================
// getEvePointArgonCube
//============================================
TEvePointSet *getEvePointArgonCube(TGeoManager *geo){
    //geo->cd("/volWorld_1/volDetEnclosure_0/volArgonCubeDetector_0/volArgonCubeCryostat_0/volReinforcedConcrete_0/volArgonCubeActive_0");
    TString pathname = "/volWorld_1/volDetEnclosure_0/volArgonCubeDetector_0/volArgonCubeCryostat_0/";
    pathname += "volReinforcedConcrete_0/volMoistureBarrier_0/volInsulationBoard2_0/";
    pathname += "volGREBoard2_0/volInsulationBoard1_0/volGREBoard1_0/volFireproofBoard_0/";
    pathname += "volSSMembrane_0/volArgonCubeService_0/volArgonCube_0/volArgonCubeActive_0";
    if ( geo->CheckPath(pathname) )
    {
    std::cout << " cd into : " << pathname << "\n";
    geo->cd(pathname);
    }
    //geo->cd(pathname);
    TGeoMatrix *active = gGeoManager->GetCurrentMatrix();
    double local_active[3]={0,0,0};
    double master_active[3]={0,0,0};
    active->LocalToMaster(local_active,master_active);
    std::cout<<"The center of ArgonCubeActive in the global coordinate system: \n"<<" ( "<<master_active[0]<<", "<<master_active[1]<<", "<<master_active[2]<<" )"<<"\n";

    geo->cd("/volWorld_1/volDetEnclosure_0");
    TGeoMatrix *enclosure = gGeoManager->GetCurrentMatrix();
    double local_enclosure[3]={0,0,0};
    double master_enclosure[3]={0,0,0};
    enclosure->LocalToMaster(local_enclosure,master_enclosure);
    std::cout<<"The center of DetEnclosure in the global coordinate system: \n"<<" ( "<<master_enclosure[0]<<", "<<master_enclosure[1]<<", "<<master_enclosure[2]<<" )"<<"\n";

    double active_in_enclosure[3]={0,0,0};
    enclosure->MasterToLocal(master_active,active_in_enclosure);

    std::cout<<"The center of ArgonCubeActive in the DetEnclosure coordinate system: \n"<<" ( "<<active_in_enclosure[0]<<", "<<active_in_enclosure[1]<<", "<<active_in_enclosure[2]<<" )"<<"\n";

    TEvePointSet *marker = new TEvePointSet(1);
    marker->SetName("ArgonCube Marker");
    marker->SetMarkerColor(6);
    marker->SetMarkerStyle(29);
    marker->SetMarkerSize(2);
    marker->SetPoint(0, master_active[0], master_active[1], master_active[2]);
    return marker;
}

//============================================
// getEvePointDipole
//============================================
TEvePointSet *getEvePointDipole(TGeoManager *geo){
    TString pathname = "/volWorld_1/volDetEnclosure_0/volIronDipole_0/innerDet_volume_0/";
    if ( geo->CheckPath(pathname) )
    {
    std::cout << " cd into : " << pathname << "\n";
    geo->cd(pathname);
    }
    //geo->cd(pathname);
    TGeoMatrix *active = gGeoManager->GetCurrentMatrix();
    double local_active[3]={0,0,0};
    double master_active[3]={0,0,0};
    active->LocalToMaster(local_active,master_active);
    std::cout<<"The center of Dipole in the global coordinate system: \n"<<" ( "<<master_active[0]<<", "<<master_active[1]<<", "<<master_active[2]<<" )"<<"\n";

    geo->cd("/volWorld_1/volDetEnclosure_0");
    TGeoMatrix *enclosure = gGeoManager->GetCurrentMatrix();
    double local_enclosure[3]={0,0,0};
    double master_enclosure[3]={0,0,0};
    enclosure->LocalToMaster(local_enclosure,master_enclosure);

    double active_in_enclosure[3]={0,0,0};
    enclosure->MasterToLocal(master_active,active_in_enclosure);
    std::cout<<"The center of Dipole in the DetEnclosure coordinate system: \n"<<" ( "<<active_in_enclosure[0]<<", "<<active_in_enclosure[1]<<", "<<active_in_enclosure[2]<<" )"<<"\n";

    TEvePointSet *marker = new TEvePointSet(1);
    marker->SetName("Dipole Marker");
    marker->SetMarkerColor(6);
    marker->SetMarkerStyle(29);
    marker->SetMarkerSize(2);
    marker->SetPoint(0, master_active[0], master_active[1], master_active[2]);
    return marker;
}



//============================================
// std string trimmer
//============================================
std::string trim(std::string input){
    std::string output;

    std::stringstream trimmer;  //trims white spaces in both ends
    trimmer << input;
    trimmer >> output;

    return output;
}



//============================================
// TString trimmer
//============================================
TString Ttrim(std::string input){
    TString output;

    std::stringstream trimmer;  //trims white spaces in both ends
    trimmer << input;
    trimmer >> output;

    return output;
}
