#!/usr/bin/env python3
import gegede.builder
import math
from duneggd.LocalTools import localtools as ltools
from duneggd.LocalTools import materialdefinition as materials
from gegede import Quantity as Q


class SandEmiBarrelModBuilder(gegede.builder.Builder):
    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self, 
		  trapezoidDim=None, 
		  ScintMat=None, 
		  PasMat=None, 
		  PasSlabThickness=None, 
		  ActiveSlabThickness=None, 
		  nSlabs=None, 
		  **kwds):
        self.trapezoidDim = trapezoidDim
        self.ScintMat = ScintMat
        self.PasMat = PasMat
        self.PasSlabThickness = PasSlabThickness
        self.ActiveSlabThickness = ActiveSlabThickness
        self.nSlabs = nSlabs
        self.Segmentation = 24.
    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):
        print("\033[36mconstruct in \033[1mSandEmiBarrelModBuilder\033[m\033[m")
        print( "PasSlabThickness:------------> ", self.PasSlabThickness)
        print( "ActiveSlabThickness:---------> ", self.ActiveSlabThickness)

        EMI_shape = geom.shapes.Trapezoid('EMI_shape', 
					   dx1=self.trapezoidDim[0], 
					   dx2=self.trapezoidDim[1],
					   dy1=self.trapezoidDim[2], 
					   dy2=self.trapezoidDim[2], 
					   dz=self.trapezoidDim[3])

        EMI_lv = geom.structure.Volume('EMI_lv', material='Air', shape=EMI_shape)
        self.add_volume(EMI_lv)
        print(self.name)
#       EMI_position = geom.structure.Position('EMI_position', Position[0], Position[1], Position[2])
#       EMI_place = geom.structure.Placement('EMI_place', volume = EMI_lv, pos=EMI_position)
            
            
        
        for i in range(self.nSlabs): #nSlabs
       
            #rotation = geom.structure.Rotation(
            #    'rotation' + '_' + str(i), Q('0deg'),Q('-15deg'),Q('0deg'))  #Rotating the module on its axis accordingly
            
            tan = math.tan(math.pi/self.Segmentation)
            #tan = 0.5*(self.trapezoidDim[1] - self.trapezoidDim[0])/self.trapezoidDim[3]
            #tan = 0.5*(self.trapezoidDim[1] - self.trapezoidDim[0])/self.trapezoidDim[3]
            xposSlab=Q('0cm')
            yposSlab=Q('0cm')
            zposSlabActive = (-self.trapezoidDim[3] + 
		             (i+0.5)*self.ActiveSlabThickness + 
                             i*self.PasSlabThickness)
            #print("active slab position= "+ str(zposSlabActive))
            zposSlabPassive = (-self.trapezoidDim[3] + 
                              (i+1.)*self.ActiveSlabThickness + 
                              (i+0.5)*self.PasSlabThickness)
            #print("passive slab position= "+ str(zposSlabPassive))
            bhalfActive=(self.trapezoidDim[0]+
                        i*(self.ActiveSlabThickness*tan)+
                        i*(self.PasSlabThickness*tan))
            bhalfPassive=bhalfActive+(self.ActiveSlabThickness*tan)
            BhalfActive=bhalfActive+self.ActiveSlabThickness*tan
            BhalfPassive=BhalfActive+(self.PasSlabThickness*tan)
            #print("BhalfPassive= "+ str(BhalfPassive))
            
            #creating and appending active slabs to the EMI module
            print('Active slab[',i,'/',self.nSlabs,']')
            
            aEMIActiveSlab = geom.shapes.Trapezoid('EMIActiveSlab'+'_'+str(i), 
						    dx1=bhalfActive, 
						    dx2=BhalfActive,
						    dy1=self.trapezoidDim[2], 
						    dy2=self.trapezoidDim[2], 
						    dz=0.5*self.ActiveSlabThickness)

            aEMIActiveSlab_lv = geom.structure.Volume('volEMIActiveSlab'+'_'+str(i), 
						       material=self.ScintMat, 
						       shape=aEMIActiveSlab)
            aEMIActiveSlab_lv.params.append(("SensDet","EMISci"))
            
            aEMIActiveSlabPos = geom.structure.Position('emiactiveslabpos'+'_'+str(i),
							 xposSlab,
							 yposSlab,
							 zposSlabActive)
           

            aEMIActiveSlabPlace = geom.structure.Placement('emiactiveslabpla'+'_'+str(i),
							    volume = aEMIActiveSlab_lv,
							    pos = aEMIActiveSlabPos)

            EMI_lv.placements.append( aEMIActiveSlabPlace.name )
            
            #creating and appending passive slabs to the EMI module
            if i < self.nSlabs - 1:
                print('Passive slab[',i,'/',self.nSlabs,']')
                aEMIPassiveSlab = geom.shapes.Trapezoid('EMIPassiveSlab'+'_'+str(i), 
                                                         dx1=bhalfPassive, 
                                                         dx2=BhalfPassive,
                                                         dy1=self.trapezoidDim[2], 
                                                         dy2=self.trapezoidDim[2], 
                                                         dz=0.5*self.PasSlabThickness)

                aEMIPassiveSlab_lv = geom.structure.Volume('volEMIPassiveSlab'+'_'+str(i), 
                                                            material=self.PasMat, 
                                                            shape=aEMIPassiveSlab)
                
                aEMIPassiveSlab_lv.params.append(("SensDet","EMISci"))
                aEMIPassiveSlabPos = geom.structure.Position('emipassiveslabpos'+'_'+str(i),
                                                              xposSlab,
                                                              yposSlab,
                                                              zposSlabPassive)
                
                aEMIPassiveSlabPlace = geom.structure.Placement('emipassiveslabpla'+'_'+str(i),
                                                                 volume = aEMIPassiveSlab_lv,
                                                                 pos = aEMIPassiveSlabPos) 
               

                EMI_lv.placements.append( aEMIPassiveSlabPlace.name )

