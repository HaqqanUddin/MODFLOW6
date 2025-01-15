import flopy
import numpy as np
import matplotlib.pyplot as plt

# Define the path to the .bhd file
head_file_path = '/home/haqqanuddin/mf6_quetta_run/mf6_quetta.bhd'

# Read the head data from the .bhd file (last time step)
head = flopy.utils.HeadFile(head_file_path).get_data()[-1]

# Replace no-data values (1e30) with NaN
head = np.where(head == 1e30, np.nan, head)

# Plot the head data
plt.figure(figsize=(10, 8))
plt.pcolormesh(head, cmap='cividis', shading='auto')
plt.colorbar(label="Head (m)")

# Set labels and title
plt.title("Head Distribution at Last Time Step")
plt.xlabel("Heads (m)")
plt.ylabel("Distance (m)")

# Invert the Y-axis to correct the orientation
plt.gca().invert_yaxis()

# Save the plot as an image file (e.g., PNG)
plt.savefig('model_heads.png')

# Optional: Close the plot after saving to avoid memory issues
plt.close()
