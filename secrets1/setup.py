import os
cwd = os.getcwd()
from distutils.core import setup
from Cython.Build import cythonize
 
setup(ext_modules=cythonize([f"{cwd}/secrets1/secret_telegram.py"]))
setup(ext_modules=cythonize([f"{cwd}/secrets1/secret_account.py"]))
setup(ext_modules=cythonize([f"{cwd}/secrets1/secret_chat_id.py"]))