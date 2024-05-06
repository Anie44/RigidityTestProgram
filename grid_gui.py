import tkinter as tk
from tkinter import ttk
import grid_program

class GridGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Rigidity Test")
        self.window_width = 1200
        self.window_height = 800
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x_offset = (screen_width - self.window_width) // 2
        y_offset = (screen_height - self.window_height) // 2
        self.master.geometry(f"{self.window_width}x{self.window_height}+{x_offset}+{y_offset}")

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.master)
        main_frame.pack(pady=20)

        ttk.Label(main_frame, text="Rows:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.row_var = tk.StringVar(self.master)
        self.row_dropdown = ttk.Combobox(main_frame, textvariable=self.row_var, state="readonly", width=5)
        self.row_dropdown["values"] = tuple(range(1, 11))
        self.row_dropdown.current(1)
        self.row_dropdown.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        ttk.Label(main_frame, text="Columns:").grid(row=0, column=2, padx=10, pady=10, sticky="e")
        self.column_var = tk.StringVar(self.master)
        self.column_dropdown = ttk.Combobox(main_frame, textvariable=self.column_var, state="readonly", width=5)
        self.column_dropdown["values"] = tuple(range(1, 11))
        self.column_dropdown.current(1)
        self.column_dropdown.grid(row=0, column=3, padx=10, pady=10, sticky="w")

        confirm_button = ttk.Button(main_frame, text="Confirm", command=self.update_grid)
        confirm_button.grid(row=0, column=4, padx=10, pady=10)

    def update_grid(self):
        rows = int(self.row_var.get())
        columns = int(self.column_var.get())
        grid_program.generate_grid(self.master, rows, columns)  # Update the existing grid

def main():
    root = tk.Tk()
    app = GridGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
