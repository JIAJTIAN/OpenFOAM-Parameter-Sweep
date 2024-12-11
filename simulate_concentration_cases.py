import subprocess
import os

def run_simulation(case_dir):
    """
    Run the foamJob -parallel scalarTransportFoam command for the given case directory.
    """
    command = ["foamJob", "-parallel", "scalarTransportFoam"]
    print(f"Starting simulation for case: {case_dir}")
    try:
        # Run the job in the background (with 8 cores)
        subprocess.Popen(command, cwd=case_dir)
        print(f"Started simulation for {case_dir} in the background.")
    except Exception as e:
        print(f"Error running simulation for {case_dir}: {e}")

def main():
    # List of all case directories that you want to run the simulations for
    #case_dirs = [f"concentration_case_{velocity}m_s" for velocity in [0.1, 0.15, 0.2, 0.25, 0.3]] # 64 cores max, 8 each, let's use 5 cases at one time
    case_dirs = [f"concentration_case_{velocity}m_s" for velocity in [0.35, 0.4, 0.45, 0.5]] # 64 cores max, 8 each, let's use 5 cases at one time
    # Loop over each case directory and start the simulation
    for case_dir in case_dirs:
        run_simulation(case_dir)

    print("All simulations started in the background.")

if __name__ == "__main__":
    main()

