#!/usr/bin/env python3
import gegede.builder
import math
from duneggd.LocalTools import localtools as ltools
from duneggd.LocalTools import materialdefinition as materials
from gegede import Quantity as Q


class SandEmiRpcFoam0BarrelModBuilder(gegede.builder.Builder):
    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self, 
		  trapezoidDim      = None, 
		  layerThickness    = None, 
		  FoamMat          = None, 
                  NEmiRpcModBarrel  = None,
		  **kwds):
        self.trapezoidDim = trapezoidDim
        self.layerThickness = layerThickness
        self.FoamMat = FoamMat
        self.NEmiRpcModBarrel = NEmiRpcModBarrel
        self.tan = math.tan(math.pi/self.NEmiRpcModBarrel)
        self.BasePos = -trapezoidDim[3]
        
    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):
        print("----------------------------------------------------------------------")
        print("\033[36mconstruct in \033[1mSandEmiRpcFoam0BarrelModBuilder\033[m\033[m")
        print("----------------------------------------------------------------------")
        print( "trapezoidDim                : ", self.trapezoidDim) 
        print( "layerThickness              : ", self.layerThickness)
        print("----------------------------------------------------------------------")
        print( "FoamMat                    : ", self.FoamMat)
        print("----------------------------------------------------------------------")

        EMIRPCFOAM0_shape = geom.shapes.Trapezoid('EMIRPCFOAM0_shape', 
					   dx1=self.trapezoidDim[0], 
					   dx2=self.trapezoidDim[1],
					   dy1=self.trapezoidDim[2], 
					   dy2=self.trapezoidDim[2], 
					   dz=self.trapezoidDim[3])   

        EMIRPCFOAM0_lv = geom.structure.Volume('EMIRPCFOAM0_lv', material='Air', shape=EMIRPCFOAM0_shape)
        self.add_volume(EMIRPCFOAM0_lv)
        print(self.name)
        

        xpos=Q('0cm')
        ypos=Q('0cm')
        axisx = (0, 0, 1)

        # STRUCTURE (bottom up): Foam0 -> Coat0 -> Bakelite0 -> Gas0 -> Bakelite1 -> Coat1 -> Mylar0 -> Strips0 -> Mylar1 -> Coat2 -> Bakelite2 -> Gas1 -> Bakelite3 -> Coat3 -> Foam1 
        zposFoam0       = self.BasePos  + 0.5 * self.layerThickness
        
        PosFoam0     = [xpos, ypos, zposFoam0]            

        #FIRST FOAM LAYER ==================================================================
        print('Foam [1/2]')
        aEMIRPCFoam_0 = geom.shapes.Trapezoid('EMIRPCFoam_0', 
                                                dx1=self.trapezoidDim[1], 
                                                dx2=self.trapezoidDim[1],
                                                dy1=self.trapezoidDim[2], 
                                                dy2=self.trapezoidDim[2], 
                                                dz=0.5*self.layerThickness)
        aEMIRPCFoam_0_lv = geom.structure.Volume('volEMIRPCFoam_0', 
                                                material=self.FoamMat, 
                                                shape=aEMIRPCFoam_0)
        aEMIRPCFoam_0Pos= geom.structure.Position('emiFoam_0pos',
                                                PosFoam0[0], PosFoam0[1], PosFoam0[2])
        aEMIRPCFoam_0Place = geom.structure.Placement('emiFoam_0pla',
                                                volume = aEMIRPCFoam_0_lv,
                                                pos = aEMIRPCFoam_0Pos)
        EMIRPCFOAM0_lv.placements.append( aEMIRPCFoam_0Place.name )
        print("EMIRPCFOAM0_lv.placements.append(", aEMIRPCFoam_0Place.name, ")")

