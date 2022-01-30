#!/usr/bin/env python
'''
Subbuilder of MuID*Builder
'''

import gegede.builder
from gegede import Quantity as Q

class RPCTrayRotBuilder(gegede.builder.Builder):
    '''
    Arrange the RPC modules in configured way 
    '''

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self,  compDimension = None, compMaterial = 'Air',
                  compNrpcCol = None, compNrpcRow = None, compRotation=None, compExtend=[Q('0cm'),Q('0cm'),Q('0cm')], **kwds):

      self.rpcTrayMat = compMaterial 
      self.rpcTrayDim = compDimension 
      self.nrpcCol = compNrpcCol 
      self.nrpcRow = compNrpcRow 
      self.compRotation = compRotation
      self.compExtend  = compExtend

      #print( self.builders)
      self.RPCModBldr = self.get_builder('RPCMod')
      return

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):


        # get RPCMod volume and dim
        rpcMod_lv = self.RPCModBldr.get_volume('volRPCPad')
        rpcModDim = self.RPCModBldr.rpcModDim


        # define box and volume for RPC tray,
        # to be retrieved by MuID*Builder.
        # size will depend on configuration
        rpcTray = geom.shapes.Box( self.name,
                                   dx = 0.5*self.rpcTrayDim[0],
                                   dy = 0.5*self.rpcTrayDim[1],
                                   dz = 0.5*self.rpcTrayDim[2])
        rpcTray_lv = geom.structure.Volume('vol'+self.name, material=self.rpcTrayMat, shape=rpcTray)
        self.add_volume(rpcTray_lv)
        
        
        # position and place RPCMods
        for i in range(self.nrpcRow):
            #if (self.rpcTrayDim[1] < self.nrpcRow*rpcModDim[1]):
            #    ypos = (1-i)*(-0.5*self.rpcTrayDim[1]+0.5*rpcModDim[1])
            #    if i==1:
            #          zpos = 0.25*self.rpcTrayDim[2]
            #    else:                   
            #        zpos = -0.25*self.rpcTrayDim[2]
            #else:
            ypos = self.compExtend[1] #-0.5*self.rpcTrayDim[1]+(i+0.5)*rpcModDim[1]
            zpos = (i+0.5)*rpcModDim[1]+self.compExtend[2] #'0cm'
            for j in range(self.nrpcCol):
                xpos = rpcModDim[0]+self.compExtend[0]

                rpcm_in_t  = geom.structure.Position( 'RPCMod-'+str(self.nrpcCol*i+j)+'_in_'+self.name,
                                                      xpos,  ypos,  zpos)
                prpcm_in_t = geom.structure.Placement( 'placeRPCMod-'+str(self.nrpcCol*i+j)+'_in_'+self.name,
                                                       volume = rpcMod_lv, pos = rpcm_in_t, rot = self.compRotation)
                rpcTray_lv.placements.append( prpcm_in_t.name )
                #print( 'rpctray : '+str(i)+' '+str(j)+' RPCTray- xpos: '+str(xpos)+' ypos: '+str(ypos)+' zpos: '+str(zpos))
        
        
        return
