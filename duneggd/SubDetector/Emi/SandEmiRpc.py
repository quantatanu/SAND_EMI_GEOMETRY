#!/usr/bin/env python
import gegede.builder
import math
from duneggd.LocalTools import localtools as ltools
from duneggd.LocalTools import materialdefinition as materials
from gegede import Quantity as Q

class SandEmiRpcBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self,
                  layerThickness = None,
                  layerRmin = None,
                  NEmiRpcModBarrel = None,
                  BuildEmiRpcFoam0BarrelMod = False,
                  BuildEmiRpcFoam1BarrelMod = False,
                  BuildEmiRpcInnerBarrelMod = False,
                  BuildEmiRpcStripYYBarrelMod = False,
                  BuildEmiRpcStripXXBarrelMod = False,
                  **kwds):

        self.layerThickness = layerThickness
        self.layerRmin = layerRmin
        self.NEmiRpcModBarrel = NEmiRpcModBarrel
        self.BuildEmiRpcFoam1BarrelMod = BuildEmiRpcFoam1BarrelMod
        self.BuildEmiRpcFoam0BarrelMod = BuildEmiRpcFoam0BarrelMod
        self.BuildEmiRpcInnerBarrelMod = BuildEmiRpcInnerBarrelMod
        self.BuildEmiRpcStripYYBarrelMod = BuildEmiRpcStripYYBarrelMod
        self.BuildEmiRpcStripXXBarrelMod = BuildEmiRpcStripXXBarrelMod
        self.BarrelDZ               = Q('215 cm')
        self.ang = (math.pi/self.NEmiRpcModBarrel)

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):
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

        print("EMIRPCBuilder::construct()")
        print("emi_lv = "+ emi_lv.name)
        self.add_volume(emi_lv )
        #self.build_yoke(emi_lv, geom)
        #self.build_solenoid(emi_lv, geom)


	# Ext. muon identifier EMI
        #self.build_emirpc(main_lv,geom)
        if self.BuildEmiRpcInnerBarrelMod is False:
            print("EMI RPC INNER VOLUME NOT REQUESTED..NOT BUILDING IT!")
        else:
            self.build_EmiRpcInnerBarrel(emi_lv,geom)


        if self.BuildEmiRpcStripYYBarrelMod is False:
            print("EMI RPC STRIP YY VOLUME NOT REQUESTED..NOT BUILDING IT!")
        else:
            self.build_EmiRpcStripYYBarrel(emi_lv,geom)


        if self.BuildEmiRpcStripXXBarrelMod is False:
            print("EMI RPC STRIP XX VOLUME NOT REQUESTED..NOT BUILDING IT!")
        else:
            self.build_EmiRpcStripXXBarrel(emi_lv,geom)


        if self.BuildEmiRpcFoam0BarrelMod is False:
            print("EMI RPC FOAM 0 VOLUME NOT REQUESTED..NOT BUILDING IT!")
        else:
            self.build_EmiRpcFoam0Barrel(emi_lv,geom)

        if self.BuildEmiRpcFoam1BarrelMod is False:
            print("EMI RPC FOAM1 VOLUME NOT REQUESTED..NOT BUILDING IT!")
        else:
            self.build_EmiRpcFoam1Barrel(emi_lv,geom)


    def build_EmiRpcInnerBarrel(self, emi_lv, geom):

        if self.get_builder("SANDEMIRPCINNER") == None:
            print ("SANDEMIRPCINNER builder not found");
            return
        else:
            EMIRPCINNER=self.get_builder("SANDEMIRPCINNER")
            EMIRPCINNER_lv=EMIRPCINNER.get_volume()

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
                                                  volume=EMIRPCINNER_lv,
                                                  pos=EMIRPCINNER_position,
                                                  rot=EMIRPCINNER_rotation,
                                                  copynumber=0)

            #main_lv.placements.append(EMIRPCINNER_place.name)
            emi_lv.placements.append(EMIRPCINNER_place.name)
            print("**************************************************************")




    def build_EmiRpcStripYYBarrel(self, emi_lv, geom):

        if self.get_builder("SANDEMIRPCSTRIPYY") == None:
            print ("SANDEMIRPCSTRIPYY builder not found");
            return
        else:
            EMIRPCSTRIPYY=self.get_builder("SANDEMIRPCSTRIPYY")
            EMIRPCSTRIPYY_lv=EMIRPCSTRIPYY.get_volume()

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
            EMIRPCSTRIPYY_position = geom.structure.Position(
                'EMIRPCSTRIPYY_position', ModPositionNew[0],
                ModPositionNew[1], ModPositionNew[2])

            EMIRPCSTRIPYY_rotation = geom.structure.Rotation(
                'EMIRPCSTRIPYY_rotation', Q('0deg'), 0 * Q('1deg'),
                Q('0deg'))  #Rotating the module on its axis accordingly

            print("Building Kloe EMIRPCSTRIPYY module ") # keep compatibility with Python3 pylint: disable=superfluous-parens

            ####Placing and appending the j EMIRPCSTRIPYY Module#####

            EMIRPCSTRIPYY_place = geom.structure.Placement('EMIRPCSTRIPYY_place',
                                                  volume=EMIRPCSTRIPYY_lv,
                                                  pos=EMIRPCSTRIPYY_position,
                                                  rot=EMIRPCSTRIPYY_rotation,
                                                  copynumber=0)

            #main_lv.placements.append(EMIRPCSTRIPYY_place.name)
            emi_lv.placements.append(EMIRPCSTRIPYY_place.name)
            print("**************************************************************")




    def build_EmiRpcStripXXBarrel(self, emi_lv, geom):

        if self.get_builder("SANDEMIRPCSTRIPXX") == None:
            print ("SANDEMIRPCSTRIPXX builder not found");
            return
        else:
            EMIRPCSTRIPXX=self.get_builder("SANDEMIRPCSTRIPXX")
            EMIRPCSTRIPXX_lv=EMIRPCSTRIPXX.get_volume()

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
            EMIRPCSTRIPXX_position = geom.structure.Position(
                'EMIRPCSTRIPXX_position', ModPositionNew[0],
                ModPositionNew[1], ModPositionNew[2])

            EMIRPCSTRIPXX_rotation = geom.structure.Rotation(
                'EMIRPCSTRIPXX_rotation', Q('0deg'), 0 * Q('1deg'),
                Q('0deg'))  #Rotating the module on its axis accordingly

            print("Building Kloe EMIRPCSTRIPXX module ") # keep compatibility with Python3 pylint: disable=superfluous-parens

            ####Placing and appending the j EMIRPCSTRIPXX Module#####

            EMIRPCSTRIPXX_place = geom.structure.Placement('EMIRPCSTRIPXX_place',
                                                  volume=EMIRPCSTRIPXX_lv,
                                                  pos=EMIRPCSTRIPXX_position,
                                                  rot=EMIRPCSTRIPXX_rotation,
                                                  copynumber=0)

            #main_lv.placements.append(EMIRPCSTRIPXX_place.name)
            emi_lv.placements.append(EMIRPCSTRIPXX_place.name)
            print("**************************************************************")



    def build_EmiRpcFoam0Barrel(self, emi_lv, geom):

        if self.get_builder("SANDEMIRPCFOAM0") == None:
            print ("SANDEMIRPCFOAM0 builder not found");
            return
        else:
            EMIRPCFOAM0=self.get_builder("SANDEMIRPCFOAM0")
            EMIRPCFOAM0_lv=EMIRPCFOAM0.get_volume()

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
            EMIRPCFOAM0_position = geom.structure.Position(
                'EMIRPCFOAM0_position', ModPositionNew[0],
                ModPositionNew[1], ModPositionNew[2])

            EMIRPCFOAM0_rotation = geom.structure.Rotation(
                'EMIRPCFOAM0_rotation', Q('0deg'), 0 * Q('1deg'),
                Q('0deg'))  #Rotating the module on its axis accordingly

            print("Building Kloe EMIRPCFOAM0 module ") # keep compatibility with Python3 pylint: disable=superfluous-parens

            ####Placing and appending the j EMIRPCFOAM0 Module#####

            EMIRPCFOAM0_place = geom.structure.Placement('EMIRPCFOAM0_place',
                                                  volume=EMIRPCFOAM0_lv,
                                                  pos=EMIRPCFOAM0_position,
                                                  rot=EMIRPCFOAM0_rotation,
                                                  copynumber=0)

            #main_lv.placements.append(EMIRPCFOAM0_place.name)
            emi_lv.placements.append(EMIRPCFOAM0_place.name)
            print("**************************************************************")



    def build_EmiRpcFoam1Barrel(self, emi_lv, geom):

        if self.get_builder("SANDEMIRPCFOAM1") == None:
            print ("SANDEMIRPCFOAM1 builder not found");
            return
        else:
            EMIRPCFOAM1=self.get_builder("SANDEMIRPCFOAM1")
            EMIRPCFOAM1_lv=EMIRPCFOAM1.get_volume()

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
            EMIRPCFOAM1_position = geom.structure.Position(
                'EMIRPCFOAM1_position', ModPositionNew[0],
                ModPositionNew[1], ModPositionNew[2])

            EMIRPCFOAM1_rotation = geom.structure.Rotation(
                'EMIRPCFOAM1_rotation', Q('0deg'), 0 * Q('1deg'),
                Q('0deg'))  #Rotating the module on its axis accordingly

            print("Building Kloe EMIRPCFOAM1 module ") # keep compatibility with Python3 pylint: disable=superfluous-parens

            ####Placing and appending the j EMIRPCFOAM1 Module#####

            EMIRPCFOAM1_place = geom.structure.Placement('EMIRPCFOAM1_place',
                                                  volume=EMIRPCFOAM1_lv,
                                                  pos=EMIRPCFOAM1_position,
                                                  rot=EMIRPCFOAM1_rotation,
                                                  copynumber=0)

            #main_lv.placements.append(EMIRPCFOAM1_place.name)
            emi_lv.placements.append(EMIRPCFOAM1_place.name)
            print("**************************************************************")

