try:    
    import platform
    print(f"Python Platform: {platform.platform()}")
except:
    print("***** error : platform")
try:
    import sys
    print(f"system : {sys.version}")
except:
    print("***** error : sys")
try:
    import pathlib
    # print(f"Python {pathlib.__version__}")
except:
    print("***** error : pathlib")
try:
    import datetime
    # print(f"Python {datetime.__version__}")
except:
    print("***** error : datetime")
try:
    import glob
    # print(f"Python {glob.__version__}")
except:
    print("***** error : glob")
try:
    import tqdm
    # print(f"tqdm {tqdm.version}")
except:
    print("***** error : tqdm")
try:
    import json
    print(f"json : {json.__version__}")
except:
    print("***** error : json")
try:
    import sqlalchemy
    print(f"sqlalchemy : {sqlalchemy.__version__}")
except:
    print("***** error : sqlalchemy")
try:
    import pandas
    print(f"pandas : {pandas.__version__}")
except:
    print("***** error : pandas")
try:
    import mysql
    # print(f"mysql : {mysql.__version__}")
except:
    print("***** error : mysql")
try:
    import sklearn
    print(f"sklearn : {sklearn.__version__}")
except:
    print("***** error : sklearn")
try:
    import itertools
    # print(f"Python {itertools.__version__}")
except:
    print("***** error : itertools")
try:
    import pyowm
    # print(f"Python {pyowm.__version__}")
except:
    print("***** error : pyowm")
try:
    import geopy
    print(f"geopy : {geopy.__version__}")
except:
    print("***** error : geopy")
try:
    import meteostat
    print(f"meteostat : {meteostat.__version__}")
except:
    print("***** error : geometeostatpy")

try:
    from common import *
    from preprocess import *
    from vector import *
    from update_product import *
    from weather import *
except:
    print('Files not fond')
