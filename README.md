# OpenFOAM-Parameter-Sweep
Python script for parameter sweep during CFD using OpenFOAM. 
# 1. The parameter sweep requires a basecase folder as a template for generating new cases
# 2. Starting the flow simulation by running the parameter_sweep.py. The inlet U normals need to be provided.
# 4. The scalar transform parameter sweep simulation requires huge computational resources. Run prepare_concentration_cases.py for preparation of transform scalar simulation in parallel. A base case folder for the transform scalar simulation is required. 
# 5. Run simulate_concentration_cases.py to start transform scalar simulation in parallel. Once it is done, run reconcstruct_case.py to reconstruct the mesh.
