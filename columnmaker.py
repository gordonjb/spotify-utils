import pandas
import re
import progressbar
from tqdm import tqdm
import numpy as np
import csv


sorted = pandas.read_csv('/mnt/c/Users/Gordon/Desktop/gpm/sorted.csv', sep="|")
sorted['spotid'] = 'spotify:track:' + sorted['spotid'].astype(str).str.strip()
sorted.to_csv('/mnt/c/Users/Gordon/Desktop/gpm/sortedids.csv', index=False, columns=["spotid"])
