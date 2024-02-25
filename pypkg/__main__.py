from ctypes import c_int, c_char_p
from pathlib import Path
import ctypes
import sys

if sys.platform.startswith("win32"):
    lib_filename = "libextern.dll"
elif sys.platform.startswith("darwin"):
    lib_filename = "libextern.dylib"
else:
    lib_filename = "libextern.so"
lib_path = str(Path(__file__).with_name(lib_filename))
lib = ctypes.cdll.LoadLibrary(lib_path)

lib.bar.argtypes = [c_int, c_int]
lib.bar.restype = None

lib.bar(35, 2*17)
