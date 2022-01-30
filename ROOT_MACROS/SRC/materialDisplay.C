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


int main(int argc, char *argv[])
//void geoDisplay(TString filename)
{
    std::cout << "                                                                                   \n";
    std::cout << "-----------------------------------------------------------------------------------\n";
    std::cout << "                     GDML Overlap Checker Program from DUNEGGD                     \n";
    std::cout << "-----------------------------------------------------------------------------------\n";
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

    Bool_t checkoverlaps = kFALSE;
    TString label = "geom-test.root";
    Int_t PriKolor[] = {  2,  3,  4,  5,  6,  7,  8, 9, 28, 30, 38, 40, 41, 42, 46 };
    Int_t PriIndex = 0;
    std::map<TString,Int_t> Kolor;
    Kolor["Steel"] = kGreen;
    Kolor["Copper"] = kYellow;
    Kolor["Aluminum"] = kRed;
    Kolor["FR4"] = kGray;

    TGeoManager *geo2 = new TGeoManager("geo2","test");
    geo2->Import(filename);
    if ( checkoverlaps )
    {
        geo2->CheckOverlaps(1e-5,"d");
        geo2->CheckOverlaps(1e-5,"s10000000");
        geo2->PrintOverlaps();
    }
    geo2->SetVisLevel(20);
    TGeoVolume *volume = NULL;
    TObjArray *volumes = geo2->GetListOfVolumes();
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
        Int_t daughters = volume->GetNdaughters();
        std::cout << volume->GetName() << " NDaughters = " << volume->GetMaterial()->GetName() << " " << daughters << "\n";
        volume->SetLineColor(Kolor[volume->GetMaterial()->GetName()]);
        switch ( daughters )
        {
            case 0: volume->SetTransparency(100);
            case 1: volume->SetTransparency(80);
            case 2: volume->SetTransparency(60);
            case 3: volume->SetTransparency(40);
            default: volume->SetTransparency(10);
        }

    }
    geo2->Export(label);
    geo2->GetTopVolume()->Draw("ogl");
    
    
    std::cout << "                                                                                   \n";
    std::cout << "-----------------------------------------------------------------------------------\n";
    std::cout << "                       Press CTRL + C to quit!                                     \n";
    std::cout << "-----------------------------------------------------------------------------------\n";
    std::cout << "                                                                                   \n";

    disp->Run();
    return 0;
}




//============================================
//	std::string trimmer
//============================================
std::string trim(std::string input)
{
    std::string output;

    std::stringstream trimmer;  //trims white spaces in both ends
    trimmer << input;
    trimmer >> output;

    return output;
}


//============================================
//	TString trimmer
//============================================
TString Ttrim(std::string input)
{
    TString output;

    std::stringstream trimmer;  //trims white spaces in both ends
    trimmer << input;
    trimmer >> output;

    return output;
}

