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

#include <sstream>
#include <cassert>
#include <string>

#include <bits/stdc++.h>

TString Ttrim(std::string input);
std::string trim(std::string input);


int main(int argc, char *argv[])
{
    std::cout << "                                                                                   \n";
    std::cout << "###################################################################################\n";
    std::cout << "#                GDML Geometry Display Program from DUNE GGD                      #\n";
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
  
    gROOT->ProcessLine( "gErrorIgnoreLevel = kError;");


    TString filename = Ttrim(argv[1]);
    TApplication* disp = new TApplication("Geometry Display",&argc, argv);
    
	TGeoManager *geo = new TGeoManager();
    //Int_t VisLevel=5;
    Int_t VisLevel = 100;
    geo->Import(filename);
	geo->DefaultColors();


    std::cout << "                                                                                   \n";
    std::cout << "----------------------------- Checking Overlaps -----------------------------------\n";
	geo->CheckOverlaps(1e-5,"d");
 	geo->PrintOverlaps();
	geo->SetVisOption(1);
	geo->SetVisLevel(VisLevel);
    std::cout << "------------------------------------ Done! ----------------------------------------\n";
    std::cout << "                                                                                   \n";
    geo->GetTopVolume()->Print("Q");
	geo->GetTopVolume()->Draw("ogl");
	
	TGLViewer * vGeom = (TGLViewer *)gPad->GetViewer3D();
    vGeom->SetStyle(TGLRnrCtx::kOutline);
	vGeom->SetSmoothPoints(kTRUE);
	vGeom->SetLineScale(0.5);


    std::cout << "                                                                                   \n";
    std::cout << "###################################################################################\n";
    std::cout << "#                      Press CTRL + C to quit!                                    #\n";
    std::cout << "###################################################################################\n";
    std::cout << "                                                                                   \n";

    disp->Run();
    return 0;
}




std::string trim(std::string input)
{
    std::string output;

    std::stringstream trimmer;  //trims white spaces in both ends
    trimmer << input;
    trimmer >> output;

    return output;
}



TString Ttrim(std::string input)
{
    TString output;

    std::stringstream trimmer;  //trims white spaces in both ends
    trimmer << input;
    trimmer >> output;

    return output;
}
