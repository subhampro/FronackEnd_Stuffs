import os
from PIL import Image, ImageTk, ImageEnhance, ImageFilter
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, simpledialog
import numpy as np
from lib import initialize
import struct
import io
import signal
import sys
import uuid
import json
import requests
from pathlib import Path
import platform
import datetime
import hashlib
import winreg
import base64
import win32api
import win32security

class PreviewWindow:
    def __init__(self, parent, title):
        self.window = tk.Toplevel(parent)
        self.window.title(title)
        self.window.geometry("800x600")
        
        self.preview_frame = ttk.Frame(self.window)
        self.preview_frame.pack(expand=True, fill="both", side=tk.LEFT)
        
        self.preview_canvas = tk.Canvas(self.preview_frame, width=600, height=600)
        self.preview_canvas.pack(expand=True, fill="both", padx=10, pady=10)
        
        self.controls_frame = ttk.Frame(self.window)
        self.controls_frame.pack(fill="y", side=tk.RIGHT, padx=10, pady=10)
        
        self.zoom_frame = ttk.LabelFrame(self.controls_frame, text="Zoom")
        self.zoom_frame.pack(fill="x", pady=5)
        
        self.zoom_var = tk.DoubleVar(value=1.0)
        self.zoom_label = ttk.Label(self.zoom_frame, text="100%")
        self.zoom_label.pack()
        
        self.zoom_slider = ttk.Scale(
            self.zoom_frame, 
            from_=0.1, 
            to=2.0, 
            variable=self.zoom_var,
            command=self.on_zoom_change
        )
        self.zoom_slider.pack(fill="x")
        
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        self.is_active = True
        
    def on_close(self):
        self.is_active = False
        self.window.withdraw()
    
    def on_zoom_change(self, value):
        zoom = float(value)
        self.zoom_label.config(text=f"{int(zoom * 100)}%")
        if hasattr(self, 'update_callback'):
            self.update_callback()
    
    def set_update_callback(self, callback):
        self.update_callback = callback
        
    def update_preview(self, image):
        if not self.is_active:
            return
            
        if image:
            zoom = self.zoom_var.get()
            orig_size = image.size
            new_size = (int(orig_size[0] * zoom), int(orig_size[1] * zoom))
            zoomed = image.resize(new_size, Image.Resampling.LANCZOS)
            
            self.preview_image = ImageTk.PhotoImage(zoomed)
            
            self.preview_canvas.config(width=new_size[0], height=new_size[1])
            self.preview_canvas.create_image(
                new_size[0]//2, 
                new_size[1]//2, 
                image=self.preview_image, 
                anchor="center"
            )

    def show(self):
        self.is_active = True
        self.window.deiconify()
        
    def hide(self):
        self.is_active = False
        self.window.withdraw()

class DDSViewer(PreviewWindow):
    def __init__(self, parent):
        super().__init__(parent, "DDS Viewer")
        self.window.geometry("1024x768")
        
        self.fullscreen = False
        self.fullscreen_btn = ttk.Button(
            self.controls_frame,
            text="Toggle Fullscreen",
            command=self.toggle_fullscreen
        )
        self.fullscreen_btn.pack(fill="x", pady=5)
        
        self.window.bind('<Escape>', lambda e: self.exit_fullscreen())
    
    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        self.window.attributes('-fullscreen', self.fullscreen)
    
    def exit_fullscreen(self):
        self.fullscreen = False
        self.window.attributes('-fullscreen', False)

class UsageTracker:
    def __init__(self):
        self.api_url = 'https://wordpress.atz.li/pro_dds_tool_tracker/track.php'  
        self.user_id = self.get_machine_id()
        
    def get_machine_id(self):
        """Generate a unique machine ID that persists across runs"""
        try:
            system_info = f"{platform.node()}-{platform.machine()}-{platform.processor()}"
            machine_id = hashlib.md5(system_info.encode()).hexdigest()
            return machine_id
        except:
            return hashlib.md5(os.urandom(32)).hexdigest()
            
    def track_usage(self, event_type='start'):
        """Track usage with retry mechanism"""
        try:
            data = {
                'user_id': self.user_id,
                'event': event_type,
                'system': platform.system(),
                'version': '1.0.0',  
                'timestamp': datetime.datetime.now().isoformat()
            }
            
            for _ in range(3):
                try:
                    response = requests.post(
                        self.api_url, 
                        json=data, 
                        timeout=2,
                        headers={'User-Agent': 'DDS-Converter/1.0'}
                    )
                    if response.status_code == 200:
                        return True
                except:
                    continue
        except:
            pass
        return False

class LicenseManager:
    def __init__(self):
        self.api_url = 'https://wordpress.atz.li/pro_dds_tool_tracker/'
        self.registry_key = r'Software\DDSConverter'
        self.machine_id = self.get_secure_machine_id()
        
    def get_secure_machine_id(self):
        """Generate a tamper-proof machine ID"""
        try:
            # Get hardware info
            cpu_id = win32api.GetSystemFirmwareTable('RSMB', 0)
            hdd_serial = win32api.GetVolumeInformation("C:\\")[1]
            
            # Get system security identifiers
            sid = win32security.GetTokenInformation(
                win32security.OpenProcessToken(win32api.GetCurrentProcess(), win32security.TOKEN_QUERY),
                win32security.TokenUser
            )[0]
            
            # Combine and hash
            system_info = f"{cpu_id}-{hdd_serial}-{sid}"
            return hashlib.sha256(system_info.encode()).hexdigest()
        except:
            return None
            
    def check_license(self):
        """Check license status"""
        try:
            # Try to read existing license info
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, self.registry_key)
            stored_data = winreg.QueryValueEx(key, "license_data")[0]
            license_data = json.loads(base64.b64decode(stored_data))
            
            # Verify license with server
            response = requests.post(
                f"{self.api_url}verify_license.php",
                json={
                    'machine_id': self.machine_id,
                    'license_key': license_data.get('key'),
                    'install_date': license_data.get('installed')
                },
                headers={'User-Agent': 'DDS-Converter/1.0'}
            )
            
            if response.status_code == 200:
                result = response.json()
                if result['status'] == 'valid':
                    return True, None
                return False, result['message']
            
            return False, "Failed to verify license"
            
        except FileNotFoundError:
            # First time run - start trial
            self.start_trial()
            return True, None
        except Exception as e:
            return False, str(e)
    
    def start_trial(self):
        """Initialize trial period"""
        install_date = datetime.datetime.now().isoformat()
        
        # Save trial info
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, self.registry_key)
        license_data = {
            'type': 'trial',
            'machine_id': self.machine_id,
            'installed': install_date
        }
        encoded_data = base64.b64encode(json.dumps(license_data).encode()).decode()
        winreg.SetValueEx(key, "license_data", 0, winreg.REG_SZ, encoded_data)
        
        # Register trial with server
        requests.post(
            f"{self.api_url}register_trial.php",
            json={
                'machine_id': self.machine_id,
                'install_date': install_date
            },
            headers={'User-Agent': 'DDS-Converter/1.0'}
        )
    
    def activate_license(self, license_key):
        """Activate a license key"""
        try:
            response = requests.post(
                f"{self.api_url}activate_license.php",
                json={
                    'machine_id': self.machine_id,
                    'license_key': license_key
                },
                headers={'User-Agent': 'DDS-Converter/1.0'}
            )
            
            if response.status_code == 200:
                result = response.json()
                if result['status'] == 'success':
                    # Save activated license
                    key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, self.registry_key)
                    license_data = {
                        'type': 'full',
                        'key': license_key,
                        'machine_id': self.machine_id,
                        'activated': datetime.datetime.now().isoformat()
                    }
                    encoded_data = base64.b64encode(json.dumps(license_data).encode()).decode()
                    winreg.SetValueEx(key, "license_data", 0, winreg.REG_SZ, encoded_data)
                    return True, "License activated successfully"
                    
                return False, result['message']
            
            return False, "Failed to activate license"
            
        except Exception as e:
            return False, str(e)

class ImageConverter:
    def __init__(self):
        self.license_manager = LicenseManager()
        is_licensed, message = self.license_manager.check_license()
        
        if not is_licensed:
            root = tk.Tk()
            root.withdraw()
            
            if messagebox.showerror("License Required", 
                f"{message}\n\nPlease enter your license key or contact support.",
                type=messagebox.OKCANCEL) == messagebox.OK:
                
                license_key = simpledialog.askstring("License Activation", 
                    "Please enter your license key:")
                
                if license_key:
                    success, msg = self.license_manager.activate_license(license_key)
                    if not success:
                        messagebox.showerror("Activation Failed", msg)
                        sys.exit(1)
                else:
                    sys.exit(1)
            else:
                sys.exit(1)
        
        self.tracker = UsageTracker()
        self.tracker.track_usage('start')
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        self.version = '1.0.0'
        
        self.NORMAL_DEFAULTS = {
            'blur': 0,
            'scale': 300,
            'high': 100,
            'medium': 100,
            'low': 100
        }
        
        self.ROUGHNESS_DEFAULTS = {
            'blur': 0,
            'detail_scale': 100,
            'low': 50,
            'medium': 50,
            'high': 50,
            'bump': 10
        }
        self.dimensions = {
            "Original Size": "original",
            "Custom Size": "custom",
            "4x4": (4, 4),
            "128x128": (128, 128),
            "289x289": (289, 289),
            "512x512": (512, 512),
            "1024x1024": (1024, 1024),
            "2048x2048": (2048, 2048),
        }
        self.compression_options = {
            "No Compression": {"format": "RGBA", "block_size": 32},
            "8x | BC1": {"format": "BC1", "block_size": 4},
            "4x | BC3": {"format": "BC3", "block_size": 8},
            "4x | BC7": {"format": "BC7", "block_size": 8}
        }
        self.preview_image = None
        self.preview_roughness_image = None
        self.normal_preview_window = None
        self.roughness_preview_window = None
        self.dds_viewer = None
        self.setup_gui()

    def signal_handler(self, sig, frame):
        """Handle Ctrl+C and other termination signals"""
        print("\nClosing application gracefully...")
        if hasattr(self, 'window'):
            self.window.quit()
            self.window.destroy()
        sys.exit(0)

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

        self.view_dds_button = tk.Button(source_frame, text="View DDS File", command=self.open_dds_viewer)
        self.view_dds_button.pack(side="left", padx=5)

        tk.Label(self.window, text="Select Output Directory:").pack(pady=5)
        self.output_button = tk.Button(self.window, text="Browse", command=self.select_output_dir)
        self.output_button.pack(pady=5)

        tk.Label(self.window, text="Select Output Dimension:").pack(pady=5)
        self.dim_var = tk.StringVar()
        self.dim_combo = ttk.Combobox(self.window, textvariable=self.dim_var)
        self.dim_combo['values'] = list(self.dimensions.keys())
        self.dim_combo.set("Original Size")
        self.dim_combo.pack(pady=5)
        
        self.custom_dim_frame = ttk.Frame(self.window)
        tk.Label(self.custom_dim_frame, text="Width:").pack(side=tk.LEFT, padx=5)
        self.custom_width = ttk.Entry(self.custom_dim_frame, width=6)
        self.custom_width.pack(side=tk.LEFT, padx=5)
        
        tk.Label(self.custom_dim_frame, text="Height:").pack(side=tk.LEFT, padx=5)
        self.custom_height = ttk.Entry(self.custom_dim_frame, width=6)
        self.custom_height.pack(side=tk.LEFT, padx=5)
        
        self.dim_combo.bind('<<ComboboxSelected>>', self.on_dimension_change)

        tk.Label(self.window, text="Select Compression:").pack(pady=5)
        self.compression_var = tk.StringVar()
        self.compression_combo = ttk.Combobox(self.window, textvariable=self.compression_var)
        self.compression_combo['values'] = list(self.compression_options.keys())
        self.compression_combo.set("No Compression")
        self.compression_combo.pack(pady=5)

        checkbox_frame = ttk.LabelFrame(self.window, text="Additional Maps", padding=5)
        checkbox_frame.pack(fill="x", padx=5, pady=5)

        ttk.Checkbutton(
            checkbox_frame, 
            text="Generate Normal Map",
            variable=self.generate_heightmap
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Checkbutton(
            checkbox_frame, 
            text="Generate Specular Map",
            variable=self.generate_roughness
        ).pack(side=tk.LEFT, padx=5)

        self.normal_controls_frame = self.create_map_controls("Normal Map Controls", self.update_preview)
        self.roughness_controls_frame = self.create_roughness_controls("Speculer Map", self.update_roughness_preview)
        
        self.normal_controls_frame.pack_forget()
        self.roughness_controls_frame.pack_forget()

        self.generate_heightmap.trace('w', self.toggle_normal_controls)
        self.generate_roughness.trace('w', self.toggle_roughness_controls)

        self.convert_button = tk.Button(self.window, text="Convert Images", command=self.convert_images)
        self.convert_button.pack(pady=20)

        self.status_label = tk.Label(self.window, text="")
        self.status_label.pack(pady=10)

    def create_map_controls(self, title, preview_callback):
        prefix = title.split()[0].lower()
        if prefix == "height/roughness":
            return self.create_roughness_controls(title, preview_callback)
        elif prefix == "normal":

            control_frame = ttk.LabelFrame(self.window, text=title, padding=5)
            
            reset_button = tk.Button(
                control_frame, 
                text="Reset to Default", 
                command=self.reset_normal_values
            )
            reset_button.pack(fill="x", padx=5, pady=5)
            
            preview_canvas = tk.Canvas(control_frame, width=200, height=200)
            preview_canvas.pack(side=tk.RIGHT, padx=5)

            sliders_frame = ttk.Frame(control_frame)
            sliders_frame.pack(side=tk.LEFT, fill="x", expand=True)


            scale_frame = ttk.Frame(sliders_frame)
            scale_frame.pack(fill="x")
            tk.Label(scale_frame, text="Scale:").pack(side=tk.LEFT)
            scale_label = tk.Label(scale_frame, text="100%")
            scale_label.pack(side=tk.RIGHT)
            
            scale_var = tk.DoubleVar(value=self.NORMAL_DEFAULTS['scale'])
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
            
            blur_var = tk.DoubleVar(value=self.NORMAL_DEFAULTS['blur'])
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
                
                var = tk.DoubleVar(value=self.NORMAL_DEFAULTS[detail.lower()])
                setattr(self, f"normal_{detail.lower()}_var", var)
                slider = ttk.Scale(
                    sliders_frame, from_=0, to=detail_ranges[detail],
                    variable=var,
                    command=lambda v, l=label: self.update_slider_label(v, l, "%", preview_callback)
                )
                slider.pack(fill="x")


            setattr(self, "normal_preview_canvas", preview_canvas)
            setattr(self, "normal_scale_var", scale_var)
            setattr(self, "normal_blur_var", blur_var)

            return control_frame

    def create_roughness_controls(self, title, preview_callback):
        """Create roughness specific controls"""
        control_frame = ttk.LabelFrame(self.window, text=title, padding=5)
        
        reset_button = tk.Button(
            control_frame, 
            text="Reset to Default", 
            command=self.reset_roughness_values
        )
        reset_button.pack(fill="x", padx=5, pady=5)

        preview_canvas = tk.Canvas(control_frame, width=200, height=200)
        preview_canvas.pack(side=tk.RIGHT, padx=5)


        controls_frame = ttk.Frame(control_frame)
        controls_frame.pack(side=tk.LEFT, fill="x", expand=True)


        blur_frame = ttk.Frame(controls_frame)
        blur_frame.pack(fill="x")
        tk.Label(blur_frame, text="Blur:").pack(side=tk.LEFT)
        blur_label = tk.Label(blur_frame, text="0px")
        blur_label.pack(side=tk.RIGHT)
        
        blur_var = tk.DoubleVar(value=self.ROUGHNESS_DEFAULTS['blur'])
        ttk.Scale(
            controls_frame, from_=0, to=100,
            variable=blur_var,
            command=lambda v: self.update_slider_label(v, blur_label, "px", preview_callback)
        ).pack(fill="x")


        scale_frame = ttk.Frame(controls_frame)
        scale_frame.pack(fill="x")
        tk.Label(scale_frame, text="Detail Scale:").pack(side=tk.LEFT)
        scale_label = tk.Label(scale_frame, text="50%")
        scale_label.pack(side=tk.RIGHT)
        
        detail_scale_var = tk.DoubleVar(value=self.ROUGHNESS_DEFAULTS['detail_scale'])
        ttk.Scale(
            controls_frame, from_=0, to=150,
            variable=detail_scale_var,
            command=lambda v: self.update_slider_label(v, scale_label, "%", preview_callback)
        ).pack(fill="x")


        contrast_frame = ttk.LabelFrame(controls_frame, text="Contrast Details", padding=5)
        contrast_frame.pack(fill="x", pady=5)
        
        contrast_vars = {}
        for level in ["Low", "Medium", "High"]:
            frame = ttk.Frame(contrast_frame)
            frame.pack(fill="x")
            tk.Label(frame, text=f"{level}:").pack(side=tk.LEFT)
            label = tk.Label(frame, text="50%")
            label.pack(side=tk.RIGHT)
            
            var = tk.DoubleVar(value=self.ROUGHNESS_DEFAULTS[level.lower()])
            contrast_vars[level.lower()] = var
            ttk.Scale(
                contrast_frame, from_=0, to=100,
                variable=var,
                command=lambda v, l=label: self.update_slider_label(v, l, "%", preview_callback)
            ).pack(fill="x")


        material_frame = ttk.LabelFrame(controls_frame, text="Material Preview", padding=5)
        material_frame.pack(fill="x", pady=5)
        
        bump_frame = ttk.Frame(material_frame)
        bump_frame.pack(fill="x")
        tk.Label(bump_frame, text="Bump:").pack(side=tk.LEFT)
        bump_label = tk.Label(bump_frame, text="50%")
        bump_label.pack(side=tk.RIGHT)
        
        bump_var = tk.DoubleVar(value=self.ROUGHNESS_DEFAULTS['bump'])
        ttk.Scale(
            material_frame, from_=0, to=100,
            variable=bump_var,
            command=lambda v: self.update_slider_label(v, bump_label, "%", preview_callback)
        ).pack(fill="x")


        tiling_frame = ttk.LabelFrame(controls_frame, text="Tiling and Offset", padding=5)
        tiling_frame.pack(fill="x", pady=5)
        

        tile_frame = ttk.Frame(tiling_frame)
        tile_frame.pack(fill="x")
        tk.Label(tile_frame, text="Tile U/X:").pack(side=tk.LEFT)
        tile_u = ttk.Entry(tile_frame, width=8)
        tile_u.pack(side=tk.LEFT, padx=5)
        tile_u.insert(0, "1.0")
        
        tk.Label(tile_frame, text="V/Y:").pack(side=tk.LEFT)
        tile_v = ttk.Entry(tile_frame, width=8)
        tile_v.pack(side=tk.LEFT, padx=5)
        tile_v.insert(0, "1.0")


        offset_frame = ttk.Frame(tiling_frame)
        offset_frame.pack(fill="x", pady=2)
        tk.Label(offset_frame, text="Offset U/X:").pack(side=tk.LEFT)
        offset_u = ttk.Entry(offset_frame, width=8)
        offset_u.pack(side=tk.LEFT, padx=5)
        offset_u.insert(0, "0.0")
        
        tk.Label(offset_frame, text="V/Y:").pack(side=tk.LEFT)
        offset_v = ttk.Entry(offset_frame, width=8)
        offset_v.pack(side=tk.LEFT, padx=5)
        offset_v.insert(0, "0.0")


        setattr(self, "roughness_preview_canvas", preview_canvas)
        setattr(self, "roughness_blur_var", blur_var)
        setattr(self, "roughness_detail_scale_var", detail_scale_var)
        setattr(self, "roughness_bump_var", bump_var)
        
        for level, var in contrast_vars.items():
            setattr(self, f"roughness_{level}_contrast_var", var)
        
        setattr(self, "roughness_tile_u", tile_u)
        setattr(self, "roughness_tile_v", tile_v)
        setattr(self, "roughness_offset_u", offset_u)
        setattr(self, "roughness_offset_v", offset_v)

        return control_frame

    def toggle_normal_controls(self, *args):
        if self.generate_heightmap.get():
            self.normal_controls_frame.pack(fill="x", padx=5, pady=5)
            
            if not self.normal_preview_window or not self.normal_preview_window.is_active:
                self.normal_preview_window = PreviewWindow(self.window, "Normal Map Preview")
                self.normal_preview_window.set_update_callback(self.update_preview)
            
            self.normal_preview_window.show()
            self.update_preview()
        else:
            self.normal_controls_frame.pack_forget()
            if self.normal_preview_window:
                self.normal_preview_window.hide()

    def toggle_roughness_controls(self, *args):
        if self.generate_roughness.get():
            self.roughness_controls_frame.pack(fill="x", padx=5, pady=5)
            
            if not self.roughness_preview_window or not self.roughness_preview_window.is_active:
                self.roughness_preview_window = PreviewWindow(self.window, "Roughness Map Preview")
                self.roughness_preview_window.set_update_callback(self.update_roughness_preview)
            
            self.roughness_preview_window.show()
            self.update_roughness_preview()
        else:
            self.roughness_controls_frame.pack_forget()
            if self.roughness_preview_window:
                self.roughness_preview_window.hide()

    def update_preview(self, *args):
        if not hasattr(self, 'preview_source'):
            return
            
        preview = self.generate_normal_map(self.preview_source)
        
        if hasattr(self, 'normal_preview_canvas'):
            small_preview = preview.resize((200, 200), Image.Resampling.LANCZOS)
            self.preview_image = ImageTk.PhotoImage(small_preview)
            self.normal_preview_canvas.create_image(100, 100, image=self.preview_image, anchor="center")
        
        if self.normal_preview_window and self.normal_preview_window.is_active:
            self.normal_preview_window.update_preview(preview)

    def update_slider_label(self, value, label, unit, callback):
        """Update the label with the current slider value"""
        label.config(text=f"{float(value):.1f}{unit}")
        callback()

    def update_roughness_preview(self, *args):
        if not hasattr(self, 'preview_source'):
            return
            
        preview = self.generate_roughness_map(self.preview_source)
        
        if hasattr(self, 'roughness_preview_canvas'):
            small_preview = preview.resize((200, 200), Image.Resampling.LANCZOS)
            self.preview_roughness_image = ImageTk.PhotoImage(small_preview)
            self.roughness_preview_canvas.create_image(100, 100, image=self.preview_roughness_image, anchor="center")
        
        if self.roughness_preview_window and self.roughness_preview_window.is_active:
            self.roughness_preview_window.update_preview(preview)

    def generate_normal_map(self, image):
        gray = image.convert('L')
        
        blur_radius = self.normal_blur_var.get() / 10
        if (blur_radius > 0):
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


        detail_scale = self.roughness_detail_scale_var.get() / 100.0 * 1.5
        height_map *= detail_scale


        low = self.roughness_low_contrast_var.get() / 100.0
        med = self.roughness_medium_contrast_var.get() / 100.0
        high = self.roughness_high_contrast_var.get() / 100.0
        

        height_map = (height_map * high + height_map * med + height_map * low) / 3

 
        try:
            tile_u = float(self.roughness_tile_u.get())
            tile_v = float(self.roughness_tile_v.get())
            offset_u = float(self.roughness_offset_u.get())
            offset_v = float(self.roughness_offset_v.get())
            
            height, width = height_map.shape
            
            y, x = np.mgrid[0:height, 0:width]
            
            x = (x / width * tile_u + offset_u) % 1
            y = (y / height * tile_v + offset_v) % 1
            
            x = (x * width).astype(np.int32)
            y = (y * height).astype(np.int32)
            
            height_map = height_map[y, x]
            
        except ValueError:
            pass  

        processed_map = np.clip(height_map, 0, 1)
        roughness_map = (processed_map * 255).astype(np.uint8)
        return Image.fromarray(roughness_map, 'L')

    def select_single_file(self):
        self.source_file = filedialog.askopenfilename(
            title="Select Image File",
            filetypes=(("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff *.webp"),)
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

    def create_dds_header(self, width, height, format_type):
        """Create a DDS header with specific format"""
        header = bytearray(128)
        
        header[0:4] = b'DDS '
        
        header[4:8] = struct.pack('<I', 124)
        
        flags = 0x1 | 0x2 | 0x4 | 0x1000 
        header[8:12] = struct.pack('<I', flags)

        header[12:16] = struct.pack('<I', height)
        header[16:20] = struct.pack('<I', width)
        

        if format_type == "BC1":
            pixel_flags = 0x4  
            four_cc = b'DXT1'
            rgb_bit_count = 0
            r_mask = 0
            g_mask = 0
            b_mask = 0
            a_mask = 0
        elif format_type == "BC3":
            pixel_flags = 0x4  
            four_cc = b'DXT5'
            rgb_bit_count = 0
            r_mask = 0
            g_mask = 0
            b_mask = 0
            a_mask = 0
        elif format_type == "BC7":
            pixel_flags = 0x4  
            four_cc = b'DX10'
            rgb_bit_count = 0
            r_mask = 0
            g_mask = 0
            b_mask = 0
            a_mask = 0
        else: 
            pixel_flags = 0x41  
            four_cc = b'\0\0\0\0'
            rgb_bit_count = 32
            r_mask = 0x000000ff
            g_mask = 0x0000ff00
            b_mask = 0x00ff0000
            a_mask = 0xff000000

        header[76:80] = struct.pack('<I', pixel_flags)
        header[80:84] = four_cc
        header[88:92] = struct.pack('<I', rgb_bit_count)
        header[92:96] = struct.pack('<I', r_mask)
        header[96:100] = struct.pack('<I', g_mask)
        header[100:104] = struct.pack('<I', b_mask)
        header[104:108] = struct.pack('<I', a_mask)
        
        return header

    def apply_compression(self, img, compression_settings):
        """Apply compression and create DDS file with proper format"""
        img_array = np.array(img)
        height, width = img_array.shape[:2]
        format_type = compression_settings["format"]
        block_size = compression_settings["block_size"]
        
        new_height = ((height + 3) // 4) * 4
        new_width = ((width + 3) // 4) * 4
        
        if new_height != height or new_width != width:
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            img_array = np.array(img)
        
        header = self.create_dds_header(new_width, new_height, format_type)
        
        if format_type == "BC1":
            compressed = self.compress_bc1(img_array)
        elif format_type == "BC3":
            compressed = self.compress_bc3(img_array)
        elif format_type == "BC7":
            compressed = self.compress_bc7(img_array)
        else:
            compressed = img_array.tobytes()
        
        dds_data = header + compressed
        
        return dds_data

    def compress_bc1(self, img_array):
        """BC1 compression (RGB only, 1-bit alpha)"""
        height, width = img_array.shape[:2]
        block_size = 8  
        compressed = bytearray((width * height * block_size) // 16)
        
        for y in range(0, height, 4):
            for x in range(0, width, 4):
                block = img_array[y:y+4, x:x+4]
                avg_color = np.mean(block, axis=(0,1))
                idx = ((y * width) + x) // 2
                compressed[idx:idx+8] = struct.pack('<2I', 
                    int(avg_color[0]) | (int(avg_color[1]) << 8) | (int(avg_color[2]) << 16),
                    0xFFFF0000
                )
        
        return compressed

    def compress_bc3(self, img_array):
        """BC3 compression (RGB + alpha)"""
        height, width = img_array.shape[:2]
        block_size = 16 
        compressed = bytearray((width * height * block_size) // 16)
        
        for y in range(0, height, 4):
            for x in range(0, width, 4):
                block = img_array[y:y+4, x:x+4]
                avg_color = np.mean(block, axis=(0,1))
                idx = ((y * width) + x)
                compressed[idx:idx+16] = struct.pack('<4I',
                    255,
                    0,    
                    int(avg_color[0]) | (int(avg_color[1]) << 8) | (int(avg_color[2]) << 16),
                    0xFFFF0000  
                )
        
        return compressed

    def compress_bc7(self, img_array):
        """BC7 compression (High quality RGB + alpha)"""
        height, width = img_array.shape[:2]
        block_size = 16  
        compressed = bytearray((width * height * block_size) // 16)
        
        for y in range(0, height, 4):
            for x in range(0, width, 4):
                block = img_array[y:y+4, x:x+4]
                avg_color = np.mean(block, axis=(0,1))
                idx = ((y * width) + x)
                compressed[idx:idx+16] = struct.pack('<4I',
                    int(avg_color[0]) | (int(avg_color[1]) << 8) | (int(avg_color[2]) << 16) | (255 << 24),
                    0xFFFFFFFF,
                    0xFFFFFFFF,
                    0xFFFFFFFF
                )
        
        return compressed

    def convert_images(self):
        self.tracker.track_usage('conversion')
        if not hasattr(self, 'source_dir') or not hasattr(self, 'output_dir'):
            messagebox.showerror("Error", "Please select both source and output locations!")
            return

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        selected_dim = self.dimensions[self.dim_var.get()]
        
        if selected_dim == "custom":
            try:
                width = int(self.custom_width.get())
                height = int(self.custom_height.get())
                if width <= 0 or height <= 0:
                    raise ValueError("Dimensions must be positive numbers")
                selected_dim = (width, height)
            except ValueError as e:
                messagebox.showerror("Error", "Please enter valid dimensions!")
                return
        
        if hasattr(self, 'single_file_mode') and self.single_file_mode:
            image_files = [os.path.basename(self.source_file)]
        else:
            image_files = [f for f in os.listdir(self.source_dir) 
                          if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp'))]

        if not image_files:
            messagebox.showinfo("Info", "No image files found!")
            return

        compression_settings = self.compression_options[self.compression_var.get()]
        
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
                    
                   
                    dds_data = self.apply_compression(resized_img, compression_settings)
                    
                    
                    output_path = os.path.join(self.output_dir, base_name + '.dds')
                    with open(output_path, 'wb') as f:
                        f.write(dds_data)

                    if self.generate_heightmap.get():
                        height_path = os.path.join(self.output_dir, base_name + '_normal.dds')
                        normal_map = self.generate_normal_map(resized_img)
                        normal_map.save(height_path, "DDS")

                    if self.generate_roughness.get():
                        roughness_path = os.path.join(self.output_dir, base_name + '_roughness.dds')
                        roughness_map = self.generate_roughness_map(resized_img)
                        roughness_map.save(roughness_path, "DDS")

                    processed += 1
                    
            except Exception as e:
                messagebox.showerror("Error", f"Error processing {image_file}: {str(e)}")

        status_msg = f"Successfully converted {processed} images to DDS"
        if self.generate_heightmap.get():
            status_msg += " with height maps"
        if self.generate_roughness.get():
            status_msg += " and roughness maps"
        self.status_label.config(text=status_msg + "!")

    def reset_normal_values(self):
        """Reset all Normal Map controls to their default values"""
        self.normal_scale_var.set(self.NORMAL_DEFAULTS['scale'])
        self.normal_blur_var.set(self.NORMAL_DEFAULTS['blur'])
        self.normal_high_var.set(self.NORMAL_DEFAULTS['high'])
        self.normal_medium_var.set(self.NORMAL_DEFAULTS['medium'])
        self.normal_low_var.set(self.NORMAL_DEFAULTS['low'])
        self.update_preview()

    def reset_roughness_values(self):
        """Reset all Roughness Map controls to their default values"""
        self.roughness_blur_var.set(self.ROUGHNESS_DEFAULTS['blur'])
        self.roughness_detail_scale_var.set(self.ROUGHNESS_DEFAULTS['detail_scale'])
        self.roughness_low_contrast_var.set(self.ROUGHNESS_DEFAULTS['low'])
        self.roughness_medium_contrast_var.set(self.ROUGHNESS_DEFAULTS['medium'])
        self.roughness_high_contrast_var.set(self.ROUGHNESS_DEFAULTS['high'])
        self.roughness_bump_var.set(self.ROUGHNESS_DEFAULTS['bump'])
        self.update_roughness_preview()

    def on_dimension_change(self, event=None):
        if self.dim_var.get() == "Custom Size":
            self.custom_dim_frame.pack(pady=5)
        else:
            self.custom_dim_frame.pack_forget()

    def read_dds_file(self, dds_file):
        """Custom DDS file reader"""
        with open(dds_file, 'rb') as f:
            header = f.read(128)
            if not header.startswith(b'DDS '):
                raise ValueError("Not a valid DDS file")
                
            height = struct.unpack('<I', header[12:16])[0]
            width = struct.unpack('<I', header[16:20])[0]
            
            flags = struct.unpack('<I', header[76:80])[0]
            fourcc = header[80:84]
            
            pixel_data = f.read()
            
            if fourcc == b'DXT1':
                img_array = np.frombuffer(pixel_data, dtype=np.uint8)
                img_array = img_array.reshape((height, width, 4))
            elif fourcc == b'DXT5':
                img_array = np.frombuffer(pixel_data, dtype=np.uint8)
                img_array = img_array.reshape((height, width, 4))
            else:
                img_array = np.frombuffer(pixel_data, dtype=np.uint8)
                img_array = img_array.reshape((height, width, 4))
            
            return Image.fromarray(img_array, 'RGBA')

    def open_dds_viewer(self):
        dds_file = filedialog.askopenfilename(
            title="Select DDS File",
            filetypes=(("DDS files", "*.dds"),)
        )
        if dds_file:
            try:
                img = self.read_dds_file(dds_file)
                
                if not self.dds_viewer:
                    self.dds_viewer = DDSViewer(self.window)
                self.dds_viewer.show()
                self.dds_viewer.update_preview(img)
            except Exception as e:
                messagebox.showerror("Error", f"Error opening DDS file: {str(e)}")
                if self.dds_viewer:
                    self.dds_viewer.hide()

    def run(self):
        try:
            self.window.mainloop()
        except KeyboardInterrupt:
            self.tracker.track_usage('stop')
            self.signal_handler(signal.SIGINT, None)
        except Exception as e:
            self.tracker.track_usage('error')
            print(f"Error: {str(e)}")
            self.signal_handler(signal.SIGTERM, None)

if __name__ == "__main__":
    converter = ImageConverter()
    converter.run()