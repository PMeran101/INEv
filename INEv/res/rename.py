import os

# Define the suffix you want to add
<<<<<<< HEAD
suffix = "_normal"  # Replace with your desired suffix
=======
suffix = "_Fog"  # Replace with your desired suffix
>>>>>>> fog_cloud_topology

# Get the current directory
current_directory = os.getcwd()

# Loop through all files in the current directory
for filename in os.listdir(current_directory):
    # Check if the file is a CSV
<<<<<<< HEAD
    if filename.endswith(".csv"):
=======
    if filename.endswith(".csv") and not filename.endswith("_Fog.csv"):
>>>>>>> fog_cloud_topology
        # Split the file name and extension
        name, ext = os.path.splitext(filename)
        
        # Create the new file name by adding the suffix
        new_name = f"{name}{suffix}{ext}"
        
        # Rename the file
        os.rename(os.path.join(current_directory, filename), os.path.join(current_directory, new_name))
        print(f"Renamed: {filename} to {new_name}")

print("Renaming completed.")
