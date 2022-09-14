import glob
import os


print(os.path.abspath(glob.glob(('.env'))[0]))