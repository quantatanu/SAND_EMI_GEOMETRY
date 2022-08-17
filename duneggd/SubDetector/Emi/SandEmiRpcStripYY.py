#!/usr/bin/env python
import gegede.builder
import math
from duneggd.LocalTools import localtools as ltools
from duneggd.LocalTools import materialdefinition as materials
from gegede import Quantity as Q


class SandEmiRpcStripYYBuilder(gegede.builder.Builder):
    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self,
                # atanu adding these -------
		BuildEmiRpcStripYYBarrelMod   = False,
                layerThickness             = None,
                trapezoidDim                = None,
                layerRmin                   = None,
                NEmiRpcStripYYModBarrel       = None,
                # --------------------------
                **kwds):
        #-------------------------------------------
        self.BuildEmiRpcStripYYBarrelMod = BuildEmiRpcStripYYBarrelMod
        #-------------------------------------------
        self.NEmiRpcStripYYModBarrel  = NEmiRpcStripYYModBarrel            # need 24 slabs if we want 15 degree coverage
        self.layerThickness        = layerThickness  # taken from the cfg file
        self.layerRmin              = layerRmin
        self.BarrelDZ               = Q('215 cm')   # yoke half-length 
        self.ang                    = (math.pi/self.NEmiRpcStripYYModBarrel)
        self.rmax_layer            = (self.layerRmin + self.layerThickness)/math.cos(self.ang) # for cylinder-shaped emirpcstripyy enclosing logical volume
        self.trapezoidDim           = trapezoidDim 
        print("**************************************************************")
        print ("SandEmiRpcStripYYBuilder: ")
        print("---------------------------------------------------------------")
        print("trapezoidDim: ", self.trapezoidDim)
    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):
        print("\033[36mconstruct in \033[1mSandEmiRpcStripYYBuilder\033[m\033[m")
        print ("==============VARIOUS DIMENSIONS=================================================================")
        print ("# OF MODULES         :                       ",self.NEmiRpcStripYYModBarrel)
        print ("BARREL RMIN          :                       ",self.layerRmin)
        print ("BARREL LENGTH        :                       ",self.BarrelDZ)    
        print (":AYER      THICKNESS :                       ",self.layerThickness)
        print ("MODULE HALF ANGLE    :                       ",self.ang)
        print ("-------------------------------------------------------------------------------------------------")
        
        # barrel
        barrel_shape = geom.shapes.PolyhedraRegular("sand_emirpcstripyy_barrel_shape",\
                                                    numsides=self.NEmiRpcStripYYModBarrel, 
                                                    rmin=self.layerRmin, 
                                                    rmax=self.layerRmin + 
                                                    self.layerThickness, # 2 * for alternating structure
                                                    dz=self.BarrelDZ,
                                                    sphi=Q(self.ang))

        emirpcstripyy_lv = geom.structure.Volume('sand_emirpcstripyy_volume',
                                              material="Air",
                                              shape=barrel_shape)
                                    
        self.add_volume(emirpcstripyy_lv)

        if self.BuildEmiRpcStripYYBarrelMod is False:
            print ("EMIRPCSTRIPYY not requested, not building it!")
            return
        else:
            self.build_EmiRpcStripYYBarrel(emirpcstripyy_lv, geom)
       

    # STRIPYY RPC VOLUME   
    def build_EmiRpcStripYYBarrel(self, main_lv, geom):

        if self.get_builder("SANDEMIRPCSTRIPYYBARRELMOD") == None:
            print ("SANDEMIRPCSTRIPYYBARRELMOD builder not found");
            return 

        emirpcstripyy_module_builder=self.get_builder("SANDEMIRPCSTRIPYYBARRELMOD")
        emirpcstripyy_module_lv=emirpcstripyy_module_builder.get_volume()

        #'''
        emirpcstripyyMin = self.layerRmin;
        ang = 360 / self.NEmiRpcStripYYModBarrel
        delta = ang/2
        #for k in range(5):
        for k in range(2):
                for j in range(self.NEmiRpcStripYYModBarrel):
                    axisy = (0, 1, 0)
                    axisz = (1, 0, 0)
                    theta = j * ang
                    ModPosition = [Q('0mm'), - self.trapezoidDim[2] + 2 * self.trapezoidDim[2] * k, emirpcstripyyMin + 0.5*self.layerThickness]
                    print ("________________________________________")
                    print ("k: ",k, "j: ",j, ", Pos: ", ModPosition)
                    print ("________________________________________")

                    ModPositionNew = ltools.rotation(
                        axisy, theta, ModPosition
                    )
                    
                    #Rotating the position vector (the slabs will be rotated automatically after append)
                    ModPositionNew = ltools.rotation(axisz, -90, ModPositionNew)

                    
                    EMIRPCSTRIPYY_position = geom.structure.Position(
                        'EMIRPCSTRIPYY_position' + '_' + str(j) + '_' + str(k) , ModPositionNew[0],
                        ModPositionNew[1], ModPositionNew[2])

                    
                    EMIRPCSTRIPYY_rotation = geom.structure.Rotation(
                        'EMIRPCSTRIPYY_rotation' + '_'  + str(j) + '_' + str(k), Q('90deg'), -theta * Q('1deg'),
                        Q('0deg'))  #Rotating the module on its axis accordingly

                    print("Building Kloe EMIRPCSTRIPYY module " + str(j)) # keep compatibility with Python3 pylint: disable=superfluous-parens

                    ####Placing and appending the j EMIRPCSTRIPYY Module#####

                    EMIRPCSTRIPYY_place = geom.structure.Placement('EMIRPCSTRIPYY_place' + '_' + str(j) + '_' + str(k),
                                                          volume=emirpcstripyy_module_lv,
                                                          pos=EMIRPCSTRIPYY_position,
                                                          rot=EMIRPCSTRIPYY_rotation,
                                                          copynumber=j+k
                                                          )
                    main_lv.placements.append(EMIRPCSTRIPYY_place.name)
                
                # next minimum radius to start the layer
                print("**************************************************************")

