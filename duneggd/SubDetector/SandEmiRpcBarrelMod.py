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
        

        xposXXStrip = -self.trapezoidDim[0] + 0.5 * self.StripWidth
        yposYYStrip = -self.trapezoidDim[0] + 0.5 * self.StripWidth
        print("--------------------------------------------------------->INITIAL STRIP POSITION: ")
        print("xposXXStrip = ", -self.trapezoidDim[0], "+ 0.5 * ", self.StripWidth, " =", xposXXStrip)
        xpos=Q('0cm')
        ypos=Q('0cm')
        axisx = (0, 0, 1)

        # STRUCTURE (bottom up): Foam0 -> Coat0 -> Bakelite0 -> Gas0 -> Bakelite1 -> Coat1 -> Mylar0 -> Strips0 -> Mylar1 -> Coat2 -> Bakelite2 -> Gas1 -> Bakelite3 -> Coat3 -> Foam1 
        zposFoam0       = self.BasePos  + 0.5 * self.FoamThickness
        zposXXStrip      = self.BasePos  + self.FoamThickness + 0.5 * self.StripThickness
        zposMylar0      = self.BasePos  + self.FoamThickness + self.StripThickness + 0.5 * self.MylarThickness
        zposCoat0       = self.BasePos  + self.FoamThickness + self.StripThickness + self.MylarThickness + 0.5 * self.CoatThickness
        zposBakelite0   = self.BasePos  + self.FoamThickness + self.StripThickness + self.MylarThickness + self.CoatThickness + 0.5 * self.BakeliteThickness
        zposGas0        = self.BasePos  + self.FoamThickness + self.StripThickness + self.MylarThickness + self.CoatThickness + self.BakeliteThickness + 0.5 * self.GasThickness
        zposBakelite1   = self.BasePos  + self.FoamThickness + self.StripThickness + self.MylarThickness + self.CoatThickness + self.BakeliteThickness + self.GasThickness + 0.5 * self.BakeliteThickness
        zposCoat1       = self.BasePos  + self.FoamThickness + self.StripThickness + self.MylarThickness + self.CoatThickness + self.BakeliteThickness + self.GasThickness + self.BakeliteThickness + 0.5 * self.CoatThickness
        zposMylar1      = self.BasePos  + self.FoamThickness + self.StripThickness + self.MylarThickness + self.CoatThickness + self.BakeliteThickness + self.GasThickness + self.BakeliteThickness + self.CoatThickness + 0.5 * self.MylarThickness
        zposYYStrip      = self.BasePos  + self.FoamThickness + self.StripThickness + self.MylarThickness + self.CoatThickness + self.BakeliteThickness + self.GasThickness + self.BakeliteThickness + self.CoatThickness + self.MylarThickness + 0.5 * self.StripThickness 
        zposFoam1       = self.BasePos  + self.FoamThickness + self.StripThickness + self.MylarThickness + self.CoatThickness + self.BakeliteThickness + self.GasThickness + self.BakeliteThickness + self.CoatThickness + self.MylarThickness + self.StripThickness + self.MylarThickness + self.CoatThickness + self.BakeliteThickness + self.GasThickness + self.BakeliteThickness + self.CoatThickness + self.MylarThickness + 0.5 * self.FoamThickness
        
        PosFoam0    = [xpos, ypos, zposFoam0]            
        PosXXStrip   = [xpos, ypos, zposXXStrip]            
        PosMylar0   = [xpos, ypos, zposMylar0]            
        PosCoat0    = [xpos, ypos, zposCoat0]            
        PosBakelite0= [xpos, ypos, zposBakelite0]            
        PosGas0     = [xpos, ypos, zposGas0]            
        PosBakelite1= [xpos, ypos, zposBakelite1]            
        PosCoat1    = [xpos, ypos, zposCoat1]            
        PosMylar1   = [xpos, ypos, zposMylar1]            
        PosYYStrip   = [xpos, ypos, zposYYStrip]            
        PosFoam1    = [xpos, ypos, zposFoam1]            
        


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



        #FIRST STRIP  LAYER ================================================================
        print('Strip [XX]')
        for j in range(self.nStrips+1):  # 2 cm wide Strips cover the whole 46 cm breadth if we place every 2.5 times their width
            aEMIRPCXXStrip = geom.shapes.Trapezoid('EMIRPCXXStrip_'+str(j), 
                                                    dx1=self.StripWidth/2, 
                                                    dx2=self.StripWidth/2,
                                                    dy1=self.trapezoidDim[2], 
                                                    dy2=self.trapezoidDim[2], 
                                                    dz=0.5*self.StripThickness)
            aEMIRPCXXStrip_lv = geom.structure.Volume('volEMIRPCXXStrip_'+str(j), 
                                                    material=self.StripMat, 
                                                    shape=aEMIRPCXXStrip)
            aEMIRPCXXStripPos= geom.structure.Position('emiXXStrippos_'+str(j),
                                                    xposXXStrip, PosXXStrip[1], PosXXStrip[2])
            aEMIRPCXXStripPlace = geom.structure.Placement('emiXXStrippla_'+str(j),
                                                    volume = aEMIRPCXXStrip_lv,
                                                    pos = aEMIRPCXXStripPos)
            EMIRPC_lv.placements.append( aEMIRPCXXStripPlace.name )
            print("EMIRPC_lv.placements.append(", aEMIRPCXXStripPlace.name, ")")
            xposXXStrip = xposXXStrip + self.StripWidth + self.StripGap


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
        EField="(0.0, 0.0, 5000)"
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
        #for j in range(self.nStrips+1):  # 2 cm wide Gas segments cover the whole 46 cm breadth if we place every 2.5 times their width
        aEMIRPCGas = geom.shapes.Trapezoid('EMIRPCGas', 
                                                dx1=self.StripWidth/2, 
                                                dx2=self.StripWidth/2,
                                                dy1=self.trapezoidDim[2], 
                                                dy2=self.trapezoidDim[2], 
                                                dz=0.5*self.StripThickness)
        aEMIRPCGas_lv = geom.structure.Volume('volEMIRPCGas', 
                                                material=self.GasMat, 
                                                shape=aEMIRPCGas)
        aEMIRPCGas_lv.params.append(("SensDet","EMIGas"))
        # EFIELD ----
        EField="(0.0, 0.0, 5000)"
        print("Setting aEMIRPCGas_lv EField : ", EField)
        aEMIRPCGas_lv.params.append(("EField",EField))
        # EFIELD ----

        aEMIRPCGas_Pos= geom.structure.Position('emiGas_pos',
                                                PosGas0[0], PosGas0[1], PosGas0[2])
        aEMIRPCGas_Place = geom.structure.Placement('emiGas_pla',
                                                volume = aEMIRPCGas_lv,
                                                pos = aEMIRPCGas_Pos)
        EMIRPC_lv.placements.append( aEMIRPCGas_Place.name )
        print("EMIRPC_lv.placements.append(", aEMIRPCGas_Place.name, ")")

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
        EField="(0.0, 0.0, 5000)"
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
        print('Strip [YY]')
        for j in range(self.nStrips+1):  # 2 cm wide Strips cover the whole 46 cm breadth if we place every 2.5 times their width
            aEMIRPCYYStrip = geom.shapes.Trapezoid('EMIRPCYYStrip_'+str(j), 
                                                    dx1=self.StripWidth/2, 
                                                    dx2=self.StripWidth/2,
                                                    dy1=self.trapezoidDim[2], 
                                                    dy2=self.trapezoidDim[2], 
                                                    dz=0.5*self.StripThickness)
            aEMIRPCYYStrip_lv = geom.structure.Volume('volEMIRPCYYStrip_'+str(j), 
                                                    material=self.StripMat, 
                                                    shape=aEMIRPCXXStrip)
            aEMIRPCYYStripPos= geom.structure.Position('emiYYStrippos_'+str(j),
                                                    PosYYStrip[0], yposYYStrip, PosYYStrip[2])
            
            aEMIRPCYYStriprotation = geom.structure.Rotation(
                'EMIRPCYYStriprotation_'+str(j), Q('0deg'),  Q('0deg'),
                Q('90deg'))  #Rotating the module on its axis accordingly
            aEMIRPCYYStripPlace = geom.structure.Placement('emiYYStrippla'+str(j),
                                                  volume=aEMIRPCYYStrip_lv,
                                                  pos=aEMIRPCYYStripPos,
                                                  rot=aEMIRPCYYStriprotation,
                                                  copynumber=j)

            
            '''
            aEMIRPCYYStripPlace = geom.structure.Placement('emiYYStrippla_'+str(j),
                                                    volume = aEMIRPCYYStrip_lv,
                                                    pos = aEMIRPCYYStripPos)
            '''

            EMIRPC_lv.placements.append( aEMIRPCYYStripPlace.name )
            
            print("EMIRPC_lv.placements.append(", aEMIRPCYYStripPlace.name, ")")
            yposYYStrip = yposYYStrip + self.StripWidth + self.StripGap
            

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
