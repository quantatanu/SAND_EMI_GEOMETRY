#!/usr/bin/env python3
import gegede.builder
import math
from duneggd.LocalTools import localtools as ltools
from duneggd.LocalTools import materialdefinition as materials
from gegede import Quantity as Q


class SandEmiRpcStripYYBarrelModBuilder(gegede.builder.Builder):
    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self, 
		  trapezoidDim      = None, 
		  layerThickness    = None, 
		  StripWidth        = None, 
		  StripGap          = None, 
		  StripMat          = None, 
		  ynStrips          = None,
                  NEmiRpcModBarrel  = None,
                  layerRmin         = None,
		  **kwds):
        self.trapezoidDim = trapezoidDim
        self.StripThickness = layerThickness
        self.StripWidth = StripWidth
        self.StripGap = StripGap
        self.StripMat = StripMat
        self.ynStrips = ynStrips
        self.NEmiRpcModBarrel = NEmiRpcModBarrel
        self.tan = math.tan(math.pi/self.NEmiRpcModBarrel)
        self.BasePos = -trapezoidDim[3]
        
    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):
        print("----------------------------------------------------------------------")
        print("\033[36mconstruct in \033[1mSandEmiRpcBarrelModBuilder\033[m\033[m")
        print("----------------------------------------------------------------------")
        print( "trapezoidDim                : ", self.trapezoidDim) 
        print( "StripThickness              : ", self.StripThickness)
        print("----------------------------------------------------------------------")
        print( "StripMat                    : ", self.StripMat)
        print( "StripWidth                  : ", self.StripWidth)
        print( "StripGap                  : ", self.StripGap)
        print("----------------------------------------------------------------------")
        print( "ynStrips                     : ", self.ynStrips)
        print("----------------------------------------------------------------------")


        EMIRPCSTRIPYY_shape = geom.shapes.Trapezoid('EMIRPCSTRIPYY_shape', 
					   dx1=self.trapezoidDim[0], 
					   dx2=self.trapezoidDim[1],
					   dy1=self.trapezoidDim[2], 
					   dy2=self.trapezoidDim[2], 
					   dz=self.trapezoidDim[3])   

        EMIRPCSTRIPYY_lv = geom.structure.Volume('EMIRPCSTRIPYY_lv', material='Air', shape=EMIRPCSTRIPYY_shape)
        self.add_volume(EMIRPCSTRIPYY_lv)
        print(self.name)
        

        yposYYStrip = -self.trapezoidDim[2] + 0.5 * self.StripWidth
        print("--------------------------------------------------------->INITIAL STRIP POSITION: ")
        xpos=Q('0cm')
        ypos=Q('0cm')
        axisx = (0, 0, 1)

        # STRUCTURE (bottom up): Foam0 -> Coat0 -> Bakelite0 -> Gas0 -> Bakelite1 -> Coat1 -> Mylar0 -> Strips0 -> Mylar1 -> Coat2 -> Bakelite2 -> Gas1 -> Bakelite3 -> Coat3 -> Foam1 
        zposYYStrip      = self.BasePos  + 0.5 * self.StripThickness 
        
        PosYYStrip   = [xpos, ypos, zposYYStrip]            
        
        #FIRST STRIP  LAYER ================================================================
        print('Strip [YY]')
        for j in range(self.ynStrips):  # 2 cm wide Strips cover the whole 46 cm breadth if we place every 2.5 times their width
            aEMIRPCSTRIPYYYYStrip = geom.shapes.Trapezoid('EMIRPCSTRIPYYYYStrip_'+str(j), 
                                                    dx1=self.StripWidth/2, 
                                                    dx2=self.StripWidth/2,
                                                    dy1=self.trapezoidDim[0], 
                                                    dy2=self.trapezoidDim[0], 
                                                    dz=0.5*self.StripThickness)
            aEMIRPCSTRIPYYYYStrip_lv = geom.structure.Volume('volEMIRPCSTRIPYYYYStrip_'+str(j), 
                                                    material=self.StripMat, 
                                                    shape=aEMIRPCSTRIPYYYYStrip)
            aEMIRPCSTRIPYYYYStripPos= geom.structure.Position('emiYYStrippos_'+str(j),
                                                    PosYYStrip[0], yposYYStrip, PosYYStrip[2])
                                                    #xposYYStrip, yposYYStrip, PosYYStrip[2])
            
            aEMIRPCSTRIPYYYYStriprotation = geom.structure.Rotation(
                'EMIRPCSTRIPYYYYStriprotation_'+str(j), Q('0deg'),  Q('0deg'),
                Q('90deg'))  #Rotating the module on its axis accordingly
            aEMIRPCSTRIPYYYYStripPlace = geom.structure.Placement('emiYYStrippla'+str(j),
                                                  volume=aEMIRPCSTRIPYYYYStrip_lv,
                                                  pos=aEMIRPCSTRIPYYYYStripPos,
                                                  rot=aEMIRPCSTRIPYYYYStriprotation,
                                                  copynumber=j)

            
            EMIRPCSTRIPYY_lv.placements.append( aEMIRPCSTRIPYYYYStripPlace.name )
            
            print("EMIRPCSTRIPYY_lv.placements.append(", aEMIRPCSTRIPYYYYStripPlace.name, ")")
            yposYYStrip = yposYYStrip + self.StripWidth + self.StripGap
            #xposYYStrip = xposYYStrip + self.StripWidth + self.StripGap
            

