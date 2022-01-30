//ROOT
#include "TCanvas.h"
#include "TRandom3.h"
#include "TGraph.h"
#include "TProfile.h"
#include "TFile.h"
#include "TApplication.h"
#include "TROOT.h"
#include "TH1.h"
#include "TH2.h"
#include "TString.h"
#include "TMath.h"
#include "TStyle.h"
#include "TLegend.h"

//STL
#include <fstream>
#include <iostream>


//____________________________________________________________________
//void fitCircle(std::string InFile) {
int main(int argc, char** argv)
{
    if (argc < 3)
    {
        std::cout << "\033[91mError: path to the txt file and the number of line entries, required!!!\033[0m\n";
        return -1;
    }
    //TString InFileName = argv[1];
    std::ifstream infile(argv[1]);

	TApplication circle("circle",&argc,argv);
    int i = 0, n = std::atoi(argv[2]);

    TString post_vol, s_orig_prim_muminus, s_cross_prim_muminus, s_stuck_prim_muminus;
    TString s_orig_piminus, s_orig_piplus, s_cross_piminus, s_cross_piplus, s_stuck_piminus, s_stuck_piplus;
    TString rock;
    double orig_prim_muminus, cross_prim_muminus, stuck_prim_muminus;
    double orig_piminus, orig_piplus, cross_piminus, cross_piplus, stuck_piminus, stuck_piplus;
    
    double N0_muminus_prim, N0_muminus_orig;
    double N0_piminus, N0_piplus, N0_piminus_orig, N0_piplus_orig;
    
    double cross_muminus_prim_perc;
    double cross_piminus_perc, cross_piplus_perc;

    TH1F *h_cross_muminus_prim   = new TH1F("h_cross_muminus_prim","#mu^{-} primary", n, 0, n);

    if(infile.is_open())
    {
        while (!infile.eof()) 
        {
           infile >> post_vol >> s_cross_prim_muminus;
           std::cout << "post vol: " << post_vol << ", #: " << s_orig_prim_muminus << "\n";
           if (post_vol.Sizeof() <= 1)continue;
           cross_prim_muminus   = s_cross_prim_muminus.Atof();

           if (i==0)
           {
                N0_muminus_prim = cross_prim_muminus;
                std::cout << "NO: " << N0_muminus_prim << "\n";
           }

           cross_muminus_prim_perc = cross_prim_muminus*100./N0_muminus_prim;

           h_cross_muminus_prim->SetBinContent(i+1, cross_muminus_prim_perc);
           h_cross_muminus_prim->GetXaxis()->SetBinLabel(i+1, post_vol.Data());
           
           i++;
        }
    }

    printf ("\n---------- x -------------\n");

    h_cross_muminus_prim->SetMarkerStyle(21);
    h_cross_muminus_prim->SetMarkerSize(1.0);
    h_cross_muminus_prim->SetMarkerColor(kGreen+2);
    h_cross_muminus_prim->GetXaxis()->SetTitleOffset(1.5);
    h_cross_muminus_prim->GetYaxis()->SetTitle("\% of prim. #mu^{-} entering");
    h_cross_muminus_prim->GetXaxis()->SetTitle("volume");
    h_cross_muminus_prim->GetYaxis()->SetTitleOffset(1.5);
    

    gStyle->SetOptStat(0);

    TCanvas *c1 = new TCanvas("c1","c1",900,900);
    c1->Divide(2,1);
    c1->cd(1);
    gPad->SetGrid();
    h_cross_muminus_prim->Draw("P");
    c1->Update();
    
    
    circle.Run(); 
    return 0;
}
