#!/usr/bin/env python3
import gegede.builder
import math
from duneggd.LocalTools import localtools as ltools
from duneggd.LocalTools import materialdefinition as materials
from gegede import Quantity as Q


class SandEmiRpcInnerBarrelModBuilder(gegede.builder.Builder):
    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self, 
		  trapezoidDim=None, 
		  GasThickness=None, 
		  GasMat=None, 
		  BakeliteThickness=None, 
		  BakeliteMat=None, 
		  CoatThickness=None, 
		  CoatMat=None, 
		  MylarThickness=None, 
		  MylarMat=None, 
		  **kwds):
        self.trapezoidDim = trapezoidDim
        self.MylarThickness = MylarThickness
        self.CoatThickness = CoatThickness
        self.BakeliteThickness = BakeliteThickness
        self.GasThickness = GasThickness
        self.MylarMat = MylarMat
        self.CoatMat = CoatMat
        self.BakeliteMat = BakeliteMat
        self.GasMat = GasMat
        self.Segmentation = 24.
        self.tan = math.tan(math.pi/self.Segmentation)
        self.BasePos = -trapezoidDim[3]
        
    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):
        print("----------------------------------------------------------------------")
        print("\033[36mconstruct in \033[1mSandEmiRpcInnerBarrelModBuilder\033[m\033[m")
        print("----------------------------------------------------------------------")
        print( "trapezoidDim                : ", self.trapezoidDim) 
        print( "MylarThickness              : ", self.MylarThickness)
        print( "BakeliteThickness           : ", self.BakeliteThickness)
        print( "GasThickness                : ", self.GasThickness)
        print( "CoatThickness               : ", self.CoatThickness)
        print("----------------------------------------------------------------------")
        print( "MylarMat                    : ", self.MylarMat)
        print( "BakeliteMat                 : ", self.BakeliteMat)
        print( "GasMat                      : ", self.GasMat)
        print( "CoatMat                     : ", self.CoatMat)
        print("----------------------------------------------------------------------")


        EMIRPCINNER_shape = geom.shapes.Trapezoid('EMIRPCINNER_shape', 
					   dx1=self.trapezoidDim[0], 
					   dx2=self.trapezoidDim[1],
					   dy1=self.trapezoidDim[2], 
					   dy2=self.trapezoidDim[2], 
					   dz=self.trapezoidDim[3])   

        EMIRPCINNER_lv = geom.structure.Volume('EMIRPCINNER_lv', material='Air', shape=EMIRPCINNER_shape)
        self.add_volume(EMIRPCINNER_lv)
        print(self.name)

        xpos=Q('0cm')
        ypos=Q('0cm')
        axisx = (0, 0, 1)

        # STRUCTURE (bottom up): Foam0 -> Coat0 -> Bakelite0 -> Gas0 -> Bakelite1 -> Coat1 -> Mylar0 -> Strips0 -> Mylar1 -> Coat2 -> Bakelite2 -> Gas1 -> Bakelite3 -> Coat3 -> Foam1 
        zposMylar0      = self.BasePos + 0.5 * self.MylarThickness
        zposCoat0       = self.BasePos + self.MylarThickness + 0.5 * self.CoatThickness
        zposBakelite0   = self.BasePos + self.MylarThickness + self.CoatThickness + 0.5 * self.BakeliteThickness
        zposGas0        = self.BasePos + self.MylarThickness + self.CoatThickness + self.BakeliteThickness + 0.5 * self.GasThickness
        zposBakelite1   = self.BasePos + self.MylarThickness + self.CoatThickness + self.BakeliteThickness + self.GasThickness + 0.5 * self.BakeliteThickness
        zposCoat1       = self.BasePos + self.MylarThickness + self.CoatThickness + self.BakeliteThickness + self.GasThickness + self.BakeliteThickness + 0.5 * self.CoatThickness
        zposMylar1      = self.BasePos + self.MylarThickness + self.CoatThickness + self.BakeliteThickness + self.GasThickness + self.BakeliteThickness + self.CoatThickness + 0.5 * self.MylarThickness
        
        PosMylar0    = [xpos, ypos, zposMylar0]            
        PosCoat0     = [xpos, ypos, zposCoat0]            
        PosBakelite0 = [xpos, ypos, zposBakelite0]            
        PosGas0      = [xpos, ypos, zposGas0]            
        PosBakelite1 = [xpos, ypos, zposBakelite1]            
        PosCoat1     = [xpos, ypos, zposCoat1]            
        PosMylar1    = [xpos, ypos, zposMylar1]            

        #FIRST MYLAR LAYER =================================================================
        print('Mylar [1/2]')
        aEMIRPCINNERMylar_0 = geom.shapes.Trapezoid('EMIRPCINNERMylar_0', 
                                                dx1=self.trapezoidDim[1], 
                                                dx2=self.trapezoidDim[1],
                                                dy1=self.trapezoidDim[2], 
                                                dy2=self.trapezoidDim[2], 
                                                dz=0.5*self.MylarThickness)
        aEMIRPCINNERMylar_0_lv = geom.structure.Volume('volEMIRPCINNERMylar_0', 
                                                material=self.MylarMat, 
                                                shape=aEMIRPCINNERMylar_0)
        aEMIRPCINNERMylar_0Pos= geom.structure.Position('emiMylar_0pos',
                                                PosMylar0[0], PosMylar0[1], PosMylar0[2])
        aEMIRPCINNERMylar_0Place = geom.structure.Placement('emiMylar_0pla',
                                                volume = aEMIRPCINNERMylar_0_lv,
                                                pos = aEMIRPCINNERMylar_0Pos)
        EMIRPCINNER_lv.placements.append( aEMIRPCINNERMylar_0Place.name )
        print("EMIRPCINNER_lv.placements.append(", aEMIRPCINNERMylar_0Place.name ,")")


        #FIRST COAT  LAYER =================================================================
        # Coat 0 starts --------------------
        print('Coat [1/4]')
        aEMIRPCINNERCoat_0 = geom.shapes.Trapezoid('EMIRPCINNERCoat_0', 
                                                dx1=self.trapezoidDim[1], 
                                                dx2=self.trapezoidDim[1],
                                                dy1=self.trapezoidDim[2], 
                                                dy2=self.trapezoidDim[2], 
                                                dz=0.5*self.CoatThickness)
        aEMIRPCINNERCoat_0_lv = geom.structure.Volume('volEMIRPCINNERCoat_0', 
                                                material=self.CoatMat, 
                                                shape=aEMIRPCINNERCoat_0)
        aEMIRPCINNERCoat_0Pos= geom.structure.Position('emiCoat_0pos',
                                                PosCoat0[0], PosCoat0[1], PosCoat0[2])
        aEMIRPCINNERCoat_0Place = geom.structure.Placement('emiCoat_0pla',
                                                volume = aEMIRPCINNERCoat_0_lv,
                                                pos = aEMIRPCINNERCoat_0Pos)
        EMIRPCINNER_lv.placements.append( aEMIRPCINNERCoat_0Place.name )
        print("EMIRPCINNER_lv.placements.append(", aEMIRPCINNERCoat_0Place.name, ")")
        
        #FIRST BAKELITE LAYER ==============================================================
        print('Bakelite [1/4]')
        aEMIRPCINNERBakelite_0 = geom.shapes.Trapezoid('EMIRPCINNERBakelite_0', 
                                                dx1=self.trapezoidDim[1], 
                                                dx2=self.trapezoidDim[1],
                                                dy1=self.trapezoidDim[2], 
                                                dy2=self.trapezoidDim[2], 
                                                dz=0.5*self.BakeliteThickness)

        aEMIRPCINNERBakelite_0_lv = geom.structure.Volume('volEMIRPCINNERBakelite_0', 
                                                material=self.BakeliteMat, 
                                                shape=aEMIRPCINNERBakelite_0)
      
        # EFIELD ----
        EField="(0.0, 0.0, 5000)"
        print("Setting aEMIRPCINNERBakelite_0_lv EField : ", EField)
        aEMIRPCINNERBakelite_0_lv.params.append(("EField",EField))
        # EFIELD ----

        aEMIRPCINNERBakelite_0Pos= geom.structure.Position('emiBakelite_0pos',
                                                PosBakelite0[0], PosBakelite0[1], PosBakelite0[2])
        aEMIRPCINNERBakelite_0Place = geom.structure.Placement('emiBakelitepla_0',
                                                volume = aEMIRPCINNERBakelite_0_lv,
                                                pos = aEMIRPCINNERBakelite_0Pos)

        print("EMIRPCINNER_lv.placements.append(", aEMIRPCINNERBakelite_0Place.name, ")")
        EMIRPCINNER_lv.placements.append( aEMIRPCINNERBakelite_0Place.name )


        #FIRST GAS LAYER ===================================================================
        print('Gas [1/2]')
        #for j in range(self.nStrips+1):  # 2 cm wide Gas segments cover the whole 46 cm breadth if we place every 2.5 times their width
        aEMIRPCINNERGas = geom.shapes.Trapezoid('EMIRPCINNERGas', 
                                                dx1=self.trapezoidDim[1], 
                                                dx2=self.trapezoidDim[1],
                                                dy1=self.trapezoidDim[2], 
                                                dy2=self.trapezoidDim[2], 
                                                dz=0.5*self.GasThickness)
        aEMIRPCINNERGas_lv = geom.structure.Volume('volEMIRPCINNERGas', 
                                                material=self.GasMat, 
                                                shape=aEMIRPCINNERGas)
        aEMIRPCINNERGas_lv.params.append(("SensDet","EMIGas"))
        # EFIELD ----
        EField="(0.0, 0.0, 5000)"
        print("Setting aEMIRPCINNERGas_lv EField : ", EField)
        aEMIRPCINNERGas_lv.params.append(("EField",EField))
        # EFIELD ----

        aEMIRPCINNERGas_Pos= geom.structure.Position('emiGas_pos',
                                                PosGas0[0], PosGas0[1], PosGas0[2])
        aEMIRPCINNERGas_Place = geom.structure.Placement('emiGas_pla',
                                                volume = aEMIRPCINNERGas_lv,
                                                pos = aEMIRPCINNERGas_Pos)
        EMIRPCINNER_lv.placements.append( aEMIRPCINNERGas_Place.name )
        print("EMIRPCINNER_lv.placements.append(", aEMIRPCINNERGas_Place.name, ")")

        #SECOND BAKELITE LAYER =============================================================
        print('Bakelite [2/4]')
        aEMIRPCINNERBakelite_1 = geom.shapes.Trapezoid('EMIRPCINNERBakelite_1', 
                                                dx1=self.trapezoidDim[1], 
                                                dx2=self.trapezoidDim[1],
                                                dy1=self.trapezoidDim[2], 
                                                dy2=self.trapezoidDim[2], 
                                                dz=0.5*self.BakeliteThickness)
        aEMIRPCINNERBakelite_1_lv = geom.structure.Volume('volEMIRPCINNERBakelite_1', 
                                                material=self.BakeliteMat, 
                                                shape=aEMIRPCINNERBakelite_1)
        # EFIELD ----
        EField="(0.0, 0.0, 5000)"
        print("Setting aEMIRPCINNERBakelite_0_lv EField : ", EField)
        aEMIRPCINNERBakelite_1_lv.params.append(("EField",EField))
        # EFIELD ----
        
        aEMIRPCINNERBakelite_1Pos= geom.structure.Position('emiBakelite_1pos',
                                                PosBakelite1[0], PosBakelite1[1], PosBakelite1[2])
        aEMIRPCINNERBakelite_1Place = geom.structure.Placement('emiBakelitepla_1',
                                                volume = aEMIRPCINNERBakelite_1_lv,
                                                pos = aEMIRPCINNERBakelite_1Pos)

        EMIRPCINNER_lv.placements.append( aEMIRPCINNERBakelite_1Place.name )
        print("EMIRPCINNER_lv.placements.append(", aEMIRPCINNERBakelite_1Place.name, ")")
       

        #SECOND COAT LAYER =================================================================
        print('Coat [2/4]')
        aEMIRPCINNERCoat_1 = geom.shapes.Trapezoid('EMIRPCINNERCoat_1', 
                                                dx1=self.trapezoidDim[1], 
                                                dx2=self.trapezoidDim[1],
                                                dy1=self.trapezoidDim[2], 
                                                dy2=self.trapezoidDim[2], 
                                                dz=0.5*self.CoatThickness)
        aEMIRPCINNERCoat_1_lv = geom.structure.Volume('volEMIRPCINNERCoat_1', 
                                                material=self.CoatMat, 
                                                shape=aEMIRPCINNERCoat_1)
        aEMIRPCINNERCoat_1Pos= geom.structure.Position('emiCoat_1pos',
                                                PosCoat1[0], PosCoat1[1], PosCoat1[2])
        aEMIRPCINNERCoat_1Place = geom.structure.Placement('emiCoat_1pla',
                                                volume = aEMIRPCINNERCoat_1_lv,
                                                pos = aEMIRPCINNERCoat_1Pos)

        EMIRPCINNER_lv.placements.append( aEMIRPCINNERCoat_1Place.name )
        print("EMIRPCINNER_lv.placements.append(", aEMIRPCINNERCoat_1Place.name, ")")


        #SECOND MYLAR LAYER ================================================================
        print('Mylar [2/2]')
        aEMIRPCINNERMylar_1 = geom.shapes.Trapezoid('EMIRPCINNERMylar_1', 
                                                dx1=self.trapezoidDim[1], 
                                                dx2=self.trapezoidDim[1],
                                                dy1=self.trapezoidDim[2], 
                                                dy2=self.trapezoidDim[2], 
                                                dz=0.5*self.MylarThickness)
        aEMIRPCINNERMylar_1_lv = geom.structure.Volume('volEMIRPCINNERMylar_1', 
                                                material=self.MylarMat, 
                                                shape=aEMIRPCINNERMylar_1)
        aEMIRPCINNERMylar_1Pos= geom.structure.Position('emiMylar_1pos',

                                                PosMylar1[0], PosMylar1[1], PosMylar1[2])
        aEMIRPCINNERMylar_1Place = geom.structure.Placement('emiMylar_1pla',
                                                volume = aEMIRPCINNERMylar_1_lv,
                                                pos = aEMIRPCINNERMylar_1Pos)
        EMIRPCINNER_lv.placements.append( aEMIRPCINNERMylar_1Place.name )
        print("EMIRPCINNER_lv.placements.append(", aEMIRPCINNERMylar_1Place.name, ")")




        # updating the base position for the next layer
        #self.BasePos       = self.BasePos  + self.FoamThickness + self.MylarThickness + self.CoatThickness + self.BakeliteThickness + self.GasThickness + self.BakeliteThickness + self.CoatThickness + self.MylarThickness + self.StripThickness + self.MylarThickness + self.CoatThickness + self.BakeliteThickness + self.GasThickness + self.BakeliteThickness + self.CoatThickness + self.MylarThickness + self.FoamThickness
