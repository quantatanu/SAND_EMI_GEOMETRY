void geoDisplay(TString fname)
{
	//gSystem->Load("libGdml");
	gSystem->Load("libGeom");
	TGeoManager *geo = new TGeoManager();
    geo->Import(fname);
    //geo->Import("example.gdml");
	//geo->Import("/mnt/bb47c2d1-aa7d-42ef-a4b2-33198d035691/atanu/Software/academic/NoVenvGeGeDe/DUNENDGGD/SAND_EMI_GEOMETRY/OUTPUT/GDML/SAND_opt3RPC_test_2022-04-03_IST_test.gdml");
	geo->DefaultColors();


	geo->CheckOverlaps(1e-5,"d");
 	geo->PrintOverlaps();

	//geo->SetMaxVisNodes(70000);
	//geo->SetVisLevel(3);
	geo->SetVisLevel(4);
	//geo->ViewLeaves(true);

       	geo->GetTopVolume()->Draw("ogl");
}
