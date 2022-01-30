/************************************************************************************
 * Originally Rene Brun's code that generates random points on a circle with		*
 * some scatter and fits a circle to it, has been edited by Atanu Nath to now		*
 * take a TXT file containing the rock_propagation circular boundary				*
 * (coordinates of particle leaving the pre volume and entering the post volume)	*
 * coordinates in the form of 3 columns:											*
 *																					*
 *		x   y   z																	*
 *																					*	
 * This code must be compiles using root flags, the executable will then take		*
 * the txt file path as the only input and will plot the y-z data and fit a			*
 * circle on it and will give the center and the radius.							*
 *																					*
 * Note: this is hardcoded for KLOE, so the ranges are:								*
 *																					*
 *	Y = [ -600 cm,  +200 cm]														*
 *	Z = [+2000 cm, +2800 cm]														*
 *																					*
 * Radius initial guess 3 m, which is OK enough for any KLOE barrel shapes			*
 * around the center.																*
 * **********************************************************************************/

//Author: Rene Brun
//Edited by Atanu for data fitting
//ROOT
#include "TCanvas.h"
#include "TRandom3.h"
#include "TGraph.h"
#include "TMath.h"
#include "TArc.h"
#include "TVirtualFitter.h"
#include "TFile.h"
#include "TApplication.h"
#include "TROOT.h"
#include "TH1.h"
#include "TH2.h"
#include "TString.h"

//STL
#include <fstream>
#include <iostream>

TGraph *gr;

//____________________________________________________________________
void myfcn(Int_t &, Double_t *, Double_t &f, Double_t *par, Int_t) {
//minimisation function computing the sum of squares of residuals
    Int_t np = gr->GetN();
    f = 0;
    Double_t *z = gr->GetX();
    Double_t *y = gr->GetY();
    for (Int_t i=0;i<np;i++) {
        Double_t u = z[i] - par[0];
        Double_t v = y[i] - par[1];
        Double_t dr = par[2] - TMath::Sqrt(u*u+v*v);
        f += dr*dr;
    }
}

//____________________________________________________________________
//void fitCircle(std::string InFile) {
int main(int argc, char** argv)
{
    if (argc < 3)
    {
        std::cout << "\033[91mError: path to the txt file \"containing particle_name pre_vol post_vol x y z\"\n       and the length (wc -l) of the file must be provieded!\033[0m\n";
        return -1;
    }
    //TString InFileName = argv[1];
    std::ifstream infile(argv[1]);

	TApplication circle("circle",&argc,argv);
    TCanvas *c1 = new TCanvas("c1","c1",900,900);
    //c1->SetGrid();
    int i = 0, n = std::atoi(argv[2]);

    gr = new TGraph(n);
    gr->SetMarkerStyle(21);
    gr->SetMarkerSize(0.2);
    TString particle, pre_vol, post_vol, xx, yy, zz;
    TString rock;
    Double_t x,y,z;
    if(infile.is_open())
    {
        std::cout << __LINE__ << "\n";
        while (!infile.eof()) 
        {
            infile >> particle >> pre_vol >> post_vol >> xx >> yy >> zz;

            x = xx.Atof();
            y = yy.Atof();
            z = zz.Atof();
            if(post_vol.Contains("vol"))
            {
                rock = post_vol;
                //std::cout << "\033[33mYes " << post_vol << " contains vol, therefore, rock: " << rock << "\033[0m\n";
            }
            gr->SetPoint(i, z*100, y*100);
            //printf ("|   %-15s   |   %-15s |   %5.2f   |   %5.2f |   %10d / %10d  |\n",pre_vol.Data(), post_vol.Data(), y, z, i, n);
            i++;
        }
    }
    printf ("-----------------------\n");
    gr->SetTitle(pre_vol + "-" + post_vol + " boundary; Z (cm); Y (cm);");
    gr->Draw("AP");
    TH1F *frame = new TH1F("frame", rock + " start boundary", 1000, 1800, 2800);
    frame = c1->DrawFrame(1950,-700,2850,200);
    //frame->SetTitle(pre_vol + "-" + post_vol + " boundary");
    frame->GetXaxis()->SetTitle("Z (cm)");
    frame->GetXaxis()->SetTitleOffset(1.5);
    frame->GetYaxis()->SetTitle("Y (cm)");
    frame->GetYaxis()->SetTitleOffset(1.5);
    c1->Update();
    gr->SetTitle(rock + " start boundary; Z (cm); Y (cm);");
    gr->Draw("same P");
    c1->Update();
    printf (" ROCK: %-10s\n", rock.Data());
    
    
    //Fit a circle to the graph points
    TVirtualFitter::SetDefaultFitter("Minuit");  //default is Minuit
    TVirtualFitter *fitter = TVirtualFitter::Fitter(0, 3);
    fitter->SetFCN(myfcn);

    fitter->SetParameter(0, "z0",   2391, 0.1, 0,0);
    fitter->SetParameter(1, "y0",   -238.473, 0.1, 0,0);
    fitter->SetParameter(2, "R",    300, 0.1, 0,0);

    Double_t arglist[1] = {0};
    fitter->ExecuteCommand("MIGRAD", arglist, 0);

    //Draw the circle on top of the points
    double R  = fitter->GetParameter(2);
    double z0 = fitter->GetParameter(0);
    double y0 = fitter->GetParameter(1);
    //TArc *arc = new TArc(fitter->GetParameter(0), fitter->GetParameter(1), fitter->GetParameter(2));
    TArc *arc = new TArc(z0, y0, R);
    arc->SetFillStyle(3001); 
    arc->SetLineColor(kRed);
    arc->SetLineWidth(2);
    arc->SetLineStyle(5);
    arc->Draw();
    
    circle.Run(); 
    return 0;
}
