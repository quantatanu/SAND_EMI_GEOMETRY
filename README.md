# SAND_EMI_GEOMETRY

This is a tool to build proposal geometries for DUNE near detector.

It's based on the dunendggd [dunendggd](https://github.com/gyang9/dunendggd)



# Note:
    * Currently strip width/segment-size is used to segment the gas volume, with width of 1.5 mm and a gap of 0.05 mm between two segments/strips



# Setup

```bash
python setup.py develop
```

# Example
To run an example containing basic detectors, you could process like:
```bash
./build_hall.sh justemi
```

To run a full example containing surrounded magnet
```bash
./build_hall.sh opt3
```

# Quick Visualization
To do a quick check or your geometry file you can use ROOT-CERN:
```bash
./ROOT_MACROS/BIN/geodisplay_gdml 'example.gdml'
```


# Contact
* **SAND_EMI_GEOMETRY:**
  * Atanu Nath `atanu.quanta@gmail.com`
* **dunendggd:**
  * Guang Yang `guang.yang.1@stonybrook.edu`
  * Jose Palomino`jose.palominogallo@stonybrook.edu`
* **GeGeDe:**
  * Brett Viren `bviren@bnl.gov`
