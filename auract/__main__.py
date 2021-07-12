#!/usr/bin/env python3
import argparse
import logging
import codecs
import shutil
import csv
import os
import sys
import pandas as pd

from .microreact import Microreact
from .auspice import Auspice
from .log import log, quit_with_error

import importlib.util
import time

package_augur = 'augur'
package_jinja2 = 'jinja2'


def csv_verif(arguments):
    try:
        codecs.open(arguments.csv, encoding="utf-8", errors="strict").readlines()
    except IOError as e:
        log(e)
        log("csv file not found", type='warning')
        arguments.no_addlatlong = True
        arguments.no_microreact = True
        return arguments

    try:
        with open(arguments.csv) as csvfile:
            csv.Sniffer().sniff(csvfile.read())
            csvfile.seek(0)
    except csv.Error as e:
        log(e)
        log("csv file not valid", type='warning')
        arguments.no_addlatlong = True
        arguments.no_microreact = True
        return arguments

    df = pd.read_csv(arguments.csv)
    if df.empty:
        log("csv file empty", type='warning')
        arguments.no_addlatlong = True
        arguments.no_microreact = True
        return arguments

    for col in df.columns:
        if col.lower() in ('strain', 'strains', 'id'):
            break
    else:
        log("csv file not valid missing column id or strain", type='warning')
        arguments.no_addlatlong = True
        arguments.no_microreact = True
        return arguments
    return arguments


def newick_verif(arguments):
    try:
        codecs.open(arguments.newick, encoding="utf-8", errors="strict").readlines()
    except IOError as e:
        log(e)
        log("newick file not found", type='warning')
        arguments.no_auspice = True
        arguments.newick = False
    return arguments


def matrice_verif(arguments):
    try:
        codecs.open(arguments.matrice, encoding="utf-8", errors="strict").readlines()
    except IOError as e:
        log(e)
        log("matrice file not found", type='warning')

    try:
        with open(arguments.matrice) as csvfile:
            csv.Sniffer().sniff(csvfile.read())
            csvfile.seek(0)
    except csv.Error as e:
        log(e)
        log("matrice file not valid make sure it's a csv or tsv file", type='warning')
        arguments.matrice = None
        return arguments

    df = pd.read_csv(arguments.matrice, sep='\t', index_col=[0])
    if df.empty:
        log('matrice file is empty matrice set to None', type='warning')
        arguments.matrice = None
        return arguments

    log('check matrice integrity', type='debug')
    cols = df.columns.astype(str).tolist()
    index = df.index.astype(str)
    array = index.isin(cols)
    if array.all():
        pass
    else:
        z = 0
        for i in array:
            if not i:
                log(message=('Warning- index: ' + str(index[z]) + ' dont have any corresponding column'),
                    type='warning')
            z += 1
        log("Warning- Matrice index not equal to matrice column, arguments matrice set to None", type='warning')
        arguments.matrice = False
        return arguments
    dico = df.to_dict()
    for key, val in dico.items():
        for key2, val2 in val.items():
            try:
                float(val2)
            except ValueError:
                log('matrice contain value that are not number : '+val2, type='warning')
                arguments.matrice = None
                return arguments

    log('\t Matrice valid', type='debug')
    return arguments


# test argument passed
def verification_args(arguments):
    log("Verifying arguments", type='info')
    if arguments.output:
        if not os.path.exists(arguments.output):
            log('output path not find', type='info')
            arguments.output = None
            
    # csv
    if arguments.csv:
        arguments = csv_verif(arguments)
    else:
        log("no csv file given argument no_addlatlong and no_microreact set to true", type='info')
        arguments.no_addlatlong = True
        arguments.no_microreact = True

    # newick
    if arguments.newick:
        newick_verif(arguments)
    else:
        log("no newick file given argument no_auspice set to True", type='info')
        arguments.no_auspice = True

    if arguments.no_auspice and arguments.no_microreact:
        quit_with_error('both argument no_auspice and no_microreact have been set to True exit program')

    # matrice
    if arguments.matrice:
        matrice_verif(arguments)

    log('Info- Argument that will be use to run: ')
    log()
    for arg in vars(arguments):
        log(message=(arg + ': ' + str(getattr(arguments, arg))), type='info')
    return arguments


def argsparser():
    # Argument parsing
    parser = argparse.ArgumentParser(
        prog='auract',
        description="A toolkit to create microreact and auspice output from csv and newick can also add a matrix that "
                    "will be display in auspice if using custom auspice build "
    )
    parser.add_argument('-c', '--csv', help="path to csv file")
    parser.add_argument('-n', '--newick', help="path to newick file needed for auspice")
    parser.add_argument('-m', '--matrice', help="path to matrice csv or tsv file")
    parser.add_argument("--no_microreact", action='store_true', help='if call cancel microreact process')
    parser.add_argument("--no_auspice", action='store_true', help='if call cancel auspice process')
    parser.add_argument("-nll", "--no_addlatlong", action='store_true', help='if call cancel latlong process')
    parser.add_argument("--no_clearfile", action='store_true', help='if call cancel secondfile clear ')
    parser.add_argument("--output", help="path for Auract output files")

    if len(sys.argv) == 1:
        parser.print_help()
        parser.exit()

    args = parser.parse_args()
    args = verification_args(args)
    return args


def version():
    return "Auract - version 0.9"


def main():
    logging.basicConfig(filename='log.log', filemode="w", level=logging.DEBUG,
                        format='%(levelname)s - %(asctime)s - %(message)s')
    log(version(), type='info')
    log()
    args = argsparser()

    if not args.no_microreact:
        log('-----------------------------------')
        log('microreact call', type='info')
        log()
        Microreact(csv_path=args.csv, newick_path=args.newick, no_latlong=args.no_addlatlong,
                         matrice=args.matrice, output=args.output)

    augur = importlib.util.find_spec(package_augur)
    jinja = importlib.util.find_spec(package_jinja2)

    if jinja is None:
        log(package_jinja2 + " is not installed matrice will not be render in auspice", type='info')
    if augur is None:
        log(package_augur + " is not installed auspice ignored", type='warning')
    else:
        if not args.no_auspice:
            log('-----------------------------------')
            log('auspice call', type='info')
            log()
            Auspice(csv_path=args.csv, newick_path=args.newick, no_latlong=args.no_addlatlong,
                            matrice=args.matrice, jinja=jinja, output=args.output)

    if not args.no_clearfile:
        from .settings import second_file_dir
        if not os.path.exists(second_file_dir):
            pass
        else:
            log()
            shutil.rmtree(second_file_dir)
            log("Second file folder remove", type='info')


if __name__ == "__main__":
    start_time = time.time()
    main()
    log('end', type='debug')
    g_time = time.time() - start_time
    log('Time '+str(g_time)+' second', type='info')

