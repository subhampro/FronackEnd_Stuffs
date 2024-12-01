import os
from PIL import Image, ImageTk, ImageEnhance, ImageFilter
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import numpy as np

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
        self.preview_image = None
        self.preview_roughness_image = None
        self.setup_gui()

    def setup_gui(self):
        self.window = tk.Tk()
        self.window.title("Image to DDS Converter by SubhaM")
        self.window.geometry("500x400")

        self.generate_heightmap = tk.BooleanVar()
        self.generate_roughness = tk.BooleanVar()

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

        checkbox_frame = ttk.LabelFrame(self.window, text="Additional Maps", padding=5)
        checkbox_frame.pack(fill="x", padx=5, pady=5)

        ttk.Checkbutton(
            checkbox_frame, 
            text="Generate Normal Map",
            variable=self.generate_heightmap
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Checkbutton(
            checkbox_frame, 
            text="Generate Height/Roughness Map",
            variable=self.generate_roughness
        ).pack(side=tk.LEFT, padx=5)

        self.normal_controls_frame = self.create_map_controls("Normal Map Controls", self.update_preview)
        self.roughness_controls_frame = self.create_map_controls("Height/Roughness Map Controls", self.update_roughness_preview)
        
        self.normal_controls_frame.pack_forget()
        self.roughness_controls_frame.pack_forget()

        self.generate_heightmap.trace('w', self.toggle_normal_controls)
        self.generate_roughness.trace('w', self.toggle_roughness_controls)

        self.convert_button = tk.Button(self.window, text="Convert Images", command=self.convert_images)
        self.convert_button.pack(pady=20)

        self.status_label = tk.Label(self.window, text="")
        self.status_label.pack(pady=10)

    def create_map_controls(self, title, preview_callback):
        """Create a control frame with sliders and preview for map generation"""
        control_frame = ttk.LabelFrame(self.window, text=title, padding=5)
        
        preview_canvas = tk.Canvas(control_frame, width=200, height=200)
        preview_canvas.pack(side=tk.RIGHT, padx=5)

        sliders_frame = ttk.Frame(control_frame)
        sliders_frame.pack(side=tk.LEFT, fill="x", expand=True)

        scale_frame = ttk.Frame(sliders_frame)
        scale_frame.pack(fill="x")
        tk.Label(scale_frame, text="Scale:").pack(side=tk.LEFT)
        scale_label = tk.Label(scale_frame, text="100%")
        scale_label.pack(side=tk.RIGHT)
        
        scale_var = tk.DoubleVar(value=100)
        scale_slider = ttk.Scale(
            sliders_frame, from_=0, to=300,
            variable=scale_var,
            command=lambda v: self.update_slider_label(v, scale_label, "%", preview_callback)
        )
        scale_slider.pack(fill="x")

        blur_frame = ttk.Frame(sliders_frame)
        blur_frame.pack(fill="x")
        tk.Label(blur_frame, text="Blur:").pack(side=tk.LEFT)
        blur_label = tk.Label(blur_frame, text="0px")
        blur_label.pack(side=tk.RIGHT)
        
        blur_var = tk.DoubleVar(value=0)
        blur_slider = ttk.Scale(
            sliders_frame, from_=0, to=100,
            variable=blur_var,
            command=lambda v: self.update_slider_label(v, blur_label, "px", preview_callback)
        )
        blur_slider.pack(fill="x")

        detail_ranges = {
            "High": 150,
            "Medium": 150,
            "Low": 150
        }
        
        for detail in detail_ranges:
            frame = ttk.Frame(sliders_frame)
            frame.pack(fill="x")
            tk.Label(frame, text=f"{detail} Detail:").pack(side=tk.LEFT)
            label = tk.Label(frame, text="50%")
            label.pack(side=tk.RIGHT)
            setattr(self, f"{detail.lower()}_label", label)
            
            var = tk.DoubleVar(value=50)
            setattr(self, f"{detail.lower()}_detail_var", var)
            slider = ttk.Scale(
                sliders_frame, from_=0, to=detail_ranges[detail],
                variable=var,
                command=lambda v, l=label: self.update_slider_label(v, l, "%", preview_callback)
            )
            slider.pack(fill="x")

            for item in ['var', 'slider', 'label']:
                setattr(self, f"{title.split()[0].lower()}_{detail.lower()}_{item}", locals()[item])

        setattr(self, f"{title.split()[0].lower()}_preview_canvas", preview_canvas)
        setattr(self, f"{title.split()[0].lower()}_scale_var", scale_var)
        setattr(self, f"{title.split()[0].lower()}_blur_var", blur_var)

        return control_frame

    def toggle_normal_controls(self, *args):
        if self.generate_heightmap.get():
            self.normal_controls_frame.pack(fill="x", padx=5, pady=5)
        else:
            self.normal_controls_frame.pack_forget()

    def toggle_roughness_controls(self, *args):
        if self.generate_roughness.get():
            self.roughness_controls_frame.pack(fill="x", padx=5, pady=5)
        else:
            self.roughness_controls_frame.pack_forget()

    def update_preview(self, *args):
        if not hasattr(self, 'preview_source'):
            return
        
        preview = self.generate_normal_map(self.preview_source)
        preview = preview.resize((200, 200), Image.Resampling.LANCZOS)
        self.preview_image = ImageTk.PhotoImage(preview)
        self.normal_preview_canvas.create_image(100, 100, image=self.preview_image, anchor="center")

    def update_slider_label(self, value, label, unit, callback):
        """Update the label with the current slider value"""
        label.config(text=f"{float(value):.1f}{unit}")
        callback()

    def update_roughness_preview(self, *args):
        if not hasattr(self, 'preview_source'):
            return
        
        preview = self.generate_roughness_map(self.preview_source)
        preview = preview.resize((200, 200), Image.Resampling.LANCZOS)
        self.preview_roughness_image = ImageTk.PhotoImage(preview)
        self.roughness_preview_canvas.create_image(100, 100, image=self.preview_roughness_image, anchor="center")

    def generate_normal_map(self, image):
        gray = image.convert('L')
        
        blur_radius = self.normal_blur_var.get() / 10
        if blur_radius > 0:
            gray = gray.filter(ImageFilter.GaussianBlur(radius=blur_radius))

        height_map = np.array(gray).astype(np.float32) / 255.0

        high = (self.normal_high_var.get() / 100.0) * 1.5
        med = (self.normal_medium_var.get() / 100.0) * 1.5
        low = (self.normal_low_var.get() / 100.0) * 1.5

        scale = (self.normal_scale_var.get() / 100.0) * 3.0

        dy, dx = np.gradient(height_map)
        

        dx = dx * scale
        dy = dy * scale


        z = np.ones_like(dx)
        strength = np.sqrt(dx**2 + dy**2 + z**2)
        
        normal_map = np.stack([
            ((dx / strength) + 1) / 2,
            ((dy / strength) + 1) / 2,
            (z / strength)
        ], axis=-1)
        

        normal_map = (normal_map * 255).astype(np.uint8)
        return Image.fromarray(normal_map, 'RGB')

    def generate_roughness_map(self, image):
        gray = image.convert('L')
        
        blur_radius = self.roughness_blur_var.get() / 10
        if blur_radius > 0:
            gray = gray.filter(ImageFilter.GaussianBlur(radius=blur_radius))

        height_map = np.array(gray).astype(np.float32) / 255.0

        high = (self.roughness_high_var.get() / 100.0) * 1.5
        med = (self.roughness_medium_var.get() / 100.0) * 1.5
        low = (self.roughness_low_var.get() / 100.0) * 1.5

        scale = (self.roughness_scale_var.get() / 100.0) * 3.0

        processed_map = height_map * scale
        processed_map = np.clip(processed_map, 0, 1)
        
        roughness_map = (processed_map * 255).astype(np.uint8)
        return Image.fromarray(roughness_map, 'L')

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

            self.preview_source = Image.open(self.source_file)
            self.update_preview()
            self.update_roughness_preview()

    def select_source_dir(self):
        self.source_dir = filedialog.askdirectory(title="Select Source Directory")
        if self.source_dir:
            self.single_file_mode = False
            self.source_button.config(text=f"Dir: {os.path.basename(self.source_dir)}")
            self.single_file_button.config(text="Select Single File")

    def select_output_dir(self):
        self.output_dir = filedialog.askdirectory(title="Select Output Directory")
        self.output_button.config(text=f"Output: {os.path.basename(self.output_dir)}")

    def generate_height_map(self, image):

        height_map = image.convert('L')
        return height_map

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
                base_name = os.path.splitext(os.path.basename(image_file))[0]
                
                with Image.open(input_path) as img:
                    img = img.convert('RGBA')
                    
                    if selected_dim == "original":
                        resized_img = img
                    else:
                        resized_img = img.resize(selected_dim, Image.Resampling.LANCZOS)
                    
 
                    output_path = os.path.join(self.output_dir, base_name + '.dds')
                    resized_img.save(output_path, "DDS")


                    if self.generate_heightmap.get():
                        height_path = os.path.join(self.output_dir, base_name + '_normal.png')
                        self.generate_normal_map(resized_img).save(height_path)
                        
                    if self.generate_roughness.get():
                        roughness_path = os.path.join(self.output_dir, base_name + '_roughness.png')
                        self.generate_roughness_map(resized_img).save(roughness_path)
                    
                    processed += 1
                    
            except Exception as e:
                messagebox.showerror("Error", f"Error processing {image_file}: {str(e)}")


        status_msg = f"Successfully converted {processed} images to DDS"
        if self.generate_heightmap.get():
            status_msg += " with height maps"
        if self.generate_roughness.get():
            status_msg += " and roughness maps"
        self.status_label.config(text=status_msg + "!")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    converter = ImageConverter()
    converter.run()