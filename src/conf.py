
from glob import glob
import os


print(os.path.abspath(glob("**/.env")[0]) == os.path.abspath(glob("**/.env")[0]))
