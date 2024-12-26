# Import necessary libraries
import flopy  # Library to work with MODFLOW models, including reading head data
import numpy as np  # For numerical operations, especially with arrays
import matplotlib.pyplot as plt  # For creating plots

# Define the path to the MODFLOW head data file (.bhd)
head_file_path = r'D:\D\Masters Courses\Thesis\New\Model Data\Model\mf630years-run\Rio_Grande_Basin.bhd'

# Read the head data from the .bhd file using FloPy's HeadFile function
# This will allow us to access the groundwater head data for each timestep
head_obj = flopy.utils.HeadFile(head_file_path)

# Get the head data for the last time step
# The get_data() method returns the head data for all time steps, and [-1] extracts the last time step
head = head_obj.get_data()[-1]

# Replace no-data values (1e30) with NaN (Not a Number) for proper visualization
# No-data values are typically represented by a very large number, like 1e30
head = np.where(head == 1e30, np.nan, head)

# Prepare the plot (create a figure and axis object)
fig, ax = plt.subplots(figsize=(10, 8))  # Adjust the size of the plot as necessary

# Set the minimum and maximum head values for better scaling of the plot (optional)
# This is useful if you want to control the color scale manually
vmin = np.nanmin(head)  # Minimum value of the head data
vmax = np.nanmax(head)  # Maximum value of the head data

# Alternatively, you can set fixed values for vmin and vmax if you know the expected range, e.g.:
# vmin = 0
# vmax = 1000

# Create a pcolormesh plot of the head data
# pcolormesh is used for creating 2D grid plots where the color represents the head value
pc = ax.pcolormesh(head, cmap='cividis', vmin=vmin, vmax=vmax, shading='auto')

# Add a colorbar to the plot to indicate the value range
cbar = plt.colorbar(pc, ax=ax, label="Head (m)")  # Label the colorbar with "Head (m)"

# Set the plot title and axis labels
ax.set_title("Head Distribution at Last Time Step", fontsize=16)  # Title of the plot
ax.set_xlabel("Column Index", fontsize=12)  # Label for the x-axis
ax.set_ylabel("Row Index", fontsize=12)  # Label for the y-axis

# Optionally add gridlines to make the grid more visible
# The 'which' argument controls whether to apply to both major and minor gridlines
ax.grid(True, which='both', color='k', linewidth=0.5)

# Set aspect ratio to be equal to avoid distortion of the grid in the plot
ax.set_aspect('equal', adjustable='box')

# Display the plot
plt.show()  # This shows the plot to the user