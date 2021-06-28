# Markdown

## About Auract

**Auract** is an open-source project to help getting right input for [Microreact](https://microreact.org/showcase) and [Auspice](https://github.com/nextstrain/auspice) if you already have a newick and or metadata file.  
You can also add a distance matrix to improved the metadata. Note that i have also made a [custom Auspice build](https://github.com/Iry63/custom_auspice_build) to display the matrix which dynamically evolve with the tree state.


## Installation

Create a virtual environment(recommended)
```bash
python3 -m venv /path/to/new/virtual/environment
```

Clone the repository
```bash
git clone https://github.com/Iry63/Auract.git
cd Auract
```

Install package in requirement.txt
```bash
python -m pip install -r requirements.txt
```

## What data to use

#### Newick
For the newick file Auract currently support .nwk and .newick file

#### Metadata
And for the metadata .csv and .tsv file are supported.
Only an id or strain column is required note that specific column find in [microreact documentation](https://microreact.org/instructions) and [auspice documentation](https://docs.nextstrain.org/projects/augur/en/stable/faq/metadata.html) will also be aplied such as __autocolor prefix

#### Geocoding
Auract also include a geocoding features based on zip-code to use it all you need to do is add zip-code column in your metadata file and Auract will try to find a corresponding latitude and longitude. For more information on the current used database, check the file data/geodata/readme.txt

#### example
You can see an example for each file in data/test/

## Run Auract

For help on input:
```bash
python3 main.py -h
```

Basic command:
```bash
python3 main.py -c path/to/metadata.csv -n path/to/newick.newick
```

Add matrix:  
Adding matrix will only give you a color filter base on minimum distance but if you plan on using my [custom Auspice build](https://github.com/Iry63/custom_auspice_build) the matrix will also be display in Auspice.
```bash
python3 main.py -c path/to/metadata.csv -n path/to/newick.newick -m path/to/matrix.csv
```

## Results

All result of Auract will appear in a folder name result/.  
Inside it you will find auspice and microreact folder.  
In microreact folder there will be a .tsv file open it and will have the name of your dataset and a microreact url just open it in your favorite webbrowser.

And in Auspice folder you will find a json file drag and drop it at [auspice.us](https://auspice.us/) to see result. If you used a matrix you will also see an html file which is the table for the matrix it will also be displayed in auspice if using my custom build.

[![License GPL v3](https://img.shields.io/badge/license-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.en.html)
