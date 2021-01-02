import cx_Freeze
import sys
import os


PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')


print(os.environ['TCL_LIBRARY'],os.environ['TK_LIBRARY'])

base = None

if sys.platform == 'win32':
    base = 'Win32GUI'
syspath = r"C:\Python\DLLs"
buildOptions = dict(
    packages=["tkinter","pandas","numpy"],
    excludes=[],
    include_files=[('tcl86t.dll', os.path.join('lib', 'tcl86t.dll')),('tk86t.dll', os.path.join('lib', 'tk86t.dll'))]
)
executables = [cx_Freeze.Executable("[Gems of Atlantis].py", base=base, icon="hitek.ico")]
cx_Freeze.setup(
    name = "Gems of Atlantis",
    options = dict(build_exe=buildOptions),
    version = "0.02",
    description = "Gems of Atlantis",
    executables = executables
)
