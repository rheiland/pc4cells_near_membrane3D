# pc4cells_near_membrane

Experimental PhysiCell 3D model for testing cell mechanics near a "membrane" (in this case, the x-z plane (y=0)).

Compile, copy the executable to the root directory, run the GUI:
```
cd pc4cells_near_membrane/src
make
cp mymodel ..
cd ..
python bin/studio.py
```

In the GUI:
* in the Run tab, click `Run Simulation` (it will use all the default parameters)
* in the Plot tab, click `Play`
* edit params if you want then repeat: Run, Play
