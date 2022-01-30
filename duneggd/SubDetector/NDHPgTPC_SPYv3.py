#!/usr/bin/env python
'''
NDHPgTPC_SPYv3_Builder: Builds the multi purpose tracker
'''

import gegede.builder
from gegede import Quantity as Q
from math import asin, sqrt

class NDHPgTPC_SPYv3_Builder(gegede.builder.Builder):
    '''
    Build a concept of the ND HPgTPC detector. This class directly
    sub-builders for the GArTPC, the ECAL and for the Yoke.

    Arguments:
    innerBField: the magnetic field inside of the magnet
    buildGarTPC: Flag to build the GArTPC
    buildEcal: Flag to build the Ecal
    buildYoke: Flag to build the Yoke

    '''

    defaults=dict( innerBField="0.5 T, 0.0 T, 0.0 T",
                   TPCStepLimit = "10 mm",
                   ECALStepLimit = "5 mm",
                   buildGarTPC=True,
                   buildEcalBarrel=True,
                   buildEcalEndcap=True,
                   buildYoke=False,
                   buildCryostat=False,
                   space=Q("10cm")
                   )

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):

        ''' Top level volume (MPD) - It is rotated later in the cavern (x, y, z) -> (z, y, x)'''

        magnet_shape = geom.get_shape("Cryostat")
        r = magnet_shape.rmax
        dz = magnet_shape.dz

        if self.buildYoke == True:
            eyoke_shape = geom.get_shape("YokeEndcap_max")
            if r < eyoke_shape.rmax:
                r = eyoke_shape.rmax
            if dz < eyoke_shape.dz:
                dz = eyoke_shape.dz

        dx_main=r+self.space #dimension along the beam
        dy_main=r+self.space #dimension in height
        dz_main=dz+self.space #dimension perp to the beam

        print("Dimension of the MPD in along the beam ", dx_main*2, " dimension in height ", dy_main*2, " and dimension perp to the beam ", dz_main*2)

        main_shape = geom.shapes.Box('MPD', dx=dx_main, dy=dy_main, dz=dz_main)
        main_lv = geom.structure.Volume('vol'+main_shape.name, material='Air', shape=main_shape)

        self.add_volume(main_lv)

        ##### build a fake volume that contains the MPD without the magnet to define the magnetized volume correctly ###
        # fake_lv = self.buildMagnetizedVolume(main_lv, geom)

        ######### build the TPC       ##########################
        # use GArTPC Builder, but "disable" the cyrostat by tweaking
        # EndcapThickness, WallThickness, and ChamberMaterial
        # do that in the cfg file
        if self.buildGarTPC:
            print("Adding TPC to main volume")
            self.build_gartpc(main_lv, geom)

        ######### build an ecal ##########################
        # Build the Barrel and Endcaps using the ECALBarrelBuilder and
        # ECALEndcapBuilder in the cfg file
        self.build_ecal(main_lv, geom)


        ######### magnet ##################################
        # Build a simple magnet of Al to get the total mass
        # A description of the return magnetic field and the coils is not implemented
        if self.buildCryostat:
            print("Adding Cryostat+Coils to main volume")
            self.build_cryostat(main_lv, geom)

        ######### magnet yoke ##################################
        # Build the yoke Barrel and Endcaps
        # A description of the return magnetic field and the coils is not implemented
        if self.buildYoke:
            print("Adding Yoke to main volume")
            self.build_yoke(main_lv, geom)

        return

    def buildMagnetizedVolume(self, main_lv, geom):
        '''Magnetized volume (fake volume) for G4 that includes the TPC + ECAL only'''

        print("Making fake magnetized volume and adding to main volume")

        eECal_shape = geom.get_shape("ECALEndcap_max")
        fake_shape = geom.shapes.PolyhedraRegular('NDHPgTPC', numsides=eECal_shape.numsides, rmin=Q("0m"), rmax=eECal_shape.rmax, dz=eECal_shape.dz)
        fake_lv = geom.structure.Volume('vol'+fake_shape.name, material='Air', shape=fake_shape)
        fake_lv.params.append(("BField", self.innerBField))
        rot_z = Q("90.0deg")-Q("180.0deg")/eECal_shape.numsides
        fake_lv_rot = geom.structure.Rotation(fake_lv.name+"_rot", z=rot_z)
        fake_pla = geom.structure.Placement("NDHPgTPC"+"_pla", volume=fake_lv, rot=fake_lv_rot)
        # Place it in the main lv
        main_lv.placements.append(fake_pla.name)

        return fake_lv

    def build_gartpc(self, main_lv, geom):

        #Build TPC
        tpc_builder = self.get_builder('GArTPC')
        if tpc_builder == None:
            return

        tpc_vol = tpc_builder.get_volume()
        # Add the magnetic field to the volume
        tpc_vol.params.append(("BField", self.innerBField))
        tpc_vol.params.append(("StepLimit", self.TPCStepLimit))

        tpc_pla = geom.structure.Placement("GArTPC"+"_pla", volume=tpc_vol)
        # Place it in the main lv
        main_lv.placements.append(tpc_pla.name)

    def build_ecal(self, main_lv, geom):

        if self.buildEcalBarrel == True:
            print("Adding ECAL Barrel to main volume")
            # build the ecalbarrel
            ibb = self.get_builder('ECALBarrelBuilder')
            if ibb == None:
                return

            ib_vol = ibb.get_volume()
            # Add the magnetic field to the volume
            ib_vol.params.append(("BField", self.innerBField))
            ib_vol.params.append(("StepLimit", self.ECALStepLimit))

            ecal_shape = geom.store.shapes.get(ib_vol.shape)
            nsides = ecal_shape.numsides
            rot_z = Q("90.0deg")-Q("180.0deg")/nsides

            ib_rot = geom.structure.Rotation(ibb.name+"_rot", z=rot_z)
            ib_pla = geom.structure.Placement(ibb.name+"_pla", volume=ib_vol, rot=ib_rot)
            # ib_pla = geom.structure.Placement(ibb.name+"_pla", volume=ib_vol)
            # Place it in the main lv
            main_lv.placements.append(ib_pla.name)

        if self.buildEcalEndcap == True:
            print("Adding ECAL Endcap to main volume")
            # build the ecal endcap
            iecb = self.get_builder("ECALEndcapBuilder")
            if iecb == None:
                return

            iec_vol = iecb.get_volume()
            # Add the magnetic field to the volume
            iec_vol.params.append(("BField", self.innerBField))
            iec_vol.params.append(("StepLimit", self.ECALStepLimit))

            iec_rot = geom.structure.Rotation(iecb.name+"_rot", z=rot_z)
            iec_pla = geom.structure.Placement(iecb.name+"_pla", volume=iec_vol, rot=iec_rot)
            # iec_pla = geom.structure.Placement(iecb.name+"_pla", volume=iec_vol)
            # Place it in the main lv
            main_lv.placements.append(iec_pla.name)

    def build_cryostat(self, main_lv, geom):

        #Build the PV Barrel
        cryostat_builder = self.get_builder('CryostatBuilder')
        if cryostat_builder == None:
            return

        cryo_vol = cryostat_builder.get_volume("volCryostat")
        cryo_pla = geom.structure.Placement("Cryostat"+"_pla", volume=cryo_vol)
        # Place it in the main lv
        main_lv.placements.append(cryo_pla.name)

        rot_z = Q("0.0deg")
        ecryo_vol = cryostat_builder.get_volume("volCryostatEndcap")
        ecryo_rot = geom.structure.Rotation(ecryo_vol.name+"_rot", z=rot_z)
        ecryo_pla = geom.structure.Placement("CryostatEndcap"+"_pla", volume=ecryo_vol, rot=ecryo_rot)

        # Place it in the main lv
        main_lv.placements.append(ecryo_pla.name)

    def build_yoke(self,main_lv,geom):

        yoke_builder = self.get_builder('YokeBuilder')
        if yoke_builder == None:
            return

        byoke_vol = yoke_builder.get_volume("volYokeBarrel")
        yoke_shape = geom.store.shapes.get(byoke_vol.shape)
        nsides = yoke_shape.numsides
        print("Number of yoke sides", nsides)

        rot_z = Q("90.0deg")-Q("180.0deg")/nsides
        if nsides == 16:
            rot_z = rot_z + Q("22.5deg")

        byoke_rot = geom.structure.Rotation(byoke_vol.name+"_rot", z=rot_z)
        byoke_pla = geom.structure.Placement("YokeBarrel"+"_pla", volume=byoke_vol, rot=byoke_rot)

        # Place it in the main lv
        main_lv.placements.append(byoke_pla.name)

        eyoke_vol = yoke_builder.get_volume("volYokeEndcap")
        eyoke_rot = geom.structure.Rotation(eyoke_vol.name+"_rot", z=rot_z)
        eyoke_pla = geom.structure.Placement("YokeEndcap"+"_pla", volume=eyoke_vol, rot=eyoke_rot)

        # Place it in the main lv
        main_lv.placements.append(eyoke_pla.name)
