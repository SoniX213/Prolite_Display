import tkinter as tk
from tkinter import messagebox

# Define the size of the grid
GRID_WIDTH = 18
GRID_HEIGHT = 7
MAX_BYTES = 126  # Maximum length for the bit pattern

# Color mappings
COLOR_MAP = {
    "R": "Red",
    "G": "Green",
    "Y": "Yellow",
    "B": "Black"
}

# Function to generate the code for the graphic block
def generate_code():
    bit_pattern = ""
    for row in range(GRID_HEIGHT):
        line = ""
        for col in range(GRID_WIDTH):
            selected_color = color_vars[row][col].get()
            line += selected_color
        bit_pattern += line[:18]  # Ensure each row is exactly 18 characters
    if len(bit_pattern) > MAX_BYTES:
        messagebox.showwarning("Input Error", f"Graphic block update must not exceed {MAX_BYTES} bytes.")
    else:
        # Display the generated code
        code_text.delete('1.0', tk.END)  # Clear previous code
        code_text.insert(tk.END, bit_pattern.strip())

# Create the tkinter UI
root = tk.Tk()
root.title("Graphic Block Editor")

# Initialize a 2D list to store the color selection variables
color_vars = []
for row in range(GRID_HEIGHT):
    row_vars = []
    for col in range(GRID_WIDTH):
        var = tk.StringVar(value="B")  # Default to black
        option_menu = tk.OptionMenu(root, var, *COLOR_MAP.keys())
        option_menu.grid(row=row, column=col, padx=2, pady=2)
        row_vars.append(var)
    color_vars.append(row_vars)

# Button to generate code
generate_button = tk.Button(root, text="Generate Code", command=generate_code)
generate_button.grid(row=GRID_HEIGHT, columnspan=GRID_WIDTH, pady=10)

# Text widget to display generated code
code_text = tk.Text(root, height=5, width=70)
code_text.grid(row=GRID_HEIGHT+1, columnspan=GRID_WIDTH, padx=10, pady=10)

root.mainloop()
