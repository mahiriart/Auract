"""
This module contain the subclass Microreact
"""

import json
import pandas as pd
import src.dataset as dataset
import src.color_from_matrice as matrice
from src.log import log
from settings import *
import subprocess
import os
import csv
import datetime


class Microreact(dataset.Dataset):
    def __init__(self, csv_path, newick_path, no_latlong, matrice):
        log()
        super().__init__(csv_path, newick_path, no_latlong, matrice)
        self.microreactlink = None
        self.jsonfile = None
        self.check_column()
        if self.matrice:
            self.apply_matrice_color()
        self.microreact_api()
        self.store_result()
        log()
        log()

    def store_result(self):
        if not os.path.exists(result_Dir_micro):
            os.makedirs(result_Dir_micro)
        file = os.path.join(result_Dir_micro, "results.tsv")
        file_exist = os.path.isfile(file)
        fieldname = ['name',  'link', 'csv', 'newick', 'matrice', 'll', 'date']
        with open(file, 'a+') as results:
            writer = csv.DictWriter(results, fieldnames=fieldname, delimiter="\t")
            if not file_exist:
                log("creating results.csv that store metadata of the request", type='info')
                writer.writeheader()
            writer.writerow({'name': self.name, 'csv': self.basecsv, 'newick': self.newick, 'll': self.ll, 'date': datetime.datetime.now(), 'link': self.microreactlink, 'matrice': self.matrice})
            log("adding new result from the request to results.csv", type='info')

    def apply_matrice_color(self):
        df = pd.read_csv(self.csvadapte)
        df_color = matrice.min_distance_value(self.matrice)
        df = df.set_index('id').join(df_color.set_index('id'))
        df.reset_index(inplace=True)
        df.to_csv(self.csvadapte, index=False)

    def check_column(self):
        log("check columns for microreact and adapt if possible", type='debug')
        df = pd.read_csv(self.csvadapte)
        for col in df.columns:
            if col.lower() in ('strain', 'strains', 'id'):
                df.rename(columns={col: 'id'}, inplace=True)
                break
        else:
            log("column id or strain is missing", type='error')
            exit()
        listdate = ['date', 'Date', 'date sample', 'Date sample', 'Date Sample']
        if df.filter(items=listdate).empty:
            pass
        else:
            if df.filter(items=['year', 'month', 'day']).empty:
                z = list(df.filter(items=listdate))
                df[['year', 'month', 'day']] = df[z[0]].str.split("-", expand=True)
        df.to_csv(self.csvadapte, index=False)

    def microreact_api(self):
        with open(self.csvadapte, "r") as f:
            datatext = f.read()
        if self.newick:
            with open(self.newick, "r") as z:
                treetext = z.read()
            x = {
                "name": self.name,
                "data": datatext,
                "tree": treetext
            }
        else:
            x = {
                "name": self.name,
                "data": datatext
            }
        if not os.path.exists(micro_json_dir):
            os.makedirs(micro_json_dir)
        jsonpath = os.path.join(micro_json_dir, self.name + ".json")
        with open(jsonpath, "w") as json_file:
            json.dump(x, json_file, indent=1)
            self.jsonfile = jsonpath

        # request API MicroReact
        log("Processing Microreact api request", type='debug')
        try:
            log()
            result = subprocess.check_output(
                'curl -H "Content-type: application/json; charset=UTF-8" -X POST -d @' + jsonpath +
                ' https://microreact.org/api/project/', shell=True)
            api_result = json.loads(result)
            log('Microreact link : ' + api_result['url'])
            log()
            self.microreactlink = api_result['url']
        except OSError as error:
            log(error, type='debug')
            log("Error- connection to microreact api failed check log file for more information", type='error')
