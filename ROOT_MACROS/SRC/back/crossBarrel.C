#include <iostream>
#include <cstddef>
#include <sstream>
#include <vector>
#include <stdexcept>
#include <assert.h>
#include <iterator>
#include <utility> 

//root classes
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

    TString filename = argv[1];
	std::string print = "", print2 = "";
	if (argc >= 3 )
	{
		print = argv[2];
	}
	if (argc >= 4 )
	{
		print2 = argv[3];
	}


    //TApplication rack("rack",0,0);
    std::string Fname = argv[1];
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
    printf ("------------------  SUMMARY  TABLE  ------------------\n");
    printf ("FILE: %s\n", Fname.c_str());
    printf("Number of entries: %d", n);
    std::map <TString, int> new_particle_count, crossed_particle_count, stopped_particle_count, orig_particle_count;
	std::map <TString, int> orig_particle_id, orig_particle_kid, orig_particle_mom, orig_particle_ist;    
	std::map <TString, int> new_particle_id, new_particle_kid, new_particle_mom, new_particle_ist;    
	std::map <TString, int> crossed_particle_id, crossed_particle_kid, crossed_particle_mom, crossed_particle_ist;   
	std::map <TString, int> pdg;
    std::vector <std::string> allPdg;
    TParticlePDG *pdgSelf = new TParticlePDG();
	TParticlePDG *pdgMom = new TParticlePDG();
	TString ROOTSYS = getenv("ROOTSYS");
	ROOTSYS = ROOTSYS + "/etc/pdg_table.txt";
	std::cout << "\nROOT: " << ROOTSYS << "\n";
	std::string self, mom;
    for(int i=0; i < tree->GetEntries(); i++) 
    {
        tree->GetEntry(i);
        if (print == "-P" )
        {   
            printf("\n ----------------------------------------------------------------------------------------------------------------------------------------------");
            printf("\n Event code                 : %s", EvtCode->String().Data());
            printf("\n Event x-section            : %10.5f * 1E-38* cm^2",  EvtXSec);
            printf("\n Event kinematics x-section : %10.5f * 1E-38 * cm^2/{K^n}", EvtDXSec);
            printf("\n Event weight               : %10.8f", EvtWght);
            printf("\n Event vertex               : x = %8.2f mm, y = %8.2f mm, z = %8.2f mm", EvtVtx[0], EvtVtx[1], EvtVtx[2]);
            printf("\n *Particle list:");
            printf("\n ----------------------------------------------------------------------------------------------------------------------------------------------");
            printf("\n | Idx | Ist |    PDG     | Rescat |   Mother  |  Daughter |     Px    |    Py     |     Pz    |     E    |      x    |     y     |     z     |");
            printf("\n |     |     |            |        |           |           |  (GeV/c)  |  (GeV/c)  |  (GeV/c)  |   (GeV)  |     (m)   |    (m)    |    (m)    |");
            printf("\n ----------------------------------------------------------------------------------------------------------------------------------------------");
        }
        for(int ip = 0; ip < StdHepN; ip++) 
        {
			self = std::to_string(StdHepPdg[ip]);
			mom = std::to_string(StdHepPdg[StdHepFm[ip]]);
			if (std::find(allPdg.begin(), allPdg.end(), self) == allPdg.end()) 
			{
				  // someName not in name, add it
				  allPdg.push_back(self);
			}
            if (print == "-P" )
            {   
                printf("\n | %3d | %3d | %10d | %6d | %3d | %3d | %3d | %3d | %+.2e | %+.2e | %+.2e | %.2e | %+.2e | %+.2e | %+.2e |",
                ip, StdHepStatus[ip],  StdHepPdg[ip], StdHepRescat[ip], 
                StdHepFm[ip],  StdHepLm[ip], StdHepFd[ip],  StdHepLd[ip],
                StdHepP4[ip][0], StdHepP4[ip][1], StdHepP4[ip][2], StdHepP4[ip][3],
                StdHepX4[ip][0], StdHepX4[ip][1], StdHepX4[ip][2]);
				
			}
			
            pdg[self] = StdHepPdg[ip];
			
            if (StdHepPdg[ip] == StdHepPdg[StdHepFm[ip]])
            {
                if (print == "-P" && print2 == "-Q")
                {   
                    printf("\n\033[32m\t%s (id: %d, status: %d) has crossed the int scint, because mom %s is itself :)\033[0m\n", self.c_str(), crossed_particle_id[self], crossed_particle_ist[self], mom.c_str());
                }
                crossed_particle_count[self]++;
            } 
			else if (StdHepFm[ip] == 3) 
			//if (StdHepFm[ip] == 3) 
            //{
                if (print == "-P" && print2 == "-Q")
                {   
                    printf("\n\033[33m\t%s (id: %d, status: %d) was produced from %s decay \033[0m\n", self.c_str(), new_particle_id[self], new_particle_ist[self], mom.c_str());
                }
                new_particle_count[self]++;
            //}
			
        } 
		if (print == "-P" )
		{   
			printf("\n ----------------------------------------------------------------------------------------------------------------------------------------------");
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
			printf("\n ----------------------------------------------------------------------------------------------------------------------------------------------");
		}
    }
    printf("\n");
    //printf(" ..............................................................................................................................................");
    printf ("------------------------------------------------------\n");
    printf ("|         PDG        |       CROSSED   |      NEW     |\n");
    printf ("------------------------------------------------------\n");
    double total_orig = 0;
	for(size_t i = 0; i<allPdg.size(); ++i)
	{
		self = allPdg.at(i);
		printf ("|     %-10s     |      %6d     |     %6d   |\n", self.c_str(), (int)(crossed_particle_count[self]), (int)(new_particle_count[self]));
	}
    printf ("------------------------------------------------------\n");
    printf ("  Pre-yoke content:                                                   \n");    
    printf ("------------------------------------------------------\n");
    printf ("------------------------------------------------------\n");
    printf("\n");
    file.Close();
    return 0;
}



