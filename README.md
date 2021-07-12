# Markdown

## About Auract

**Auract** is an open-source project to help getting right input for [Microreact](https://microreact.org/showcase) and [Auspice](https://github.com/nextstrain/auspice) if you already have a newick and or metadata file.  
You can also add a distance matrix to improved the metadata. Note that I have also made a [custom Auspice build](https://github.com/Iry63/custom_auspice_build) to display the matrix which dynamically evolve with the tree state.

Auract also include a geocoding features based on zip-code to use it all you need to do is add zip-code to your metadata file and Auract will try to find a corresponding latitude and longitude.
For more information on the current used database, check the file auract/data/geodata/readme.txt

## Installation

Create a virtual environment(recommended)
```bash
python3 -m venv auract_venv/
```

Clone the repository
```bash
git clone https://github.com/Iry63/Auract.git
cd Auract
pip3 install .
```

## Input

#### Newick
For the newick file Auract currently support .nwk and .newick file

#### Metadata
For metadata .csv file are supported.
Only an id or strain column is required note that specific column find in [microreact documentation](https://microreact.org/instructions) and [auspice documentation](https://docs.nextstrain.org/projects/augur/en/stable/faq/metadata.html) will also be aplied such as __autocolor prefix

#### Matrix
And for the matrix you will need a .tsv file with first row and column being strain id.

### example
You can see an example for each file in data_test/ folder.

## Output

Auract result are two files one for microreact and one for auspice.
These two file are created in your working directory inside an **auract_result/** folder or at the given path if arguments --output is used.

The **micoreact file** is a tsv that contain a link to the microreact project and some information on the dataset.
And the **auspice file** is json that can be used at [auspice.us](https://auspice.us/) or in a local instance of [Auspice](https://github.com/nextstrain/auspice).
If you plan on having the distance matrix in auspice again, I have made a [custom Auspice build](https://github.com/Iry63/custom_auspice_build) for that.


## Run Auract

For help on input:
```bash
auract -h

optional arguments:
  -h, --help            show this help message and exit
  -c CSV, --csv CSV     path to csv file
  -n NEWICK, --newick NEWICK
                        path to newick file needed for auspice
  -m MATRICE, --matrice MATRICE
                        path to matrice csv or tsv file
  --no_microreact       if call cancel microreact process
  --no_auspice          if call cancel auspice process
  -nll, --no_addlatlong
                        if call cancel latlong process
  --no_clearfile        if call cancel secondfile clear
```

Basic command:
```bash
auract -c data_test/metadata.csv -n data_test/newick_tree.nwk
```

Add matrix:  
Adding matrix will only give you a color filter base on minimum distance but if you plan on using my [custom Auspice build](https://github.com/Iry63/custom_auspice_build) the matrix will also be display in Auspice.
```bash
auract -c data_test/metadata.csv -n data_test/newick_tree.nwk -m data_test/matrix.tsv
```

[![License GPL v3](https://img.shields.io/badge/license-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.en.html)
