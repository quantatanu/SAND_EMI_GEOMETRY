#!/usr/bin/env python
import gegede.builder
import math
from duneggd.LocalTools import localtools as ltools
from duneggd.LocalTools import materialdefinition as materials
from gegede import Quantity as Q


class SandEmiRpcFoam0Builder(gegede.builder.Builder):
    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self,
                # atanu adding these -------
		BuildEmiRpcFoam0BarrelMod   = False,
                layerThickness             = None,
                trapezoidDim                = None,
                layerRmin                   = None,
                NEmiRpcModBarrel            = None,
                # --------------------------
                **kwds):
        #-------------------------------------------
        self.BuildEmiRpcFoam0BarrelMod = BuildEmiRpcFoam0BarrelMod
        #-------------------------------------------
        self.NEmiRpcModBarrel       = NEmiRpcModBarrel                 # need 24 slabs if we want 15 degree coverage
        self.layerThickness        = layerThickness  # taken from the cfg file
        self.layerRmin              = layerRmin
        self.BarrelDZ               = Q('215 cm')   # yoke half-length 
        self.layerThickness        = layerThickness
        self.ang                    = (math.pi/self.NEmiRpcModBarrel)
        self.rmax_layer            = (self.layerRmin + self.layerThickness)/math.cos(self.ang) # for cylinder-shaped emirpcfoam0 enclosing logical volume
        self.trapezoidDim           = trapezoidDim 
        print("**************************************************************")
        print ("SandEmiRpcFoam0Builder: ")
        print("---------------------------------------------------------------")
        print("trapezoidDim: ", self.trapezoidDim)
    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):
        print("\033[36mconstruct in \033[1mSandEmiRpcFoam0Builder\033[m\033[m")
        print ("==============VARIOUS DIMENSIONS=================================================================")
        print ("# OF MODULES         :                       ",self.NEmiRpcModBarrel)
        print ("BARREL RMIN          :                       ",self.layerRmin)
        print ("BARREL LENGTH        :                       ",self.BarrelDZ)    
        print ("EMI MODULE THICKNESS :                       ",self.layerThickness)
        print ("EMI EMI    THICKNESS :                       ",self.layerThickness)
        print ("MODULE HALF ANGLE    :                       ",self.ang)
        print ("-------------------------------------------------------------------------------------------------")
        
        # barrel
        barrel_shape = geom.shapes.PolyhedraRegular("sand_emirpcfoam0_barrel_shape",\
                                                    numsides=self.NEmiRpcModBarrel, 
                                                    rmin=self.layerRmin, 
                                                    rmax=self.layerRmin + 
                                                    self.layerThickness, # 2 * for alternating structure
                                                    dz=self.BarrelDZ,
                                                    sphi=Q(self.ang))

        emirpcfoam0_lv = geom.structure.Volume('sand_emirpcfoam0_volume',
                                              material="Air",
                                              shape=barrel_shape)
                                    
        self.add_volume(emirpcfoam0_lv)

        if self.BuildEmiRpcFoam0BarrelMod is False:
            print ("EMIRPCSFOAM0 not requested, not building it!")
            return
        else:
            self.build_EmiRpcFoam0Barrel(emirpcfoam0_lv, geom)
       

    # SFOAM0 RPC VOLUME   
    def build_EmiRpcFoam0Barrel(self, main_lv, geom):

        if self.get_builder("SANDEMIRPCFOAM0BARRELMOD") == None:
            print ("SANDEMIRPCFOAM0BARRELMOD builder not found");
            return 

        emirpcfoam0_module_builder=self.get_builder("SANDEMIRPCFOAM0BARRELMOD")
        emirpcfoam0_module_lv=emirpcfoam0_module_builder.get_volume()

        #'''
        emirpcfoam0Min = self.layerRmin;
        ang = 360 / self.NEmiRpcModBarrel
        delta = ang/2
        #for k in range(5):
        for k in range(2):
                for j in range(self.NEmiRpcModBarrel):
                    axisy = (0, 1, 0)
                    axisz = (1, 0, 0)
                    theta = j * ang
                    ModPosition = [Q('0mm'), - self.trapezoidDim[2] + 2 * self.trapezoidDim[2] * k, emirpcfoam0Min + 0.5*self.layerThickness]
                    print ("________________________________________")
                    print ("k: ",k, "j: ",j, ", Pos: ", ModPosition)
                    print ("________________________________________")

                    ModPositionNew = ltools.rotation(
                        axisy, theta, ModPosition
                    )
                    
                    #Rotating the position vector (the slabs will be rotated automatically after append)
                    ModPositionNew = ltools.rotation(axisz, -90, ModPositionNew)

                    
                    EMIRPCSFOAM0_position = geom.structure.Position(
                        'EMIRPCSFOAM0_position' + '_' + str(j) + '_' + str(k) , ModPositionNew[0],
                        ModPositionNew[1], ModPositionNew[2])

                    
                    EMIRPCSFOAM0_rotation = geom.structure.Rotation(
                        'EMIRPCSFOAM0_rotation' + '_'  + str(j) + '_' + str(k), Q('90deg'), -theta * Q('1deg'),
                        Q('0deg'))  #Rotating the module on its axis accordingly

                    print("Building Kloe EMIRPCSFOAM0 module " + str(j)) # keep compatibility with Python3 pylint: disable=superfluous-parens

                    ####Placing and appending the j EMIRPCSFOAM0 Module#####

                    EMIRPCSFOAM0_place = geom.structure.Placement('EMIRPCSFOAM0_place' + '_' + str(j) + '_' + str(k),
                                                          volume=emirpcfoam0_module_lv,
                                                          pos=EMIRPCSFOAM0_position,
                                                          rot=EMIRPCSFOAM0_rotation,
                                                          copynumber=j+k
                                                          )
                    main_lv.placements.append(EMIRPCSFOAM0_place.name)
                
                # next minimum radius to start the layer
                print("**************************************************************")

