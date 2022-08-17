#!/usr/bin/env python
import gegede.builder
import math
from duneggd.LocalTools import localtools as ltools
from duneggd.LocalTools import materialdefinition as materials
from gegede import Quantity as Q


class SandEmiRpcStripXXBuilder(gegede.builder.Builder):
    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self,
                # atanu adding these -------
		BuildEmiRpcStripXXBarrelMod   = False,
                layerThickness             = None,
                trapezoidDim                = None,
                layerRmin                   = None,
                NEmiRpcStripXXModBarrel       = None,
                # --------------------------
                **kwds):
        #-------------------------------------------
        self.BuildEmiRpcStripXXBarrelMod = BuildEmiRpcStripXXBarrelMod
        #-------------------------------------------
        self.NEmiRpcStripXXModBarrel  = NEmiRpcStripXXModBarrel            # need 24 slabs if we want 15 degree coverage
        self.layerThickness        = layerThickness  # taken from the cfg file
        self.layerRmin              = layerRmin
        self.BarrelDZ               = Q('215 cm')   # yoke half-length 
        self.layerThickness        = layerThickness
        self.ang                    = (math.pi/self.NEmiRpcStripXXModBarrel)
        self.rmax_layer            = (self.layerRmin + self.layerThickness)/math.cos(self.ang) # for cylinder-shaped emirpcstripxx enclosing logical volume
        self.trapezoidDim           = trapezoidDim 
        print("**************************************************************")
        print ("SandEmiRpcStripXXBuilder: ")
        print("---------------------------------------------------------------")
        print("trapezoidDim: ", self.trapezoidDim)
    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):
        print("\033[36mconstruct in \033[1mSandEmiRpcStripXXBuilder\033[m\033[m")
        print ("==============VARIOUS DIMENSIONS=================================================================")
        print ("# OF MODULES         :                       ",self.NEmiRpcStripXXModBarrel)
        print ("BARREL RMIN          :                       ",self.layerRmin)
        print ("BARREL LENGTH        :                       ",self.BarrelDZ)    
        print ("EMI MODULE THICKNESS :                       ",self.layerThickness)
        print ("EMI EMI    THICKNESS :                       ",self.layerThickness)
        print ("MODULE HALF ANGLE    :                       ",self.ang)
        print ("-------------------------------------------------------------------------------------------------")
        
        # barrel
        barrel_shape = geom.shapes.PolyhedraRegular("sand_emirpcstripxx_barrel_shape",\
                                                    numsides=self.NEmiRpcStripXXModBarrel, 
                                                    rmin=self.layerRmin, 
                                                    rmax=self.layerRmin + 
                                                    self.layerThickness, # 2 * for alternating structure
                                                    dz=self.BarrelDZ,
                                                    sphi=Q(self.ang))

        emirpcstripxx_lv = geom.structure.Volume('sand_emirpcstripxx_volume',
                                              material="Air",
                                              shape=barrel_shape)
                                    
        self.add_volume(emirpcstripxx_lv)

        if self.BuildEmiRpcStripXXBarrelMod is False:
            print ("EMIRPCSTRIPXX not requested, not building it!")
            return
        else:
            self.build_EmiRpcStripXXBarrel(emirpcstripxx_lv, geom)
       

    # STRIPXX RPC VOLUME   
    def build_EmiRpcStripXXBarrel(self, main_lv, geom):

        if self.get_builder("SANDEMIRPCSTRIPXXBARRELMOD") == None:
            print ("SANDEMIRPCSTRIPXXBARRELMOD builder not found");
            return 

        emirpcstripxx_module_builder=self.get_builder("SANDEMIRPCSTRIPXXBARRELMOD")
        emirpcstripxx_module_lv=emirpcstripxx_module_builder.get_volume()

        #'''
        emirpcstripxxMin = self.layerRmin;
        ang = 360 / self.NEmiRpcStripXXModBarrel
        delta = ang/2
        #for k in range(5):
        for k in range(2):
                for j in range(self.NEmiRpcStripXXModBarrel):
                    axisy = (0, 1, 0)
                    axisz = (1, 0, 0)
                    theta = j * ang
                    ModPosition = [Q('0mm'), - self.trapezoidDim[2] + 2 * self.trapezoidDim[2] * k, emirpcstripxxMin + 0.5*self.layerThickness]
                    print ("________________________________________")
                    print ("k: ",k, "j: ",j, ", Pos: ", ModPosition)
                    print ("________________________________________")

                    ModPositionNew = ltools.rotation(
                        axisy, theta, ModPosition
                    )
                    
                    #Rotating the position vector (the slabs will be rotated automatically after append)
                    ModPositionNew = ltools.rotation(axisz, -90, ModPositionNew)

                    
                    EMIRPCSTRIPXX_position = geom.structure.Position(
                        'EMIRPCSTRIPXX_position' + '_' + str(j) + '_' + str(k) , ModPositionNew[0],
                        ModPositionNew[1], ModPositionNew[2])

                    
                    EMIRPCSTRIPXX_rotation = geom.structure.Rotation(
                        'EMIRPCSTRIPXX_rotation' + '_'  + str(j) + '_' + str(k), Q('90deg'), -theta * Q('1deg'),
                        Q('0deg'))  #Rotating the module on its axis accordingly

                    print("Building Kloe EMIRPCSTRIPXX module " + str(j)) # keep compatibility with Python3 pylint: disable=superfluous-parens

                    ####Placing and appending the j EMIRPCSTRIPXX Module#####

                    EMIRPCSTRIPXX_place = geom.structure.Placement('EMIRPCSTRIPXX_place' + '_' + str(j) + '_' + str(k),
                                                          volume=emirpcstripxx_module_lv,
                                                          pos=EMIRPCSTRIPXX_position,
                                                          rot=EMIRPCSTRIPXX_rotation,
                                                          copynumber=j+k
                                                          )
                    main_lv.placements.append(EMIRPCSTRIPXX_place.name)
                
                # next minimum radius to start the layer
                print("**************************************************************")

