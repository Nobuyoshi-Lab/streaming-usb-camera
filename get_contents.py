import os
import tkinter as tk
from tkinter import filedialog

# Create Tkinter root window
root = tk.Tk()
root.withdraw()

# Open file dialog and get selected file paths
file_paths = filedialog.askopenfilenames()

# Loop through selected files and append their content to new content
new_content = ""
for path in file_paths:
    # Get file name
    file_name = os.path.basename(path)
    # Add colon to file name
    file_name += ":"
    # Read file content
    with open(path, "r") as file:
        content = file.read()
    # Prepend file name to content
    new_content += f"{file_name}\n{content}\n\n"

# Set output file path to "output.txt" in the same directory as the script
output_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output.txt")

# Write new content to file
with open(output_file_path, "w") as output_file:
    output_file.write(new_content)

print("Files appended and saved to the output file.")
