import sys
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import flopy
from flopy.mf6.utils import Mf6Splitter

# Define the model directory and simulation name
model_directory = "/home/haqqanuddin/mf6_quetta/"
sim_name = "mfsim.nam"

# Load the MODFLOW 6 simulation
try:
    sim = flopy.mf6.MFSimulation.load(sim_name=sim_name, sim_ws=model_directory, exe_name='mf6')
except Exception as e:
    print(f"Error loading simulation: {e}")
    sys.exit(1)

# Initialize the splitter and optimize the splitting mask for 6 parts
try:
    mfsplit = Mf6Splitter(sim)
    split_array = mfsplit.optimize_splitting_mask(nparts=2)

    # Debugging: Check the type and shape of the split_array
    print(f"split_array type: {type(split_array)}")
    print(f"split_array shape: {np.shape(split_array)}")
    print(f"split_array: {split_array[:10]}")  # Display first 10 elements for inspection
    
    # Plot the split_array for visual verification (optional)
    plt.imshow(split_array, cmap='viridis', interpolation='nearest')
    plt.colorbar()
    plt.show()

    # Ensure split_array is an integer array
    if not np.issubdtype(split_array.dtype, np.integer):
        print("Converting split_array to integers...")
        split_array = split_array.astype(int)
        
    # Additional check to ensure split_array is 1D or 2D and contains valid indices
    if split_array.ndim not in [1, 2]:
        print(f"Error: split_array is not 1D or 2D, its shape is {np.shape(split_array)}")
        sys.exit(1)

    # Ensure there are no non-integer values in split_array
    if not np.all(np.isin(split_array, np.arange(0, np.max(split_array) + 1))):
        print("Error: split_array contains invalid indices.")
        sys.exit(1)

except Exception as e:
    print(f"Error during splitting mask optimization: {e}")
    sys.exit(1)

# Perform the actual model split
try:
    new_sim = mfsplit.split_model(split_array)
except Exception as e:
    print(f"Error during model splitting: {e}")
    sys.exit(1)

# Setup a directory for the split models
workspace = Path("/home/haqqanuddin/mf6_quetta_splitted_2/")
workspace.mkdir(parents=True, exist_ok=True)

# Get the split model names and verify
new_model_names = new_sim.model_names
print(f"Created {len(new_model_names)} submodels: {new_model_names}")

# Set the path for the new simulation and write the simulation files
new_sim.set_sim_path(workspace)
new_sim.write_simulation()

print(f"Split models have been saved in: {workspace}")
