#!/usr/bin/env python
import gegede.builder
import math
from duneggd.LocalTools import localtools as ltools
from duneggd.LocalTools import materialdefinition as materials
from gegede import Quantity as Q


class SandEmiBuilder(gegede.builder.Builder):
    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self,
                # atanu adding these -------
		BuildEmiBarrelMod  = False,
                emiThickness = None,
                # --------------------------
                **kwds):
        #-------------------------------------------
        self.BuildEmiBarrelMod = BuildEmiBarrelMod
        #-------------------------------------------
        self.NEmiModBarrel     = 24            # need 24 slabs if we want 15 degree coverage
        #self.emiThickness      = Q('60cm')    # to fulfill the nedd of 5 * 10 + 6 * 2 = 62 cm of total external mu ID thickness
        self.emiThickness      = emiThickness  # taken from the cfg file
        self.BarrelRmin         = Q('3.30m')   # yoke rmax
        #self.BarrelRmin         = Q('3.60m')   # yoke rmax
        self.BarrelDZ           = Q('2.15m')   # yoke half-length 
        
    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):
        print("\033[36mconstruct in \033[1mSandEmiBuilder\033[m\033[m")
        print ("RMAX_BARREL::::::::::::::::::::::::::::::::  ",self.emiThickness)
        ang = (math.pi/self.NEmiModBarrel)
        print ("ANG::::::::::::::::::::::::::::::::::::::::  ",ang)
        
        # barrel
        #'''
        rmax_barrel = (self.BarrelRmin + self.emiThickness)/math.cos(ang)
        print ("RMAX_BARREL::::::::::::::::::::::::::::::::  ",rmax_barrel)
        barrel_shape = geom.shapes.PolyhedraRegular("sand_emi_barrel_shape",\
                                                    numsides=self.NEmiModBarrel, 
                                                    rmin=self.BarrelRmin, 
                                                    rmax=self.BarrelRmin + 
                                                    self.emiThickness, 
                                                    dz=self.BarrelDZ,
                                                    sphi=Q('7.5deg'))
        #'''
        '''
        barrel_shape = geom.shapes.Tubs("sand_emi_barrel_shape",
                                        rmin=self.BarrelRmin, 
                                        rmax=rmax_barrel, 
                                        dz=self.BarrelDZ)
        '''
        emi_lv = geom.structure.Volume('sand_emi_volume',
                                              material="Air",
                                              shape=barrel_shape)
                                    
        self.add_volume(emi_lv)

        if self.BuildEmiBarrelMod is False:
            print ("EMI BARREL not requested, not building it!")
        else:
            self.buildEmiBarrel(emi_lv, geom)
        
    def buildEmiBarrel(self, main_lv, geom):
        # there is a barrel section that is nearly cylindrical, with 24 modules
        # each covering 15 degrees. The modules are 4.3m long, 62cm thick,
        # trapezoids with bases of 86.39 (at radius 330 cm) and 102.62 cm (at radius 330 cm + 62 cm).


        if self.get_builder("SANDEMIBARRELMOD") == None:
            print ("SANDEMIBARRELMOD builder not found");
            return 

        emi_module_builder=self.get_builder("SANDEMIBARRELMOD")
        emi_module_lv=emi_module_builder.get_volume()


        for j in range(self.NEmiModBarrel):

            axisy = (0, 1, 0)
            axisz = (1, 0, 0)
            ang = 360 / self.NEmiModBarrel
            theta = j * ang
            ModPosition = [Q('0mm'), Q('0mm'), self.BarrelRmin + 0.5*self.emiThickness]
            #ModPosition = [Q('0mm'), Q('0mm'), 0.5*self.emiThickness+(self.BarrelRmin + self.emiThickness)/math.cos(math.pi/self.NEmiModBarrel)]
            ModPositionNew = ltools.rotation(
                axisy, theta, ModPosition
            )  #Rotating the position vector (the slabs will be rotated automatically after append)
            ModPositionNew = ltools.rotation(axisz, -90, ModPositionNew)

            
            EMI_position = geom.structure.Position(
                'EMI_position' + '_' + str(j), ModPositionNew[0],
                ModPositionNew[1], ModPositionNew[2])


            
            EMI_rotation = geom.structure.Rotation(
                'EMI_rotation' + '_' + str(j), Q('90deg'), -theta * Q('1deg'),
                Q('0deg'))  #Rotating the module on its axis accordingly
                #Q('10deg'))  #Rotating the module on its axis accordingly

            print("Building Kloe EMI module " + str(j)) # keep compatibility with Python3 pylint: disable=superfluous-parens

            ####Placing and appending the j EMI Module#####

            EMI_place = geom.structure.Placement('EMI_place' + '_' + str(j),
                                                  volume=emi_module_lv,
                                                  pos=EMI_position,
                                                  rot=EMI_rotation,
                                                  copynumber=j
                                                  )
            main_lv.placements.append(EMI_place.name)

            ################################################

