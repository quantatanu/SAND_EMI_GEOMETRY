#!/usr/bin/env python
import gegede.builder
import math
from duneggd.LocalTools import localtools as ltools
from duneggd.LocalTools import materialdefinition as materials
from gegede import Quantity as Q


class SandEmiRpcBuilder(gegede.builder.Builder):
    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self,
                # atanu adding these -------
		BuildEmiRpcInnerBarrelMod  = False,
		BuildEmiRpcStripYYBarrelMod  = False,
                layerThickness = None,
                layerRmin = None,
                #trapezoidDim = None,
                NEmiRpcModBarrel = None,
                # --------------------------
                **kwds):
        #-------------------------------------------
        self.BuildEmiRpcInnerBarrelMod = BuildEmiRpcInnerBarrelMod
        self.BuildEmiRpcStripYYBarrelMod = BuildEmiRpcStripYYBarrelMod
        #-------------------------------------------
        self.layerThickness         = layerThickness  # taken from the cfg file
        self.layerRmin              = layerRmin
        self.BarrelDZ               = Q('215 cm')   # yoke half-length 
        self.NEmiRpcModBarrel       = NEmiRpcModBarrel
        self.ang = (math.pi/self.NEmiRpcModBarrel)
        #self.trapezoidDim      = trapezoidDim 
        print("**************************************************************")
        print ("SandEmiRpcBuilder: ")
        print("---------------------------------------------------------------")
        #print("trapezoidDim: ", self.trapezoidDim)
    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):
        print("\033[36mconstruct in \033[1mSandEmiRpcBuilder\033[m\033[m")
        print ("==============VARIOUS DIMENSIONS=================================================================")
        print ("# OF MODULES         :                       ",self.NEmiRpcModBarrel)
        print ("BARREL RMIN          :                       ",self.layerRmin)
        print ("BARREL LENGTH        :                       ",self.BarrelDZ)    
        print ("EMI MODULE THICKNESS :                       ",self.layerThickness)
        print ("-------------------------------------------------------------------------------------------------")
        
        # barrel
        # POLYHEDRON SHAPED EMI ENCLOSING LOGICAL VOLUME
        barrel_shape = geom.shapes.PolyhedraRegular("sand_emi_barrel_shape",
                                                    numsides=self.NEmiRpcModBarrel, 
                                                    rmin=self.layerRmin, 
                                                    rmax=self.layerRmin +  
                                                    self.layerThickness, 
                                                    dz=self.BarrelDZ,
                                                    sphi=Q(self.ang))

        emi_lv = geom.structure.Volume('sand_emi_volume',
                                              material="Air",
                                              shape=barrel_shape)
                                    
        self.add_volume(emi_lv)

        if self.BuildEmiRpcInnerBarrelMod is False:
            print ("EMIRPC INNER not requested, not building it!")
            #return
        else:
            self.buildEmiRpcInnerBarrel(emi_lv, geom)

        '''
        if self.BuildEmiRpcStripYYBarrelMod is False:
            print ("EMIRPC STRIPYY not requested, not building it!")
            #return
        else:
            self.buildEmiRpcStripYYBarrel(emi_lv, geom)
        '''

    #def buildEmiRpcInnerBarrel(self, main_lv, geom):
    def buildEmiRpcInnerBarrel(self, emi_lv, geom):
        
        if self.get_builder("SANDEMIRPCINNER") == None:
            print ("SANDEMIRPCINNER builder not found");
            return 
        else:
            emi_module_builder=self.get_builder("SANDEMIRPCINNER")
            emi_module_lv=emi_module_builder.get_volume()

            emiMin = self.layerRmin;
            ang = 360 / self.NEmiRpcModBarrel
            delta = ang/2
            #testing for a single module building
            axisx = (0, 0, 1)
            axisy = (0, 1, 0)
            axisz = (1, 0, 0)
            theta = 0
            ModPosition = [Q('0 cm'), Q('0 cm'), Q('0 cm')]
            print("----------------> MODPOSITION-----------------------: ", ModPosition)
            ModPositionNew = ltools.rotation(
                axisy, theta, ModPosition
            )  #Rotating the position vector (the slabs will be rotated automatically after append)
            print("----------------> MODPOSITIONNEW--------------------: ", ModPositionNew)
            ModPositionNew = ltools.rotation(axisz, 0, ModPositionNew)
            print("----------------> MODPOSITIONNEW--------------------: ", ModPositionNew)
            EMIRPCINNER_position = geom.structure.Position(
                'EMIRPCINNER_position', ModPositionNew[0],
                ModPositionNew[1], ModPositionNew[2])
            
            EMIRPCINNER_rotation = geom.structure.Rotation(
                'EMIRPCINNER_rotation', Q('0deg'), 0 * Q('1deg'),
                Q('0deg'))  #Rotating the module on its axis accordingly

            print("Building Kloe EMIRPCINNER module ") # keep compatibility with Python3 pylint: disable=superfluous-parens

            ####Placing and appending the j EMIRPCINNER Module#####

            EMIRPCINNER_place = geom.structure.Placement('EMIRPCINNER_place',
                                                  volume=emi_module_lv,
                                                  pos=EMIRPCINNER_position,
                                                  rot=EMIRPCINNER_rotation,
                                                  copynumber=0)

            #main_lv.placements.append(EMIRPCINNER_place.name)
            emi_lv.placements.append(EMIRPCINNER_place.name)
            print("**************************************************************")

