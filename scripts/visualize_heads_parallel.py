import numpy as np
import matplotlib.pyplot as plt
import flopy
import flopy.utils.binaryfile as bf
import os

# Path to the directory containing the .bhd files
model_ws = '/home/haqqanuddin/mf630years_splitted'

# Paths to the .bhd files for each submodel
bhd_files = [
    os.path.join(model_ws, 'Rio_Grande_Basin_0.bhd'),
    os.path.join(model_ws, 'Rio_Grande_Basin_1.bhd'),
    os.path.join(model_ws, 'Rio_Grande_Basin_2.bhd'),
    os.path.join(model_ws, 'Rio_Grande_Basin_3.bhd')
]

# Create a list to hold the head data for each submodel
head_data = []

# Loop through each .bhd file and load the head data
for bhd_file in bhd_files:
    try:
        # Load the head data from the .bhd file using FloPy
        head_file = bf.HeadFile(bhd_file)
        
        # Get the array of head data for the last time step
        head_array = head_file.get_data(totim=head_file.get_times()[-1])
        
        # Append the head data to the list
        head_data.append(head_array)
    except Exception as e:
        print(f"Error loading head data from {bhd_file}: {e}")
        head_data.append(None)  # Append None for failed files

# Handle NaNs or infinities in head data
# Replace NaN with the median of the array and set infinities to finite values
head_data_cleaned = []
for head in head_data:
    if head is not None:
        clean_head = np.nan_to_num(head, nan=np.nanmedian(head), posinf=np.nanmax(head), neginf=np.nanmin(head))
        head_data_cleaned.append(clean_head)
    else:
        head_data_cleaned.append(None)

# Calculate global min and max for consistent color scaling across subplots
vmin = min([np.nanmin(h) for h in head_data_cleaned if h is not None])
vmax = max([np.nanmax(h) for h in head_data_cleaned if h is not None])

# Create the plot layout (2x2 grid for 4 submodels)
fig, axes = plt.subplots(2, 2, figsize=(18, 14))  # Increased height for better spacing
axes = axes.flatten()

# Select a suitable colormap
cmap = "viridis"
# Plot each submodel's head data
for i, ax in enumerate(axes):
    if head_data_cleaned[i] is not None:
        # Plot the head data for the current submodel
        c = ax.imshow(
            head_data_cleaned[i][0, :, :], 
            cmap=cmap, origin='lower', vmin=vmin, vmax=vmax
        )
        
        # Set the title
        ax.set_title(f"Submodel {i}", pad=20, fontsize=12)
        
        # Set x and y labels
        ax.set_xlabel("Distance (m)", labelpad=15, fontsize=10)
        ax.set_ylabel("Head (m)", labelpad=15, fontsize=10)
        
        # Rotate x-axis tick labels for visibility
        ax.tick_params(axis='x', labelrotation=45)
    else:
        ax.text(0.5, 0.5, "No Data", ha='center', va='center', fontsize=12)
        ax.axis("off")

# Adjust layout to avoid overlaps
fig.subplots_adjust(left=0.1, right=0.85, top=0.92, bottom=0.08, hspace=0.5, wspace=0.5)

# Add colorbar
cbar_ax = fig.add_axes([0.87, 0.15, 0.03, 0.7])  # Adjust for better placement
fig.colorbar(c, cax=cbar_ax, label="Hydraulic Head (m)")

# Show the plot
plt.show()
