import sys
from pathlib import Path
from tempfile import TemporaryDirectory
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import flopy
from flopy.mf6.utils import Mf6Splitter

# Define the model directory and simulation name
model_directory = r"F:\E\Master courses\Semesters\Thesis\New\GW Model Data\Model\Model (FPS-new)\Model (FPS)"
sim_name = "mfsim.nam"

# Load the MODFLOW 6 simulation
sim = flopy.mf6.MFSimulation.load(sim_name=sim_name, sim_ws=model_directory, exe_name='mf6')

# Initialize the splitter and optimize the splitting mask for 4 parts
mfsplit = Mf6Splitter(sim)
split_array = mfsplit.optimize_splitting_mask(nparts=4)

# Perform the actual model split
new_sim = mfsplit.split_model(split_array)

# Setup a directory for the split models
workspace = Path(r"F:\E\Master courses\Semesters\Thesis\New\GW Model Data\Model\mf630years_splitted_6")
workspace.mkdir(parents=True, exist_ok=True)

# Set the path for the new simulation and write the simulation files
new_sim.set_sim_path(str(workspace))
new_sim.write_simulation()

print(f"Split models have been saved in: {workspace}")