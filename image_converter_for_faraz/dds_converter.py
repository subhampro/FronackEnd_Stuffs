import os
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

class ImageConverter:
    def __init__(self):
        self.dimensions = {
            "Original Size": "original",
            "4x4": (4, 4),
            "128x128": (128, 128),
            "289x289": (289, 289),
            "512x512": (512, 512),
            "1024x1024": (1024, 1024),
            "2048x2048": (2048, 2048),
        }
        self.setup_gui()

    def setup_gui(self):
        self.window = tk.Tk()
        self.window.title("Image to DDS Converter by SubhaM")
        self.window.geometry("500x400")


        source_frame = ttk.LabelFrame(self.window, text="Source Selection", padding=5)
        source_frame.pack(fill="x", padx=5, pady=5)

        self.source_button = tk.Button(source_frame, text="Select Directory", command=self.select_source_dir)
        self.source_button.pack(side="left", padx=5)
        
        self.single_file_button = tk.Button(source_frame, text="Select Single File", command=self.select_single_file)
        self.single_file_button.pack(side="left", padx=5)

        tk.Label(self.window, text="Select Output Directory:").pack(pady=5)
        self.output_button = tk.Button(self.window, text="Browse", command=self.select_output_dir)
        self.output_button.pack(pady=5)

        tk.Label(self.window, text="Select Output Dimension:").pack(pady=5)
        self.dim_var = tk.StringVar()
        self.dim_combo = ttk.Combobox(self.window, textvariable=self.dim_var)
        self.dim_combo['values'] = list(self.dimensions.keys())
        self.dim_combo.set("Original Size")
        self.dim_combo.pack(pady=5)

        self.convert_button = tk.Button(self.window, text="Convert Images", command=self.convert_images)
        self.convert_button.pack(pady=20)

        self.status_label = tk.Label(self.window, text="")
        self.status_label.pack(pady=10)

    def select_single_file(self):
        self.source_file = filedialog.askopenfilename(
            title="Select Image File",
            filetypes=(("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff"),)
        )
        if self.source_file:
            self.source_dir = os.path.dirname(self.source_file)
            self.single_file_mode = True
            self.source_button.config(text="Single File Selected")
            self.single_file_button.config(text=f"File: {os.path.basename(self.source_file)}")

    def select_source_dir(self):
        self.source_dir = filedialog.askdirectory(title="Select Source Directory")
        if self.source_dir:
            self.single_file_mode = False
            self.source_button.config(text=f"Dir: {os.path.basename(self.source_dir)}")
            self.single_file_button.config(text="Select Single File")

    def select_output_dir(self):
        self.output_dir = filedialog.askdirectory(title="Select Output Directory")
        self.output_button.config(text=f"Output: {os.path.basename(self.output_dir)}")

    def convert_images(self):
        if not hasattr(self, 'source_dir') or not hasattr(self, 'output_dir'):
            messagebox.showerror("Error", "Please select both source and output locations!")
            return

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        selected_dim = self.dimensions[self.dim_var.get()]
        
        if hasattr(self, 'single_file_mode') and self.single_file_mode:
            image_files = [os.path.basename(self.source_file)]
        else:
            image_files = [f for f in os.listdir(self.source_dir) 
                          if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff'))]

        if not image_files:
            messagebox.showinfo("Info", "No image files found!")
            return

        processed = 0
        for image_file in image_files:
            try:
                input_path = self.source_file if hasattr(self, 'single_file_mode') and self.single_file_mode else os.path.join(self.source_dir, image_file)
                
                with Image.open(input_path) as img:
                    img = img.convert('RGBA')
                    
                    if selected_dim == "original":
                        resized_img = img
                    else:
                        resized_img = img.resize(selected_dim, Image.Resampling.LANCZOS)
                    
                    output_path = os.path.join(self.output_dir, 
                                             os.path.splitext(os.path.basename(image_file))[0] + '.dds')
                    resized_img.save(output_path, "DDS")
                    processed += 1
                    
            except Exception as e:
                messagebox.showerror("Error", f"Error processing {image_file}: {str(e)}")

        self.status_label.config(text=f"Successfully converted {processed} images!")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    converter = ImageConverter()
    converter.run()