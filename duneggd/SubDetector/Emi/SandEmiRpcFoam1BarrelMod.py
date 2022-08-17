#!/usr/bin/env python3
import gegede.builder
import math
from duneggd.LocalTools import localtools as ltools
from duneggd.LocalTools import materialdefinition as materials
from gegede import Quantity as Q


class SandEmiRpcFoam1BarrelModBuilder(gegede.builder.Builder):
    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self, 
		  trapezoidDim      = None, 
		  FoamMat          = None, 
                  layerThickness    = None,
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
        print("\033[36mconstruct in \033[1mSandEmiRpcFoam1BarrelModBuilder\033[m\033[m")
        print("----------------------------------------------------------------------")
        print( "trapezoidDim                : ", self.trapezoidDim) 
        print( "layerThickness              : ", self.layerThickness)
        print("----------------------------------------------------------------------")
        print( "FoamMat                    : ", self.FoamMat)
        print("----------------------------------------------------------------------")

        EMIRPCFOAM1_shape = geom.shapes.Trapezoid('EMIRPCFOAM1_shape', 
					   dx1=self.trapezoidDim[0], 
					   dx2=self.trapezoidDim[1],
					   dy1=self.trapezoidDim[2], 
					   dy2=self.trapezoidDim[2], 
					   dz=self.trapezoidDim[3])   

        EMIRPCFOAM1_lv = geom.structure.Volume('EMIRPCFOAM1_lv', material='Air', shape=EMIRPCFOAM1_shape)
        self.add_volume(EMIRPCFOAM1_lv)
        print(self.name)
        

        xpos=Q('0cm')
        ypos=Q('0cm')
        axisx = (0, 0, 1)

        # STRUCTURE (bottom up): Foam1 -> Coat0 -> Bakelite0 -> Gas0 -> Bakelite1 -> Coat1 -> Mylar0 -> Strips0 -> Mylar1 -> Coat2 -> Bakelite2 -> Gas1 -> Bakelite3 -> Coat3 -> Foam1 
        zposFoam1       = self.BasePos  + 0.5 * self.layerThickness
        
        PosFoam1     = [xpos, ypos, zposFoam1]            

        #FIRST FOAM LAYER ==================================================================
        aEMIRPCFoam_1 = geom.shapes.Trapezoid('EMIRPCFoam_1', 
                                                dx1=self.trapezoidDim[1], 
                                                dx2=self.trapezoidDim[1],
                                                dy1=self.trapezoidDim[2], 
                                                dy2=self.trapezoidDim[2], 
                                                dz=0.5*self.layerThickness)
        aEMIRPCFoam_1_lv = geom.structure.Volume('volEMIRPCFoam_1', 
                                                material=self.FoamMat, 
                                                shape=aEMIRPCFoam_1)
        aEMIRPCFoam_1Pos= geom.structure.Position('emiFoam_1pos',
                                                PosFoam1[0], PosFoam1[1], PosFoam1[2])
        aEMIRPCFoam_1Place = geom.structure.Placement('emiFoam_1pla',
                                                volume = aEMIRPCFoam_1_lv,
                                                pos = aEMIRPCFoam_1Pos)
        EMIRPCFOAM1_lv.placements.append( aEMIRPCFoam_1Place.name )
        print("EMIRPCFOAM1_lv.placements.append(", aEMIRPCFoam_1Place.name, ")")

