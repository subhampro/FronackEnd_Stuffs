import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk
import os

def convert_to_dds(image_path, output_path, size_option):
    image = Image.open(image_path)
    original_size = image.size
    
    if size_option == "512x512":
        image = image.resize((512, 512), Image.Resampling.LANCZOS)
    elif size_option == "1024x1024":
        image = image.resize((1024, 1024), Image.Resampling.LANCZOS)
    elif size_option == "Custom":
        try:
            width = int(width_entry.get())
            height = int(height_entry.get())
            image = image.resize((width, height), Image.Resampling.LANCZOS)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid dimensions")
            return
    # Original size option will use the image as is
    
    image.save(output_path, format='DDS')

def select_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
    if file_path:
        output_path = filedialog.asksaveasfilename(defaultextension=".dds", filetypes=[("DDS files", "*.dds")])
        if output_path:
            size_option = size_var.get()
            convert_to_dds(file_path, output_path, size_option)
            messagebox.showinfo("Success", "Image converted to DDS format successfully!")

def on_size_change(*args):
    if size_var.get() == "Custom":
        custom_frame.pack(pady=5)
    else:
        custom_frame.pack_forget()

def zoom_image(event, canvas, image, scale_factor):
    global current_scale
    if event.delta > 0:  # Zoom in
        current_scale *= scale_factor
    else:  # Zoom out
        current_scale /= scale_factor
    
    # Apply zoom
    new_size = (int(original_image_size[0] * current_scale), 
                int(original_image_size[1] * current_scale))
    resized_image = image.resize(new_size, Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(resized_image)
    canvas.image = photo
    canvas.config(width=new_size[0], height=new_size[1])
    canvas.create_image(new_size[0]//2, new_size[1]//2, image=photo)

def view_dds():
    global current_scale, original_image_size
    file_path = filedialog.askopenfilename(filetypes=[("DDS files", "*.dds")])
    if file_path:
        try:
            image = Image.open(file_path)
            original_image_size = image.size
            current_scale = 1.0
            
            # Create properties window
            prop_window = tk.Toplevel(root)
            prop_window.title("DDS Viewer")
            prop_window.geometry("800x600")
            
            # Create left panel for image
            left_panel = tk.Frame(prop_window)
            left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            # Create canvas for image display with scrollbars
            canvas_frame = tk.Frame(left_panel)
            canvas_frame.pack(fill=tk.BOTH, expand=True)
            
            canvas = tk.Canvas(canvas_frame, width=600, height=400)
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            # Scrollbars
            v_scrollbar = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL)
            v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            h_scrollbar = tk.Scrollbar(left_panel, orient=tk.HORIZONTAL)
            h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
            
            # Configure scrollbars
            canvas.config(xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)
            v_scrollbar.config(command=canvas.yview)
            h_scrollbar.config(command=canvas.xview)
            
            # Display image
            photo = ImageTk.PhotoImage(image)
            canvas.image = photo
            canvas.create_image(image.size[0]//2, image.size[1]//2, image=photo)
            
            # Bind mouse wheel for zoom
            canvas.bind('<MouseWheel>', lambda e: zoom_image(e, canvas, image, 1.1))
            
            # Create right panel for properties
            right_panel = tk.Frame(prop_window)
            right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=10)
            
            # Properties
            tk.Label(right_panel, text="DDS Properties", font=('Arial', 12, 'bold')).pack(pady=10)
            
            file_size = os.path.getsize(file_path) / 1024
            props = [
                f"Dimensions: {image.size[0]}x{image.size[1]}",
                f"Format: {image.format}",
                f"Mode: {image.mode}",
                f"File Size: {file_size:.2f} KB",
                f"File Path: {file_path}"
            ]
            
            for prop in props:
                tk.Label(right_panel, text=prop, wraplength=200, justify="left").pack(pady=5)
            
            # Zoom controls
            zoom_frame = tk.Frame(right_panel)
            zoom_frame.pack(pady=10)
            tk.Button(zoom_frame, text="Zoom In", command=lambda: zoom_image(type('Event', (), {'delta': 1})(), canvas, image, 1.1)).pack(side=tk.LEFT, padx=5)
            tk.Button(zoom_frame, text="Zoom Out", command=lambda: zoom_image(type('Event', (), {'delta': -1})(), canvas, image, 1.1)).pack(side=tk.LEFT, padx=5)
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not open DDS file: {str(e)}")

# Add these global variables at the top of your script
current_scale = 1.0
original_image_size = (0, 0)

root = tk.Tk()
root.title("Image to DDS Converter")
root.geometry("300x250")

# Size options
size_var = tk.StringVar(value="Original")
size_label = tk.Label(root, text="Output Size:")
size_label.pack(pady=5)

size_options = ttk.Combobox(root, textvariable=size_var, 
                           values=["Original", "512x512", "1024x1024", "Custom"])
size_options.pack(pady=5)
size_var.trace('w', on_size_change)  # Add trace to monitor changes

# Custom size entries
custom_frame = tk.Frame(root)
# Don't pack the frame initially - it will be shown only when Custom is selected

width_label = tk.Label(custom_frame, text="Width:")
width_label.pack(side=tk.LEFT)
width_entry = tk.Entry(custom_frame, width=6)
width_entry.pack(side=tk.LEFT, padx=2)

height_label = tk.Label(custom_frame, text="Height:")
height_label.pack(side=tk.LEFT)
height_entry = tk.Entry(custom_frame, width=6)
height_entry.pack(side=tk.LEFT, padx=2)

# Create button frame for better organization
button_frame = tk.Frame(root)
button_frame.pack(pady=20)

select_button = tk.Button(button_frame, text="Convert to DDS", command=select_image)
select_button.pack(side=tk.LEFT, padx=5)

view_button = tk.Button(button_frame, text="View DDS", command=view_dds)
view_button.pack(side=tk.LEFT, padx=5)

root.mainloop()