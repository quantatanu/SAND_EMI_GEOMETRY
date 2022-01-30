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

    //TString post_vol, s_thickness, s_mu_rock, s_muminus_rock, s_muplus_rock, s_orig_prim_muminus, s_orig_primary_muplus, s_cross_prim_muminus, s_cross_prim_muplus, s_orig_sec_muminus, s_orig_sec_muplus, s_cross_sec_muminus, s_cross_sec_muplus;
    TString post_vol, s_orig_prim_muminus, s_cross_prim_muminus, s_stuck_prim_muminus;
    TString s_orig_piminus, s_orig_piplus, s_cross_piminus, s_cross_piplus, s_stuck_piminus, s_stuck_piplus;
    TString rock;
    double orig_prim_muminus, cross_prim_muminus, stuck_prim_muminus;
    double orig_piminus, orig_piplus, cross_piminus, cross_piplus, stuck_piminus, stuck_piplus;
    
    double N0_muminus_prim, N0_muminus_orig;
    double N0_piminus, N0_piplus, N0_piminus_orig, N0_piplus_orig;
    
    double cross_muminus_prim_perc;
    double cross_piminus_perc, cross_piplus_perc;

    TH1F *h_cross_muminus_prim_energy   = new TH1F("h_cross_muminus_prim_energy","#mu^{-} primary average energy", n, 0, n);
    TH1F *h_cross_muminus_sec_energy   = new TH1F("h_cross_muminus_sec_energy","#mu^{-} secondary average energy", n, 0, n);
    TH1F *h_cross_muminus_prim   = new TH1F("h_cross_muminus_prim","#mu^{-} primary", n, 0, n);
    TH1F *h_cross_muplus_prim    = new TH1F("h_cross_muplus_prim","#mu^{+} primary", n, 0, n);
    TH1F *h_cross_muminus_sec    = new TH1F("h_cross_muminus_sec","#mu^{-} secondary", n, 0, n);
    TH1F *h_cross_muplus_sec     = new TH1F("h_cross_muplus_sec","#mu^{+} secondary", n ,0 ,n);
    TH1F *h_cross_piminus        = new TH1F("h_cross_piminus","#pi^{-}",n, 0, n);
    TH1F *h_cross_piplus         = new TH1F("h_cross_piplus","#pi^{+}", n, 0, n);

    TH2F *cross_muminus_count_vs_energy = new TH2F("cross_muminus_count_vs_energy","\% count vs energy",100,0,100,100,0,100);

    if(infile.is_open())
    {
        while (!infile.eof()) 
        {
           infile >> post_vol >> s_orig_prim_muminus  >> s_cross_prim_muminus >> s_stuck_prim_muminus >> s_orig_piminus >> s_cross_piminus >> s_stuck_piminus >> s_orig_piplus >> s_cross_piplus >> s_stuck_piplus;
           if (post_vol.Sizeof() <= 1)continue;
           orig_prim_muminus    = s_orig_prim_muminus.Atof();
           cross_prim_muminus   = s_cross_prim_muminus.Atof();
           stuck_prim_muminus   = s_stuck_prim_muminus.Atof();
           orig_piminus         = s_orig_piminus.Atof();
           cross_piminus        = s_cross_piminus.Atof();
           stuck_piminus        = s_stuck_piminus.Atof();
           orig_piplus          = s_orig_piplus.Atof();
           cross_piplus         = s_cross_piplus.Atof();
           stuck_piplus        = s_stuck_piplus.Atof();
           //printf ("\n %-16s\t %8.2f\t %-8.2f\t %-8.2f\t %-8.2f\t %-8.2f\t %-8.2f\t %-8.2f\t %-8.2f\t %-8.2f\t %-8.2f\t %-8.2f\t %-8.2f", post_vol.Data() , orig_prim_muminus , orig_primary_muplus , orig_sec_muminus , orig_sec_muplus  , cross_prim_muminus , cross_prim_muplus , cross_sec_muminus , cross_sec_muplus , orig_piminus , orig_piplus , cross_piminus, cross_piplus);

           if (i==0)
           {
                N0_muminus_orig = orig_prim_muminus;
                N0_muminus_prim = cross_prim_muminus;
                N0_piminus_orig = orig_piminus;
                N0_piminus = cross_piminus;
                N0_piplus_orig = orig_piplus;
                N0_piplus = cross_piplus;
                //std::cout << "\n-----------\n" << N0_muminus_prim << ", " <<  N0_piminus << ", " << N0_piplus << "\n";
           }

           cross_muminus_prim_perc = cross_prim_muminus*100./N0_muminus_prim;
           cross_piminus_perc = cross_piminus*100./N0_piminus;
           cross_piplus_perc = cross_piplus*100./N0_piplus;
           /*cross_muminus_prim_perc = 100*(cross_prim_muminus/orig_prim_muminus)/(N0_muminus_prim/N0_muminus_orig);
           cross_piminus_perc = 100*(cross_piminus/orig_piminus)/(N0_piminus/N0_piminus_orig);
           cross_piplus_perc = 100*(cross_piplus/orig_piplus)/(N0_piplus/N0_piplus_orig);*/

           /*cross_muminus_prim_perc = cross_prim_muminus*100./N0_muminus_orig;
           cross_piminus_perc = cross_piminus*100./N0_piminus_orig;
           cross_piplus_perc = cross_piplus*100./N0_piplus_orig;*/



           //std::cout << cross_muminus_prim_perc << "\t\t" << cross_muplus_prim_perc << "\t\t" << cross_muminus_sec_perc << "\t\t" << cross_muplus_sec_perc << "\t\t" << cross_piminus_perc << "\t\t" << cross_piplus_perc << "\n";

           h_cross_muminus_prim->SetBinContent(i+1, cross_muminus_prim_perc);
           h_cross_muminus_prim->GetXaxis()->SetBinLabel(i+1, post_vol.Data());
           
           h_cross_piminus->SetBinContent(i+1, cross_piminus_perc);
           h_cross_piminus->GetXaxis()->SetBinLabel(i+1, post_vol.Data());
           
           h_cross_piplus->SetBinContent(i+1, cross_piplus_perc);
           h_cross_piplus->GetXaxis()->SetBinLabel(i+1, post_vol.Data());
           
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
    
    //pions
    h_cross_piminus->SetMarkerStyle(22);
    h_cross_piminus->SetMarkerSize(1.0);
    h_cross_piminus->SetMarkerColor(kBlack);
    h_cross_piminus->GetXaxis()->SetTitleOffset(1.5);
    h_cross_piminus->GetYaxis()->SetTitle("\% of #pi^{-} entering");
    h_cross_piminus->GetXaxis()->SetTitle("volume");
    h_cross_piminus->GetYaxis()->SetTitleOffset(1.5);

    h_cross_piplus->SetMarkerStyle(26);
    h_cross_piplus->SetMarkerSize(1.4);
    h_cross_piplus->SetMarkerColor(kGray+2);
    h_cross_piplus->GetXaxis()->SetTitleOffset(1.5);
    h_cross_piplus->GetYaxis()->SetTitle("\% of #pi^{+} entering");
    h_cross_piplus->GetXaxis()->SetTitle("volume");
    h_cross_piplus->GetYaxis()->SetTitleOffset(1.5);

    gStyle->SetOptStat(0);

    TCanvas *c1 = new TCanvas("c1","c1",900,900);
    c1->Divide(2,1);
    c1->cd(1);
    gPad->SetGrid();
    h_cross_muminus_prim->Draw("P");
    c1->Update();
    //TLegend *cross_mu_prim_leg = new TLegend(0.1,0.7,0.48,0.9);
    //cross_mu_prim_leg->SetHeader("#mu^{-}","C");
    //cross_mu_prim_leg->AddEntry(h_cross_muminus_prim,"primary #mu^{-} entering","p");
    //cross_mu_prim_leg->Draw(); 
    //c1->Update();
    
    c1->cd(2);
    gPad->SetGrid();
    h_cross_piminus->Draw("P");
    c1->Update();
    h_cross_piplus->Draw("SAME P");
    c1->Update();
    TLegend *cross_pi_leg = new TLegend(0.1,0.7,0.48,0.9);
    cross_pi_leg->SetHeader("#pi^{-}","C");
    cross_pi_leg->AddEntry(h_cross_piminus,"#pi^{-} entering","p");
    cross_pi_leg->AddEntry(h_cross_piplus,"#pi^{+} entering","p");
    cross_pi_leg->Draw(); 
    c1->Update();
    
    circle.Run(); 
    return 0;
}
