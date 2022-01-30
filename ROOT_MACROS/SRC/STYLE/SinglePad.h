#include <iostream>

#include "TCanvas.h"
#include "TString.h"
#include "TROOT.h"
#include "TStyle.h"
#include "TPaveStats.h"
#include "TH1.h"
#include "TH2.h"


class SinglePad{

    public:
        TCanvas *caname;
        TCanvas canvas(TString Caname, TH2F hist)
        {
           gStyle->SetCanvasPreferGL(kTRUE);

           caname = new TCanvas("caname", Caname + "_canvas", 0, 64, 1745, 975);
           //caname->Draw();
           std::cout << "Drawing: " << hist.GetName() << "\n";
           std::cout << "NEntries: " << hist.GetEntries() << "\n";
           gStyle->SetOptFit(1111);
           gStyle->SetPalette(57);
           gStyle->SetOptTitle(0);
           caname->SetHighLightColor(2);
           caname->Range(1787.5,-700,2912.5,300);
           caname->SetFillColor(0);
           caname->SetBorderMode(0);
           caname->SetBorderSize(2);
           caname->SetFrameBorderMode(0);
           caname->SetFrameLineWidth(2);
           caname->SetFrameBorderMode(0);
           
           TPaveStats *ptstats = new TPaveStats(0.6878944,0.7236287,0.8881239,0.8839662,"brNDC");
           ptstats->SetName("stats");
           ptstats->SetBorderSize(1);
           ptstats->SetFillColor(0);
           ptstats->SetTextAlign(12);
           ptstats->SetTextFont(22);
           TText *ptstats_LaTex = ptstats->AddText(hist.GetName());
           ptstats_LaTex->SetTextSize(0.03687764);
           ptstats_LaTex = ptstats->AddText("Entries = 4823676");
           ptstats_LaTex = ptstats->AddText("Mean x =   2441");
           ptstats_LaTex = ptstats->AddText("Mean y = -242.3");
           ptstats->SetOptStat(111);
           ptstats->SetOptFit(1);
           ptstats->Draw();
           hist.GetListOfFunctions()->Add(ptstats);
           ptstats->SetParent(&hist);

           Int_t ci;      // for color index setting
           TColor *color; // for color definition with alpha
           ci = TColor::GetColor("#000099");
           hist.SetLineColor(ci);

           ci = TColor::GetColor("#ff0000");
           hist.SetMarkerColor(ci);
           hist.GetXaxis()->SetTitle("Z (cm)");
           hist.GetXaxis()->SetLabelFont(32);
           hist.GetXaxis()->SetLabelSize(0.035);
           hist.GetXaxis()->SetTitleSize(0.05);
           hist.GetXaxis()->SetTitleOffset(1.02);
           hist.GetXaxis()->SetTitleFont(22);
           hist.GetYaxis()->SetTitle("Y (cm)");
           hist.GetYaxis()->SetDecimals();
           hist.GetYaxis()->SetLabelFont(32);
           hist.GetYaxis()->SetLabelSize(0.035);
           hist.GetYaxis()->SetTitleSize(0.05);
           hist.GetYaxis()->SetTitleOffset(1.05);
           hist.GetYaxis()->SetTitleFont(22);
           hist.GetZaxis()->SetLabelFont(42);
           hist.GetZaxis()->SetLabelSize(0.035);
           hist.GetZaxis()->SetTitleSize(0.035);
           hist.GetZaxis()->SetTitleFont(42);
           hist.Draw("colz");
           
           TPaveText *pt = new TPaveText(0.1626058,0.94,0.8373942,0.995,"blNDC");
           pt->SetName("title");
           pt->SetBorderSize(0);
           pt->SetFillColor(0);
           pt->SetFillStyle(0);
           pt->SetTextFont(22);
           pt->SetTextSize(0.04746836);
           TText *pt_LaTex = pt->AddText("Eevents in detector coords.");
           pt->Draw();
           caname->Modified();
           caname->cd();
           caname->SetSelected(caname);
           
        }


        void draw(TCanvas *canvas)
        {
            canvas->Draw();
        }

};
