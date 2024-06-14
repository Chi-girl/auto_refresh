import PyInstaller.__main__
import os

# builds application using pyinstaller
PyInstaller.__main__.run([
    # '--noconsole',
    
    # #"--onefile"
    # '--onedir',
    "--hidden-import=pkg_resources.py2_warn",
    "--hidden-import=importlib_resources",
    # "--hidden-import=sklearn.utils._weight_vector",
    "--add-data=assets;./assets",
    # #"--add-data=assets;./Anaconda3/Lib/site-packages",
    '--icon=assets/accenture_logo.ico',
    # Parquet to add
    "--add-data=C:/Users/gabriel.lacanilao.jr/Desktop/TULIP SAMPLE/Bootleg/venv/Lib/site-packages/fastparquet.libs;./fastparquet.libs",
# Parquet to add
    # "--add-data=C:/Users/gabriel.lacanilao.jr/Desktop/TULIP SAMPLE/Bootleg/venv/Lib/site-packages/pyarrow",.
    
    os.path.join("test_v1.py")
])