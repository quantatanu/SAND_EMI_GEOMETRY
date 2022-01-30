//ROOT
#include "TFile.h"
#include "TH2F.h"
#include "TTreeReader.h"
#include "TTreeReaderValue.h"
#include "TApplication.h"
#include "TCanvas.h"
#include "TNtuple.h"

//STL
#include <fstream>
#include <iostream>
#include <string>


int main(int argc, char** argv)
{

    TString InFileName = argv[1];
    TString OutFileName = argv[2];
    std::ifstream infile(argv[1]);	 

	OutFileName = OutFileName + "_xyz.root";
	TApplication boundary("boundary", &argc, argv);
    TNtuple xyz("xyz","xyz","x:y:z");
	TH2F hyz("hyz","y vs z coordinates of the rock propapgation boundary", 8000, 2000, 2800, 8000, -600, 200);
    hyz.GetXaxis()->SetTitle("Z (cm)");
    hyz.GetYaxis()->SetTitle("Y (cm)");
    hyz.SetMarkerColor(kRed);          
    double x, y, z;
    printf ("----------------------------------\n");
    printf ("|    X (m)  |  Y (m)  |   Z (m)  |\n");
    printf ("----------------------------------\n");
    if(infile.is_open())
    {
        while (!infile.eof()) 
        {
            infile >> x >> y >> z;
            xyz.Fill(x,y,z);
			hyz.Fill(z*100,y*100);
            printf ("|   %5.2f   |   %5.2f |   %5.2f  |\n", x, y, z);
        }
    }
    printf ("----------------------------------\n");
    TFile OutFile(OutFileName, "RECREATE");
	OutFile.cd();
    xyz.Write();
	hyz.Write();
    OutFile.Write();
    OutFile.Close();


	TCanvas Cboundary("Cboundary","",0,0,1000,1000);
	hyz.Draw();
    Cboundary.Modified();
    Cboundary.Update();

	boundary.Run();
	return 0;
}
