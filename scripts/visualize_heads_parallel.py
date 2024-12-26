# Import necessary libraries
import numpy as np  # For numerical operations, especially with arrays
import matplotlib.pyplot as plt  # For creating plots
import flopy  # For working with MODFLOW model data
import flopy.utils.binaryfile as bf  # To read binary head files (.bhd)
import os  # For handling file paths

# Define the path to the directory containing the .bhd files (head data files)
model_ws = '/home/haqqanuddin/mf630years_splitted'

# Define the paths to the .bhd files for each submodel (part of the split model)
bhd_files = [
    os.path.join(model_ws, 'Rio_Grande_Basin_0.bhd'),
    os.path.join(model_ws, 'Rio_Grande_Basin_1.bhd'),
    os.path.join(model_ws, 'Rio_Grande_Basin_2.bhd'),
    os.path.join(model_ws, 'Rio_Grande_Basin_3.bhd')
]

# Create an empty list to hold the head data for each submodel
head_data = []

# Loop through each .bhd file, load the head data, and handle any errors
for bhd_file in bhd_files:
    try:
        # Load the head data from the .bhd file using FloPy's HeadFile
        head_file = bf.HeadFile(bhd_file)
        
        # Extract the head data for the last time step from the file
        head_array = head_file.get_data(totim=head_file.get_times()[-1])
        
        # Append the head data to the list for later use
        head_data.append(head_array)
    except Exception as e:
        # If there's an error (e.g., file not found), print the error message and append None
        print(f"Error loading head data from {bhd_file}: {e}")
        head_data.append(None)  # Append None for any failed files

# Handle NaNs or infinities in the head data for proper visualization
# Replace NaN values with the median of the array and infinities with extreme finite values
head_data_cleaned = []
for head in head_data:
    if head is not None:
        # Use np.nan_to_num to clean the data by replacing NaNs and infinities
        clean_head = np.nan_to_num(head, nan=np.nanmedian(head), posinf=np.nanmax(head), neginf=np.nanmin(head))
        head_data_cleaned.append(clean_head)
    else:
        head_data_cleaned.append(None)  # Keep None for failed files

# Calculate global minimum and maximum head values across all submodels for consistent color scaling
vmin = min([np.nanmin(h) for h in head_data_cleaned if h is not None])
vmax = max([np.nanmax(h) for h in head_data_cleaned if h is not None])

# Create the plot layout (2x2 grid for 4 submodels)
fig, axes = plt.subplots(2, 2, figsize=(18, 14))  # Increased height for better spacing between plots
axes = axes.flatten()  # Flatten the 2x2 array to iterate through each subplot

# Choose a colormap for the plots
cmap = "viridis"  # 'viridis' is a popular perceptually uniform colormap

# Plot the head data for each submodel
for i, ax in enumerate(axes):
    if head_data_cleaned[i] is not None:
        # For each submodel, plot the head data (first slice of the 3D data)
        c = ax.imshow(
            head_data_cleaned[i][0, :, :],  # Plot the first time step's head data (index 0)
            cmap=cmap, origin='lower', vmin=vmin, vmax=vmax  # Adjust origin and color scale
        )
        
        # Set the title for the subplot
        ax.set_title(f"Submodel {i}", pad=20, fontsize=12)
        
        # Label the x and y axes
        ax.set_xlabel("Distance (m)", labelpad=15, fontsize=10)
        ax.set_ylabel("Head (m)", labelpad=15, fontsize=10)
        
        # Rotate x-axis tick labels for visibility
        ax.tick_params(axis='x', labelrotation=45)
    else:
        # If no head data is available, display a message and turn off the axis
        ax.text(0.5, 0.5, "No Data", ha='center', va='center', fontsize=12)
        ax.axis("off")

# Adjust layout to avoid overlapping labels and ensure proper spacing between subplots
fig.subplots_adjust(left=0.1, right=0.85, top=0.92, bottom=0.08, hspace=0.5, wspace=0.5)

# Add a colorbar to the plot to indicate the hydraulic head scale
cbar_ax = fig.add_axes([0.87, 0.15, 0.03, 0.7])  # Adjust the colorbar's position
fig.colorbar(c, cax=cbar_ax, label="Hydraulic Head (m)")  # Label the colorbar

# Show the plot
plt.show()  # Display the plot with all submodels