import PyInstaller.__main__
import sys
import os
import tkinter
import tkinter.ttk
from distutils.sysconfig import get_python_lib

def find_tcl_tk_dirs():
    """Find Tcl/Tk directories in various possible locations"""
    possible_locations = [
        
        os.path.join(os.path.dirname(sys.executable), 'tcl'),
        os.path.join(get_python_lib(), 'tcl'),
        r'C:\Python313\tcl',
        r'C:\Program Files\Python313\tcl',
        r'C:\Program Files (x86)\Python313\tcl',
    ]
    
    for base_dir in possible_locations:
        if os.path.exists(base_dir):
            tcl_dir = os.path.join(base_dir, 'tcl8.6')
            tk_dir = os.path.join(base_dir, 'tk8.6')
            if os.path.exists(tcl_dir) and os.path.exists(tk_dir):
                return tcl_dir, tk_dir
    return None, None

script_dir = os.path.dirname(os.path.abspath(__file__))
icon_path = os.path.join(script_dir, 'favicon.ico')

if not os.path.exists(icon_path):
    print(f"Error: Icon file not found at {icon_path}")
    sys.exit(1)

print(f"Using icon from: {icon_path}")

tcl_lib, tk_lib = find_tcl_tk_dirs()

options = [
    'dds_converter.py',
    '--name=DDS_Converter',
    '--onefile',
    '--windowed',
    '--clean',
    '--noconsole',
    f'--icon={icon_path}',  
]

if tcl_lib and tk_lib:
    options.extend([
        f'--add-data={tcl_lib};tcl8.6',
        f'--add-data={tk_lib};tk8.6',
    ])

options.extend([
    '--hidden-import=tkinter',
    '--hidden-import=tkinter.ttk',
    '--hidden-import=tkinter.filedialog',
    '--hidden-import=tkinter.messagebox',
    '--hidden-import=tkinter.font',
    '--hidden-import=_tkinter',
    '--hidden-import=PIL',
    '--hidden-import=PIL._imagingtk',
    '--hidden-import=PIL._tkinter_finder',
    '--hidden-import=PIL.ImageTk',
    '--hidden-import=PIL.Image',
    '--hidden-import=numpy',
    '--collect-all=tkinter',
    '--collect-all=PIL',
])

os.system('rmdir /S /Q build dist 2>nul')
os.system('del /F /Q DDS_Converter.spec 2>nul')

print(f"TCL path: {tcl_lib}")
print(f"TK path: {tk_lib}")

PyInstaller.__main__.run(options)