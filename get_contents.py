import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

# Create Tkinter root window
root = tk.Tk()
root.withdraw()

# Get script directory path
script_dir = os.path.dirname(os.path.abspath(__file__))

# Open file dialog and get selected file paths
file_paths = filedialog.askopenfilenames()

# Loop through selected files and append their content to new content
new_content = ""
for path in file_paths:
    # Get relative file path
    rel_path = os.path.relpath(path, script_dir)
    # Add colon to file name
    file_name = rel_path + ":"
    # Read file content
    with open(path, "r") as file:
        content = file.read()
    # Prepend file name to content
    new_content += f"{file_name}\n{content}\n\n"

# Set output file path to "output.txt" in the same directory as the script
output_file_path = os.path.join(script_dir, "output.txt")

# Check if output file already exists
if os.path.exists(output_file_path):
    # Create message box with "Replace" and "Append" buttons
    answer = messagebox.askquestion("Output file exists", "The output file already exists. Do you want to replace its contents?", icon="question", type="yesnocancel", default="yes")
    if answer == "no":
        # If user chooses not to replace, open file in "append" mode
        mode = "a"
    elif answer == "yes":
        # If user chooses to replace, open file in "write" mode and clear its contents
        mode = "w"
        with open(output_file_path, "w") as output_file:
            pass
    else:
        # If user chooses to cancel, exit the program
        exit()
else:
    # If output file doesn't exist, open it in "write" mode
    mode = "w"

# Write new content to file
with open(output_file_path, mode) as output_file:
    output_file.write(new_content)

print("Files appended and saved to the output file.")
