//radial distance from the KLOE barrel center : (z,y) = (2391.0 cm, -238.473 cm) 

#include <string>

class distance {
	public:
            std::string where_is(double R){
            
            //for external active-passive layers ( n starts from 0 )
            //nth_passive_rmin = yoke_rmax + ext_air1_thickness + (n+1)*active_thickness + n*passive_thickness  
            //nth_passive_rmax = yoke_rmax + ext_air1_thickness + (n+1)*active_thickness + (n+1)*passive_thickness  
            //nth_active_rmin  = yoke_rmax + ext_air1_thickness + n*active_thickness  
            //nth_active_rmax  = yoke_rmax + ext_air1_thickness + (n+1)*active_thickness  

			double ext_air1_rmax = 3300 + 0.5;                              //3300.5
			double ext_air1_rmin = 3300 - 0.01;                             //3299.99
            double yoke_rmax = ext_air1_rmin;	                            //3299.99
			double yoke_rmin = 2930;	                                    //2930
			double int_air2_rmax = yoke_rmin;	                            //2930
			double int_air2_rmin = int_air2_rmax - 0.5-0.01;	            //2929.49
			double int_scint_rmax = int_air2_rmin;	                        //2929.5
			double int_scint_rmin = int_scint_rmax - 49 -0.01;	            //2880.49
			double int_air1_rmax = int_scint_rmin;	                        //2880.5
			double int_air1_rmin = int_air1_rmax - 0.5 - 0.01;              //2879.99
			double cryo_outer_rmax = int_air1_rmin;			                //2880	
			double cryo_outer_rmin = int_air1_rmin - 15 - 0.01;	            //2864.99
			//there's a gap here... large gap of 25.4 cm between the coil end and the outer wall start
			double outer_wall_shell_gap_rmax = cryo_outer_rmin - 0.1;             //2864.9 //just to avoid boundary match  
			double outer_wall_shell_gap_rmin = 2611;                       //2611
			double coil_rmax = outer_wall_shell_gap_rmin;                  //2611
			double coil_rmin = coil_rmax - 10 - 0.01;                             //2600.99
			double coil_shell_rmax = coil_rmin;                            //2601
			double coil_shell_rmin = coil_shell_rmax - 11 - 0.01;          //2589.99
			//there's another gap here... a gap of 14.5 cm between the inner wall end and the coil shell start
			double inner_wall_shell_gap_rmax = coil_shell_rmin - 0.1;             //2589.9 //just to avoid...
			double inner_wall_shell_gap_rmin = 2445;                       //2445
			double cryo_inner_rmax = inner_wall_shell_gap_rmin;	            //2445
			double cryo_inner_rmin = cryo_inner_rmax - 15 - 0.01;           //2429.99
            //there's a gap between the ecal and the cryo wall (I have inserted a 0.5 mm air layer there)
            double ecal_cryo_3rd_gap_rmax = cryo_inner_rmin - 0.1;                //2429.9 //just to avoid boundary match
            double ecal_cryo_3rd_gap_rmin = 2420;                          //2420
            double postEcalAir2_rmax = 2420;                               //2420
            double postEcalAir2_rmin = postEcalAir2_rmax - 0.5 - 0.01;              //2419.49 //just two include the boundary
            double ecal_cryo_sec_gap_rmax = postEcalAir2_rmin - 0.1;              //2419.4   //just to avoid boundary matching with air volume
            double ecal_cryo_sec_gap_rmin = 2252.2;                         //2252.2
            double postEcalAir1_rmax = ecal_cryo_sec_gap_rmin;              //2252.2
            double postEcalAir1_rmin = postEcalAir1_rmax - 0.5 - 0.01;      //2251.69   //just to include the boundary
            double ecal_cryo_first_gap_rmax = postEcalAir1_rmin - 0.1;            //2251.6 // just to avoid....
            double ecal_cryo_first_gap_rmin = 2242.2;                       //2242.2
            double ecal_rmax = ecal_cryo_first_gap_rmin;                    //2242.2
            double ecal_rmin = 2000-0.01;                                       //1999.99
            double stt_ecal_gap_rmax = ecal_rmin - 0.01;                           //1999.98
            double stt_ecal_gap_rmin = 2000 - 200;                        //1800
            double stt_rmax = stt_ecal_gap_rmin;                          // 180 excluding 20 cm edge of vol STT
			
            
            if (R >= ext_air1_rmin && R < ext_air1_rmax)
			{
				return "post_yoke_ext_first_air";
			}
			else if (R >= yoke_rmin && R < yoke_rmax)
			{
				return "yoke";
			}
			else if (R >= int_air2_rmin && R < int_air2_rmax)
			{
				return "int_air2";
			}
			else if (R >= int_scint_rmin && R < int_scint_rmax)
			{
				return "int_scint";
			}
			else if (R >= int_air1_rmin && R < int_air1_rmax)
			{
				return "int_air1";
			}
			else if (R >= cryo_outer_rmin && R < cryo_outer_rmax)
			{
				return "cryo_outer_wall";
			}
			else if (R >= outer_wall_shell_gap_rmin && R < outer_wall_shell_gap_rmax)
			{
				return "coil_cryo_outer_wall_gap";
			}
			else if (R >= coil_rmin && R < coil_rmax)
			{
				return "coil";
			}
			else if (R >= coil_shell_rmin && R < coil_shell_rmax)
			{
				return "coil_shell";
			}
			else if (R >= inner_wall_shell_gap_rmin && R < inner_wall_shell_gap_rmax)
			{
				return "coil_cryo_inner_wall_gap";
			}
			else if (R >= cryo_inner_rmin && R < cryo_inner_rmax)
			{
				return "cryo_inner_wall";
			}
			else if (R >= ecal_cryo_3rd_gap_rmin && R < ecal_cryo_3rd_gap_rmax)
            {
                return "ecal_cryo_last_gap";
            }
            else if (R >= postEcalAir2_rmin && R < postEcalAir2_rmax)
            {
                return "post_ecal_air2";
            }
			else if (R >= ecal_cryo_sec_gap_rmin && R < ecal_cryo_sec_gap_rmax)
            {
                return "ecal_cryo_second_gap";
            }
            else if (R >= postEcalAir1_rmin && R < postEcalAir1_rmax)
            {
                return "post_ecal_air1";
            }
			else if (R >= ecal_cryo_first_gap_rmin && R < ecal_cryo_first_gap_rmax)
            {
                return "ecal_cryo_first_gap";
            }
			else if (R >= ecal_rmin && R < ecal_rmax)
            {
                return "ecal";
            }
			else if (R >= stt_ecal_gap_rmin && R < stt_ecal_gap_rmax)
            {
                return "stt_ecal_gap";
            }
			else if (R < stt_rmax)
            {
                return "stt";
            }
            else if (R >= yoke_rmax)
			{
                std::string rr = std::to_string(R);
				return "outside yoke: " + rr + " mm";
			}
			else
			{
                std::string rr = std::to_string(R);
				return rr + " mm";
			}
		}
};




