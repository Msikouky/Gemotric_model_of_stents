import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk

class InterfaceUtilisateur:
    def __init__(self, root):
        self.root = root
        self.root.title("Stent sampler")

        # Set window size and position it in the center of the screen
        window_width = 400
        window_height = 300  # Increased height to accommodate new widgets
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        # Load the logo image
        self.logo_image = Image.open('logo_UCA.png')  # Replace with the actual path to your logo file
        self.logo_image = self.logo_image.resize((50, 50), Image.Resampling.LANCZOS)
        self.logo_photoimage = ImageTk.PhotoImage(self.logo_image)

        # Place the logo
        self.logo_label = tk.Label(self.root, image=self.logo_photoimage, bg='#ffffff')
        self.logo_label.image = self.logo_photoimage
        self.logo_label.place(x=10, y=10)

        # Use ttk for styling
        style = ttk.Style()
        style.configure('TButton', font=('Helvetica', 11), padding=6)
        style.configure('TLabel', font=('Helvetica', 11), background='#f0f0f0')

        # Set a background color
        self.root.configure(bg='#ffffff')

        # Buttons
        self.bouton_selection = ttk.Button(root, text="Select a SVG file", command=self.open_file)
        self.bouton_selection.pack(padx=20, pady=20)

        # Dropdown for selecting the sampler
        self.sampler_selection = ttk.Combobox(root, values=["Equidistant Sampler", "Curvature Sampler"])
        self.sampler_selection.set("Select Sampler")  # default value
        self.sampler_selection.pack(padx=20, pady=10)

        # Label for the plot number entry
        self.plot_number_label = ttk.Label(root, text="Choose the total number of points:", background='#ffffff')
        self.plot_number_label.pack(padx=20, pady=5)

        # Entry for inputting the number for plot_shape
        self.plot_number_entry = ttk.Entry(root, text="Choose the total number of points:")
        self.plot_number_entry.pack(padx=20, pady=10)

        self.launch_button = ttk.Button(root, text="Launch Program", command=self.launch_program)
        self.launch_button.pack(padx=20, pady=15)

        # Label to display the selected file name
        self.selected_file_label = ttk.Label(root, text="", background='#ffffff')
        self.selected_file_label.pack(padx=20, pady=5)

        self.file_path = None

    def open_file(self):
        initial_directory = "../"
        self.file_path = filedialog.askopenfilename(initialdir=initial_directory, filetypes=[("Fichiers SVG", "*.svg")])
        if self.file_path:
            print(f'The SVG file path is: {self.file_path}')
            self.selected_file_label.config(text=f"Selected File: {self.file_path.split('/')[-1]}")  # Displays only the file name
        else:
            messagebox.showwarning("Warning", "You did not select a file")

    def launch_program(self):
        if self.file_path and self.sampler_selection.get() != "Select Sampler" and self.plot_number_entry.get().isdigit():
            self.sampler_type = self.sampler_selection.get()
            self.plot_number = int(self.plot_number_entry.get())

            # Add additional code to handle the launch with the selected sampler and plot number
            print(f"Launching program with {self.sampler_type} and plot shape number: {self.plot_number}")
            self.root.destroy()
        else:
            messagebox.showwarning("Warning", "Please select a file, sampler, and enter a valid number for plot shape")

    def get_file_path(self):
        return self.file_path

    def get_sampler_type(self):
        return getattr(self, 'sampler_type', None)

    def get_plot_number(self):
        return getattr(self, 'plot_number', None)

