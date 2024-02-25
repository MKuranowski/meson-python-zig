from ctypes import c_int, c_char_p
from pathlib import Path
import ctypes
import sys

if sys.platform.startswith("win32"):
    lib_filename = "extern.dll"
elif sys.platform.startswith("darwin"):
    lib_filename = "libextern.dylib"
else:
    lib_filename = "libextern.so"
lib_path = str(Path(__file__).with_name(lib_filename))
lib = ctypes.cdll.LoadLibrary(lib_path)

lib.add.argtypes = [c_int, c_int]
lib.add.restype = c_int

lib.print.argtypes = [c_char_p]
lib.print.restype = None

print(lib.add(35, 2*17))
lib.print("Hello, world!".encode("utf-8"))
