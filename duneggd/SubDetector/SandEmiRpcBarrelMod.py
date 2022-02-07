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
		  StripMat=None, 
		  nModules=None, 
		  **kwds):
        self.trapezoidDim = trapezoidDim
        self.BakeliteMat = BakeliteMat
        self.BakeliteThickness = BakeliteThickness
        self.GasThickness = GasThickness
        self.GasMat = GasMat
        self.FoamThickness = FoamThickness
        self.FoamMat = FoamMat
        self.CoatThickness = CoatThickness
        self.CoatMat = CoatMat
        self.MylarThickness = MylarThickness
        self.MylarMat = MylarMat
        self.StripWidth = StripWidth
        self.StripThickness = StripThickness
        self.StripMat = StripMat
        self.nModules = nModules
        self.nSlabs = 3
        self.Segmentation = 24.
        self.tan = math.tan(math.pi/self.Segmentation)
        self.nStrips = int((trapezoidDim[0].magnitude)/(StripThickness.magnitude))

        
    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):
        print("\033[36mconstruct in \033[1mSandEmiRpcBarrelModBuilder\033[m\033[m")
        print( "CoatThickness:------------> ", self.CoatThickness)
        print( "StripThickness:------------> ", self.StripThickness)
        print( "StripWidth:------------> ", self.StripWidth)
        print( "GasThickness:------------> ", self.GasThickness)
        print( "BakeliteThickness:---------> ", self.BakeliteThickness)
        print( "nStrips:-------------------> ", self.nStrips)


        EMIRPC_shape = geom.shapes.Trapezoid('EMIRPC_shape', 
					   dx1=self.trapezoidDim[0], 
					   dx2=self.trapezoidDim[1],
					   dy1=self.trapezoidDim[2], 
					   dy2=self.trapezoidDim[2], 
					   dz=self.trapezoidDim[3])

        EMIRPC_lv = geom.structure.Volume('EMIRPC_lv', material='Air', shape=EMIRPC_shape)
        self.add_volume(EMIRPC_lv)
        print(self.name)
        

        xpos=Q('0cm')
        ypos=Q('0cm')
        # STRUCTURE (bottom up): foam0 -> coat0 -> bakelite0 -> gas0 -> bakelite1 -> coat1 -> mylar0 -> strips0 -> mylar1 -> coat2 -> bakelite2 -> gas1 -> bakelite3 -> coat3 -> foam1 
        zposFoam0       = -self.trapezoidDim[3]  + 0.5 * self.FoamThickness
        zposMylar0      = -self.trapezoidDim[3]  + self.FoamThickness + 0.5 * self.MylarThickness
        zposCoat0       = -self.trapezoidDim[3]  + self.FoamThickness + self.MylarThickness + 0.5 * self.CoatThickness
        zposBakelite0   = -self.trapezoidDim[3]  + self.FoamThickness + self.MylarThickness + self.CoatThickness + 0.5 * self.BakeliteThickness
        zposGas0        = -self.trapezoidDim[3]  + self.FoamThickness + self.MylarThickness + self.CoatThickness + self.BakeliteThickness + 0.5 * self.GasThickness
        zposBakelite1   = -self.trapezoidDim[3]  + self.FoamThickness + self.MylarThickness + self.CoatThickness + self.BakeliteThickness + self.GasThickness + 0.5 * self.BakeliteThickness
        zposCoat1       = -self.trapezoidDim[3]  + self.FoamThickness + self.MylarThickness + self.CoatThickness + self.BakeliteThickness + self.GasThickness + self.BakeliteThickness + 0.5 * self.CoatThickness
        zposMylar1      = -self.trapezoidDim[3]  + self.FoamThickness + self.MylarThickness + self.CoatThickness + self.BakeliteThickness + self.GasThickness + self.BakeliteThickness + self.CoatThickness + 0.5 * self.MylarThickness
        zposStrip0      = -self.trapezoidDim[3]  + self.FoamThickness + self.MylarThickness + self.CoatThickness + self.BakeliteThickness + self.GasThickness + self.BakeliteThickness + self.CoatThickness + self.MylarThickness + 0.5 * self.StripThickness 
        zposMylar2      = -self.trapezoidDim[3]  + self.FoamThickness + self.MylarThickness + self.CoatThickness + self.BakeliteThickness + self.GasThickness + self.BakeliteThickness + self.CoatThickness + self.MylarThickness + self.StripThickness + 0.5 * self.MylarThickness
        zposCoat2       = -self.trapezoidDim[3]  + self.FoamThickness + self.MylarThickness + self.CoatThickness + self.BakeliteThickness + self.GasThickness + self.BakeliteThickness + self.CoatThickness + self.MylarThickness + self.StripThickness + self.MylarThickness + 0.5 * self.CoatThickness
        zposBakelite2   = -self.trapezoidDim[3]  + self.FoamThickness + self.MylarThickness + self.CoatThickness + self.BakeliteThickness + self.GasThickness + self.BakeliteThickness + self.CoatThickness + self.MylarThickness + self.StripThickness + self.MylarThickness + self.CoatThickness + 0.5 * self.BakeliteThickness
        zposGas1        = -self.trapezoidDim[3]  + self.FoamThickness + self.MylarThickness + self.CoatThickness + self.BakeliteThickness + self.GasThickness + self.BakeliteThickness + self.CoatThickness + self.MylarThickness + self.StripThickness + self.MylarThickness + self.CoatThickness + self.BakeliteThickness + 0.5 * self.GasThickness
        zposBakelite3   = -self.trapezoidDim[3]  + self.FoamThickness + self.MylarThickness + self.CoatThickness + self.BakeliteThickness + self.GasThickness + self.BakeliteThickness + self.CoatThickness + self.MylarThickness + self.StripThickness + self.MylarThickness + self.CoatThickness + self.BakeliteThickness + self.GasThickness + 0.5 * self.BakeliteThickness
        zposCoat3       = -self.trapezoidDim[3]  + self.FoamThickness + self.MylarThickness + self.CoatThickness + self.BakeliteThickness + self.GasThickness + self.BakeliteThickness + self.CoatThickness + self.MylarThickness + self.StripThickness + self.MylarThickness + self.CoatThickness + self.BakeliteThickness + self.GasThickness + self.BakeliteThickness + 0.5 * self.CoatThickness
        zposMylar3      = -self.trapezoidDim[3]  + self.FoamThickness + self.MylarThickness + self.CoatThickness + self.BakeliteThickness + self.GasThickness + self.BakeliteThickness + self.CoatThickness + self.MylarThickness + self.StripThickness + self.MylarThickness + self.CoatThickness + self.BakeliteThickness + self.GasThickness + self.BakeliteThickness + self.CoatThickness + 0.5 * self.MylarThickness
        zposFoam1       = -self.trapezoidDim[3]  + self.FoamThickness + self.MylarThickness + self.CoatThickness + self.BakeliteThickness + self.GasThickness + self.BakeliteThickness + self.CoatThickness + self.MylarThickness + self.StripThickness + self.MylarThickness + self.CoatThickness + self.BakeliteThickness + self.GasThickness + self.BakeliteThickness + self.CoatThickness + self.MylarThickness + 0.5 * self.FoamThickness
        

        '''
        zposCoat0       = (-self.trapezoidDim[3] + 0.5*self.CoatThickness)
        zposBakelite0   = -self.trapezoidDim[3] + self.CoatThickness +  .5*self.BakeliteThickness 
        zposBakelite1   = -self.trapezoidDim[3] + self.CoatThickness + self.BakeliteThickness + self.GasThickness + .5*self.BakeliteThickness 
        zposStrip0      = -self.trapezoidDim[3] + self.CoatThickness + self.BakeliteThickness + self.GasThickness + self.BakeliteThickness + 0.5*self.StripThickness
        zposBakelite2   = -self.trapezoidDim[3] + self.CoatThickness + self.BakeliteThickness + self.GasThickness + self.BakeliteThickness + self.StripThickness + .5*self.BakeliteThickness
        zposBakelite3   = -self.trapezoidDim[3] + self.CoatThickness + self.BakeliteThickness + self.GasThickness + self.BakeliteThickness + self.StripThickness + self.BakeliteThickness + self.GasThickness + .5*self.BakeliteThickness
        zposGas0        = -self.trapezoidDim[3] + self.CoatThickness + self.BakeliteThickness + 0.5*self.GasThickness
        zposGas1        = -self.trapezoidDim[3] + self.CoatThickness + self.BakeliteThickness + self.GasThickness + self.BakeliteThickness + self.StripThickness + + self.BakeliteThickness + + 0.5*self.GasThickness
        zposCoat1       = (-self.trapezoidDim[3]+ self.CoatThickness + self.StripThickness + self.nSlabs * self.BakeliteThickness + (self.nSlabs - 1) * self.GasThickness + 0.5*self.CoatThickness)
        '''


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
        #aEMIRPCFoam_lv.params.append(("SensDet","EMIRPCSci"))
        aEMIRPCFoam_0Pos = geom.structure.Position('emifoam_0pos',
                                                xpos,
                                                ypos,
                                                zposFoam0)
        aEMIRPCFoam_0Place = geom.structure.Placement('emifoam_0pla',
                                                volume = aEMIRPCFoam_0_lv,
                                                pos = aEMIRPCFoam_0Pos)
        EMIRPC_lv.placements.append( aEMIRPCFoam_0Place.name )


        #FIRST MYLAR LAYER =================================================================
        print('Mylar [0/2]')
        aEMIRPCMylar_0 = geom.shapes.Trapezoid('EMIRPCMylar_0', 
                                                dx1=self.trapezoidDim[1], 
                                                dx2=self.trapezoidDim[1],
                                                dy1=self.trapezoidDim[2], 
                                                dy2=self.trapezoidDim[2], 
                                                dz=0.5*self.MylarThickness)
        aEMIRPCMylar_0_lv = geom.structure.Volume('volEMIRPCMylar_0', 
                                                material=self.MylarMat, 
                                                shape=aEMIRPCMylar_0)
        #aEMIRPCMylar_lv.params.append(("SensDet","EMIRPCSci"))
        aEMIRPCMylar_0Pos = geom.structure.Position('emimylar_0pos',
                                                xpos,
                                                ypos,
                                                zposMylar0)
        aEMIRPCMylar_0Place = geom.structure.Placement('emimylar_0pla',
                                                volume = aEMIRPCMylar_0_lv,
                                                pos = aEMIRPCMylar_0Pos)
        EMIRPC_lv.placements.append( aEMIRPCMylar_0Place.name )




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
        #aEMIRPCCoat_lv.params.append(("SensDet","EMIRPCSci"))
        aEMIRPCCoat_0Pos = geom.structure.Position('emicoat_0pos',
                                                xpos,
                                                ypos,
                                                zposCoat0)
        aEMIRPCCoat_0Place = geom.structure.Placement('emicoat_0pla',
                                                volume = aEMIRPCCoat_0_lv,
                                                pos = aEMIRPCCoat_0Pos)
        EMIRPC_lv.placements.append( aEMIRPCCoat_0Place.name )
        
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
        #aEMIRPCBakelite0_lv.params.append(("SensDet","EMIRPCSci"))
      
        # EFIELD ----
        #EField="(0.0 kilovolt/mm, 0.0 kilovolt/mm, 5 kilovolt/mm)"
        EField="(0.0, 0.0, 5000)"
        print("Setting aEMIRPCBakelite_0_lv EField >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ", EField)
        aEMIRPCBakelite_0_lv.params.append(("EField",EField))
        # EFIELD ----

        aEMIRPCBakelite_0Pos = geom.structure.Position('emibakelite_0labpos',
                                                xpos,
                                                ypos,
                                                zposBakelite0)

        aEMIRPCBakelite_0Place = geom.structure.Placement('emibakelitepla_0',
                                                volume = aEMIRPCBakelite_0_lv,
                                                pos = aEMIRPCBakelite_0Pos)

        EMIRPC_lv.placements.append( aEMIRPCBakelite_0Place.name )
       


        #FIRST GAS LAYER ===================================================================
        print('Gas [1/2]')
        aEMIRPCGas_0 = geom.shapes.Trapezoid('EMIRPCGas_0', 
                                                 dx1=self.trapezoidDim[1], 
                                                 dx2=self.trapezoidDim[1],
                                                 dy1=self.trapezoidDim[2], 
                                                 dy2=self.trapezoidDim[2], 
                                                 dz=0.5*self.GasThickness)

        aEMIRPCGas_0_lv = geom.structure.Volume('volEMIRPCGas_0', 
                                                 material=self.GasMat, 
                                                 shape=aEMIRPCGas_0)
        
        aEMIRPCGas_0_lv.params.append(("SensDet","EMISci"))
        aEMIRPCGas_0Pos = geom.structure.Position('emigass_0pos',
                                                 xpos,
                                                 ypos,
                                                 zposGas0)
        
        aEMIRPCGas_0Place = geom.structure.Placement('emigas_0pla',
                                                 volume = aEMIRPCGas_0_lv,
                                                 pos = aEMIRPCGas_0Pos) 
       

        EMIRPC_lv.placements.append( aEMIRPCGas_0Place.name )

        xposStrip0 = -self.trapezoidDim[1] - 0.5 * self.StripWidth



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
        #aEMIRPCBakelite0_lv.params.append(("SensDet","EMIRPCSci"))
        
        aEMIRPCBakelite_1Pos = geom.structure.Position('emibakelite_1labpos',
                                                xpos,
                                                ypos,
                                                zposBakelite1)

        aEMIRPCBakelite_1Place = geom.structure.Placement('emibakelitepla_1',
                                                volume = aEMIRPCBakelite_1_lv,
                                                pos = aEMIRPCBakelite_1Pos)

        EMIRPC_lv.placements.append( aEMIRPCBakelite_1Place.name )
       

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
        #aEMIRPCCoat_lv.params.append(("SensDet","EMIRPCSci"))
        aEMIRPCCoat_1Pos = geom.structure.Position('emicoat_1pos',
                                                xpos,
                                                ypos,
                                                zposCoat1)
        aEMIRPCCoat_1Place = geom.structure.Placement('emicoat_1pla',
                                                volume = aEMIRPCCoat_1_lv,
                                                pos = aEMIRPCCoat_1Pos)
        EMIRPC_lv.placements.append( aEMIRPCCoat_1Place.name )

        #SECOND MYLAR LAYER ================================================================
        print('Mylar [0/2]')
        aEMIRPCMylar_1 = geom.shapes.Trapezoid('EMIRPCMylar_1', 
                                                dx1=self.trapezoidDim[1], 
                                                dx2=self.trapezoidDim[1],
                                                dy1=self.trapezoidDim[2], 
                                                dy2=self.trapezoidDim[2], 
                                                dz=0.5*self.MylarThickness)
        aEMIRPCMylar_1_lv = geom.structure.Volume('volEMIRPCMylar_1', 
                                                material=self.MylarMat, 
                                                shape=aEMIRPCMylar_1)
        #aEMIRPCMylar_lv.params.append(("SensDet","EMIRPCSci"))
        aEMIRPCMylar_1Pos = geom.structure.Position('emimylar_1pos',
                                                xpos,
                                                ypos,
                                                zposMylar1)
        aEMIRPCMylar_1Place = geom.structure.Placement('emimylar_1pla',
                                                volume = aEMIRPCMylar_1_lv,
                                                pos = aEMIRPCMylar_1Pos)
        EMIRPC_lv.placements.append( aEMIRPCMylar_1Place.name )



        #FIRST STRIP  LAYER ================================================================
        #for j in range(18):  # 2 cm wide strips cover the whole 46 cm breadth if we place every 2.5 times their width
        for j in range(self.nStrips):  # 2 cm wide strips cover the whole 46 cm breadth if we place every 2.5 times their width
            #xposStrip0 = xposStrip0 + 2.5 * self.StripWidth
            xposStrip0 = xposStrip0 + self.StripWidth
            #print("xposStrip:::::::::::::::::::: ", xposStrip0)
            aEMIRPCStrip_0 = geom.shapes.Trapezoid('EMIRPCStrip_0'+'_'+str(j), 
                                                    dx1=self.StripWidth, 
                                                    dx2=self.StripWidth,
                                                    dy1=self.trapezoidDim[2], 
                                                    dy2=self.trapezoidDim[2], 
                                                    dz=0.5*self.StripThickness)
            aEMIRPCStrip_0_lv = geom.structure.Volume('volEMIRPCStrip_0'+'_'+str(j), 
                                                    material=self.StripMat, 
                                                    shape=aEMIRPCStrip_0)
            #aEMIRPCStrip_lv.params.append(("SensDet","EMIRPCSci"))
            aEMIRPCStrip_0Pos = geom.structure.Position('emistrip_0pos'+'_'+str(j),
                                                    xposStrip0,
                                                    ypos,
                                                    zposStrip0)
            aEMIRPCStrip_0Place = geom.structure.Placement('emistrip_0pla'+'_'+str(j),
                                                    volume = aEMIRPCStrip_0_lv,
                                                    pos = aEMIRPCStrip_0Pos)
            EMIRPC_lv.placements.append( aEMIRPCStrip_0Place.name )



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
        #aEMIRPCMylar_lv.params.append(("SensDet","EMIRPCSci"))
        aEMIRPCMylar_2Pos = geom.structure.Position('emimylar_2pos',
                                                xpos,
                                                ypos,
                                                zposMylar2)
        aEMIRPCMylar_2Place = geom.structure.Placement('emimylar_2pla',
                                                volume = aEMIRPCMylar_2_lv,
                                                pos = aEMIRPCMylar_2Pos)
        EMIRPC_lv.placements.append( aEMIRPCMylar_2Place.name )


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
        #aEMIRPCCoat_lv.params.append(("SensDet","EMIRPCSci"))
        aEMIRPCCoat_2Pos = geom.structure.Position('emicoat_2pos',
                                                xpos,
                                                ypos,
                                                zposCoat2)
        aEMIRPCCoat_2Place = geom.structure.Placement('emicoat_2pla',
                                                volume = aEMIRPCCoat_2_lv,
                                                pos = aEMIRPCCoat_2Pos)
        EMIRPC_lv.placements.append( aEMIRPCCoat_2Place.name )


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
        #aEMIRPCBakelite0_lv.params.append(("SensDet","EMIRPCSci"))
        
        aEMIRPCBakelite_2Pos = geom.structure.Position('emibakelite_2pos_',
                                                xpos,
                                                ypos,
                                                zposBakelite2)

        aEMIRPCBakelite_2Place = geom.structure.Placement('emibakelitepla_2',
                                                volume = aEMIRPCBakelite_0_lv,
                                                pos = aEMIRPCBakelite_2Pos)

        EMIRPC_lv.placements.append( aEMIRPCBakelite_2Place.name )


        #SECOND GAS LAYER ==================================================================
        print('Gas [1/2]')
        aEMIRPCGas_1 = geom.shapes.Trapezoid('EMIRPCGas_1', 
                                                 dx1=self.trapezoidDim[1], 
                                                 dx2=self.trapezoidDim[1],
                                                 dy1=self.trapezoidDim[2], 
                                                 dy2=self.trapezoidDim[2], 
                                                 dz=0.5*self.GasThickness)

        aEMIRPCGas_1_lv = geom.structure.Volume('volEMIRPCGas_1', 
                                                 material=self.GasMat, 
                                                 shape=aEMIRPCGas_0)
        
        aEMIRPCGas_1_lv.params.append(("SensDet","EMISci"))
        aEMIRPCGas_1Pos = geom.structure.Position('emigaspos_1',
                                                 xpos,
                                                 ypos,
                                                 zposGas1)
        
        aEMIRPCGas_1Place = geom.structure.Placement('emigaspla_1',
                                                 volume = aEMIRPCGas_1_lv,
                                                 pos = aEMIRPCGas_1Pos) 
       

        EMIRPC_lv.placements.append( aEMIRPCGas_1Place.name )

        #FOURTH BAKELITE LAYER =============================================================
        print('Bakelite [3/4]')
        aEMIRPCBakelite_3 = geom.shapes.Trapezoid('EMIRPCBakelite_3', 
                                                dx1=self.trapezoidDim[1], 
                                                dx2=self.trapezoidDim[1],
                                                dy1=self.trapezoidDim[2], 
                                                dy2=self.trapezoidDim[2], 
                                                dz=0.5*self.BakeliteThickness)

        aEMIRPCBakelite_3_lv = geom.structure.Volume('volEMIRPCBakelite_3', 
                                                material=self.BakeliteMat, 
                                                shape=aEMIRPCBakelite_3)
        #aEMIRPCBakelite0_lv.params.append(("SensDet","EMIRPCSci"))
        
        aEMIRPCBakelite_3Pos = geom.structure.Position('emibakelite_3pos',
                                                xpos,
                                                ypos,
                                                zposBakelite3)

        aEMIRPCBakelite_3Place = geom.structure.Placement('emibakelite_3pla',
                                                volume = aEMIRPCBakelite_3_lv,
                                                pos = aEMIRPCBakelite_3Pos)

        EMIRPC_lv.placements.append( aEMIRPCBakelite_3Place.name )


        #FOURTH COAT LAYER =================================================================
        aEMIRPCCoat_3 = geom.shapes.Trapezoid('EMIRPCCoat_3', 
                                                dx1=self.trapezoidDim[1], 
                                                dx2=self.trapezoidDim[1],
                                                dy1=self.trapezoidDim[2], 
                                                dy2=self.trapezoidDim[2], 
                                                dz=0.5*self.CoatThickness)
        aEMIRPCCoat_3_lv = geom.structure.Volume('volEMIRPCCoat_3', 
                                                material=self.CoatMat, 
                                                shape=aEMIRPCCoat_3)
        #aEMIRPCCoat_lv.params.append(("SensDet","EMIRPCSci"))
        aEMIRPCCoat_3Pos = geom.structure.Position('emicoat_3pos',
                                                xpos,
                                                ypos,
                                                zposCoat3)
        aEMIRPCCoat_3Place = geom.structure.Placement('emicoat_3pla',
                                                volume = aEMIRPCCoat_3_lv,
                                                pos = aEMIRPCCoat_3Pos)
        EMIRPC_lv.placements.append( aEMIRPCCoat_3Place.name )



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
        #aEMIRPCMylar_lv.params.append(("SensDet","EMIRPCSci"))
        aEMIRPCMylar_3Pos = geom.structure.Position('emimylar_3pos',
                                                xpos,
                                                ypos,
                                                zposMylar2)
        aEMIRPCMylar_3Place = geom.structure.Placement('emimylar_3pla',
                                                volume = aEMIRPCMylar_3_lv,
                                                pos = aEMIRPCMylar_3Pos)
        EMIRPC_lv.placements.append( aEMIRPCMylar_3Place.name )



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
        #aEMIRPCFoam_lv.params.append(("SensDet","EMIRPCSci"))
        aEMIRPCFoam_1Pos = geom.structure.Position('emifoam_1pos',
                                                xpos,
                                                ypos,
                                                zposFoam1)
        aEMIRPCFoam_1Place = geom.structure.Placement('emifoam_1pla',
                                                volume = aEMIRPCFoam_1_lv,
                                                pos = aEMIRPCFoam_1Pos)
        EMIRPC_lv.placements.append( aEMIRPCFoam_1Place.name )
