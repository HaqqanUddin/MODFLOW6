import flopy
import numpy as np
import matplotlib.pyplot as plt

# Define the paths to the .bhd files for each submodel
head_file_paths = [
    '/home/haqqanuddin/mf6_quetta_splitted_2/mf6_quetta_0.bhd',
    '/home/haqqanuddin/mf6_quetta_splitted_2/mf6_quetta_1.bhd'
]

# Create a list to hold the head data for each submodel
head_data = []

# Read the head data for each submodel (last time step)
for head_file_path in head_file_paths:
    head = flopy.utils.HeadFile(head_file_path).get_data()[-1]
    
    # Replace no-data values (1e30) with NaN
    head = np.where(head == 1e30, np.nan, head)
    
    head_data.append(head)

# Create a plot layout (1x2 grid for 2 submodels)
fig, axes = plt.subplots(1, 2, figsize=(14, 7))  # 1 row, 2 columns
axes = axes.flatten()

# Select a colormap
cmap = 'cividis'

# Plot each submodel's head data
for i, ax in enumerate(axes):
    # Plot the head data for the current submodel
    c = ax.pcolormesh(head_data[i], cmap=cmap, shading='auto')
    
    # Set the title for each subplot
    ax.set_title(f"Submodel {i}", pad=20, fontsize=12)
    
    # Set labels for x and y axes
    ax.set_xlabel("Distance (m)", fontsize=10)
    ax.set_ylabel("Head (m)", fontsize=10)
    
    # Invert the y-axis to correct the orientation
    ax.invert_yaxis()

    # Add a colorbar
    fig.colorbar(c, ax=ax, label="Head (m)")

# Adjust layout for better spacing
fig.subplots_adjust(left=0.1, right=0.85, top=0.92, bottom=0.08, hspace=0.5, wspace=0.5)

# Save the plot as an image file (e.g., PNG)
plt.savefig('/home/haqqanuddin/scripts/final/submodel_heads.png', bbox_inches='tight')

# Optional: Close the plot after saving to avoid memory issues
plt.close()

