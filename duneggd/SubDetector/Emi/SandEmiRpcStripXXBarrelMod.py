#!/usr/bin/env python3
import gegede.builder
import math
from duneggd.LocalTools import localtools as ltools
from duneggd.LocalTools import materialdefinition as materials
from gegede import Quantity as Q


class SandEmiRpcStripXXBarrelModBuilder(gegede.builder.Builder):
    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self, 
		  trapezoidDim      = None, 
		  layerThickness    = None, 
		  StripWidth        = None, 
		  StripGap          = None, 
		  StripMat          = None, 
		  xnStrips          = None,
                  NEmiRpcModBarrel  = None,
                  layerRmin         = None,
		  **kwds):
        self.trapezoidDim = trapezoidDim
        self.StripThickness = layerThickness
        self.StripWidth = StripWidth
        self.StripGap = StripGap
        self.StripMat = StripMat
        self.xnStrips = xnStrips
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
        print( "xnStrips                     : ", self.xnStrips)
        print("----------------------------------------------------------------------")


        EMIRPCSTRIPXX_shape = geom.shapes.Trapezoid('EMIRPCSTRIPXX_shape', 
					   dx1=self.trapezoidDim[0], 
					   dx2=self.trapezoidDim[1],
					   dy1=self.trapezoidDim[2], 
					   dy2=self.trapezoidDim[2], 
					   dz=self.trapezoidDim[3])   

        EMIRPCSTRIPXX_lv = geom.structure.Volume('EMIRPCSTRIPXX_lv', material='Air', shape=EMIRPCSTRIPXX_shape)
        self.add_volume(EMIRPCSTRIPXX_lv)
        print(self.name)
        
        xposXXStrip = -self.trapezoidDim[0] + 0.5 * self.StripWidth
        yposXXStrip = -self.trapezoidDim[0] + 0.5 * self.StripWidth
        print("--------------------------------------------------------->INITIAL STRIP POSITION: ")
        xpos=Q('0cm')
        ypos=Q('0cm')
        axisx = (0, 0, 1)

        # STRUCTURE (bottom up): Foam0 -> Coat0 -> Bakelite0 -> Gas0 -> Bakelite1 -> Coat1 -> Mylar0 -> Strips0 -> Mylar1 -> Coat2 -> Bakelite2 -> Gas1 -> Bakelite3 -> Coat3 -> Foam1 
        zposXXStrip      = self.BasePos  + 0.5 * self.StripThickness 
        
        PosXXStrip   = [xpos, ypos, zposXXStrip]            
        
        #FIRST STRIP  LAYER ================================================================
        print('Strip [XX]')
        for j in range(self.xnStrips):  # 2 cm wide Strips cover the whole 46 cm breadth if we place every 2.5 times their width
            aEMIRPCSTRIPXXXXStrip = geom.shapes.Trapezoid('EMIRPCSTRIPXXXXStrip_'+str(j), 
                                                    dx1=self.StripWidth/2, 
                                                    dx2=self.StripWidth/2,
                                                    dy1=self.trapezoidDim[2], 
                                                    dy2=self.trapezoidDim[2], 
                                                    dz=0.5*self.StripThickness)
            aEMIRPCSTRIPXXXXStrip_lv = geom.structure.Volume('volEMIRPCSTRIPXXXXStrip_'+str(j), 
                                                    material=self.StripMat, 
                                                    shape=aEMIRPCSTRIPXXXXStrip)
            aEMIRPCSTRIPXXXXStripPos= geom.structure.Position('emiXXStrippos_'+str(j),
                                                    xposXXStrip, PosXXStrip[1], PosXXStrip[2])
            aEMIRPCSTRIPXXXXStripPlace = geom.structure.Placement('emiXXStrippla_'+str(j),
                                                  volume = aEMIRPCSTRIPXXXXStrip_lv,
                                                  pos = aEMIRPCSTRIPXXXXStripPos)
            EMIRPCSTRIPXX_lv.placements.append( aEMIRPCSTRIPXXXXStripPlace.name )
            
            print("EMIRPCSTRIPXX_lv.placements.append(", aEMIRPCSTRIPXXXXStripPlace.name, ")")
            xposXXStrip = xposXXStrip + self.StripWidth + self.StripGap
            

