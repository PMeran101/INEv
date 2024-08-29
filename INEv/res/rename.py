import os

# Define the suffix you want to add
suffix = "_fog"  # Replace with your desired suffix

# Get the current directory
current_directory = os.getcwd()

# Loop through all files in the current directory
for filename in os.listdir(current_directory):
    # Check if the file is a CSV
    if filename.endswith(".csv"):
        # Split the file name and extension
        name, ext = os.path.splitext(filename)
        
        # Create the new file name by adding the suffix
        new_name = f"{name}{suffix}{ext}"
        
        # Rename the file
        os.rename(os.path.join(current_directory, filename), os.path.join(current_directory, new_name))
        print(f"Renamed: {filename} to {new_name}")

print("Renaming completed.")
