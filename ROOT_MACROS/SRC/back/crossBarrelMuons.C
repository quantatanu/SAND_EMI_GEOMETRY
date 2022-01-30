#include <iostream>
#include <cstddef>
#include <sstream>
#include <vector>
#include <stdexcept>
#include <assert.h>
#include <iterator>
//root classes
#include <TFile.h>
#include <TTree.h>
#include <TBranch.h>
#include <TBits.h>
#include <TObjString.h>
#include <TString.h>
#include <TCanvas.h>
#include <TApplication.h>




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
	//particle names
	vect<std::string> particle(-9999999,9999999);
	particle[2]  = "u";
	particle[-2]  = "ubar";
	particle[11]  = "e-";
	particle[-11] = "e+";
	//particle[13]  = "\033[47mmu-\033[49m";
	particle[12]  = "nu_e";
	particle[-12]  = "nu_ebar";
	particle[13]  = "mu-";
	particle[-13] = "mu+";
	particle[14]  = "nu_mu";
	particle[-14]  = "nu_mubar";
	particle[22]  = "gamma";
	particle[111] = "pi0";
	particle[130] = "K0_L";
	particle[310] = "K0_S";
	particle[211] = "pi+";
	particle[-211] = "pi-";
	particle[321] = "K+";
	particle[-321] = "K-";
	particle[221] = "eta";
	particle[311] = "K0";
	particle[-311] = "K0bar";
	particle[331] = "etaprime";
	particle[2112] = "n";
	particle[-2112] = "nbar";
	particle[2114] = "Delta0";
	particle[2212] = "p+";
	particle[-2212] = "p-";
	particle[2214] = "Delta+";
	particle[2224] = "Delta++";
	particle[3222] = "Sigma+";
	particle[3122] = "Lambda0";
	particle[12212] = "P11m1440_N+";
	particle[22212] = "S11m1535_N+";
	particle[32124] = "P13m1720_N+";
	particle[8888] = "HadrSyst"; //2000000001 --> 8008 (as my max array size is 9999999, so I am aliasing it)
	particle[8009] = "C12";//1000060120 --> 8009 (.... )
	particle[8010] = "HardBlob";//2000000002 --> 8010 (.... )
	particle[8011] = "Mn55";//1000250550 --> 8011 (.... )
	particle[8012] = "Fe56";//1000260560 --> 8012 (.... )
	particle[8013] = "Fe55";//1000260550 --> 8013 (.... )
	particle[8014] = "CompNuclCluster";//2000000300 --> 8014 (.... )
	particle[8015] = "Unknown";//1000060110 --> 8015 (.... )
	particle[8016] = "Unknown";//1000050110 --> 8016 (.... )
	particle[8017] = "Unknown";//1000180400 --> 8017 (.... )


	int particle_list[1000] = {2,-2,11,-11,12,-12,13,-13,14,-14,22,111,130,310,211,-211,321,-321,221,311,-311,331,2112,-2112,2212,-2212,2114,2214,2224,3122,3222,12212,22212,32124,8008,8009,8010,8011,8012,8013,8014,8015,8016,8017};

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
    printf ("\n------------------------ SUMMARY TABLE -------------------------------\n");
    printf ("FILE: %s\n", Fname.c_str());
    printf("Number of entries: %d", n);
    vect<double> new_particle_count(-9999999,9999999), crossed_particle_count(-9999999,9999999), stopped_particle_count(-9999999,9999999), orig_particle_count(-9999999,9999999);
	vect<int> orig_particle_id(-9999999,9999999), orig_particle_kid(-9999999,9999999), orig_particle_mom(-9999999,9999999), orig_particle_ist(-9999999,9999999);    
	vect<int> new_particle_id(-9999999,9999999), new_particle_kid(-9999999,9999999), new_particle_mom(-9999999,9999999), new_particle_ist(-9999999,9999999);    
	vect<int> crossed_particle_id(-9999999,9999999), crossed_particle_kid(-9999999,9999999), crossed_particle_mom(-9999999,9999999), crossed_particle_ist(-9999999,9999999);   
	vect<int> pdg(-9999999,9999999);
    vect<double> Anew_particle_count(-9999999,9999999), Acrossed_particle_count(-9999999,9999999), Astopped_particle_count(-9999999,9999999), Aorig_particle_count(-9999999,9999999);
	vect<int> Aorig_particle_id(-9999999,9999999), Aorig_particle_kid(-9999999,9999999), Aorig_particle_mom(-9999999,9999999), Aorig_particle_ist(-9999999,9999999);    
	vect<int> Anew_particle_id(-9999999,9999999), Anew_particle_kid(-9999999,9999999), Anew_particle_mom(-9999999,9999999), Anew_particle_ist(-9999999,9999999);    
	vect<int> Acrossed_particle_id(-9999999,9999999), Acrossed_particle_kid(-9999999,9999999), Acrossed_particle_mom(-9999999,9999999), Acrossed_particle_ist(-9999999,9999999);   
	vect<int> Apdg(-9999999,9999999);
    bool mom_exists;
    bool self_exists;
	// read tree & print some info for each entry
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
        for(int ip=0; ip<StdHepN; ip++) 
        {
			if (StdHepPdg[ip] == 1000180400) StdHepPdg[ip] = 8017;
			if (StdHepPdg[ip] == 1000050110) StdHepPdg[ip] = 8016;
			if (StdHepPdg[ip] == 1000060110) StdHepPdg[ip] = 8015;
			if (StdHepPdg[ip] == 2000000300) StdHepPdg[ip] = 8014;
			if (StdHepPdg[ip] == 1000260550) StdHepPdg[ip] = 8013;
			if (StdHepPdg[ip] == 1000250550) StdHepPdg[ip] = 8011;
			if (StdHepPdg[ip] == 2000000002) StdHepPdg[ip] = 8010;
			if (StdHepPdg[ip] == 2000000001) StdHepPdg[ip] = 8008;
			if (StdHepPdg[ip] == 1000060120) StdHepPdg[ip] = 8009;
            //if(abs(StdHepPdg[ip]) <= 9999999)
            //{
                if (print == "-P" )
                {   
                    printf("\n | %3d | %3d | %10d | %6d | %3d | %3d | %3d | %3d | %+.2e | %+.2e | %+.2e | %.2e | %+.2e | %+.2e | %+.2e |",
                    ip, StdHepStatus[ip],  StdHepPdg[ip], StdHepRescat[ip], 
                    StdHepFm[ip],  StdHepLm[ip], StdHepFd[ip],  StdHepLd[ip],
                    StdHepP4[ip][0], StdHepP4[ip][1], StdHepP4[ip][2], StdHepP4[ip][3],
                    StdHepX4[ip][0], StdHepX4[ip][1], StdHepX4[ip][2]);
                }
                if(abs(abs(StdHepPdg[ip])) == 13)
                {
					mom_exists = std::find(std::begin(particle_list), std::end(particle_list), StdHepPdg[StdHepFm[ip]]) != std::end(particle_list);
					self_exists = std::find(std::begin(particle_list), std::end(particle_list), StdHepPdg[ip]) != std::end(particle_list);
					pdg[StdHepPdg[ip]] = StdHepPdg[ip];
					if(mom_exists && self_exists)
					{
						if (particle[StdHepPdg[ip]] == particle[StdHepPdg[StdHepFm[ip]]])
						{
							if (print == "-P" && print2 == "-Q")
							{   
								printf("\n\033[33m\t%s (id: %d, status: %d) has crossed the int scint, because mom %s is itself :)\033[0m\n", particle[StdHepPdg[ip]].c_str(), crossed_particle_id[StdHepPdg[ip]], crossed_particle_ist[StdHepPdg[ip]], particle[StdHepPdg[StdHepFm[ip]]].c_str());
							}
							crossed_particle_count[StdHepPdg[ip]]++;
						} else if (abs(StdHepPdg[StdHepFm[ip]]) == 14) 
						{
							if (print == "-P" && print2 == "-Q")
							{   
								printf("\n\033[32m\t%s (id: %d, status: %d) is primary produced by %s \033[0m\n", particle[StdHepPdg[ip]].c_str(), new_particle_id[StdHepPdg[ip]], new_particle_ist[StdHepPdg[ip]], particle[StdHepPdg[StdHepFm[ip]]].c_str() );
							}
							orig_particle_count[StdHepPdg[ip]]++;
						} else  
						{
							if (print == "-P" && print2 == "-Q")
							{   
								printf("\n\033[31m\t%s (id: %d, status: %d) is newly produced from the decay of %s \033[0m\n", particle[StdHepPdg[ip]].c_str(), new_particle_id[StdHepPdg[ip]], new_particle_ist[StdHepPdg[ip]], particle[StdHepPdg[StdHepFm[ip]]].c_str() );
							}
							new_particle_count[StdHepPdg[ip]]++;
						}
						//}
					} else
					{
						if (print == "-P" && print2 == "-Q")
						{   
							printf ("\nTHIS SELF PDG: %d, OR MOM PDG: %d, IS NOT IN MY PARTICLE LIST!!!\n",StdHepPdg[ip], StdHepPdg[StdHepFm[ip]]);
							if (StdHepPdg[ip] == 0 || StdHepPdg[StdHepFm[ip]])std::cout << ip << "\n";
							sleep(1);
						}
					}
                }
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
    printf ("---------------------------------------------------------------------------\n");
    printf ("|   particle   |  # primary   | # crossed (%% of primary)  |   # secondary |\n");
    printf ("---------------------------------------------------------------------------\n");
    double total_orig = 0;
//    for (int ipdg = -13; ipdg <= 13; ipdg++)
//    {
		//if(pdg[ipdg] != -999 && crossed_particle_count[ipdg] > 0)
//		if(pdg[ipdg] != -999)
//		{
//			total_orig = total_orig + orig_particle_count[ipdg]; 
			printf ("|   %-7s    |    %6d    |  %6d       %5.2f %%     |    %6d     |\n", particle[13].c_str(), (int)(orig_particle_count[13]), (int)(crossed_particle_count[13]), 100.*crossed_particle_count[13]/orig_particle_count[13], (int)(new_particle_count[13]));
			printf ("|   %-7s    |    %6d    |  %6d       %5.2f %%     |    %6d     |\n", particle[-13].c_str(), (int)(orig_particle_count[-13]), (int)(crossed_particle_count[-13]), 100.*crossed_particle_count[-13]/orig_particle_count[-13], (int)(new_particle_count[-13]));
//		}
//	}
    printf ("---------------------------------------------------------------------------\n");
/*    printf ("----------------------------------------------------------------------\n");
    printf ("  Pre-yoke content:                                                   \n");    
    printf ("----------------------------------------------------------------------\n");
    if(orig_particle_count[13])printf ("| %-8s: %6.3f %%                                                 |\n",   particle[13].c_str(),  100*orig_particle_count[13]/total_orig);    //mu-
    if(orig_particle_count[-13])printf ("| %-8s: %6.3f %%                                                 |\n",  particle[-13].c_str(),  100*orig_particle_count[-13]/total_orig);  //mu+  
    printf ("----------------------------------------------------------------------\n");
*/
    printf("\n");
    file.Close();
    return 0;
}

