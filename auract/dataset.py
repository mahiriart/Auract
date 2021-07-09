"""
This module contain the class Dataset super class
"""

import os
import shutil
from .settings import second_file_dir
from .geocoding import geocoding


class Dataset:
    def __init__(self, csv_path, newick_path, no_latlong, matrice):
        self.name = None
        self.basecsv = csv_path
        self.newick = newick_path
        self.matrice = matrice
        self.ll = not no_latlong
        self.csvadapte = None

        if self.basecsv:
            self.name = os.path.splitext(os.path.basename(self.basecsv))[0]
            if not os.path.exists(second_file_dir):
                os.makedirs(second_file_dir)
            self.csvadapte = os.path.join(second_file_dir, os.path.splitext(os.path.basename(self.name))[0] + "_cp.csv")
            shutil.copyfile(self.basecsv, self.csvadapte)
        else:
            self.name = os.path.splitext(os.path.basename(newick_path))[0]

        if self.ll and self.csvadapte:
            self.addll()

    def addll(self):
            self.csvadapte = geocoding(self.csvadapte)

