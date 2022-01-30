#include "TFile.h"
#include "TH1F.h"
#include "TTreeReader.h"
#include "TTreeReaderValue.h"
#include <fstream>
#include <iostream>
#include <string>

void copy(std::string InFileName)
{

    ifstream infile(InFileName.c_str());	 
    TNtuple *xyz = new TNtuple("xyz","xyz","x:y:z");
    double x, y, z;
    if(infile.is_open())
    {
        while (!infile.eof()) 
        {
            infile >> x >> y >> z;
            std::cout << x << "\t " << y << "\t " << z << "\n";
            xyz->Fill(x,y,z);
        }
    }
    TFile *OutFile = new TFile("xyz.root","RECREATE");
	OutFile->cd();
    xyz->Write();
    OutFile->Write();
    OutFile->Close();
}
