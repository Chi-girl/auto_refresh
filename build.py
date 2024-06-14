import PyInstaller.__main__
import os

# builds application using pyinstaller
PyInstaller.__main__.run([
    '--noconsole',
    #"--onefile"
    '--onedir',
    "--hidden-import=pkg_resources.py2_warn",
    "--hidden-import=importlib_resources",
    "--hidden-import=sklearn.utils._weight_vector",
    "--add-data=assets;./assets",
    #"--add-data=assets;./Anaconda3/Lib/site-packages",
    '--icon=assets/accenture_logo.ico',
    
    os.path.join("src", "main.py")
])