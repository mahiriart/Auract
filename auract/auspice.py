"""
This module contain the subclass Auspice
"""
import os
import pandas as pd
import subprocess
import json

from .dataset import Dataset
from .log import log, quit_with_error
from .color_from_matrice import min_distance_value
from .settings import auspice_refine_dir, auspice_config_dir, result_Dir_auspice, data_dir, auspice_data_dir, second_file_dir

from Bio import Phylo
from matplotlib import cm


class Auspice(Dataset):
    def __init__(self, csv_path, newick_path, no_latlong, matrice, jinja, output):
        super().__init__(csv_path, newick_path, no_latlong, matrice)
        self.metadata = None
        self.llconfig = None
        self.colorconfig = None
        self.table = None
        self.table_html = None
        if output:
            self.resultdir = os.path.join(output, 'auspice')
        else:
            self.resultdir = result_Dir_auspice
        self.lastresultjson = os.path.join(self.resultdir, self.name + '.json')
        self.refinertree = os.path.join(auspice_refine_dir, self.name + '_tree.nwk')
        self.refinernode = os.path.join(auspice_refine_dir, self.name + '_node_data.nwk')
        self.config = os.path.join(data_dir, 'config/baseconfig.json')

        if self.basecsv:
            self.checkcolumn()
            if self.matrice:
                self.apply_matrice_color()

        if self.ll and self.basecsv:
            self.lat_long_gen()

        log("Augur call:", type='info')
        self.commandaugurrefine()
        if jinja and self.matrice:
            self.get_html_matrice()
        self.commandaugurexport()

    def checkcolumn(self):
        log("check columns for auspice and adapt if needed and possible", type='debug')
        df = pd.read_csv(self.csvadapte)
        for col in df.columns:
            if col.lower() in ('strain', 'strains', 'id'):
                df.rename(columns={col: 'strain'}, inplace=True)
                break
        else:
            quit_with_error("column id or strain missing")

        for col in df.columns:
            if col.lower() in ('date', 'date sample', 'date_sample', 'date-sample'):
                df.rename(columns={col: 'date'}, inplace=True)
                break
            else:
                pass
        else:
            if df.filter(items=['year', 'month', 'day']).empty:
                pass
            else:
                df["date"] = df["year"].astype(str) + "-" + df["month"].astype(str) + "-" + df["day"].astype(str)
                df = df.drop(columns=['year', 'month', 'day'])

        if not os.path.exists(auspice_data_dir):
            os.makedirs(auspice_data_dir)
        metadata_path = os.path.join(auspice_data_dir, self.name + 'metadata.tsv')
        self.metadata = metadata_path
        df.to_csv(self.metadata, index=False)

    def lat_long_gen(self):
        df_ll = pd.read_csv(self.csvadapte, usecols=['zip-code', 'latitude', 'longitude'])
        df_ll['type'] = 'zip-code'
        cols = df_ll.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        df_ll = df_ll[cols]
        df_ll = df_ll.drop_duplicates()
        df_ll = df_ll.dropna()

        if not os.path.exists(auspice_config_dir):
            os.makedirs(auspice_config_dir)
        llconfig_path = os.path.join(auspice_config_dir, self.name + '_ll.tsv')
        self.llconfig = llconfig_path
        df_ll.to_csv(self.llconfig, index=False, header=None, sep='\t')

    def apply_matrice_color(self):
        df_color = min_distance_value(self.matrice)
        df = pd.read_csv(self.metadata)
        df = df.astype({"strain": str})
        df_color = df_color.astype({"id": str})

        df = df.set_index('strain').join(df_color.set_index('id'))
        df.reset_index(inplace=True)
        df = df.drop(columns=['min_value_compare_to_other__colour'])
        df.to_csv(self.metadata, index=False)

        df_color = df_color.drop(columns=['id'])
        df_color["trait"] = "min_value_compare_to_other"
        df_color = df_color.drop_duplicates()
        cols = df_color.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        df_color = df_color[cols]
        df_color = df_color.sort_values(by='min_value_compare_to_other')

        if not os.path.exists(auspice_config_dir):
            os.makedirs(auspice_config_dir)
        colorconfig = os.path.join(auspice_config_dir, self.name + '_color.tsv')
        self.colorconfig = colorconfig
        df_color.to_csv(self.colorconfig, index=False, sep="\t", header=None)

    def get_html_matrice(self):
        if not os.path.exists(self.resultdir):
            os.makedirs(self.resultdir)
        matrix = pd.read_csv(self.matrice, sep="\t", index_col=0)

        tree = Phylo.read(self.refinertree, 'newick')
        list_ordered = []
        clades = tree.get_terminals()
        for i in clades:
            list_ordered.append(str(i))

        matrix.columns = matrix.columns.astype(str)
        matrix = matrix[list_ordered]
        matrix.index = matrix.index.astype(str)
        matrix = matrix.reindex(index=list_ordered)

        s = matrix.to_numpy().max()
        viridis_r = cm.get_cmap('viridis_r', s)

        matrix = matrix.style.background_gradient(axis=None, cmap=viridis_r, text_color_threshold=0.3)
        tablepath = os.path.join(second_file_dir, self.name + '_table.html')
        self.table = tablepath
        with open(self.table, "w") as mc:
            mc.write(str(matrix.render()))
            self.table_html = matrix.render()

    def commandaugurrefine(self):
        if not os.path.exists(auspice_refine_dir):
            os.makedirs(auspice_refine_dir)
        argument = ['augur refine', '--tree', self.newick, '--output-tree', self.refinertree, '--output-node-data',
                    self.refinernode]
        if self.metadata:
            argument.append('--metadata')
            argument.append(self.metadata)
        if not os.path.exists(self.resultdir):
            os.makedirs(self.resultdir)
        with open(os.path.join(self.resultdir, 'auspice_command_result.log'), 'w+') as f:
            command = " ".join(argument)
            try:
                log('\tRunning augur refine command can check output in ' + self.resultdir + '/auspice_command_result.log',
                    type='info')
                subprocess.run(command, stdout=f, stderr=subprocess.STDOUT, shell=True)
                log('\tAugur refine ended', type='info')
                log()
            except OSError as error:
                log(error, type='debug')
                log("Error- augur command export failed check log file for more information", type='error')
            except ModuleNotFoundError as ie:
                log(ie, type='error')

    def commandaugurexport(self):
        if not os.path.exists(self.resultdir):
            os.makedirs(self.resultdir)
        argument = ['augur export v2', '-t', self.refinertree, '--node-data', self.refinernode, '--output',
                    self.lastresultjson, '--auspice-config', self.config]
        if self.metadata:
            argument.append('--metadata')
            argument.append(self.metadata)
        if self.llconfig:
            argument.append('--lat-longs')
            argument.append(self.llconfig)
        if self.colorconfig:
            argument.append('--colors')
            argument.append(self.colorconfig)
        with open(os.path.join(self.resultdir, 'auspice_command_result.log'), 'a+') as f:
            command = " ".join(argument)
            try:
                log('\tRunning augur export command can check output in '+ self.resultdir + '/auspice_command_result.log',
                    type='info')
                subprocess.run(command, stdout=f, stderr=subprocess.STDOUT, shell=True)
                log('\tAugur export ended', type='info')
                log()
            except OSError as error:
                log(error, type='debug')
                log("Error- augur command export failed check log file for more information", type='error')
            except ModuleNotFoundError as ie:
                log(ie, type='error')

        if self.table_html:
            try:
                a = {'matrice': self.table_html}
                with open(self.lastresultjson) as f:
                    data = json.load(f)
                data.update(a)
                with open(self.lastresultjson, 'w') as f:
                    json.dump(data, f)
            except OSError as err:
                log("Can't modify auspice json result", type='error')
