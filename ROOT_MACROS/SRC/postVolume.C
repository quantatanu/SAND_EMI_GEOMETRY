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
#include "TFile.h"
#include "TApplication.h"
#include "TROOT.h"
#include "TH2.h"
#include "TString.h"

//STL
#include <fstream>
#include <iostream>
#include <bits/stdc++.h>    //for math
#include <math.h> 
//____________________________________________________________________




int main(int argc, char** argv)
{
    //TString InFileName = argv[1];
    if (argc < 3)
    {
        std::cout << "\033[91mError: path to the txt file \"containing particle_name pre_vol post_vol x y z\"\n       and the length (wc -l) of the file must be provieded!\033[0m\n";
        return -1;
    }
    std::ifstream infile(argv[1]);

	TApplication circle("circle",&argc,argv);
    int i = 0, n = std::atoi(argv[2]);
    double z0 = 2390.89, y0 = -238.463; //center
    double dz = 0, dy = 0, theta = 0;
    double pi = 4*atan(1);
    TH2F pv("pv","The post volume",500,1950,2850,500,-700,200);
    TH1F ang_dist("ang_dist","angular distr. of rock. entry vertices", n/100, -30, 30);
    TH1F ang_dist2("ang_dist2","y/z of the circle", 1000, -500, 500);
    ang_dist.GetXaxis()->SetTitle("#theta (deg)");
    ang_dist.GetYaxis()->SetTitle("# of rock vertices");
    
    ang_dist2.GetXaxis()->SetTitle("y");
    TString particle, pre_vol, post_vol, xx, yy, zz;
    TString rock;
    Double_t x,y,z;
    if(infile.is_open())
    {
        while (!infile.eof()) 
        {
            infile >> particle >> pre_vol >> post_vol >> xx >> yy >> zz;

            x = xx.Atof();
            y = yy.Atof();
            z = zz.Atof();
            dz = - z + z0;
            dy = - y + y0;
            //theta = atan(dy/dz)*180./3.14156;
            theta = 180. * atan2(dy, dz)/pi;
            //theta = 2* 180. * atan(dy/(dz+sqrt(pow(dz,2)+pow(dy,2))))/pi;
            //theta = 180. * atan2(y, z)/pi;
            //std::cout << "atan (" << dy << "/" << dz << ") = " << theta << "\n";
            ang_dist.Fill(theta);
            ang_dist2.Fill(dy);
            if(post_vol.Contains("vol"))
            {
                rock = post_vol;
            }
            pv.Fill(z*100.0, y*100.0);
            //printf ("|   %-15s   |   %-15s |   %5.2f   |   %5.2f |   %10d / %10d  |\n",pre_vol.Data(), post_vol.Data(), y, z, i, n);
            i++;
        }
    }
    printf ("-----------------------\n");
    TCanvas *c1 = new TCanvas("c1","c1",900,600);
    c1->Divide(2,1);
    //c1->SetGrid();
    c1->cd(1);
    pv.Draw("colz");
    c1->Modified();
    c1->Update();
    c1->cd(2);
    ang_dist.Draw();
    //ang_dist2.Draw();
    c1->Modified();
    c1->Update();
    printf (" ROCK: %-10s\n", rock.Data());
    
    circle.Run(); 
    return 0;
}
