import subprocess
import os
import shutil

def run_command(command, cwd=None):
    """
    Run a shell command and wait for it to complete.
    """
    try:
        print(f"Running command: {command}")
        result = subprocess.run(command, shell=True, cwd=cwd, check=True, text=True)
        print(f"Command completed successfully: {command}")
    except subprocess.CalledProcessError as e:
        print(f"Error while running command: {command}\n{e}")

def update_velocity_inlet(case_dir, velocity, inlet_normals):
    """
    Update the velocity values in the 0/U file for each inlet based on the given velocity and normal vectors.
    """
    # Iterate over the inlets and update their velocity values
    for inlet_name, normal_inlet in inlet_normals.items():
        U_x = velocity * normal_inlet[0]
        U_y = velocity * normal_inlet[1]
        U_z = velocity * normal_inlet[2]

        file_path = os.path.join(case_dir, '0', 'U')

        with open(file_path, 'r') as file:
            data = file.readlines()

        # Initialize flags to mark which inlets are already updated
        inlets_updated = {name: False for name in inlet_normals}

        # Iterate over the file lines and update each inlet boundary condition
        for i, line in enumerate(data):
            if inlet_name in line and not inlets_updated[inlet_name]:
                # Update for the current inlet
                data[i] = f'    {inlet_name}\n'  # Correct indentation
                data[i + 1] = '    {\n'
                data[i + 2] = f'        type            fixedValue;\n'
                data[i + 3] = f'        value           uniform ({U_x} {U_y} {U_z});\n'
                data[i + 4] = '    }\n'
                inlets_updated[inlet_name] = True

        # Write the updated data back to the file
        with open(file_path, 'w') as file:
            file.writelines(data)

def delete_processor_folders(case_dir):
    """
    Delete all processor directories (e.g., processor0, processor1, etc.) in the case directory.
    """
    for folder_name in os.listdir(case_dir):
        if folder_name.startswith("processor"):
            processor_dir = os.path.join(case_dir, folder_name)
            if os.path.isdir(processor_dir):
                print(f"Deleting processor directory: {processor_dir}")
                shutil.rmtree(processor_dir)

def setup_case(case_dir, velocity, inlet_normals):
    """
    Set up the OpenFOAM case by copying the base case and updating the 0/U file with new velocity.
    """
    # Step 1: If the case directory exists, remove it before copying baseCase
    if os.path.exists(case_dir):
        print(f"Deleting existing case directory: {case_dir}")
        shutil.rmtree(case_dir)
    
    # Step 2: Copy baseCase to create a new case directory
    print(f"Creating new case directory: {case_dir}")
    shutil.copytree("baseCase", case_dir)

    # Step 3: Update velocity values for inlets in the 0/U file
    update_velocity_inlet(case_dir, velocity, inlet_normals)

def run_simulation(case_dir):
    """
    Run the OpenFOAM simulation (decompose, solver, reconstruct).
    """
    print(f"Running simulation in case directory: {case_dir}")

    # Step 1: Delete existing processor directories (if any)
    delete_processor_folders(case_dir)

    # Step 2: Decompose the domain (will now run in the foreground)
    run_command("decomposePar", cwd=case_dir)

    # Step 3: Run the solver in parallel (will now run in the foreground)
    run_command("mpirun --mca btl ^openib -np 8 simpleFoam -parallel", cwd=case_dir)

    # Step 4: Reconstruct the results
    run_command("reconstructPar", cwd=case_dir)

def main():
    # Updated velocity list
    velocities = [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]  # Example velocity values (m/s)

    # Inlet normals
    inlet_normals = {
        "inlet1": [0.293894, 0.4045075, 0.0],
        "inlet2": [0.4755275, 0.154511, 0.0],
        "inlet3": [0.475528, -0.1545085, 0.0],
        "inlet4": [0.2938955, -0.4045065, 0.0]
    }

    for velocity in velocities:
        case_dir = f"case_{velocity}m_s"
        print(f"Starting simulation for velocity {velocity} m/s")

        # Setup the case directory and update velocities
        setup_case(case_dir, velocity, inlet_normals)

        # Run the OpenFOAM simulation (decompose, run solver, reconstruct)
        run_simulation(case_dir)

        print(f"Simulation for velocity {velocity} m/s completed.\n")

    print("All simulations completed!")

if __name__ == "__main__":
    main()

