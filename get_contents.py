import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

class CustomDialog(tk.Toplevel):
    def __init__(self, parent, title, message):
        super().__init__(parent)
        self.title(title)
        self.message = message
        self.result = None

        self.create_widgets()
        self.protocol("WM_DELETE_WINDOW", self.cancel)

    def create_widgets(self):
        label = ttk.Label(self, text=self.message)
        label.pack(padx=20, pady=10)

        button_frame = ttk.Frame(self)
        button_frame.pack(padx=20, pady=(0, 10))

        replace_button = ttk.Button(button_frame, text="Replace", command=self.replace)
        replace_button.pack(side="left", padx=(0, 10))

        append_button = ttk.Button(button_frame, text="Append", command=self.append)
        append_button.pack(side="left", padx=(0, 10))

        cancel_button = ttk.Button(button_frame, text="Cancel", command=self.cancel)
        cancel_button.pack(side="left")

    def replace(self):
        self.result = "w"
        self.destroy()

    def append(self):
        self.result = "a"
        self.destroy()

    def cancel(self):
        self.result = None
        self.destroy()

def create_root_window():
    root = tk.Tk()
    root.withdraw()
    style = ttk.Style()
    style.theme_use('clam')
    return root

def get_file_paths(root):
    return filedialog.askopenfilenames(parent=root)

def read_and_combine_files(file_paths, script_dir):
    new_content = ""
    for path in file_paths:
        rel_path = os.path.relpath(path, script_dir)
        file_name = f"{rel_path}:"
        with open(path, "r") as file:
            content = file.read()
        new_content += f"{file_name}\n{content}\n\n"
    return new_content

def get_output_file_mode(root, output_file_path):
    if os.path.exists(output_file_path):
        dialog = CustomDialog(root, "Output file exists", "The output file already exists. Do you want to replace its contents?")
        root.wait_window(dialog)
        result = dialog.result
        if result is not None:
            return result
        else:
            exit()
    else:
        return "w"

def write_output_file(output_file_path, mode, new_content):
    with open(output_file_path, mode) as output_file:
        output_file.write(new_content)

def display_success_message(operation_type):
    if operation_type == "w":
        print("Files have been combined and saved to the output file, replacing its previous contents.")
    elif operation_type == "a":
        print("Files have been combined and appended to the output file.")
    else:
        print("Unknown operation type.")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root = create_root_window()
    file_paths = get_file_paths(root)
    new_content = read_and_combine_files(file_paths, script_dir)
    output_file_path = os.path.join(script_dir, "output.txt")
    mode = get_output_file_mode(root, output_file_path)
    write_output_file(output_file_path, mode, new_content)
    display_success_message(mode)

if __name__ == "__main__":
    main()
