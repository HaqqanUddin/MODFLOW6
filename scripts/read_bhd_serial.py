import flopy
import numpy as np
import matplotlib.pyplot as plt

# Define the path to your .bhd file (MODFLOW head data file)
head_file_path = r'D:\D\Masters Courses\Thesis\New\Model Data\Model\mf630years-run\Rio_Grande_Basin.bhd'

# Read the head data from the .bhd file using FloPy
head_obj = flopy.utils.HeadFile(head_file_path)

# Get the head data for the last time step
head = head_obj.get_data()[-1]  # Get the last time step's head data

# Replace no-data values (1e30) with NaN for plotting
head = np.where(head == 1e30, np.nan, head)

# Prepare the plot
fig, ax = plt.subplots(figsize=(10, 8))

# Set the minimum and maximum head values for better scaling (optional)
vmin = np.nanmin(head)
vmax = np.nanmax(head)
# You can set your own values to improve the visualization if you know your head ranges, e.g.:
# vmin = 0
# vmax = 1000

# Create a pcolormesh plot for the head data
pc = ax.pcolormesh(head, cmap='cividis', vmin=vmin, vmax=vmax, shading='auto')

# Add a colorbar with a label
cbar = plt.colorbar(pc, ax=ax, label="Head (m)")

# Set plot labels and title
ax.set_title("Head Distribution at Last Time Step", fontsize=16)
ax.set_xlabel("Column Index", fontsize=12)
ax.set_ylabel("Row Index", fontsize=12)

# Optionally add gridlines to make the grid more visible
ax.grid(True, which='both', color='k', linewidth=0.5)

# Set aspect ratio to be equal to prevent distortion of the grid
ax.set_aspect('equal', adjustable='box')

# Show the plot
plt.show()
