import os
import subprocess

def run_reconstruct_par(case_dir):
    """
    Run the reconstructPar command in the specified case directory.
    """
    command = ["reconstructPar"]
    print(f"Starting reconstructPar for case: {case_dir}")
    
    try:
        # Run the command
        subprocess.run(command, cwd=case_dir, check=True, text=True)
        print(f"reconstructPar completed successfully for {case_dir}")
    except subprocess.CalledProcessError as e:
        print(f"Error running reconstructPar for {case_dir}: {e}")
    except Exception as e:
        print(f"Unexpected error for {case_dir}: {e}")

def main():
    # List of concentration values
    #concentrations = [0.1, 0.15, 0.2, 0.25, 0.3]
    concentrations = [0.35, 0.4, 0.45, 0.5]
    # Generate case directory names from concentrations
    case_dirs = [f"concentration_case_{c}m_s" for c in concentrations]
    
    # Loop through each case directory and run reconstructPar
    for case_dir in case_dirs:
        if os.path.exists(case_dir) and os.path.isdir(case_dir):
            run_reconstruct_par(case_dir)
        else:
            print(f"Case directory {case_dir} does not exist or is not a directory. Skipping...")
    
    print("All cases have been processed with reconstructPar.")

if __name__ == "__main__":
    main()

