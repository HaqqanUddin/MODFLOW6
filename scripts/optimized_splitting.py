# Import the required libraries
from pathlib import Path  # For handling and manipulating paths in the filesystem
import flopy  # For working with MODFLOW models (the core of this script)
from flopy.mf6.utils import Mf6Splitter  # For splitting MODFLOW 6 models into smaller parts

# Define the directory containing the MODFLOW 6 model and the simulation name
model_directory = r"F:\E\Master courses\Semesters\Thesis\New\GW Model Data\Model\Model (FPS-new)\Model (FPS)"
sim_name = "mfsim.nam"  # Name of the MODFLOW simulation file (typically a .nam file)

# Load the existing MODFLOW 6 simulation from the specified directory
# This will load the simulation object that can be modified or analyzed
sim = flopy.mf6.MFSimulation.load(sim_name=sim_name, sim_ws=model_directory, exe_name='mf6')

# Initialize the Mf6Splitter object which helps to split the model into smaller parts
mfsplit = Mf6Splitter(sim)

# Optimize the splitting mask by dividing the model into 4 parts
# The 'nparts=4' argument specifies that the model should be split into 4 parts
split_array = mfsplit.optimize_splitting_mask(nparts=4)

# Perform the actual model split using the optimized splitting mask
# The result is a new simulation object, which consists of the split models
new_sim = mfsplit.split_model(split_array)

# Create a new directory for saving the split model files
# This ensures that the directory exists, and creates it if it doesn't
workspace = Path(r"F:\E\Master courses\Semesters\Thesis\New\GW Model Data\Model\mf630years_splitted_6")
workspace.mkdir(parents=True, exist_ok=True)  # 'parents=True' ensures all parent directories are created

# Set the path for the new simulation and write the new simulation files to the directory
new_sim.set_sim_path(str(workspace))
new_sim.write_simulation()  # This writes the simulation files for the split model

# Print the path where the split models have been saved for user reference
print(f"Split models have been saved in: {workspace}")