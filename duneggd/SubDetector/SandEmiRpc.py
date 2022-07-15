#!/usr/bin/env python
import gegede.builder
import math
from duneggd.LocalTools import localtools as ltools
from duneggd.LocalTools import materialdefinition as materials
from gegede import Quantity as Q


class SandEmiRpcBuilder(gegede.builder.Builder):
    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self,
                # atanu adding these -------
		BuildEmiRpcBarrelMod  = False,
                moduleThickness = None,
                trapezoidDim = None,
                nLayers = None,
                # --------------------------
                **kwds):
        #-------------------------------------------
        self.BuildEmiRpcBarrelMod = BuildEmiRpcBarrelMod
        #-------------------------------------------
        self.NEmiRpcModBarrel   = 24            # need 24 slabs if we want 15 degree coverage
        self.nLayers            = nLayers
        self.moduleThickness       = moduleThickness  # taken from the cfg file
        self.BarrelRmin         = Q('330 cm')   # yoke rmax
        self.BarrelDZ           = Q('215 cm')   # yoke half-length 
        self.emiThickness = nLayers * 2 * moduleThickness
        self.ang = (math.pi/self.NEmiRpcModBarrel)
        self.rmax_barrel = (self.BarrelRmin + self.emiThickness)/math.cos(self.ang) # for cylinder-shaped emi enclosing logical volume
        #self.barrel_thickness = self.rmax_barrel - self.BarrelRmin                  # for cylinder-shaped emi enclosing logical volume
        self.trapezoidDim      = trapezoidDim 
    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):
        print("\033[36mconstruct in \033[1mSandEmiRpcBuilder\033[m\033[m")
        print ("==============VARIOUS DIMENSIONS=================================================================")
        print ("# OF MODULES         :                       ",self.NEmiRpcModBarrel)
        print ("BARREL RMIN          :                       ",self.BarrelRmin)
        print ("BARREL LENGTH        :                       ",self.BarrelDZ)    
        print ("EMI MODULE THICKNESS :                       ",self.moduleThickness)
        print ("EMI EMI    THICKNESS :                       ",self.emiThickness)
        print ("MODULE HALF ANGLE    :                       ",self.ang)
        print ("-------------------------------------------------------------------------------------------------")
        
        # barrel
        ''' POLYHEDRON SHAPED EMI ENCLOSING LOGICAL VOLUME
        barrel_shape = geom.shapes.PolyhedraRegular("sand_emi_barrel_shape",\
                                                    numsides=self.NEmiRpcModBarrel, 
                                                    rmin=self.BarrelRmin, 
                                                    rmax=self.BarrelRmin + 
                                                    self.emiThickness, # 2 * for alternating structure
                                                    dz=self.BarrelDZ,
                                                    sphi=Q(self.ang))
        '''
        #'''
        barrel_shape = geom.shapes.Tubs("sand_emi_barrel_shape",
                                rmin=self.BarrelRmin, 
                                rmax=self.rmax_barrel, 
                                dz=self.BarrelDZ)
        #'''




        emi_lv = geom.structure.Volume('sand_emi_volume',
                                              material="Air",
                                              shape=barrel_shape)
                                    
        self.add_volume(emi_lv)

        if self.BuildEmiRpcBarrelMod is False:
            print ("EMIRPC BARREL not requested, not building it!")
        else:
            self.buildEmiRpcBarrel(emi_lv, geom)
        
    def buildEmiRpcBarrel(self, main_lv, geom):
        # there is a barrel section that is nearly cylindrical, with 24 modules
        # each covering 15 degrees. The modules are 4.3m long, 62cm thick,
        # trapezoids with bases of 86.39 (at radius 330 cm) and 102.62 cm (at radius 330 cm + 62 cm).


        if self.get_builder("SANDEMIRPCBARRELMOD") == None:
            print ("SANDEMIRPCBARRELMOD builder not found");
            return 

        emi_module_builder=self.get_builder("SANDEMIRPCBARRELMOD")
        emi_module_lv=emi_module_builder.get_volume()

        #'''
        emiMin = self.BarrelRmin;
        ang = 360 / self.NEmiRpcModBarrel
        delta = ang/2
        #'''
        for k in range(5):
            #for i in range(self.nLayers):
                for j in range(self.NEmiRpcModBarrel):

                    axisy = (0, 1, 0)
                    axisz = (1, 0, 0)
                    #ang = (360 / self.NEmiRpcModBarrel)/self.nLayers
                    #theta = j * ang + i * delta
                    theta = j * ang
                    ModPosition = [Q('0mm'), - 4 * self.trapezoidDim[2] + 2 * self.trapezoidDim[2] * k, emiMin + 0.5*self.moduleThickness]
                    #ModPosition = [Q('0mm'), Q('0mm'), emiMin + 0.5*self.moduleThickness]

                    #ModPosition = [Q('0mm'), Q('-43*4 cm'), emiMin + 0.5*self.moduleThickness]
                    ModPositionNew = ltools.rotation(
                        axisy, theta, ModPosition
                    )
                    
                    #Rotating the position vector (the slabs will be rotated automatically after append)
                    ModPositionNew = ltools.rotation(axisz, -90, ModPositionNew)

                    
                    EMIRPC_position = geom.structure.Position(
                        #'EMIRPC_position' + '_' + str(i)+ '_' + str(j) + '_' + str(k) , ModPositionNew[0],
                        'EMIRPC_position' + '_' + str(j) + '_' + str(k) , ModPositionNew[0],
                        ModPositionNew[1], ModPositionNew[2])

                    
                    EMIRPC_rotation = geom.structure.Rotation(
                        #'EMIRPC_rotation' + '_' + str(i) + '_' + str(j) + '_' + str(k), Q('90deg'), -theta * Q('1deg'),
                        'EMIRPC_rotation' + '_'  + str(j) + '_' + str(k), Q('90deg'), -theta * Q('1deg'),
                        Q('0deg'))  #Rotating the module on its axis accordingly
                        #Q('10deg'))  #Rotating the module on its axis accordingly

                    print("Building Kloe EMIRPC module " + str(j)) # keep compatibility with Python3 pylint: disable=superfluous-parens

                    ####Placing and appending the j EMIRPC Module#####

                    #EMIRPC_place = geom.structure.Placement('EMIRPC_place' + '_' + str(i) + '_' + str(j) + '_' + str(k),
                    EMIRPC_place = geom.structure.Placement('EMIRPC_place' + '_' + str(j) + '_' + str(k),
                                                          volume=emi_module_lv,
                                                          pos=EMIRPC_position,
                                                          rot=EMIRPC_rotation,
                                                          #copynumber=i+j+k
                                                          copynumber=j+k
                                                          )
                    main_lv.placements.append(EMIRPC_place.name)
                
                # next minimum radius to start the layer
                #emiMin = (emiMin + self.moduleThickness)/math.cos(self.ang)
                #'''
        #'''
        ''' 
        #testing for a single module building
        axisx = (0, 0, 1)
        axisy = (0, 1, 0)
        axisz = (1, 0, 0)
        theta = 0
        #ModPosition = [Q('0 mm'), Q('3300 mm')+Q('233 mm'), Q('0 mm')]
        #ModPosition = [Q('0 cm'), self.BarrelRmin + 0.5*self.moduleThickness + Q('167 mm'), Q('0 cm')]
        ModPosition = [Q('0 cm'), self.BarrelRmin + 0.5*self.moduleThickness, Q('0 cm')]
        print("----------------> MODPOSITION-----------------------: ", ModPosition)
        ModPositionNew = ltools.rotation(
            axisy, theta, ModPosition
        )  #Rotating the position vector (the slabs will be rotated automatically after append)
        print("----------------> MODPOSITIONNEW--------------------: ", ModPositionNew)
        #ModPositionNew = ltools.rotation(axisz, -90, ModPositionNew)
        ModPositionNew = ltools.rotation(axisz, 0, ModPositionNew)
        #ModPositionNew = ModPosition
        print("----------------> MODPOSITIONNEW--------------------: ", ModPositionNew)
        EMIRPC_position = geom.structure.Position(
            'EMIRPC_position', ModPositionNew[0],
            ModPositionNew[1], ModPositionNew[2])
        
        EMIRPC_rotation = geom.structure.Rotation(
            'EMIRPC_rotation', Q('90deg'), 0 * Q('1deg'),
            Q('0deg'))  #Rotating the module on its axis accordingly
            #Q('10deg'))  #Rotating the module on its axis accordingly

        print("Building Kloe EMIRPC module ") # keep compatibility with Python3 pylint: disable=superfluous-parens

        ####Placing and appending the j EMIRPC Module#####

        EMIRPC_place = geom.structure.Placement('EMIRPC_place',
                                              volume=emi_module_lv,
                                              pos=EMIRPC_position,
                                              rot=EMIRPC_rotation,
                                              copynumber=0)



        main_lv.placements.append(EMIRPC_place.name)
        #main_lv.placements.append(emi_lv_place.name)
        '''


                ################################################

