import subprocess
import os
import shutil

def copy_latest_velocity_to_concentration_case(velocity_case_dir, concentration_case_dir):
    """
    Copy the latest U field from the velocity case directory's latest time directory
    to the 0/U file in the concentration case directory.
    """
    # Find all time directories (those with numeric names)
    time_dirs = [d for d in os.listdir(velocity_case_dir) if d.isdigit()]
    
    # Find the latest time directory (i.e., the one with the largest number)
    latest_time_dir = max(time_dirs, key=int)  # Get the largest number
    
    # Define the path to the U file in the latest time directory
    velocity_U_path = os.path.join(velocity_case_dir, latest_time_dir, 'U')
    
    # Define the path where the U field should be copied in the concentration case
    concentration_U_path = os.path.join(concentration_case_dir, '0', 'U')
    
    # Ensure the destination directory exists
    os.makedirs(os.path.dirname(concentration_U_path), exist_ok=True)
    
    # Copy the U field from the latest velocity time directory to the concentration case
    shutil.copy(velocity_U_path, concentration_U_path)
    print(f"Copied U from {velocity_case_dir}/{latest_time_dir}/U to {concentration_case_dir}/0/U")

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

def decompose_case(case_dir):
    """
    Run the decomposePar command to decompose the OpenFOAM case for parallel processing.
    """
    print(f"Running decomposePar in {case_dir}")
    try:
        subprocess.run("decomposePar", cwd=case_dir, check=True, text=True)
        print(f"decomposePar completed successfully in {case_dir}")
    except subprocess.CalledProcessError as e:
        print(f"Error during decomposePar in {case_dir}: {e}")

def setup_concentration_case(case_dir, velocity_case_dir):
    """
    Set up the concentration OpenFOAM case by copying concentration_basecase and updating the 0/U file with new velocity.
    """
    # Step 1: Always copy the concentration_basecase, overwriting if necessary
    if os.path.exists(case_dir):
        print(f"Case directory {case_dir} already exists. Overwriting it...")
        shutil.rmtree(case_dir)  # Remove the existing directory
    shutil.copytree("concentration_basecase", case_dir)
    print(f"Copied concentration_basecase to {case_dir}.")
    
    # Step 2: Copy the latest velocity field (U) from the velocity case directory
    copy_latest_velocity_to_concentration_case(velocity_case_dir, case_dir)

    # Step 3: Delete any existing processor directories (if any)
    delete_processor_folders(case_dir)

    # Step 4: Run decomposePar for parallel processing
    decompose_case(case_dir)

def main():
    velocities = [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]  # Example velocity values (m/s)

    for velocity in velocities:
        velocity_case_dir = f"case_{velocity}m_s"
        concentration_case_dir = f"concentration_case_{velocity}m_s"
        print(f"Starting setup for concentration simulation for velocity {velocity} m/s")

        # Setup the concentration case directory by copying and updating the velocity U field
        setup_concentration_case(concentration_case_dir, velocity_case_dir)

        print(f"Concentration case setup for velocity {velocity} m/s completed.\n")

    print("All concentration case setups completed!")

if __name__ == "__main__":
    main()

