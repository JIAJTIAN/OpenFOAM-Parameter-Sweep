# OpenFOAM-Parameter-Sweep
Python script for parameter sweep during CFD using OpenFOAM. 

# 1. Flow condition CFD
The parameter sweep on flow condition CFD requires a base case folder as a template for generating new cases
Starting the flow simulation by running the parameter_sweep.py. The inlet U normals need to be provided.

# 2. Scalar transform parameter sweep simulation 
scalrTransportFoam requires huge computing resources. Run prepare_concentration_cases.py for preparation of transform scalar simulation in parallel. A base case folder for the transform scalar simulation is required. 
Run simulate_concentration_cases.py to start transform scalar simulation in parallel. Once it is done, run reconcstruct_case.py to reconstruct the mesh.
