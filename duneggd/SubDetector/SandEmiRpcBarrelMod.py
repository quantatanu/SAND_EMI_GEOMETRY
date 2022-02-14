#!/usr/bin/env python3
import gegede.builder
import math
from duneggd.LocalTools import localtools as ltools
from duneggd.LocalTools import materialdefinition as materials
from gegede import Quantity as Q


class SandEmiRpcBarrelModBuilder(gegede.builder.Builder):
    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self, 
		  trapezoidDim=None, 
		  GasThickness=None, 
		  GasMat=None, 
		  BakeliteThickness=None, 
		  BakeliteMat=None, 
		  FoamThickness=None, 
		  FoamMat=None, 
		  CoatThickness=None, 
		  CoatMat=None, 
		  MylarThickness=None, 
		  MylarMat=None, 
		  StripThickness=None, 
		  StripWidth=None, 
		  StripGap=None, 
		  StripMat=None, 
		  nLayers=None, 
		  **kwds):
        self.trapezoidDim = trapezoidDim
        self.FoamThickness = FoamThickness
        self.MylarThickness = MylarThickness
        self.CoatThickness = CoatThickness
        self.BakeliteThickness = BakeliteThickness
        self.GasThickness = GasThickness
        self.StripThickness = StripThickness
        self.StripWidth = StripWidth
        self.StripGap = StripGap
        self.FoamMat = FoamMat
        self.MylarMat = MylarMat
        self.CoatMat = CoatMat
        self.BakeliteMat = BakeliteMat
        self.GasMat = GasMat
        self.StripMat = StripMat
        self.nLayers = nLayers
        #self.nSlabs = 3
        self.Segmentation = 24.
        #self.ang = 15
        self.tan = math.tan(math.pi/self.Segmentation)
        self.nStrips = 2*(int((trapezoidDim[0].magnitude)/(StripWidth.magnitude+StripGap.magnitude)))   # 2 because half lengths used in trapezoiddim
        self.BasePos = -trapezoidDim[3]
        
    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):
        print("----------------------------------------------------------------------")
        print("\033[36mconstruct in \033[1mSandEmiRpcBarrelModBuilder\033[m\033[m")
        print("----------------------------------------------------------------------")
        print( "FoamThickness               : ", self.FoamThickness)
        print( "MylarThickness              : ", self.MylarThickness)
        print( "BakeliteThickness           : ", self.BakeliteThickness)
        print( "GasThickness                : ", self.GasThickness)
        print( "StripThickness              : ", self.StripThickness)
        print("----------------------------------------------------------------------")
        print( "FoamMat                     : ", self.FoamMat)
        print( "MylarMat                    : ", self.MylarMat)
        print( "BakeliteMat                 : ", self.BakeliteMat)
        print( "GasMat                      : ", self.GasMat)
        print( "StripMat                    : ", self.StripMat)
        print( "StripWidth                  : ", self.StripWidth)
        print( "StripGap                  : ", self.StripGap)
        print("----------------------------------------------------------------------")
        print( "nLayers                     : ", self.nLayers)
        print( "nStrips                     : ", self.nStrips)
        print("----------------------------------------------------------------------")


        EMIRPC_shape = geom.shapes.Trapezoid('EMIRPC_shape', 
					   dx1=self.trapezoidDim[0], 
					   dx2=self.trapezoidDim[1],
					   dy1=self.trapezoidDim[2], 
					   dy2=self.trapezoidDim[2], 
					   dz=self.nLayers * self.trapezoidDim[3])   

        EMIRPC_lv = geom.structure.Volume('EMIRPC_lv', material='Air', shape=EMIRPC_shape)
        self.add_volume(EMIRPC_lv)
        print(self.name)
        

        xposStrip0 = -self.trapezoidDim[0] + 0.5 * self.StripWidth
        xposGasSeg0 = -self.trapezoidDim[0] + 0.5 * self.StripWidth
        xposGasSeg1 = -self.trapezoidDim[0] + 0.5 * self.StripWidth
        print("--------------------------------------------------------->INITIAL STRIP POSITION: ")
        print("xposStrip0 = ", -self.trapezoidDim[0], "+ 0.5 * ", self.StripWidth, " =", xposStrip0)
        xpos=Q('0cm')
        ypos=Q('0cm')
        axisx = (0, 0, 1)
        # STRUCTURE (bottom up): Foam0 -> Coat0 -> Bakelite0 -> Gas0 -> Bakelite1 -> Coat1 -> Mylar0 -> Strips0 -> Mylar1 -> Coat2 -> Bakelite2 -> Gas1 -> Bakelite3 -> Coat3 -> Foam1 
        zposFoam0       = self.BasePos  + 0.5 * self.FoamThickness
        zposMylar0      = self.BasePos  + self.FoamThickness + 0.5 * self.MylarThickness
        zposCoat0       = self.BasePos  + self.FoamThickness + self.MylarThickness + 0.5 * self.CoatThickness
        zposBakelite0   = self.BasePos  + self.FoamThickness + self.MylarThickness + self.CoatThickness + 0.5 * self.BakeliteThickness
        zposGas0        = self.BasePos  + self.FoamThickness + self.MylarThickness + self.CoatThickness + self.BakeliteThickness + 0.5 * self.GasThickness
        zposBakelite1   = self.BasePos  + self.FoamThickness + self.MylarThickness + self.CoatThickness + self.BakeliteThickness + self.GasThickness + 0.5 * self.BakeliteThickness
        zposCoat1       = self.BasePos  + self.FoamThickness + self.MylarThickness + self.CoatThickness + self.BakeliteThickness + self.GasThickness + self.BakeliteThickness + 0.5 * self.CoatThickness
        zposMylar1      = self.BasePos  + self.FoamThickness + self.MylarThickness + self.CoatThickness + self.BakeliteThickness + self.GasThickness + self.BakeliteThickness + self.CoatThickness + 0.5 * self.MylarThickness
        zposStrip0      = self.BasePos  + self.FoamThickness + self.MylarThickness + self.CoatThickness + self.BakeliteThickness + self.GasThickness + self.BakeliteThickness + self.CoatThickness + self.MylarThickness + 0.5 * self.StripThickness 
        zposMylar2      = self.BasePos  + self.FoamThickness + self.MylarThickness + self.CoatThickness + self.BakeliteThickness + self.GasThickness + self.BakeliteThickness + self.CoatThickness + self.MylarThickness + self.StripThickness + 0.5 * self.MylarThickness
        zposCoat2       = self.BasePos  + self.FoamThickness + self.MylarThickness + self.CoatThickness + self.BakeliteThickness + self.GasThickness + self.BakeliteThickness + self.CoatThickness + self.MylarThickness + self.StripThickness + self.MylarThickness + 0.5 * self.CoatThickness
        zposBakelite2   = self.BasePos  + self.FoamThickness + self.MylarThickness + self.CoatThickness + self.BakeliteThickness + self.GasThickness + self.BakeliteThickness + self.CoatThickness + self.MylarThickness + self.StripThickness + self.MylarThickness + self.CoatThickness + 0.5 * self.BakeliteThickness
        zposGas1        = self.BasePos  + self.FoamThickness + self.MylarThickness + self.CoatThickness + self.BakeliteThickness + self.GasThickness + self.BakeliteThickness + self.CoatThickness + self.MylarThickness + self.StripThickness + self.MylarThickness + self.CoatThickness + self.BakeliteThickness + 0.5 * self.GasThickness
        zposBakelite3   = self.BasePos  + self.FoamThickness + self.MylarThickness + self.CoatThickness + self.BakeliteThickness + self.GasThickness + self.BakeliteThickness + self.CoatThickness + self.MylarThickness + self.StripThickness + self.MylarThickness + self.CoatThickness + self.BakeliteThickness + self.GasThickness + 0.5 * self.BakeliteThickness
        zposCoat3       = self.BasePos  + self.FoamThickness + self.MylarThickness + self.CoatThickness + self.BakeliteThickness + self.GasThickness + self.BakeliteThickness + self.CoatThickness + self.MylarThickness + self.StripThickness + self.MylarThickness + self.CoatThickness + self.BakeliteThickness + self.GasThickness + self.BakeliteThickness + 0.5 * self.CoatThickness
        zposMylar3      = self.BasePos  + self.FoamThickness + self.MylarThickness + self.CoatThickness + self.BakeliteThickness + self.GasThickness + self.BakeliteThickness + self.CoatThickness + self.MylarThickness + self.StripThickness + self.MylarThickness + self.CoatThickness + self.BakeliteThickness + self.GasThickness + self.BakeliteThickness + self.CoatThickness + 0.5 * self.MylarThickness
        zposFoam1       = self.BasePos  + self.FoamThickness + self.MylarThickness + self.CoatThickness + self.BakeliteThickness + self.GasThickness + self.BakeliteThickness + self.CoatThickness + self.MylarThickness + self.StripThickness + self.MylarThickness + self.CoatThickness + self.BakeliteThickness + self.GasThickness + self.BakeliteThickness + self.CoatThickness + self.MylarThickness + 0.5 * self.FoamThickness
        PosFoam0    = [xpos, ypos, zposFoam0]            
        PosFoam1    = [xpos, ypos, zposFoam1]            
        PosMylar0   = [xpos, ypos, zposMylar0]            
        PosMylar1   = [xpos, ypos, zposMylar1]            
        PosMylar2   = [xpos, ypos, zposMylar2]            
        PosMylar3   = [xpos, ypos, zposMylar3]            
        PosCoat0    = [xpos, ypos, zposCoat0]            
        PosCoat1    = [xpos, ypos, zposCoat1]            
        PosCoat2    = [xpos, ypos, zposCoat2]            
        PosCoat3    = [xpos, ypos, zposCoat3]            
        PosBakelite0= [xpos, ypos, zposBakelite0]            
        PosBakelite1= [xpos, ypos, zposBakelite1]            
        PosBakelite2= [xpos, ypos, zposBakelite2]            
        PosBakelite3= [xpos, ypos, zposBakelite3]            
        PosGas0     = [xpos, ypos, zposGas0]            
        PosGas1     = [xpos, ypos, zposGas1]            
        PosStrip0   = [xpos, ypos, zposStrip0]            


        #FIRST FOAM LAYER ==================================================================
        print('Foam [1/2]')
        aEMIRPCFoam_0 = geom.shapes.Trapezoid('EMIRPCFoam_0', 
                                                dx1=self.trapezoidDim[1], 
                                                dx2=self.trapezoidDim[1],
                                                dy1=self.trapezoidDim[2], 
                                                dy2=self.trapezoidDim[2], 
                                                dz=0.5*self.FoamThickness)
        aEMIRPCFoam_0_lv = geom.structure.Volume('volEMIRPCFoam_0', 
                                                material=self.FoamMat, 
                                                shape=aEMIRPCFoam_0)
        aEMIRPCFoam_0Pos= geom.structure.Position('emiFoam_0pos',
                                                PosFoam0[0], PosFoam0[1], PosFoam0[2])
        aEMIRPCFoam_0Place = geom.structure.Placement('emiFoam_0pla',
                                                volume = aEMIRPCFoam_0_lv,
                                                pos = aEMIRPCFoam_0Pos)
        EMIRPC_lv.placements.append( aEMIRPCFoam_0Place.name )
        print("EMIRPC_lv.placements.append(", aEMIRPCFoam_0Place.name, ")")

        #FIRST MYLAR LAYER =================================================================
        print('Mylar [1/2]')
        aEMIRPCMylar_0 = geom.shapes.Trapezoid('EMIRPCMylar_0', 
                                                dx1=self.trapezoidDim[1], 
                                                dx2=self.trapezoidDim[1],
                                                dy1=self.trapezoidDim[2], 
                                                dy2=self.trapezoidDim[2], 
                                                dz=0.5*self.MylarThickness)
        aEMIRPCMylar_0_lv = geom.structure.Volume('volEMIRPCMylar_0', 
                                                material=self.MylarMat, 
                                                shape=aEMIRPCMylar_0)
        aEMIRPCMylar_0Pos= geom.structure.Position('emiMylar_0pos',
                                                PosMylar0[0], PosMylar0[1], PosMylar0[2])
        aEMIRPCMylar_0Place = geom.structure.Placement('emiMylar_0pla',
                                                volume = aEMIRPCMylar_0_lv,
                                                pos = aEMIRPCMylar_0Pos)
        EMIRPC_lv.placements.append( aEMIRPCMylar_0Place.name )
        print("EMIRPC_lv.placements.append(", aEMIRPCMylar_0Place.name ,")")


        #FIRST COAT  LAYER =================================================================
        # Coat 0 starts --------------------
        print('Coat [1/4]')
        aEMIRPCCoat_0 = geom.shapes.Trapezoid('EMIRPCCoat_0', 
                                                dx1=self.trapezoidDim[1], 
                                                dx2=self.trapezoidDim[1],
                                                dy1=self.trapezoidDim[2], 
                                                dy2=self.trapezoidDim[2], 
                                                dz=0.5*self.CoatThickness)
        aEMIRPCCoat_0_lv = geom.structure.Volume('volEMIRPCCoat_0', 
                                                material=self.CoatMat, 
                                                shape=aEMIRPCCoat_0)
        aEMIRPCCoat_0Pos= geom.structure.Position('emiCoat_0pos',
                                                PosCoat0[0], PosCoat0[1], PosCoat0[2])
        aEMIRPCCoat_0Place = geom.structure.Placement('emiCoat_0pla',
                                                volume = aEMIRPCCoat_0_lv,
                                                pos = aEMIRPCCoat_0Pos)
        EMIRPC_lv.placements.append( aEMIRPCCoat_0Place.name )
        print("EMIRPC_lv.placements.append(", aEMIRPCCoat_0Place.name, ")")
        
        #FIRST BAKELITE LAYER ==============================================================
        print('Bakelite [1/4]')
        aEMIRPCBakelite_0 = geom.shapes.Trapezoid('EMIRPCBakelite_0', 
                                                dx1=self.trapezoidDim[1], 
                                                dx2=self.trapezoidDim[1],
                                                dy1=self.trapezoidDim[2], 
                                                dy2=self.trapezoidDim[2], 
                                                dz=0.5*self.BakeliteThickness)

        aEMIRPCBakelite_0_lv = geom.structure.Volume('volEMIRPCBakelite_0', 
                                                material=self.BakeliteMat, 
                                                shape=aEMIRPCBakelite_0)
      
        # EFIELD ----
        EField="(0.0, 0.0, -5000)"
        print("Setting aEMIRPCBakelite_0_lv EField : ", EField)
        aEMIRPCBakelite_0_lv.params.append(("EField",EField))
        # EFIELD ----

        aEMIRPCBakelite_0Pos= geom.structure.Position('emiBakelite_0pos',
                                                PosBakelite0[0], PosBakelite0[1], PosBakelite0[2])
        aEMIRPCBakelite_0Place = geom.structure.Placement('emiBakelitepla_0',
                                                volume = aEMIRPCBakelite_0_lv,
                                                pos = aEMIRPCBakelite_0Pos)

        print("EMIRPC_lv.placements.append(", aEMIRPCBakelite_0Place.name, ")")
        EMIRPC_lv.placements.append( aEMIRPCBakelite_0Place.name )


        #FIRST GAS LAYER ===================================================================
        print('Gas [1/2]')
        for j in range(self.nStrips+1):  # 2 cm wide Gas segments cover the whole 46 cm breadth if we place every 2.5 times their width
            aEMIRPCGas_0 = geom.shapes.Trapezoid('EMIRPCGas_0_'+str(j), 
                                                    dx1=self.StripWidth/2, 
                                                    dx2=self.StripWidth/2,
                                                    dy1=self.trapezoidDim[2], 
                                                    dy2=self.trapezoidDim[2], 
                                                    dz=0.5*self.StripThickness)
            aEMIRPCGas_0_lv = geom.structure.Volume('volEMIRPCGas_0_'+str(j), 
                                                    material=self.GasMat, 
                                                    shape=aEMIRPCGas_0)
            # EFIELD ----
            EField="(0.0, 0.0, -5000)"
            print("Setting aEMIRPCGas_0_lv EField : ", EField)
            aEMIRPCGas_0_lv.params.append(("EField",EField))
            # EFIELD ----

            aEMIRPCGas_0Pos= geom.structure.Position('emiGas_0pos_'+str(j),
                                                    xposGasSeg0, PosGas0[1], PosGas0[2])
            aEMIRPCGas_0Place = geom.structure.Placement('emiGas_0pla_'+str(j),
                                                    volume = aEMIRPCGas_0_lv,
                                                    pos = aEMIRPCGas_0Pos)
            EMIRPC_lv.placements.append( aEMIRPCGas_0Place.name )
            print("EMIRPC_lv.placements.append(", aEMIRPCGas_0Place.name, ")")
            xposGasSeg0 = xposGasSeg0 + self.StripWidth + self.StripGap

        #SECOND BAKELITE LAYER =============================================================
        print('Bakelite [2/4]')
        aEMIRPCBakelite_1 = geom.shapes.Trapezoid('EMIRPCBakelite_1', 
                                                dx1=self.trapezoidDim[1], 
                                                dx2=self.trapezoidDim[1],
                                                dy1=self.trapezoidDim[2], 
                                                dy2=self.trapezoidDim[2], 
                                                dz=0.5*self.BakeliteThickness)
        aEMIRPCBakelite_1_lv = geom.structure.Volume('volEMIRPCBakelite_1', 
                                                material=self.BakeliteMat, 
                                                shape=aEMIRPCBakelite_1)
        # EFIELD ----
        EField="(0.0, 0.0, -5000)"
        print("Setting aEMIRPCBakelite_0_lv EField : ", EField)
        aEMIRPCBakelite_1_lv.params.append(("EField",EField))
        # EFIELD ----
        
        aEMIRPCBakelite_1Pos= geom.structure.Position('emiBakelite_1pos',
                                                PosBakelite1[0], PosBakelite1[1], PosBakelite1[2])
        aEMIRPCBakelite_1Place = geom.structure.Placement('emiBakelitepla_1',
                                                volume = aEMIRPCBakelite_1_lv,
                                                pos = aEMIRPCBakelite_1Pos)

        EMIRPC_lv.placements.append( aEMIRPCBakelite_1Place.name )
        print("EMIRPC_lv.placements.append(", aEMIRPCBakelite_1Place.name, ")")
       

        #SECOND COAT LAYER =================================================================
        print('Coat [2/4]')
        aEMIRPCCoat_1 = geom.shapes.Trapezoid('EMIRPCCoat_1', 
                                                dx1=self.trapezoidDim[1], 
                                                dx2=self.trapezoidDim[1],
                                                dy1=self.trapezoidDim[2], 
                                                dy2=self.trapezoidDim[2], 
                                                dz=0.5*self.CoatThickness)
        aEMIRPCCoat_1_lv = geom.structure.Volume('volEMIRPCCoat_1', 
                                                material=self.CoatMat, 
                                                shape=aEMIRPCCoat_1)
        aEMIRPCCoat_1Pos= geom.structure.Position('emiCoat_1pos',
                                                PosCoat1[0], PosCoat1[1], PosCoat1[2])
        aEMIRPCCoat_1Place = geom.structure.Placement('emiCoat_1pla',
                                                volume = aEMIRPCCoat_1_lv,
                                                pos = aEMIRPCCoat_1Pos)
        EMIRPC_lv.placements.append( aEMIRPCCoat_1Place.name )
        print("EMIRPC_lv.placements.append(", aEMIRPCCoat_1Place.name, ")")


        #SECOND MYLAR LAYER ================================================================
        print('Mylar [2/2]')
        aEMIRPCMylar_1 = geom.shapes.Trapezoid('EMIRPCMylar_1', 
                                                dx1=self.trapezoidDim[1], 
                                                dx2=self.trapezoidDim[1],
                                                dy1=self.trapezoidDim[2], 
                                                dy2=self.trapezoidDim[2], 
                                                dz=0.5*self.MylarThickness)
        aEMIRPCMylar_1_lv = geom.structure.Volume('volEMIRPCMylar_1', 
                                                material=self.MylarMat, 
                                                shape=aEMIRPCMylar_1)
        aEMIRPCMylar_1Pos= geom.structure.Position('emiMylar_1pos',

                                                PosMylar1[0], PosMylar1[1], PosMylar1[2])
        aEMIRPCMylar_1Place = geom.structure.Placement('emiMylar_1pla',
                                                volume = aEMIRPCMylar_1_lv,
                                                pos = aEMIRPCMylar_1Pos)
        EMIRPC_lv.placements.append( aEMIRPCMylar_1Place.name )
        print("EMIRPC_lv.placements.append(", aEMIRPCMylar_1Place.name, ")")


        #FIRST STRIP  LAYER ================================================================
        print('Strip [1/1]')
        for j in range(self.nStrips+1):  # 2 cm wide Strips cover the whole 46 cm breadth if we place every 2.5 times their width
            aEMIRPCStrip_0 = geom.shapes.Trapezoid('EMIRPCStrip_0_'+str(j), 
                                                    dx1=self.StripWidth/2, 
                                                    dx2=self.StripWidth/2,
                                                    dy1=self.trapezoidDim[2], 
                                                    dy2=self.trapezoidDim[2], 
                                                    dz=0.5*self.StripThickness)
            aEMIRPCStrip_0_lv = geom.structure.Volume('volEMIRPCStrip_0_'+str(j), 
                                                    material=self.StripMat, 
                                                    shape=aEMIRPCStrip_0)
            aEMIRPCStrip_0Pos= geom.structure.Position('emiStrip_0pos_'+str(j),
                                                    xposStrip0, PosStrip0[1], PosStrip0[2])
            aEMIRPCStrip_0Place = geom.structure.Placement('emiStrip_0pla_'+str(j),
                                                    volume = aEMIRPCStrip_0_lv,
                                                    pos = aEMIRPCStrip_0Pos)
            EMIRPC_lv.placements.append( aEMIRPCStrip_0Place.name )
            print("EMIRPC_lv.placements.append(", aEMIRPCStrip_0Place.name, ")")
            xposStrip0 = xposStrip0 + self.StripWidth + self.StripGap


        #THIRD  MYLAR LAYER ================================================================
        print('Mylar [3/4]')
        aEMIRPCMylar_2 = geom.shapes.Trapezoid('EMIRPCMylar_2', 
                                                dx1=self.trapezoidDim[1], 
                                                dx2=self.trapezoidDim[1],
                                                dy1=self.trapezoidDim[2], 
                                                dy2=self.trapezoidDim[2], 
                                                dz=0.5*self.MylarThickness)
        aEMIRPCMylar_2_lv = geom.structure.Volume('volEMIRPCMylar_2', 
                                                material=self.MylarMat, 
                                                shape=aEMIRPCMylar_2)
        aEMIRPCMylar_2Pos= geom.structure.Position('emiMylar_2pos',
                                                PosMylar2[0], PosMylar2[1], PosMylar2[2])
        aEMIRPCMylar_2Place = geom.structure.Placement('emiMylar_2pla',
                                                volume = aEMIRPCMylar_2_lv,
                                                pos = aEMIRPCMylar_2Pos)
        EMIRPC_lv.placements.append( aEMIRPCMylar_2Place.name )
        print("EMIRPC_lv.placements.append(", aEMIRPCMylar_2Place.name, ")")


        #THIRD  COAT LAYER =================================================================
        print('Coat [3/4]')
        aEMIRPCCoat_2 = geom.shapes.Trapezoid('EMIRPCCoat_2', 
                                                dx1=self.trapezoidDim[1], 
                                                dx2=self.trapezoidDim[1],
                                                dy1=self.trapezoidDim[2], 
                                                dy2=self.trapezoidDim[2], 
                                                dz=0.5*self.CoatThickness)
        aEMIRPCCoat_2_lv = geom.structure.Volume('volEMIRPCCoat_2', 
                                                material=self.CoatMat, 
                                                shape=aEMIRPCCoat_2)
        aEMIRPCCoat_2Pos= geom.structure.Position('emiCoat_2pos',
                                                PosCoat2[0], PosCoat2[1], PosCoat2[2])
        aEMIRPCCoat_2Place = geom.structure.Placement('emiCoat_2pla',
                                                volume = aEMIRPCCoat_2_lv,
                                                pos = aEMIRPCCoat_2Pos)
        EMIRPC_lv.placements.append( aEMIRPCCoat_2Place.name )
        print("EMIRPC_lv.placements.append(", aEMIRPCCoat_2Place.name, ")")


        #THIRD  BAKELITE LAYER =============================================================
        print('Bakelite [3/4]')
        aEMIRPCBakelite_2 = geom.shapes.Trapezoid('EMIRPCBakelite_2', 
                                                dx1=self.trapezoidDim[1], 
                                                dx2=self.trapezoidDim[1],
                                                dy1=self.trapezoidDim[2], 
                                                dy2=self.trapezoidDim[2], 
                                                dz=0.5*self.BakeliteThickness)
        aEMIRPCBakelite_2_lv = geom.structure.Volume('volEMIRPCBakelite_2', 
                                                material=self.BakeliteMat, 
                                                shape=aEMIRPCBakelite_2)
        # EFIELD ----
        EField="(0.0, 0.0, 5000)"
        print("Setting aEMIRPCBakelite_2_lv EField : ", EField)
        aEMIRPCBakelite_2_lv.params.append(("EField",EField))
        # EFIELD ----
        aEMIRPCBakelite_2Pos= geom.structure.Position('emiBakelite_2pos',
                                                PosBakelite2[0], PosBakelite2[1], PosBakelite2[2])
        aEMIRPCBakelite_2Place = geom.structure.Placement('emiBakelitepla_2',
                                                volume = aEMIRPCBakelite_0_lv,
                                                pos = aEMIRPCBakelite_2Pos)
        EMIRPC_lv.placements.append( aEMIRPCBakelite_2Place.name )
        print("EMIRPC_lv.placements.append(", aEMIRPCBakelite_2Place.name, ")")


        #SECOND GAS LAYER ==================================================================
        print('Gas [2/2]')
        for j in range(self.nStrips+1):  # 2 cm wide Gas segments cover the whole 46 cm breadth if we place every 2.5 times their width
            aEMIRPCGas_1 = geom.shapes.Trapezoid('EMIRPCGas_1_'+str(j), 
                                                    dx1=self.StripWidth/2, 
                                                    dx2=self.StripWidth/2,
                                                    dy1=self.trapezoidDim[2], 
                                                    dy2=self.trapezoidDim[2], 
                                                    dz=0.5*self.StripThickness)
            aEMIRPCGas_1_lv = geom.structure.Volume('volEMIRPCGas_1_'+str(j), 
                                                    material=self.GasMat, 
                                                    shape=aEMIRPCGas_1)
            # EFIELD ----
            EField="(0.0, 0.0, 5000)"
            print("Setting aEMIRPCGas_1_lv EField : ", EField)
            aEMIRPCGas_1_lv.params.append(("EField",EField))
            # EFIELD ----

            aEMIRPCGas_1Pos= geom.structure.Position('emiGas_1pos_'+str(j),
                                                    xposGasSeg1, PosGas1[1], PosGas1[2])
            aEMIRPCGas_1Place = geom.structure.Placement('emiGas_1pla_'+str(j),
                                                    volume = aEMIRPCGas_1_lv,
                                                    pos = aEMIRPCGas_1Pos)
            EMIRPC_lv.placements.append( aEMIRPCGas_1Place.name )
            print("EMIRPC_lv.placements.append(", aEMIRPCGas_1Place.name, ")")
            xposGasSeg1 = xposGasSeg1 + self.StripWidth + self.StripGap


        #FOURTH BAKELITE LAYER =============================================================
        print('Bakelite [4/4]')
        aEMIRPCBakelite_3 = geom.shapes.Trapezoid('EMIRPCBakelite_3', 
                                                dx1=self.trapezoidDim[1], 
                                                dx2=self.trapezoidDim[1],
                                                dy1=self.trapezoidDim[2], 
                                                dy2=self.trapezoidDim[2], 
                                                dz=0.5*self.BakeliteThickness)
        aEMIRPCBakelite_3_lv = geom.structure.Volume('volEMIRPCBakelite_3', 
                                                material=self.BakeliteMat, 
                                                shape=aEMIRPCBakelite_3)
        # EFIELD ----
        EField="(0.0, 0.0, 5000)"
        print("Setting aEMIRPCBakelite_3_lv EField : ", EField)
        aEMIRPCBakelite_3_lv.params.append(("EField",EField))
        # EFIELD ----
        aEMIRPCBakelite_3Pos= geom.structure.Position('emiBakelite_3pos',
                                                PosBakelite3[0], PosBakelite3[1], PosBakelite3[2])
        aEMIRPCBakelite_3Place = geom.structure.Placement('emiBakelite_3pla',
                                                volume = aEMIRPCBakelite_3_lv,
                                                pos = aEMIRPCBakelite_3Pos)

        EMIRPC_lv.placements.append( aEMIRPCBakelite_3Place.name )
        print("EMIRPC_lv.placements.append(", aEMIRPCBakelite_3Place.name, ")")


        #FOURTH COAT LAYER =================================================================
        print('Coat [4/4]')
        aEMIRPCCoat_3 = geom.shapes.Trapezoid('EMIRPCCoat_3', 
                                                dx1=self.trapezoidDim[1], 
                                                dx2=self.trapezoidDim[1],
                                                dy1=self.trapezoidDim[2], 
                                                dy2=self.trapezoidDim[2], 
                                                dz=0.5*self.CoatThickness)
        aEMIRPCCoat_3_lv = geom.structure.Volume('volEMIRPCCoat_3', 
                                                material=self.CoatMat, 
                                                shape=aEMIRPCCoat_3)
        aEMIRPCCoat_3Pos= geom.structure.Position('emiCoat_3pos',
                                                PosCoat3[0], PosCoat3[1], PosCoat3[2])
        aEMIRPCCoat_3Place = geom.structure.Placement('emiCoat_3pla',
                                                volume = aEMIRPCCoat_3_lv,
                                                pos = aEMIRPCCoat_3Pos)
        EMIRPC_lv.placements.append( aEMIRPCCoat_3Place.name )
        print("EMIRPC_lv.placements.append(", aEMIRPCCoat_3Place.name, ")")


        #FOURTH MYLAR LAYER ================================================================
        print('Mylar [4/4]')
        aEMIRPCMylar_3 = geom.shapes.Trapezoid('EMIRPCMylar_3', 
                                                dx1=self.trapezoidDim[1], 
                                                dx2=self.trapezoidDim[1],
                                                dy1=self.trapezoidDim[2], 
                                                dy2=self.trapezoidDim[2], 
                                                dz=0.5*self.MylarThickness)
        aEMIRPCMylar_3_lv = geom.structure.Volume('volEMIRPCMylar_3', 
                                                material=self.MylarMat, 
                                                shape=aEMIRPCMylar_3)
        aEMIRPCMylar_3Pos= geom.structure.Position('emiMylar_3pos',
                                                PosMylar3[0], PosMylar3[1], PosMylar3[2])
        aEMIRPCMylar_3Place = geom.structure.Placement('emiMylar_3pla',
                                                volume = aEMIRPCMylar_3_lv,
                                                pos = aEMIRPCMylar_3Pos)
        EMIRPC_lv.placements.append( aEMIRPCMylar_3Place.name )
        print("EMIRPC_lv.placements.append(", aEMIRPCMylar_3Place.name, ")")


        #SECOND FOAM LAYER =================================================================
        print('Foam [2/2]')
        aEMIRPCFoam_1 = geom.shapes.Trapezoid('EMIRPCFoam_1', 
                                                dx1=self.trapezoidDim[1], 
                                                dx2=self.trapezoidDim[1],
                                                dy1=self.trapezoidDim[2], 
                                                dy2=self.trapezoidDim[2], 
                                                dz=0.5*self.FoamThickness)
        aEMIRPCFoam_1_lv = geom.structure.Volume('volEMIRPCFoam_1', 
                                                material=self.FoamMat, 
                                                shape=aEMIRPCFoam_1)
        aEMIRPCFoam_1Pos= geom.structure.Position('emiFoam_3pos',
                                                PosFoam1[0], PosFoam1[1], PosFoam1[2])
        aEMIRPCFoam_1Place = geom.structure.Placement('emiFoam_1pla',
                                                volume = aEMIRPCFoam_1_lv,
                                                pos = aEMIRPCFoam_1Pos)
        EMIRPC_lv.placements.append( aEMIRPCFoam_1Place.name )
        print("EMIRPC_lv.placements.append(", aEMIRPCFoam_1Place.name, ")")


        # updating the base position for the next layer
        #self.BasePos       = self.BasePos  + self.FoamThickness + self.MylarThickness + self.CoatThickness + self.BakeliteThickness + self.GasThickness + self.BakeliteThickness + self.CoatThickness + self.MylarThickness + self.StripThickness + self.MylarThickness + self.CoatThickness + self.BakeliteThickness + self.GasThickness + self.BakeliteThickness + self.CoatThickness + self.MylarThickness + self.FoamThickness
