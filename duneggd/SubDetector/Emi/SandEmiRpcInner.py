#!/usr/bin/env python
import gegede.builder
import math
from duneggd.LocalTools import localtools as ltools
from duneggd.LocalTools import materialdefinition as materials
from gegede import Quantity as Q


class SandEmiRpcInnerBuilder(gegede.builder.Builder):
    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self,
                # atanu adding these -------
		BuildEmiRpcInnerBarrelMod   = False,
                layerThickness             = None,
                trapezoidDim                = None,
                layerRmin                   = None,
                NEmiRpcInnerModBarrel       = None,
                # --------------------------
                **kwds):
        #-------------------------------------------
        self.BuildEmiRpcInnerBarrelMod = BuildEmiRpcInnerBarrelMod
        #-------------------------------------------
        self.NEmiRpcInnerModBarrel  = NEmiRpcInnerModBarrel            # need 24 slabs if we want 15 degree coverage
        self.layerThickness        = layerThickness  # taken from the cfg file
        self.layerRmin              = layerRmin
        self.BarrelDZ               = Q('215 cm')   # yoke half-length 
        self.ang                    = (math.pi/self.NEmiRpcInnerModBarrel)
        self.rmax_layer            = (self.layerRmin + self.layerThickness)/math.cos(self.ang) # for cylinder-shaped emirpcinner enclosing logical volume
        self.trapezoidDim           = trapezoidDim 
        print("**************************************************************")
        print ("SandEmiRpcInnerBuilder: ")
        print("---------------------------------------------------------------")
        print("trapezoidDim: ", self.trapezoidDim)
    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):
        print("\033[36mconstruct in \033[1mSandEmiRpcInnerBuilder\033[m\033[m")
        print ("==============VARIOUS DIMENSIONS=================================================================")
        print ("# OF MODULES         :                       ",self.NEmiRpcInnerModBarrel)
        print ("LAYER  RMIN          :                       ",self.layerRmin)
        print ("BARREL LENGTH        :                       ",self.BarrelDZ)    
        print ("EMI INNER  THICKNESS :                       ",self.layerThickness)
        print ("MODULE HALF ANGLE    :                       ",self.ang)
        print ("-------------------------------------------------------------------------------------------------")
        
        # barrel
        barrel_shape = geom.shapes.PolyhedraRegular("sand_emirpcinner_barrel_shape",\
                                                    numsides=self.NEmiRpcInnerModBarrel, 
                                                    rmin=self.layerRmin, 
                                                    rmax=self.layerRmin + 
                                                    self.layerThickness, # 2 * for alternating structure
                                                    dz=self.BarrelDZ,
                                                    sphi=Q(self.ang))

        emirpcinner_lv = geom.structure.Volume('sand_emirpcinner_volume',
                                              material="Air",
                                              shape=barrel_shape)
                                    
        self.add_volume(emirpcinner_lv)

        if self.BuildEmiRpcInnerBarrelMod is False:
            print ("EMIRPCINNER not requested, not building it!")
            return
        else:
            self.build_EmiRpcInnerBarrel(emirpcinner_lv, geom)
       

    # INNER RPC VOLUME   
    def build_EmiRpcInnerBarrel(self, main_lv, geom):

        if self.get_builder("SANDEMIRPCINNERBARRELMOD") == None:
            print ("SANDEMIRPCINNERBARRELMOD builder not found");
            return 

        emirpcinner_module_builder=self.get_builder("SANDEMIRPCINNERBARRELMOD")
        emirpcinner_module_lv=emirpcinner_module_builder.get_volume()

        #'''
        emirpcinnerMin = self.layerRmin;
        ang = 360 / self.NEmiRpcInnerModBarrel
        delta = ang/2
        #for k in range(5):
        for k in range(2):
                for j in range(self.NEmiRpcInnerModBarrel):
                    axisy = (0, 1, 0)
                    axisz = (1, 0, 0)
                    theta = j * ang
                    ModPosition = [Q('0mm'), - self.trapezoidDim[2] + 2 * self.trapezoidDim[2] * k, emirpcinnerMin + 0.5*self.layerThickness]
                    print ("________________________________________")
                    print ("k: ",k, "j: ",j, ", Pos: ", ModPosition)
                    print ("________________________________________")

                    ModPositionNew = ltools.rotation(
                        axisy, theta, ModPosition
                    )
                    
                    #Rotating the position vector (the slabs will be rotated automatically after append)
                    ModPositionNew = ltools.rotation(axisz, -90, ModPositionNew)

                    
                    EMIRPCINNER_position = geom.structure.Position(
                        'EMIRPCINNER_position' + '_' + str(j) + '_' + str(k) , ModPositionNew[0],
                        ModPositionNew[1], ModPositionNew[2])

                    
                    EMIRPCINNER_rotation = geom.structure.Rotation(
                        'EMIRPCINNER_rotation' + '_'  + str(j) + '_' + str(k), Q('90deg'), -theta * Q('1deg'),
                        Q('0deg'))  #Rotating the module on its axis accordingly

                    print("Building Kloe EMIRPCINNER module " + str(j)) # keep compatibility with Python3 pylint: disable=superfluous-parens

                    ####Placing and appending the j EMIRPCINNER Module#####

                    EMIRPCINNER_place = geom.structure.Placement('EMIRPCINNER_place' + '_' + str(j) + '_' + str(k),
                                                          volume=emirpcinner_module_lv,
                                                          pos=EMIRPCINNER_position,
                                                          rot=EMIRPCINNER_rotation,
                                                          copynumber=j+k
                                                          )
                    main_lv.placements.append(EMIRPCINNER_place.name)
                
                # next minimum radius to start the layer
                print("**************************************************************")

