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
		  GasSlabThickness=None, 
		  GasMat=None, 
		  BakeliteSlabThickness=None, 
		  BakeliteMat=None, 
		  CoatSlabThickness=None, 
		  CoatMat=None, 
		  PlateSlabThickness=None, 
		  PlateSlabWidth=None, 
		  PlateMat=None, 
		  nSlabs=None, 
		  **kwds):
        self.trapezoidDim = trapezoidDim
        self.BakeliteMat = BakeliteMat
        self.BakeliteSlabThickness = BakeliteSlabThickness
        self.GasSlabThickness = GasSlabThickness
        self.GasMat = GasMat
        self.CoatSlabThickness = CoatSlabThickness
        self.CoatMat = CoatMat
        self.PlateSlabWidth = PlateSlabWidth
        self.PlateSlabThickness = PlateSlabThickness
        self.PlateMat = PlateMat
        self.nSlabs = nSlabs
        self.Segmentation = 24.
        self.tan = math.tan(math.pi/self.Segmentation)
        #self.tan = math.tan(math.pi/self.Segmentation)
        #self.tan = 0.5*(self.trapezoidDim[1] - self.trapezoidDim[0])/self.trapezoidDim[3]
        #self.tan = 0.5*(self.trapezoidDim[1] - self.trapezoidDim[0])/self.trapezoidDim[3]
    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):
        print("\033[36mconstruct in \033[1mSandEmiRpcBarrelModBuilder\033[m\033[m")
        print( "CoatSlabThickness:------------> ", self.CoatSlabThickness)
        print( "PlateSlabThickness:------------> ", self.PlateSlabThickness)
        print( "PlateSlabWidth:------------> ", self.PlateSlabWidth)
        print( "GasSlabThickness:------------> ", self.GasSlabThickness)
        print( "BakeliteSlabThickness:---------> ", self.BakeliteSlabThickness)

        EMIRPC_shape = geom.shapes.Trapezoid('EMIRPC_shape', 
					   dx1=self.trapezoidDim[0], 
					   dx2=self.trapezoidDim[1],
					   dy1=self.trapezoidDim[2], 
					   dy2=self.trapezoidDim[2], 
					   dz=self.trapezoidDim[3])

        EMIRPC_lv = geom.structure.Volume('EMIRPC_lv', material='Air', shape=EMIRPC_shape)
        self.add_volume(EMIRPC_lv)
        print(self.name)
#       EMIRPC_position = geom.structure.Position('EMIRPC_position', Position[0], Position[1], Position[2])
#       EMIRPC_place = geom.structure.Placement('EMIRPC_place', volume = EMIRPC_lv, pos=EMIRPC_position)
         
        
        for i in range(self.nSlabs): #nSlabs
       
            #rotation = geom.structure.Rotation(
            #    'rotation' + '_' + str(i), Q('0deg'),Q('-15deg'),Q('0deg'))  #Rotating the module on its axis accordingly
            
            xposSlab=Q('0cm')
            yposSlab=Q('0cm')

            if i == 0:
                zposSlabPlate0 = (-self.trapezoidDim[3] + 0.5*self.PlateSlabThickness)
                zposSlabCoat0 = (-self.trapezoidDim[3] + self.PlateSlabThickness + 0.5*self.CoatSlabThickness)
                bhalfPlate0=self.trapezoidDim[0]
                BhalfPlate0=bhalfPlate0+self.PlateSlabThickness*self.tan
                bhalfCoat0=BhalfPlate0
                BhalfCoat0=bhalfCoat0+(self.CoatSlabThickness*self.tan)
                # Plate 0 starts -------------------
                xposPlate0 = -self.trapezoidDim[1] - 0.5 * self.PlateSlabWidth
                for j in range(18):  # 2 cm wide strips cover the whole 46 cm breadth if we place every 2.5 times their width
                    xposPlate0 = xposPlate0 + 2.5 * self.PlateSlabWidth
                    print("xposPlate:::::::::::::::::::: ", xposPlate0)
                    aEMIRPCPlate0Slab = geom.shapes.Trapezoid('EMIRPCPlate0Slab'+'_'+str(i)+'_'+str(j), 
                                                            dx1=self.PlateSlabWidth, 
                                                            dx2=self.PlateSlabWidth,
                                                            dy1=self.trapezoidDim[2], 
                                                            dy2=self.trapezoidDim[2], 
                                                            dz=0.5*self.PlateSlabThickness)
                    aEMIRPCPlate0Slab_lv = geom.structure.Volume('volEMIRPCPlate0Slab'+'_'+str(i)+'_'+str(j), 
                                                               material=self.PlateMat, 
                                                               shape=aEMIRPCPlate0Slab)
                    #aEMIRPCPlateSlab_lv.params.append(("SensDet","EMIRPCSci"))
                    aEMIRPCPlate0SlabPos = geom.structure.Position('emiplate0slabpos'+'_'+str(i)+'_'+str(j),
                                                                 xposPlate0,
                                                                 yposSlab,
                                                                 zposSlabPlate0)
                    aEMIRPCPlate0SlabPlace = geom.structure.Placement('emiplate0slabpla'+'_'+str(i)+'_'+str(j),
                                                                    volume = aEMIRPCPlate0Slab_lv,
                                                                    pos = aEMIRPCPlate0SlabPos)
                    EMIRPC_lv.placements.append( aEMIRPCPlate0SlabPlace.name )
                # Plate 0 ends  --------------------
                # Coat 0 starts --------------------
                aEMIRPCCoat0Slab = geom.shapes.Trapezoid('EMIRPCCoat0Slab'+'_'+str(i), 
                                                        dx1=self.trapezoidDim[1], 
                                                        dx2=self.trapezoidDim[1],
                                                        dy1=self.trapezoidDim[2], 
                                                        dy2=self.trapezoidDim[2], 
                                                        dz=0.5*self.CoatSlabThickness)
                aEMIRPCCoat0Slab_lv = geom.structure.Volume('volEMIRPCCoat0Slab'+'_'+str(i), 
                                                           material=self.CoatMat, 
                                                           shape=aEMIRPCCoat0Slab)
                #aEMIRPCCoatSlab_lv.params.append(("SensDet","EMIRPCSci"))
                aEMIRPCCoat0SlabPos = geom.structure.Position('emicoat0slabpos'+'_'+str(i),
                                                             xposSlab,
                                                             yposSlab,
                                                             zposSlabCoat0)
                aEMIRPCCoat0SlabPlace = geom.structure.Placement('emicoat0slabpla'+'_'+str(i),
                                                                volume = aEMIRPCCoat0Slab_lv,
                                                                pos = aEMIRPCCoat0SlabPos)
                EMIRPC_lv.placements.append( aEMIRPCCoat0SlabPlace.name )
                # Coat 0 end  ----------------------


            if i == 1:
                zposSlabCoat1  = (-self.trapezoidDim[3] + self.PlateSlabThickness + self.CoatSlabThickness + self.BakeliteSlabThickness + self.GasSlabThickness + self.BakeliteSlabThickness + 0.5*self.CoatSlabThickness)
                zposSlabPlate1 = (-self.trapezoidDim[3] + self.PlateSlabThickness + self.CoatSlabThickness + self.BakeliteSlabThickness + self.GasSlabThickness + self.BakeliteSlabThickness + self.CoatSlabThickness + 0.5*self.PlateSlabThickness)
                BhalfPlate1=self.trapezoidDim[1]
                bhalfPlate1=BhalfPlate1-self.PlateSlabThickness*self.tan
                BhalfCoat1=bhalfPlate1
                bhalfCoat1=BhalfCoat1-self.CoatSlabThickness*self.tan
                # Plate 1 starts -------------------
                xposPlate1 = -self.trapezoidDim[1] - 0.5 * self.PlateSlabWidth
                for j in range(18):  # 2 cm wide strips cover the whole 46 cm breadth if we place every 2.5 times their width
                    xposPlate1 = xposPlate1 + 2.5 * self.PlateSlabWidth
                    print("xposPlate:::::::::::::::::::: ", xposPlate1)
                    aEMIRPCPlate1Slab = geom.shapes.Trapezoid('EMIRPCPlate1Slab'+'_'+str(i)+'_'+str(j), 
                                                            dx1=self.PlateSlabWidth, 
                                                            dx2=self.PlateSlabWidth,
                                                            dy1=self.trapezoidDim[2], 
                                                            dy2=self.trapezoidDim[2], 
                                                            dz=0.5*self.PlateSlabThickness)
                    aEMIRPCPlate1Slab_lv = geom.structure.Volume('volEMIRPCPlate1Slab'+'_'+str(i)+'_'+str(j), 
                                                               material=self.PlateMat, 
                                                               shape=aEMIRPCPlate1Slab)
                    #aEMIRPCPlateSlab_lv.params.append(("SensDet","EMIRPCSci"))
                    aEMIRPCPlate1SlabPos = geom.structure.Position('emiplate1slabpos'+'_'+str(i)+'_'+str(j),
                                                                 xposPlate1,
                                                                 yposSlab,
                                                                 zposSlabPlate1)
                    aEMIRPCPlate1SlabPlace = geom.structure.Placement('emiplate1slabpla'+'_'+str(i)+'_'+str(j),
                                                                    volume = aEMIRPCPlate1Slab_lv,
                                                                    pos = aEMIRPCPlate1SlabPos)
                    EMIRPC_lv.placements.append( aEMIRPCPlate1SlabPlace.name )
                # Plate 1 ends  --------------------
                # Coat 1 starts -------------------
                aEMIRPCCoat1Slab = geom.shapes.Trapezoid('EMIRPCCoat1Slab'+'_'+str(i), 
                                                        dx1=self.trapezoidDim[1], 
                                                        dx2=self.trapezoidDim[1],
                                                        dy1=self.trapezoidDim[2], 
                                                        dy2=self.trapezoidDim[2], 
                                                        dz=0.5*self.CoatSlabThickness)
                aEMIRPCCoat1Slab_lv = geom.structure.Volume('volEMIRPCCoat1Slab'+'_'+str(i), 
                                                           material=self.CoatMat, 
                                                           shape=aEMIRPCCoat1Slab)
                #aEMIRPCCoatSlab_lv.params.append(("SensDet","EMIRPCSci"))
                aEMIRPCCoat1SlabPos = geom.structure.Position('emicoat1slabpos'+'_'+str(i),
                                                             xposSlab,
                                                             yposSlab,
                                                             zposSlabCoat1)
                aEMIRPCCoat1SlabPlace = geom.structure.Placement('emicoat1slabpla'+'_'+str(i),
                                                                volume = aEMIRPCCoat1Slab_lv,
                                                                pos = aEMIRPCCoat1SlabPos)
                EMIRPC_lv.placements.append( aEMIRPCCoat1SlabPlace.name )
                # Coat 1 ends  --------------------


            zposSlabBakelite = (-self.trapezoidDim[3] + self.PlateSlabThickness + self.CoatSlabThickness +  
		             (i+0.5)*self.BakeliteSlabThickness + 
                             i*self.GasSlabThickness)
            #print("glass slab position= "+ str(zposSlabBakelite))
            zposSlabGas = (-self.trapezoidDim[3] + self.PlateSlabThickness + self.CoatSlabThickness + 
                              (i+1.)*self.BakeliteSlabThickness + 
                              (i+0.5)*self.GasSlabThickness)
            #print("gas slab position= "+ str(zposSlabGas))
            bhalfBakelite=(self.trapezoidDim[0]+
                        i*(self.BakeliteSlabThickness*self.tan)+
                        i*(self.GasSlabThickness*self.tan))
            bhalfGas=bhalfBakelite+(self.BakeliteSlabThickness*self.tan)
            BhalfBakelite=bhalfBakelite+self.BakeliteSlabThickness*self.tan
            BhalfGas=BhalfBakelite+(self.GasSlabThickness*self.tan)
            #print("BhalfGas= "+ str(BhalfGas))
            
            #creating and appending glass slabs to the EMIRPC module
            print('Bakelite slab[',i,'/',self.nSlabs,']')
            
            aEMIRPCBakeliteSlab = geom.shapes.Trapezoid('EMIRPCBakeliteSlab'+'_'+str(i), 
						    dx1=self.trapezoidDim[1], 
						    dx2=self.trapezoidDim[1],
						    dy1=self.trapezoidDim[2], 
						    dy2=self.trapezoidDim[2], 
						    dz=0.5*self.BakeliteSlabThickness)

            aEMIRPCBakeliteSlab_lv = geom.structure.Volume('volEMIRPCBakeliteSlab'+'_'+str(i), 
						       material=self.BakeliteMat, 
						       shape=aEMIRPCBakeliteSlab)
            aEMIRPCBakeliteSlab_lv.params.append(("SensDet","EMIRPCSci"))
            
            aEMIRPCBakeliteSlabPos = geom.structure.Position('emiglassslabpos'+'_'+str(i),
							 xposSlab,
							 yposSlab,
							 zposSlabBakelite)
           

            aEMIRPCBakeliteSlabPlace = geom.structure.Placement('emiglassslabpla'+'_'+str(i),
							    volume = aEMIRPCBakeliteSlab_lv,
							    pos = aEMIRPCBakeliteSlabPos)

            EMIRPC_lv.placements.append( aEMIRPCBakeliteSlabPlace.name )
            
            #creating and appending gas slabs to the EMIRPC module
            if i < self.nSlabs - 1:
                print('Gas slab[',i,'/',self.nSlabs,']')
                aEMIRPCGasSlab = geom.shapes.Trapezoid('EMIRPCGasSlab'+'_'+str(i), 
                                                         dx1=self.trapezoidDim[1], 
                                                         dx2=self.trapezoidDim[1],
                                                         dy1=self.trapezoidDim[2], 
                                                         dy2=self.trapezoidDim[2], 
                                                         dz=0.5*self.GasSlabThickness)

                aEMIRPCGasSlab_lv = geom.structure.Volume('volEMIRPCGasSlab'+'_'+str(i), 
                                                            material=self.GasMat, 
                                                            shape=aEMIRPCGasSlab)
                
                aEMIRPCGasSlab_lv.params.append(("SensDet","EMISci"))
                aEMIRPCGasSlabPos = geom.structure.Position('emigasslabpos'+'_'+str(i),
                                                              xposSlab,
                                                              yposSlab,
                                                              zposSlabGas)
                
                aEMIRPCGasSlabPlace = geom.structure.Placement('emigasslabpla'+'_'+str(i),
                                                                 volume = aEMIRPCGasSlab_lv,
                                                                 pos = aEMIRPCGasSlabPos) 
               

                EMIRPC_lv.placements.append( aEMIRPCGasSlabPlace.name )

