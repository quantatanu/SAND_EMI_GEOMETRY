#include "PDG/MyPDGLib.h"

#include <iostream>
#include <cstddef>
#include <sstream>
#include <vector>
#include <stdexcept>
#include <assert.h>
#include <iterator>
#include <utility> 

//root classes
#include <TROOT.h>
#include <TFile.h>
#include <TTree.h>
#include <TBranch.h>
#include <TBits.h>
#include <TObjString.h>
#include <TString.h>
#include <TCanvas.h>
#include <TApplication.h>
#include <TDatabasePDG.h>
#include <TParticlePDG.h>
#include "TH2F.h"
#include "TH1F.h"
#include "TProfile.h"
#include "TCanvas.h"
#include "TStyle.h"
#include "TF1.h"
#include "TLegend.h"


template<typename T> class vect{
//template<int T> class vect{
    const  int _maxIndex;
    const  int _minIndex;
	std::vector<T> _data;
    public:
        vect( int minIndex,  int maxIndex):
        _minIndex(minIndex),
        _maxIndex(maxIndex)
        {
            _data=std::vector<T>(_maxIndex-_minIndex+1);
        }
    public:
      T& operator[] ( int x){
          assert(!(x<_minIndex || x> _maxIndex));
          return _data[x-_minIndex];
      } 
};




int main(int argc, char** argv){
    bool using_new_version = false; // StdHepReScat and G2NeutEvtCode branches available only for versions >= 2.5.1
    const int kNPmax = 10000;

    gStyle->SetCanvasPreferGL(true); //for colors

	std::string print = "", print2 = "", print3 = "", all_args = "";

	if (argc < 2)
	{
		std::cout << "\n\033[91m Error: at least the rotracker input file must be supplied!!! Exiting... \033[39m\n\n";
		return 1;
	}

	for (int args = 2; args < argc; args++)
	{
		all_args = all_args + "_" + argv[args];
	}

	if (all_args.find("-P") != std::string::npos)
	{
		std::cout << "Parameter -P passed => Full event display\n";
		print = "-P";
	}
	if (all_args.find("-Q") != std::string::npos)
	{
		std::cout << "Parameter -Q passed => Verbose rock process\n";
		print2 = "-Q";
	}
	if (all_args.find("-D") != std::string::npos)
	{
		std::cout << "Parameter -D passed => Plots will be displayed\n";
		print3 = "-D";
	}

    std::string Fname = argv[1];
	if (Fname.find(".root") == std::string::npos)
	{
		std::cout << "\n\033[91m Error: invalid rotracker input file!!! Exiting... \033[39m\n\n";
		return 2;
	}

    
	TApplication rack("rack",0,0);
    TString filename = argv[1];
    std::size_t found = Fname.find_last_of("/\\");
    Fname = Fname.substr(found+1);

    TFile file(filename, "READ");
    TTree * tree = (TTree *) file.Get("gRooTracker");
    assert(tree);

    TBits*      EvtFlags = 0;             // generator-specific event flags
    TObjString* EvtCode = 0;              // generator-specific string with 'event code'
    int         EvtNum;                   // event num.
    double      EvtXSec;                  // cross section for selected event (1E-38 cm2)
    double      EvtDXSec;                 // cross section for selected event kinematics (1E-38 cm2 /{K^n})
    double      EvtWght;                  // weight for that event
    double      EvtProb;                  // probability for that event (given cross section, path lengths, etc)
    double      EvtVtx[4];                // event vertex position in detector coord syst (in geom units)
    int         StdHepN;                  // number of particles in particle array 
    int         StdHepPdg   [kNPmax];     // stdhep-like particle array: pdg codes (& generator specific codes for pseudoparticles)
    int         StdHepStatus[kNPmax];     // stdhep-like particle array: generator-specific status code
    int         StdHepRescat[kNPmax];     // stdhep-like particle array: intranuclear rescattering code [ >= v2.5.1 ]
    double      StdHepX4    [kNPmax][4];  // stdhep-like particle array: 4-x (x, y, z, t) of particle in hit nucleus frame (fm)
    double      StdHepP4    [kNPmax][4];  // stdhep-like particle array: 4-p (px,py,pz,E) of particle in LAB frame (GeV)
    double      StdHepPolz  [kNPmax][3];  // stdhep-like particle array: polarization vector
    int         StdHepFd    [kNPmax];     // stdhep-like particle array: first daughter
    int         StdHepLd    [kNPmax];     // stdhep-like particle array: last  daughter 
    int         StdHepFm    [kNPmax];     // stdhep-like particle array: first mother
    int         StdHepLm    [kNPmax];     // stdhep-like particle array: last  mother
    int         G2NeutEvtCode;            // NEUT code for the current GENIE event [ >= v2.5.1 ]
    int         NuParentPdg;              // parent hadron pdg code
    int         NuParentDecMode;          // parent hadron decay mode
    double      NuParentDecP4 [4];        // parent hadron 4-momentum at decay
    double      NuParentDecX4 [4];        // parent hadron 4-position at decay
    double      NuParentProP4 [4];        // parent hadron 4-momentum at production
    double      NuParentProX4 [4];        // parent hadron 4-position at production
    int         NuParentProNVtx;          // parent hadron vtx id

    // get branches
    TBranch * brEvtFlags        = tree -> GetBranch ("EvtFlags");
    TBranch * brEvtCode         = tree -> GetBranch ("EvtCode");
    TBranch * brEvtNum          = tree -> GetBranch ("EvtNum");
    TBranch * brEvtXSec         = tree -> GetBranch ("EvtXSec");
    TBranch * brEvtDXSec        = tree -> GetBranch ("EvtDXSec");
    TBranch * brEvtWght         = tree -> GetBranch ("EvtWght");
    TBranch * brEvtProb         = tree -> GetBranch ("EvtProb");
    TBranch * brEvtVtx          = tree -> GetBranch ("EvtVtx");
    TBranch * brStdHepN         = tree -> GetBranch ("StdHepN");
    TBranch * brStdHepPdg       = tree -> GetBranch ("StdHepPdg");
    TBranch * brStdHepStatus    = tree -> GetBranch ("StdHepStatus");
    TBranch * brStdHepRescat    = (using_new_version) ? tree -> GetBranch ("StdHepRescat") : 0;
    TBranch * brStdHepX4        = tree -> GetBranch ("StdHepX4");
    TBranch * brStdHepP4        = tree -> GetBranch ("StdHepP4");
    TBranch * brStdHepPolz      = tree -> GetBranch ("StdHepPolz");
    TBranch * brStdHepFd        = tree -> GetBranch ("StdHepFd");
    TBranch * brStdHepLd        = tree -> GetBranch ("StdHepLd");
    TBranch * brStdHepFm        = tree -> GetBranch ("StdHepFm");
    TBranch * brStdHepLm        = tree -> GetBranch ("StdHepLm");
    TBranch * brG2NeutEvtCode   = (using_new_version) ? tree -> GetBranch ("G2NeutEvtCode") : 0;
    TBranch * brNuParentPdg     = tree -> GetBranch ("NuParentPdg");
    TBranch * brNuParentDecMode = tree -> GetBranch ("NuParentDecMode");
    TBranch * brNuParentDecP4   = tree -> GetBranch ("NuParentDecP4");
    TBranch * brNuParentDecX4   = tree -> GetBranch ("NuParentDecX4");
    TBranch * brNuParentProP4   = tree -> GetBranch ("NuParentProP4");     
    TBranch * brNuParentProX4   = tree -> GetBranch ("NuParentProX4");     
    TBranch * brNuParentProNVtx = tree -> GetBranch ("NuParentProNVtx");   

    // set address
    brEvtFlags        -> SetAddress ( &EvtFlags         );
    brEvtCode         -> SetAddress ( &EvtCode          );
    brEvtNum          -> SetAddress ( &EvtNum           );
    brEvtXSec         -> SetAddress ( &EvtXSec          );
    brEvtDXSec        -> SetAddress ( &EvtDXSec         );
    brEvtWght         -> SetAddress ( &EvtWght          );
    brEvtProb         -> SetAddress ( &EvtProb          );
    brEvtVtx          -> SetAddress (  EvtVtx           );
    brStdHepN         -> SetAddress ( &StdHepN          );
    brStdHepPdg       -> SetAddress (  StdHepPdg        );
    brStdHepStatus    -> SetAddress (  StdHepStatus     );
    if(using_new_version) {
    brStdHepRescat    -> SetAddress (  StdHepRescat     );
    }
    brStdHepX4        -> SetAddress (  StdHepX4         );
    brStdHepP4        -> SetAddress (  StdHepP4         );
    brStdHepPolz      -> SetAddress (  StdHepPolz       );
    brStdHepFd        -> SetAddress (  StdHepFd         );
    brStdHepLd        -> SetAddress (  StdHepLd         );
    brStdHepFm        -> SetAddress (  StdHepFm         );
    brStdHepLm        -> SetAddress (  StdHepLm         );
    if(using_new_version) {
    brG2NeutEvtCode   -> SetAddress ( &G2NeutEvtCode   );
    }
    brNuParentPdg     -> SetAddress ( &NuParentPdg     );
    brNuParentDecMode -> SetAddress ( &NuParentDecMode );
    brNuParentDecP4   -> SetAddress (  NuParentDecP4   );
    brNuParentDecX4   -> SetAddress (  NuParentDecX4   );
    brNuParentProP4   -> SetAddress (  NuParentProP4   );     
    brNuParentProX4   -> SetAddress (  NuParentProX4   );     
    brNuParentProNVtx -> SetAddress ( &NuParentProNVtx );   

    int n = tree->GetEntries(); 
	printf ("\n------------------------  SUMMARY  TABLE ------------------------");
    printf ("\nFILE: %s\n", Fname.c_str());
    printf("\nNumber of entries: %d", n);

    MyPDG my_pdg;

    std::map <int, int> stuck_particle_count, new_particle_count, crossed_particle_count, stopped_particle_count, decayed_particle_count, orig_particle_count;
    std::map <int, double> crossed_percentage, stuck_percentage;
	std::map <int, int> orig_particle_id, orig_particle_kid, orig_particle_mom, orig_particle_ist;    
	std::map <int, int> new_particle_id, new_particle_kid, new_particle_mom, new_particle_ist;    
	std::map <int, int> crossed_particle_id, crossed_particle_kid, crossed_particle_mom, crossed_particle_ist;   
	std::map <int, int> pdg;


    int electron_count=0, positron_count=0, mu_count = 0, amu_count = 0;
    double MinEnergy = 0, MaxEnergy = 10000;
	int nbinEnergyW = 50;
	int nbinEnergy = (MaxEnergy - MinEnergy)/nbinEnergyW;
    double MinMomentum = 0, MaxMomentum = 30000;
	int nbinMomentumW = 1;
	int nbinMomentum = (MaxMomentum - MinMomentum)/nbinMomentumW;
    double MinMass = 0, MaxMass = 1000;
	int nbinMassW = 1;
	int nbinMass = (MaxMass - MinMass)/nbinMassW;

    //for optimization
    double minE_muon = MaxEnergy, maxE_muon = minE_muon;
    double minP2_muon = pow(MaxMomentum,2), maxP2_muon = pow(MinMomentum,2);
    double minE_pion = MaxEnergy, maxE_pion = minE_pion;
    double minP2_pion = pow(MaxMomentum,2), maxP2_pion = pow(MinMomentum,2);

    double energy, mom_energy;
    double mass, mom_mass;
    double momentum2, mom_momentum2;
    int piminus_pdg = -211, mu_pdg = 13;  // as we will be using these two extensively
    double c = 299792458.0;
    double c2 = 89875517873681764.0;
    
    std::vector <int> allPdg;
    TParticlePDG *pdgSelf = new TParticlePDG();
	TParticlePDG *pdgMom = new TParticlePDG();
	
    int self, mom;  //pdg of the particle and that of its mom
    

    //HISTOGRAM DEFINITIONS AND STYLES
	//-------------------------------------------------------------------------------------------------------------------------------------------------------------
	// FOR MUONS
	//event coords distribution
	TH2F events_yz("events_yz","Eevents in detector coords.", (2900-1900), 1900, 2800, (200+1000), -1000, 200);
	events_yz.GetXaxis()->SetTitle("Z (cm)");
	events_yz.GetYaxis()->SetTitle("Y (cm)");
	events_yz.SetMarkerColor(kRed);

	double muon_mass = 105.6583755;
   //energy vs momentum TProfile
	TProfile crossed_muminus_mom_disp("crossed_muminus_mom_disp","E^2 vs p^2 distribution of the yoke-crossing #mu^{-}'s mom #mu^{-}", nbinMomentum, MinMomentum, pow(MaxMomentum,2));
	TProfile crossed_muminus_disp("crossed_muminus_disp","E^2 vs p^2 distribution of the yoke-crossing #mu^{-}", nbinMomentum, MinMomentum, pow(MaxMomentum,2));
	TProfile stuck_muminus_disp("stuck_muminus_disp","E^2 vs p^2 distribution of the yoke-stuck #mu^{-}", nbinMomentum, MinMomentum, pow(MaxMomentum,2));
	TProfile new_muminus_disp("new_muminus_disp","E^2 vs p^2 distribution of the post-yoke-new #mu^{-}", nbinMomentum, MinMomentum, pow(MaxMomentum,2));
	crossed_muminus_mom_disp.Sumw2();
	crossed_muminus_disp.Sumw2();
	stuck_muminus_disp.Sumw2();
	new_muminus_disp.Sumw2();
	crossed_muminus_mom_disp.GetYaxis()->SetTitle("E^{2} (MeV^{2})");	
	crossed_muminus_mom_disp.GetXaxis()->SetTitle("p^{2} (MeV^{2}/c^{2})");	
	crossed_muminus_mom_disp.GetYaxis()->SetTitleSize(0.05);	
	crossed_muminus_mom_disp.GetXaxis()->SetTitleSize(0.05);	
	crossed_muminus_mom_disp.GetYaxis()->SetTitleOffset(1.0);	
	crossed_muminus_mom_disp.GetXaxis()->SetTitleOffset(1.0);	
	crossed_muminus_mom_disp.SetMarkerStyle(4);
	crossed_muminus_mom_disp.SetMarkerSize(0.2);
	crossed_muminus_mom_disp.SetMarkerColor(kSpring);
	crossed_muminus_mom_disp.SetLineColor(kSpring);

	crossed_muminus_disp.GetYaxis()->SetTitle("E^{2} (MeV^{2})");	
	crossed_muminus_disp.GetXaxis()->SetTitle("p^{2} (MeV^{2}/c^{2})");
	crossed_muminus_disp.GetYaxis()->SetTitleSize(0.05);	
	crossed_muminus_disp.GetXaxis()->SetTitleSize(0.05);	
	crossed_muminus_disp.GetYaxis()->SetTitleOffset(1.0);	
	crossed_muminus_disp.GetXaxis()->SetTitleOffset(1.0);	
	crossed_muminus_disp.SetMarkerStyle(4);
	crossed_muminus_disp.SetMarkerSize(0.2);
	crossed_muminus_disp.SetMarkerColor(kGreen);
	crossed_muminus_disp.SetLineColor(kGreen);
	
	stuck_muminus_disp.GetYaxis()->SetTitle("E^{2} (MeV^{2})");	
	stuck_muminus_disp.GetXaxis()->SetTitle("p^{2} (MeV^{2}/c^{2})");
	stuck_muminus_disp.GetYaxis()->SetTitleSize(0.05);	
	stuck_muminus_disp.GetXaxis()->SetTitleSize(0.05);	
	stuck_muminus_disp.GetYaxis()->SetTitleOffset(1.0);	
	stuck_muminus_disp.GetXaxis()->SetTitleOffset(1.0);	
	stuck_muminus_disp.SetMarkerStyle(4);
	stuck_muminus_disp.SetMarkerSize(0.2);
	stuck_muminus_disp.SetMarkerColor(kGray+2);
	stuck_muminus_disp.SetLineColor(kGray+2);
	
	new_muminus_disp.GetYaxis()->SetTitle("E^{2} (MeV^{2})");	
	new_muminus_disp.GetXaxis()->SetTitle("p^{2} (MeV^{2}/c^{2})");
	new_muminus_disp.GetYaxis()->SetTitleOffset(1.0);	
	new_muminus_disp.GetXaxis()->SetTitleOffset(1.0);	
	new_muminus_disp.GetYaxis()->SetTitleSize(0.05);	
	new_muminus_disp.GetXaxis()->SetTitleSize(0.05);	
	new_muminus_disp.SetMarkerSize(0.2);
	new_muminus_disp.SetMarkerStyle(4);
	new_muminus_disp.SetMarkerColor(kGray);
	new_muminus_disp.SetLineColor(kGray);

	//mass distribution
	TH1F crossed_muminus_mom_mass("crossed_muminus_mom_mass","sqrt(E^{2} - p^{2}) distribution of the yoke-crossing #mu^{-}'s mom #mu^{-}", nbinMass, MinMass, MaxMass);
	TH1F crossed_muminus_mass("crossed_muminus_mass","sqrt(E^{2} - p^{2}) distribution of the yoke-crossing #mu^{-}", nbinMass, MinMass, MaxMass);
	TH1F new_muminus_mass("new_muminus_mass","sqrt(E^{2} - p^{2}) distribution of the post-yoke-new #mu^{-}", nbinMass, MinMass, MaxMass);
	TH1F stuck_muminus_mass("stuck_muminus_mass","sqrt(E^{2} - p^{2}) distribution of the yoke-stuck #mu^{-}", nbinMass, MinMass, MaxMass);
    
	crossed_muminus_mom_mass.GetXaxis()->SetTitle("M (MeV/c^{2})");
    crossed_muminus_mass.GetXaxis()->SetTitle("M (MeV/c^{2})");
	new_muminus_mass.GetXaxis()->SetTitle("M (MeV/c^{2})");
	crossed_muminus_mom_mass.GetYaxis()->SetTitleOffset(1.0);	
	crossed_muminus_mom_mass.GetXaxis()->SetTitleOffset(1.0);	
	crossed_muminus_mom_mass.GetYaxis()->SetTitleSize(0.05);	
	crossed_muminus_mom_mass.GetXaxis()->SetTitleSize(0.05);	
	crossed_muminus_mass.GetYaxis()->SetTitleOffset(1.0);	
	crossed_muminus_mass.GetXaxis()->SetTitleOffset(1.0);	
	crossed_muminus_mass.GetYaxis()->SetTitleSize(0.05);	
	crossed_muminus_mass.GetXaxis()->SetTitleSize(0.05);	
	stuck_muminus_mass.GetXaxis()->SetTitle("M (MeV/c^{2})");
	stuck_muminus_mass.GetYaxis()->SetTitleOffset(1.0);	
	stuck_muminus_mass.GetXaxis()->SetTitleOffset(1.0);	
	stuck_muminus_mass.GetYaxis()->SetTitleSize(0.05);	
	stuck_muminus_mass.GetXaxis()->SetTitleSize(0.05);	
	new_muminus_mass.GetYaxis()->SetTitleOffset(1.0);	
	new_muminus_mass.GetXaxis()->SetTitleOffset(1.0);	
	new_muminus_mass.GetYaxis()->SetTitleSize(0.05);	
	new_muminus_mass.GetXaxis()->SetTitleSize(0.05);	
	
    crossed_muminus_mom_mass.SetFillColorAlpha(kSpring+1,0.5);
    crossed_muminus_mass.SetFillColorAlpha(kGreen,0.5);
    new_muminus_mass.SetFillColorAlpha(kRed,0.5);
    stuck_muminus_mass.SetFillColorAlpha(kGray+2,0.5);

    crossed_muminus_mom_mass.SetLineColor(kSpring+2);
    crossed_muminus_mass.SetLineColor(kGreen+2);
    new_muminus_mass.SetLineColor(kRed+1);
    stuck_muminus_mass.SetLineColor(kBlack);
   
    //energy distribution
	TH1F crossed_muminus_mom_energy("crossed_muminus_mom_energy","Energy distribution of the yoke-crossing #mu^{-}'s mom #mu^{-}", nbinEnergy, 0, MaxEnergy);
	TH1F crossed_muminus_energy("crossed_muminus_energy","Energy distribution of the yoke-crossing #mu^{-}", nbinEnergy, 0, MaxEnergy);
	TH1F stuck_muminus_energy("stuck_muminus_energy","Energy distribution of the stuck #mu^{-}", nbinEnergy, 0, MaxEnergy);
	TH1F new_muminus_energy("new_muminus_energy","Energy distribution of the post-yoke new #mu^{-}", nbinEnergy, 0, MaxEnergy);
	
    crossed_muminus_mom_energy.GetXaxis()->SetTitle("E (MeV)");
    crossed_muminus_energy.GetXaxis()->SetTitle("E (MeV)");
	new_muminus_energy.GetXaxis()->SetTitle("E (MeV)");
	stuck_muminus_energy.GetXaxis()->SetTitle("E (MeV)");
	crossed_muminus_mom_energy.GetYaxis()->SetTitleOffset(1.0);	
	crossed_muminus_mom_energy.GetXaxis()->SetTitleOffset(1.0);	
	crossed_muminus_mom_energy.GetYaxis()->SetTitleSize(0.05);	
	crossed_muminus_mom_energy.GetXaxis()->SetTitleSize(0.05);	
	crossed_muminus_energy.GetYaxis()->SetTitleOffset(1.0);	
	crossed_muminus_energy.GetXaxis()->SetTitleOffset(1.0);	
	crossed_muminus_energy.GetYaxis()->SetTitleSize(0.05);	
	crossed_muminus_energy.GetXaxis()->SetTitleSize(0.05);	
	stuck_muminus_energy.GetXaxis()->SetTitle("M (MeV/c^{2})");
	stuck_muminus_energy.GetYaxis()->SetTitleOffset(1.0);	
	stuck_muminus_energy.GetXaxis()->SetTitleOffset(1.0);	
	stuck_muminus_energy.GetYaxis()->SetTitleSize(0.05);	
	stuck_muminus_energy.GetXaxis()->SetTitleSize(0.05);	
	new_muminus_energy.GetYaxis()->SetTitleOffset(1.0);	
	new_muminus_energy.GetXaxis()->SetTitleOffset(1.0);	
	new_muminus_energy.GetYaxis()->SetTitleSize(0.05);	
	new_muminus_energy.GetXaxis()->SetTitleSize(0.05);	
	
    crossed_muminus_mom_energy.SetFillColorAlpha(kSpring+8,0.5);
    crossed_muminus_energy.SetFillColorAlpha(kGreen+2,0.5);
    new_muminus_energy.SetFillColorAlpha(kRed,0.5);
    stuck_muminus_energy.SetFillColorAlpha(kGray+2,0.5);
    
	crossed_muminus_mom_energy.SetLineColor(kGreen+3);
    crossed_muminus_energy.SetLineColor(kGreen+5);
    new_muminus_energy.SetLineColor(kRed+1);
    stuck_muminus_energy.SetLineColor(kBlack);
	//-------------------------------------------------------------------------------------------------------------------------------------------------------------
	// FOR PIONS

	double pion_mass = 139.57018;
   //energy vs momentum TProfile
	TProfile crossed_piminus_mom_disp("crossed_piminus_mom_disp","E^2 vs p^2 distribution of the yoke-crossing #pi^{-}^{-}'s mom #pi^{-}^{-}", nbinMomentum, MinMomentum, pow(MaxMomentum,2));
	TProfile crossed_piminus_disp("crossed_piminus_disp","E^2 vs p^2 distribution of the yoke-crossing #pi^{-}^{-}", nbinMomentum, MinMomentum, pow(MaxMomentum,2));
	TProfile stuck_piminus_disp("stuck_piminus_disp","E^2 vs p^2 distribution of the yoke-stuck #pi^{-}^{-}", nbinMomentum, MinMomentum, pow(MaxMomentum,2));
	TProfile new_piminus_disp("new_piminus_disp","E^2 vs p^2 distribution of the post-yoke-new #pi^{-}^{-}", nbinMomentum, MinMomentum, pow(MaxMomentum,2));
	crossed_piminus_mom_disp.Sumw2();
	crossed_piminus_disp.Sumw2();
	stuck_piminus_disp.Sumw2();
	new_piminus_disp.Sumw2();
	crossed_piminus_mom_disp.GetYaxis()->SetTitle("E^2 (MeV^{2})");	
	crossed_piminus_mom_disp.GetXaxis()->SetTitle("p^{2} (MeV^{2}/c^{2})");	
	crossed_piminus_mom_disp.GetYaxis()->SetTitleOffset(1.0);	
	crossed_piminus_mom_disp.GetXaxis()->SetTitleOffset(1.0);	
	crossed_piminus_mom_disp.GetYaxis()->SetTitleSize(0.05);	
	crossed_piminus_mom_disp.GetXaxis()->SetTitleSize(0.05);	
	crossed_piminus_disp.GetYaxis()->SetTitleOffset(1.0);	
	crossed_piminus_disp.GetXaxis()->SetTitleOffset(1.0);	
	crossed_piminus_disp.GetYaxis()->SetTitleSize(0.05);	
	crossed_piminus_disp.GetXaxis()->SetTitleSize(0.05);	
	stuck_piminus_disp.GetXaxis()->SetTitle("M (MeV/c^{2})");
	stuck_piminus_disp.GetYaxis()->SetTitleOffset(1.0);	
	stuck_piminus_disp.GetXaxis()->SetTitleOffset(1.0);	
	stuck_piminus_disp.GetYaxis()->SetTitleSize(0.05);	
	stuck_piminus_disp.GetXaxis()->SetTitleSize(0.05);	
	new_piminus_disp.GetYaxis()->SetTitleOffset(1.0);	
	new_piminus_disp.GetXaxis()->SetTitleOffset(1.0);	
	new_piminus_disp.GetYaxis()->SetTitleSize(0.05);	
	new_piminus_disp.GetXaxis()->SetTitleSize(0.05);	
	
    crossed_piminus_mom_disp.SetMarkerStyle(4);
	crossed_piminus_mom_disp.SetMarkerSize(0.2);
	crossed_piminus_mom_disp.SetMarkerColor(kSpring);
	crossed_piminus_mom_disp.SetLineColor(kSpring);

	crossed_piminus_disp.GetYaxis()->SetTitle("E^2 (MeV^{2})");	
	crossed_piminus_disp.GetXaxis()->SetTitle("p^{2} (MeV^{2}/c^{2})");
	crossed_piminus_disp.SetMarkerStyle(4);
	crossed_piminus_disp.SetMarkerSize(0.2);
	crossed_piminus_disp.SetMarkerColor(kGreen);
	crossed_piminus_disp.SetLineColor(kGreen);
	
	stuck_piminus_disp.GetYaxis()->SetTitle("E^2 (MeV^{2})");	
	stuck_piminus_disp.GetXaxis()->SetTitle("p^{2} (MeV^{2}/c^{2})");
	stuck_piminus_disp.SetMarkerStyle(4);
	stuck_piminus_disp.SetMarkerSize(0.2);
	stuck_piminus_disp.SetMarkerColor(kGray+2);
	stuck_piminus_disp.SetLineColor(kGray+2);
	
	new_piminus_disp.GetYaxis()->SetTitle("E^2 (MeV^{2})");	
	new_piminus_disp.GetXaxis()->SetTitle("p^{2} (MeV^{2}/c^{2})");
	new_piminus_disp.SetMarkerSize(0.2);
	new_piminus_disp.SetMarkerStyle(4);
	new_piminus_disp.SetMarkerColor(kGray);
	new_piminus_disp.SetLineColor(kGray);

	//mass distribution
	TH1F crossed_piminus_mom_mass("crossed_piminus_mom_mass","sqrt(E^{2} - p^{2}) distribution of the yoke-crossing #piminus^{-}'s mom #piminus^{-}", nbinMass, MinMass, MaxMass);
	TH1F crossed_piminus_mass("crossed_piminus_mass","sqrt(E^{2} - p^{2}) distribution of the yoke-crossing #piminus^{-}", nbinMass, MinMass, MaxMass);
	TH1F new_piminus_mass("new_piminus_mass","sqrt(E^{2} - p^{2}) distribution of the post-yoke-new #piminus^{-}", nbinMass, MinMass, MaxMass);
	TH1F stuck_piminus_mass("stuck_piminus_mass","sqrt(E^{2} - p^{2}) distribution of the yoke-stuck #piminus^{-}", nbinMass, MinMass, MaxMass);
    
	crossed_piminus_mom_mass.GetXaxis()->SetTitle("MeV/c^{2}");
    crossed_piminus_mass.GetXaxis()->SetTitle("MeV/c^{2}");
	new_piminus_mass.GetXaxis()->SetTitle("MeV/c^{2}");
	stuck_piminus_mass.GetXaxis()->SetTitle("MeV/c^{2}");
	crossed_piminus_mom_mass.GetYaxis()->SetTitleOffset(1.0);	
	crossed_piminus_mom_mass.GetXaxis()->SetTitleOffset(1.0);	
	crossed_piminus_mom_mass.GetYaxis()->SetTitleSize(0.05);	
	crossed_piminus_mom_mass.GetXaxis()->SetTitleSize(0.05);	
	crossed_piminus_mass.GetYaxis()->SetTitleOffset(1.0);	
	crossed_piminus_mass.GetXaxis()->SetTitleOffset(1.0);	
	crossed_piminus_mass.GetYaxis()->SetTitleSize(0.05);	
	crossed_piminus_mass.GetXaxis()->SetTitleSize(0.05);	
	stuck_piminus_mass.GetXaxis()->SetTitle("M (MeV/c^{2})");
	stuck_piminus_mass.GetYaxis()->SetTitleOffset(1.0);	
	stuck_piminus_mass.GetXaxis()->SetTitleOffset(1.0);	
	stuck_piminus_mass.GetYaxis()->SetTitleSize(0.05);	
	stuck_piminus_mass.GetXaxis()->SetTitleSize(0.05);	
	new_piminus_mass.GetYaxis()->SetTitleOffset(1.0);	
	new_piminus_mass.GetXaxis()->SetTitleOffset(1.0);	
	new_piminus_mass.GetYaxis()->SetTitleSize(0.05);	
	new_piminus_mass.GetXaxis()->SetTitleSize(0.05);	
	
    crossed_piminus_mom_mass.SetFillColorAlpha(kSpring+1,0.5);
    crossed_piminus_mass.SetFillColorAlpha(kGreen,0.5);
    new_piminus_mass.SetFillColorAlpha(kRed,0.5);
    stuck_piminus_mass.SetFillColorAlpha(kGray+2,0.5);

    crossed_piminus_mom_mass.SetLineColor(kSpring+2);
    crossed_piminus_mass.SetLineColor(kGreen+2);
    new_piminus_mass.SetLineColor(kRed+1);
    stuck_piminus_mass.SetLineColor(kBlack);
   
    //energy distribution
	TH1F crossed_piminus_mom_energy("crossed_piminus_mom_energy","Energy distribution of the yoke-crossing #piminus^{-}'s mom #piminus^{-}", nbinEnergy, 0, MaxEnergy);
	TH1F crossed_piminus_energy("crossed_piminus_energy","Energy distribution of the yoke-crossing #piminus^{-}", nbinEnergy, 0, MaxEnergy);
	TH1F stuck_piminus_energy("stuck_piminus_energy","Energy distribution of the stuck #piminus^{-}", nbinEnergy, 0, MaxEnergy);
	TH1F new_piminus_energy("new_piminus_energy","Energy distribution of the post-yoke new #piminus^{-}", nbinEnergy, 0, MaxEnergy);
	
    crossed_piminus_mom_energy.GetXaxis()->SetTitle("MeV");
    crossed_piminus_energy.GetXaxis()->SetTitle("MeV");
	new_piminus_energy.GetXaxis()->SetTitle("MeV");
	stuck_piminus_energy.GetXaxis()->SetTitle("MeV");
	crossed_piminus_mom_energy.GetYaxis()->SetTitleOffset(1.0);	
	crossed_piminus_mom_energy.GetXaxis()->SetTitleOffset(1.0);	
	crossed_piminus_mom_energy.GetYaxis()->SetTitleSize(0.05);	
	crossed_piminus_mom_energy.GetXaxis()->SetTitleSize(0.05);	
	crossed_piminus_energy.GetYaxis()->SetTitleOffset(1.0);	
	crossed_piminus_energy.GetXaxis()->SetTitleOffset(1.0);	
	crossed_piminus_energy.GetYaxis()->SetTitleSize(0.05);	
	crossed_piminus_energy.GetXaxis()->SetTitleSize(0.05);	
	stuck_piminus_energy.GetXaxis()->SetTitle("M (MeV/c^{2})");
	stuck_piminus_energy.GetYaxis()->SetTitleOffset(1.0);	
	stuck_piminus_energy.GetXaxis()->SetTitleOffset(1.0);	
	stuck_piminus_energy.GetYaxis()->SetTitleSize(0.05);	
	stuck_piminus_energy.GetXaxis()->SetTitleSize(0.05);	
	new_piminus_energy.GetYaxis()->SetTitleOffset(1.0);	
	new_piminus_energy.GetXaxis()->SetTitleOffset(1.0);	
	new_piminus_energy.GetYaxis()->SetTitleSize(0.05);	
	new_piminus_energy.GetXaxis()->SetTitleSize(0.05);	
	
    crossed_piminus_mom_energy.SetFillColorAlpha(kSpring+8,0.5);
    crossed_piminus_energy.SetFillColorAlpha(kGreen+2,0.5);
    new_piminus_energy.SetFillColorAlpha(kRed,0.5);
    stuck_piminus_energy.SetFillColorAlpha(kGray+2,0.5);
    
	crossed_piminus_mom_energy.SetLineColor(kGreen+3);
    crossed_piminus_energy.SetLineColor(kGreen+5);
    new_piminus_energy.SetLineColor(kRed+1);
    stuck_piminus_energy.SetLineColor(kBlack);
	//-------------------------------------------------------------------------------------------------------------------------------------------------------------


    for(int i=0; i < tree->GetEntries(); i++) 
    {
        tree->GetEntry(i);
        if (print == "-P")
        {   
            printf("\n ******************************************************************************  EVENT  START  ****************************************************************************************************");
            printf("\n Event code                 : %s", EvtCode->String().Data());
            printf("\n Event x-section            : %10.5f * 1E-38* cm^2",  EvtXSec);
            printf("\n Event kinematics x-section : %10.5f * 1E-38 * cm^2/{K^n}", EvtDXSec);
            printf("\n Event weight               : %10.8f", EvtWght);
            printf("\n Event vertex               : x = %8.2f mm, y = %8.2f mm, z = %8.2f mm", EvtVtx[0], EvtVtx[1], EvtVtx[2]);
            printf("\n *Particle list:");
            printf("\n --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------");
            printf("\n | ID  | IST | PARTICLE            (PDG)       |   RESCAT  |   MOTHER  |  DAUGHTER |       P_X     |      P_Y      |      P_Z     |       E       |        X      |        Y      |        Z      |");
            printf("\n |     |     |                                 |           |           |           |    (GeV/c)    |    (GeV/c)    |   (GeV/c)    |     (GeV)     |       (m)     |       (m)     |       (m)     |");
            printf("\n --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------");
        }
		//filling event coords in detector coords (cm)
		events_yz.Fill(100*EvtVtx[2], 100*EvtVtx[1]);

        for(int ip = 0; ip < StdHepN; ip++) 
        {
			self = StdHepPdg[ip];
			mom = StdHepPdg[StdHepFm[ip]];
            
            energy = StdHepP4[ip][3]*1000.;        
            mom_energy = StdHepP4[StdHepFm[ip]][3]*1000.;        
            
            momentum2 = (pow(StdHepP4[ip][0],2) + pow(StdHepP4[ip][1],2) + pow(StdHepP4[ip][2],2))*1000000;
            mom_momentum2 = (pow(StdHepP4[StdHepFm[ip]][0],2) + pow(StdHepP4[StdHepFm[ip]][1],2) + pow(StdHepP4[StdHepFm[ip]][2],2))*1000000;

            mass = sqrt(pow(energy,2) - momentum2);
            mom_mass = sqrt(pow(mom_energy,2) - mom_momentum2);

			if(StdHepStatus[ip] == -1)orig_particle_count[self]++;		//all particles that ever existed inside the yoke

			if (std::find(allPdg.begin(), allPdg.end(), StdHepPdg[ip]) == allPdg.end()) 
			{
				  // someName not in name, add it
				  //allPdg.push_back(self);
				  allPdg.push_back(StdHepPdg[ip]);
			}
            if (print == "-P")
            {   
                printf("\n | %-3d | %-3d | %-20s%-10d  | %-6d    | %-3d | %-3d | %-3d | %-3d | %+.2e     | %+.2e     | %+.2e    | %.2e      | %+.2e     | %+.2e     | %+.2e     |",
                ip, StdHepStatus[ip],  my_pdg.GetName(StdHepPdg[ip]).c_str(), StdHepPdg[ip], StdHepRescat[ip], 
                StdHepFm[ip],  StdHepLm[ip], StdHepFd[ip],  StdHepLd[ip],
                StdHepP4[ip][0], StdHepP4[ip][1], StdHepP4[ip][2], StdHepP4[ip][3],
                StdHepX4[ip][0], StdHepX4[ip][1], StdHepX4[ip][2]);
				
			}
			
            pdg[self] = StdHepPdg[ip];

			if (StdHepStatus[ip] == 1)
			{
				if (print2 == "-Q")printf("\n ..................................................................................................................................................................................................");
				if (StdHepPdg[ip] == StdHepPdg[StdHepFm[ip]] && ip == StdHepFd[StdHepFm[ip]] && StdHepStatus[StdHepFm[ip]] == -1)
				{
					if (print2 == "-Q")
					{
						printf("\n\033[92m\t%s has crossed the yoke\033[0m", my_pdg.GetName(StdHepPdg[ip]).c_str());
					}
					crossed_particle_count[self]++;
					if((StdHepPdg[ip])==mu_pdg)
                    {
                        if(energy>maxE_muon)maxE_muon=energy;
                        if(energy<minE_muon)minE_muon=energy;
                        if(momentum2>maxP2_muon)maxP2_muon=momentum2;
                        if(momentum2<minP2_muon)minP2_muon=momentum2;
                        crossed_muminus_mass.Fill(mass);  
                        crossed_muminus_mom_mass.Fill(mom_mass); 
                        crossed_muminus_energy.Fill(energy);  
                        crossed_muminus_mom_energy.Fill(mom_energy);
						crossed_muminus_mom_disp.Fill(mom_momentum2, pow(mom_energy,2));
						crossed_muminus_disp.Fill(momentum2, pow(energy,2));
                    }
					if((StdHepPdg[ip])==piminus_pdg)
                    { 
                        if(energy>maxE_pion)maxE_pion=energy;
                        if(energy<minE_pion)minE_pion=energy;
                        if(momentum2>maxP2_pion)maxP2_pion=momentum2;
                        if(momentum2<minP2_pion)minP2_pion=momentum2;
                        crossed_piminus_mass.Fill(mass);  
                        crossed_piminus_mom_mass.Fill(mom_mass); 
                        crossed_piminus_energy.Fill(energy);  
                        crossed_piminus_mom_energy.Fill(mom_energy);
						crossed_piminus_mom_disp.Fill(mom_momentum2, pow(mom_energy,2));
						crossed_piminus_disp.Fill(momentum2, pow(energy,2));
                    }
				} 
				if (StdHepPdg[ip] != StdHepPdg[StdHepFm[ip]] || (ip != StdHepFd[StdHepFm[ip]])) //self != mom particle-wise, or self = mom but self != first daughter of the mom, to ensure that it's not itself that crosses
				{
					if (print2 == "-Q")
					{   
						if(StdHepStatus[StdHepFm[ip]] == -1) // this section is not itself that crosses... but its other daughters
						{
							if(ip != StdHepFd[StdHepFm[ip]] && StdHepPdg[StdHepFd[StdHepFm[ip]]] == StdHepPdg[StdHepFm[ip]])printf("\n\033[38;5;193m\t%s crossed the yoke originating from pre-yoke %s that later crossed the yoke too \033[0m", my_pdg.GetName(StdHepPdg[ip]).c_str(), my_pdg.GetName(StdHepPdg[StdHepFm[ip]]).c_str());
							if(ip != StdHepFd[StdHepFm[ip]] && StdHepPdg[StdHepFd[StdHepFm[ip]]] != StdHepPdg[StdHepFm[ip]])printf("\n\033[38;5;131m\t%s crossed the yoke from pre-yoke decayed %s \033[0m", my_pdg.GetName(StdHepPdg[ip]).c_str(), my_pdg.GetName(StdHepPdg[StdHepFm[ip]]).c_str());
							if(ip == StdHepFd[StdHepFm[ip]] && StdHepPdg[StdHepFd[StdHepFm[ip]]] != StdHepPdg[StdHepFm[ip]])printf("\n\033[38;5;124m\t%s crossed the yoke from pre-yoke decayed %s \033[0m", my_pdg.GetName(StdHepPdg[ip]).c_str(), my_pdg.GetName(StdHepPdg[StdHepFm[ip]]).c_str());
						}
						
						if(StdHepStatus[StdHepFm[ip]] == 0 )printf("\n\t%s produced from a post-yoke initial state %s", my_pdg.GetName(StdHepPdg[ip]).c_str(), my_pdg.GetName(StdHepPdg[StdHepFm[ip]]).c_str());
						if(StdHepStatus[StdHepFm[ip]] == 2 )printf("\n\033[93m\t%s produced from a post-yoke intermediate %s\033[0m", my_pdg.GetName(StdHepPdg[ip]).c_str(), my_pdg.GetName(StdHepPdg[StdHepFm[ip]]).c_str());
						if(StdHepStatus[StdHepFm[ip]] == 3 )printf("\n\033[91m\t%s produced from a post-yoke %s decay\033[0m", my_pdg.GetName(StdHepPdg[ip]).c_str(), my_pdg.GetName(StdHepPdg[StdHepFm[ip]]).c_str());
						if(StdHepStatus[StdHepFm[ip]] == 11)printf("\n\033[94m\t%s produced from a post-yoke nucleon target %s\033[0m", my_pdg.GetName(StdHepPdg[ip]).c_str(), my_pdg.GetName(StdHepPdg[StdHepFm[ip]]).c_str());
						if(StdHepStatus[StdHepFm[ip]] == 12)printf("\n\033[96m\t%s produced from a post-yoke pre-fragm. hadr. state %s has crossed the yoke\033[0m", my_pdg.GetName(StdHepPdg[ip]).c_str(), my_pdg.GetName(StdHepPdg[StdHepFm[ip]]).c_str());
						if(StdHepStatus[StdHepFm[ip]] == 13)printf("\n\033[38;5;208m\t%s produced from a post-yoke resonant pre-decayed has crossed the yoke%s\033[0m", my_pdg.GetName(StdHepPdg[ip]).c_str(), my_pdg.GetName(StdHepPdg[StdHepFm[ip]]).c_str());
						if(StdHepStatus[StdHepFm[ip]] == 14)printf("\n\033[38;5;129m\t%s got released from inside a post-yoke neclus\033[0m", my_pdg.GetName(StdHepPdg[ip]).c_str());
						if(StdHepStatus[StdHepFm[ip]] == 15)printf("\n\033[95m\t%s a remnant neucleus coming from %s\033[0m", my_pdg.GetName(StdHepPdg[ip]).c_str(), my_pdg.GetName(StdHepPdg[StdHepFm[ip]]).c_str());
					}
					new_particle_count[self]++;
					if((StdHepPdg[ip])==mu_pdg)
                    { 
                        if(energy>maxE_muon)maxE_muon=energy;
                        if(energy<minE_muon)minE_muon=energy;
                        if(momentum2>maxP2_muon)maxP2_muon=momentum2;
                        if(momentum2<minP2_muon)minP2_muon=momentum2;
                        new_muminus_mass.Fill(mass);  
                        new_muminus_energy.Fill(energy);  
						new_muminus_disp.Fill(momentum2, pow(energy,2));
                    }
					if((StdHepPdg[ip])==piminus_pdg)
                    { 
                        if(energy>maxE_pion)maxE_pion=energy;
                        if(energy<minE_pion)minE_pion=energy;
                        if(momentum2>maxP2_pion)maxP2_pion=momentum2;
                        if(momentum2<minP2_pion)minP2_pion=momentum2;
                        if(energy>maxE_pion)maxE_pion=energy;
                        if(energy<minE_pion)minE_pion=energy;
                        if(momentum2>maxP2_pion)maxP2_pion=momentum2;
                        if(momentum2<minP2_pion)minP2_pion=momentum2;
                        new_piminus_mass.Fill(mass);  
                        new_piminus_energy.Fill(energy);  
						new_piminus_disp.Fill(momentum2, pow(energy,2));
                    }
				}
				if (print2 == "-Q")printf("\n ..................................................................................................................................................................................................");
			}
			else if ((StdHepPdg[ip] != StdHepPdg[StdHepFm[ip]]) && (StdHepPdg[ip] != StdHepPdg[StdHepFd[ip]]) && StdHepStatus[ip] == -1)
			{
				if (print2 == "-Q")
				{
					printf("\n ..................................................................................................................................................................................................");
					printf("\n\033[38;5;89m\t%s is stuck inside the yoke\033[0m", my_pdg.GetName(StdHepPdg[ip]).c_str());
					printf("\n ..................................................................................................................................................................................................");
				}
				stuck_particle_count[self]++;
                if((StdHepPdg[ip])==mu_pdg)
                { 
                    if(energy>maxE_muon)maxE_muon=energy;
                    if(energy<minE_muon)minE_muon=energy;
                    if(momentum2>maxP2_muon)maxP2_muon=momentum2;
                    if(momentum2<minP2_muon)minP2_muon=momentum2;
                    stuck_muminus_mass.Fill(mass);  
                    stuck_muminus_energy.Fill(energy);  
					stuck_muminus_disp.Fill(momentum2, pow(energy,2));
                }
                if((StdHepPdg[ip])==piminus_pdg)
                { 
                    if(energy>maxE_pion)maxE_pion=energy;
                    if(energy<minE_pion)minE_pion=energy;
                    if(momentum2>maxP2_pion)maxP2_pion=momentum2;
                    if(momentum2<minP2_pion)minP2_pion=momentum2;
                    stuck_piminus_mass.Fill(mass);  
                    stuck_piminus_energy.Fill(energy);  
					stuck_piminus_disp.Fill(momentum2, pow(energy,2));
                }
			}
        } 
		if (print == "-P" )
		{   
            printf("\n --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------");
			printf("\n *Flux Info:");
			printf("\n Parent hadron pdg code    : %d", NuParentPdg);
			printf("\n Parent hadron decay mode  : %d", NuParentDecMode);
			printf("\n Parent hadron 4p at decay : Px = %6.3f GeV/c, Py = %6.3f GeV/c, Pz = %6.3f GeV/c, E = %6.3f GeV", 
					   NuParentDecP4[0], NuParentDecP4[1], NuParentDecP4[2], NuParentDecP4[3]);
			printf("\n Parent hadron 4p at prod. : Px = %6.3f GeV/c, Py = %6.3f GeV/c, Pz = %6.3f GeV/c, E = %6.3f GeV", 
					   NuParentProP4[0], NuParentProP4[1], NuParentProP4[2], NuParentProP4[3]);
			printf("\n Parent hadron 4x at decay : x = %6.3f m, y = %6.3f m, z = %6.3f m, t = %6.3f s", 
					   NuParentDecX4[0], NuParentDecX4[1], NuParentDecX4[2], NuParentDecX4[3]);
			printf("\n Parent hadron 4x at prod. : x = %6.3f m, y = %6.3f m, z = %6.3f m, t = %6.3f s", 
					   NuParentProX4[0], NuParentProX4[1], NuParentProX4[2], NuParentProX4[3]);
            printf("\n ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ END OF THE EVENT ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n");
		}
    }
    printf("\n");
    //printf(" ..............................................................................................................................................");
	printf ("\n******************************************************************************");
	printf ("\n|        PARTICLE      | CROSSED  %% OF   |  POST  |  STUCK  %% OF    |  ORIG  |");
	printf ("\n|                      |          ORIG   |  YOKE  |         ORIG    |        |");
	printf ("\n******************************************************************************");
    double total_orig = 0;
	for(size_t i = 0; i<allPdg.size(); ++i)
	{
		self = allPdg.at(i);
        crossed_percentage[self] = 100.*crossed_particle_count[self]/orig_particle_count[self];
        stuck_percentage[self] = 100.*stuck_particle_count[self]/orig_particle_count[self];
        if (crossed_percentage[self] != crossed_percentage[self])crossed_percentage[self] = 0;
        if (stuck_percentage[self] != stuck_percentage[self])stuck_percentage[self] = 0;
		if ((int)(orig_particle_count[self]) > 0 || (int)(stuck_particle_count[self]) > 0 || (int)(crossed_particle_count[self]) > 0 || (int)(new_particle_count[self]) > 0)printf ("\n| %-20s | %-6d  %-5.1f%%  | %-6d | %-6d  %-5.1f%%  | %-6d |", my_pdg.GetName(allPdg.at(i)).c_str(), (int)(crossed_particle_count[self]), crossed_percentage[self], (int)(new_particle_count[self]), (int)(stuck_particle_count[self]), stuck_percentage[self], (int)(orig_particle_count[self]));
	}
	printf ("\n******************************************************************************");
	printf("\n");
    file.Close();

	if (print3 == "-D")
	{
		gStyle->SetOptFit(1);
		gStyle->SetOptStat(111);
		// event circle ------------------------------------------------------
		TCanvas events_canvas("events_canvas","",0,0,800,800);
		events_yz.Draw();
		
		//linear fit function
		//
		TF1 line("line","pol1",minP2_muon,maxP2_muon);
		line.SetParNames("m^{2}","dE^{2}/dp^{2}");
        line.SetLineStyle(9);
        line.SetLineColor(kBlack);
		//FOR MUON ----------------------------------------------------------------------------
		line.SetParameter(0,muon_mass);
		line.SetParameter(1,1);
		TCanvas muon_canvas("muon_canvas","",0,0,800,800);
		muon_canvas.Divide(3,3);
		muon_canvas.cd(1);
		crossed_muminus_mom_disp.GetXaxis()->SetRangeUser(minP2_muon,maxP2_muon);
		crossed_muminus_mom_disp.Draw("e1");
        muon_canvas.Update();
		//FITTING----------------------------------------
		crossed_muminus_mom_disp.Fit("line","QER");
		//-----------------------------------------------		
		crossed_muminus_disp.GetXaxis()->SetRangeUser(minP2_muon,maxP2_muon);
		crossed_muminus_disp.Draw("e1");
        muon_canvas.Update();
		//FITTING----------------------------------------
		crossed_muminus_disp.Fit("line","QER");
		//-----------------------------------------------		
		muon_canvas.cd(2);
		stuck_muminus_disp.GetXaxis()->SetRangeUser(minP2_muon,maxP2_muon);
		stuck_muminus_disp.Draw("e1");
        muon_canvas.Update();
		//FITTING----------------------------------------
		stuck_muminus_disp.Fit("line","QER");
		//-----------------------------------------------		
		muon_canvas.cd(3);
		new_muminus_disp.GetXaxis()->SetRangeUser(minP2_muon,maxP2_muon);
		new_muminus_disp.Draw("e1");
        muon_canvas.Update();
		//FITTING----------------------------------------
		new_muminus_disp.Fit("line","QER");
		//-----------------------------------------------		
		muon_canvas.cd(4);
        crossed_muminus_mom_mass.Draw();   //to get the statboxes
        muon_canvas.Update();
        crossed_muminus_mass.Draw();       //of both
        muon_canvas.Update();
        TLegend *crossed_muminus_mass_leg = new TLegend(0.1,0.7,0.48,0.9);
        crossed_muminus_mass_leg->SetHeader("The Legend Title","C"); // option "C" allows to center the header
        crossed_muminus_mass_leg->AddEntry(&crossed_muminus_mom_mass,"#mu^{-} mom","f");
        crossed_muminus_mass_leg->AddEntry(&crossed_muminus_mass,"#mu^{-}","f");
        if (crossed_muminus_mom_mass.GetEntries() > crossed_muminus_mass.GetEntries())
        {
            crossed_muminus_mom_mass.Draw();
            muon_canvas.Update();
            crossed_muminus_mass.Draw("same");
            muon_canvas.Update();
        } 
        else
        {
            crossed_muminus_mass.Draw();
            muon_canvas.Update();
            crossed_muminus_mom_mass.Draw("same");
            muon_canvas.Update();
        }
        crossed_muminus_mass_leg->Draw();
        muon_canvas.cd(5);
		stuck_muminus_mass.Draw();
        muon_canvas.Update();
		muon_canvas.cd(6);
		new_muminus_mass.Draw();
        muon_canvas.Update();
		muon_canvas.cd(7);
        crossed_muminus_mom_energy.Draw();   //to get the statboxes
        muon_canvas.Update();
        crossed_muminus_energy.Draw();       //of both
        muon_canvas.Update();
        TLegend *crossed_muminus_energy_leg = new TLegend(0.1,0.7,0.48,0.9);
        crossed_muminus_energy_leg->SetHeader("The Legend Title","C"); // option "C" allows to center the header
        crossed_muminus_energy_leg->AddEntry(&crossed_muminus_mom_energy,"#mu^{-} mom","f");
        crossed_muminus_energy_leg->AddEntry(&crossed_muminus_energy,"#mu^{-}","f");
        if (crossed_muminus_mom_energy.GetEntries() > crossed_muminus_energy.GetEntries())
        {
            crossed_muminus_mom_energy.Draw();
            muon_canvas.Update();
            crossed_muminus_energy.Draw("same");
            muon_canvas.Update();
        } 
        else
        {
            crossed_muminus_energy.Draw();
            muon_canvas.Update();
            crossed_muminus_mom_energy.Draw("same");
            muon_canvas.Update();
        }
        crossed_muminus_energy_leg->Draw();
		muon_canvas.cd(8);
		stuck_muminus_energy.Draw();
        muon_canvas.Update();
		muon_canvas.cd(9);
		new_muminus_energy.Draw();
        muon_canvas.Update();
	
		//FOR PION ----------------------------------------------------------------------------
		line.SetRange(minP2_pion,maxP2_pion);
		line.SetParameter(0,pion_mass);
		line.SetParameter(1,1);

		TCanvas pion_canvas("pion_canvas","",0,0,800,800);
		pion_canvas.Divide(3,3);
		pion_canvas.cd(1);
		crossed_piminus_mom_disp.GetXaxis()->SetRangeUser(minP2_pion,maxP2_pion);
		crossed_piminus_mom_disp.Draw("e1");
        pion_canvas.Update();
		//FITTING----------------------------------------
		crossed_piminus_mom_disp.Fit("line","QER");
		//-----------------------------------------------		
		crossed_piminus_disp.GetXaxis()->SetRangeUser(minP2_pion,maxP2_pion);
		crossed_piminus_disp.Draw("e1");
        pion_canvas.Update();
		//FITTING----------------------------------------
		crossed_piminus_disp.Fit("line","QER");
		//-----------------------------------------------		
		pion_canvas.cd(2);
		stuck_piminus_disp.GetXaxis()->SetRangeUser(minP2_pion,maxP2_pion);
		stuck_piminus_disp.Draw("e1");
        pion_canvas.Update();
		//FITTING----------------------------------------
		stuck_piminus_disp.Fit("line","QER");
		//-----------------------------------------------		
		pion_canvas.cd(3);
		new_piminus_disp.GetXaxis()->SetRangeUser(minP2_pion,maxP2_pion);
		new_piminus_disp.Draw("e1");
        pion_canvas.Update();
		//FITTING----------------------------------------
		new_piminus_disp.Fit("line","QER");
		//-----------------------------------------------		
		pion_canvas.cd(4);
        crossed_piminus_mom_mass.Draw();  //to get the stat boxes
        crossed_piminus_mass.Draw();      //of both
        pion_canvas.Update();
        TLegend *crossed_piminus_mass_leg = new TLegend(0.1,0.7,0.48,0.9);
        crossed_piminus_mass_leg->SetHeader("The Legend Title","C"); // option "C" allows to center the header
        crossed_piminus_mass_leg->AddEntry(&crossed_muminus_mom_mass,"#pi^{-} mom","f");
        crossed_piminus_mass_leg->AddEntry(&crossed_muminus_mass,"#pi^{-}","f");
        if (crossed_piminus_mom_mass.GetEntries() > crossed_piminus_mass.GetEntries())
        {
            crossed_piminus_mom_mass.Draw();
            pion_canvas.Update();
            crossed_piminus_mass.Draw("same");
            pion_canvas.Update();
        } 
        else
        {
            crossed_piminus_mass.Draw();
            pion_canvas.Update();
            crossed_piminus_mom_mass.Draw("same");
            pion_canvas.Update();
        }
        crossed_piminus_mass_leg->Draw();
		pion_canvas.cd(5);
		stuck_piminus_mass.Draw();
        pion_canvas.Update();
		pion_canvas.cd(6);
		new_piminus_mass.Draw();
        pion_canvas.Update();
		pion_canvas.cd(7);
        crossed_piminus_mom_energy.Draw();  //to get the stat boxes
        pion_canvas.Update();
        crossed_piminus_energy.Draw();      //of both
        pion_canvas.Update();
        TLegend *crossed_piminus_energy_leg = new TLegend(0.1,0.7,0.48,0.9);
        crossed_piminus_energy_leg->SetHeader("The Legend Title","C"); // option "C" allows to center the header
        crossed_piminus_energy_leg->AddEntry(&crossed_muminus_mom_energy,"#pi^{-} mom","f");
        crossed_piminus_energy_leg->AddEntry(&crossed_muminus_energy,"#pi^{-}","f");
        if (crossed_piminus_mom_energy.GetEntries() > crossed_piminus_energy.GetEntries())
        {
            crossed_piminus_mom_energy.Draw();
            pion_canvas.Update();
            crossed_piminus_energy.Draw("same");
            pion_canvas.Update();
        } 
        else
        {
            crossed_piminus_energy.Draw();
            pion_canvas.Update();
            crossed_piminus_mom_energy.Draw("same");
            pion_canvas.Update();
        }
        crossed_piminus_energy_leg->Draw();
		pion_canvas.cd(8);
		stuck_piminus_energy.Draw();
        pion_canvas.Update();
		pion_canvas.cd(9);
		new_piminus_energy.Draw();
        pion_canvas.Update();
		//--------------------------------PION ENDS---------------------------	
		

		rack.Run();
	} 
	return 0;
}



