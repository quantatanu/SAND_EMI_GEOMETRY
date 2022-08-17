#!/usr/bin/env python
import gegede.builder
import math
from duneggd.LocalTools import localtools as ltools
from duneggd.LocalTools import materialdefinition as materials
from gegede import Quantity as Q


class SandEmiRpcFoam1Builder(gegede.builder.Builder):
    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self,
                # atanu adding these -------
		BuildEmiRpcFoam1BarrelMod   = False,
                layerThickness             = None,
                trapezoidDim                = None,
                layerRmin                   = None,
                NEmiRpcModBarrel            = None,
                # --------------------------
                **kwds):
        #-------------------------------------------
        self.BuildEmiRpcFoam1BarrelMod = BuildEmiRpcFoam1BarrelMod
        #-------------------------------------------
        self.NEmiRpcModBarrel       = NEmiRpcModBarrel                 # need 24 slabs if we want 15 degree coverage
        self.layerThickness        = layerThickness  # taken from the cfg file
        self.layerRmin              = layerRmin
        self.BarrelDZ               = Q('215 cm')   # yoke half-length 
        self.layerThickness        = layerThickness
        self.ang                    = (math.pi/self.NEmiRpcModBarrel)
        self.rmax_layer            = (self.layerRmin + self.layerThickness)/math.cos(self.ang) # for cylinder-shaped emirpcfoam1 enclosing logical volume
        self.trapezoidDim           = trapezoidDim 
        print("**************************************************************")
        print ("SandEmiRpcFoam1Builder: ")
        print("---------------------------------------------------------------")
        print("trapezoidDim: ", self.trapezoidDim)
    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):
        print("\033[36mconstruct in \033[1mSandEmiRpcFoam1Builder\033[m\033[m")
        print ("==============VARIOUS DIMENSIONS=================================================================")
        print ("# OF MODULES         :                       ",self.NEmiRpcModBarrel)
        print ("BARREL RMIN          :                       ",self.layerRmin)
        print ("BARREL LENGTH        :                       ",self.BarrelDZ)    
        print ("EMI MODULE THICKNESS :                       ",self.layerThickness)
        print ("EMI EMI    THICKNESS :                       ",self.layerThickness)
        print ("MODULE HALF ANGLE    :                       ",self.ang)
        print ("-------------------------------------------------------------------------------------------------")
        
        # barrel
        barrel_shape = geom.shapes.PolyhedraRegular("sand_emirpcfoam1_barrel_shape",\
                                                    numsides=self.NEmiRpcModBarrel, 
                                                    rmin=self.layerRmin, 
                                                    rmax=self.layerRmin + 
                                                    self.layerThickness, # 2 * for alternating structure
                                                    dz=self.BarrelDZ,
                                                    sphi=Q(self.ang))

        emirpcfoam1_lv = geom.structure.Volume('sand_emirpcfoam1_volume',
                                              material="Air",
                                              shape=barrel_shape)
                                    
        self.add_volume(emirpcfoam1_lv)

        if self.BuildEmiRpcFoam1BarrelMod is False:
            print ("EMIRPCSFOAM1 not requested, not building it!")
            return
        else:
            self.build_EmiRpcFoam1Barrel(emirpcfoam1_lv, geom)
       

    # SFOAM1 RPC VOLUME   
    def build_EmiRpcFoam1Barrel(self, main_lv, geom):

        if self.get_builder("SANDEMIRPCFOAM1BARRELMOD") == None:
            print ("SANDEMIRPCFOAM1BARRELMOD builder not found");
            return 

        emirpcfoam1_module_builder=self.get_builder("SANDEMIRPCFOAM1BARRELMOD")
        emirpcfoam1_module_lv=emirpcfoam1_module_builder.get_volume()

        #'''
        emirpcfoam1Min = self.layerRmin;
        ang = 360 / self.NEmiRpcModBarrel
        delta = ang/2
        #for k in range(5):
        for k in range(2):
                for j in range(self.NEmiRpcModBarrel):
                    axisy = (0, 1, 0)
                    axisz = (1, 0, 0)
                    theta = j * ang
                    ModPosition = [Q('0mm'), - self.trapezoidDim[2] + 2 * self.trapezoidDim[2] * k, emirpcfoam1Min + 0.5*self.layerThickness]
                    print ("________________________________________")
                    print ("k: ",k, "j: ",j, ", Pos: ", ModPosition)
                    print ("________________________________________")

                    ModPositionNew = ltools.rotation(
                        axisy, theta, ModPosition
                    )
                    
                    #Rotating the position vector (the slabs will be rotated automatically after append)
                    ModPositionNew = ltools.rotation(axisz, -90, ModPositionNew)

                    
                    EMIRPCSFOAM1_position = geom.structure.Position(
                        'EMIRPCSFOAM1_position' + '_' + str(j) + '_' + str(k) , ModPositionNew[0],
                        ModPositionNew[1], ModPositionNew[2])

                    
                    EMIRPCSFOAM1_rotation = geom.structure.Rotation(
                        'EMIRPCSFOAM1_rotation' + '_'  + str(j) + '_' + str(k), Q('90deg'), -theta * Q('1deg'),
                        Q('0deg'))  #Rotating the module on its axis accordingly

                    print("Building Kloe EMIRPCSFOAM1 module " + str(j)) # keep compatibility with Python3 pylint: disable=superfluous-parens

                    ####Placing and appending the j EMIRPCSFOAM1 Module#####

                    EMIRPCSFOAM1_place = geom.structure.Placement('EMIRPCSFOAM1_place' + '_' + str(j) + '_' + str(k),
                                                          volume=emirpcfoam1_module_lv,
                                                          pos=EMIRPCSFOAM1_position,
                                                          rot=EMIRPCSFOAM1_rotation,
                                                          copynumber=j+k
                                                          )
                    main_lv.placements.append(EMIRPCSFOAM1_place.name)
                
                # next minimum radius to start the layer
                print("**************************************************************")

