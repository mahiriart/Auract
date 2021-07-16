# Markdown  
  
## About Auract  
  
**Auract** is an open-source project to help visualizing phylogenetique data, by helping using [Microreact](https://microreact.org/showcase) and [Auspice](https://github.com/nextstrain/auspice) for people that have already made a phylogenetique analyse but want a graphic visualisation of it.

Auract also come with few features to enhance your metadata.

&nbsp;&nbsp;&nbsp;Such as a geocoding features based on zip-code. To use it all you need to do is add zip-code to your metadata file and Auract will try to find a corresponding latitude and longitude.  
For more information on the current used database, check the **auract/data/geodata/readme.txt** file.

&nbsp;&nbsp;&nbsp;Auract also allows you to add a distance matrix to improved the metadata. The result will be a html file that can be display in any web browser. But note that I have also made a [custom Auspice build](https://github.com/Iry63/custom_auspice_build) to display the matrix which dynamically evolve with the tree state.

#### Is auract for me:
&nbsp;&nbsp;&nbsp;To use Auract there are two essential file, which are a newick file with the .nwk or .newick extension and a metadata file with the .csv extension. If you don't have any one of these two file you will not be able to use Auract. Note that if you are using only one of this two file the visualisation will be poor with only a raw tree for auspice and a metadata table for microreact.
But for more information on the input used see below.
  
## Installation  
  
Create a virtual environment(recommended)  
```bash  
python3 -m venv auract_venv/
source auract_venv/bin/activate
```  
  
Clone the repository  
```bash  
git clone https://github.com/Iry63/Auract.git
cd Auract
pip3 install .
```

Test
```
auract -h
```
  
## Input  
  
#### Newick  
For the newick file Auract currently support .nwk and .newick file.
  
#### Metadata  
&nbsp;&nbsp;&nbsp;For metadata .csv file are supported.  Any column information is accepted.
Only an id or strain column is required note that specific column find in [microreact documentation](https://microreact.org/instructions) and [auspice documentation](https://docs.nextstrain.org/projects/augur/en/stable/faq/metadata.html) will also be aplied such as column with "__autocolor" prefix .
&nbsp;&nbsp;&nbsp;An important optional column is the zip-code column, if the geocoding process is enable Auract will try to find a corresponding latitude and longitude associate to the zip-code.
For more information on the current used database, check the **auract/data/geodata/readme.txt** file.

  
#### Matrix  
And for the matrix you will need a .tsv file with first row and column being strain id.  And each cells being a distance value between the two strain.
  
### example  
You can see an example for each of these file in the **data_test/** folder.  
  
## Output  
  
Auract main result are two files one for microreact and one for auspice.  
These two file are created in your working directory inside an **auract_result/** folder or at the given path if arguments --output is used.  
  
The **micoreact file** is a tsv that contain a link to the microreact project and some information on the dataset.  
And the **auspice file** is json that can be used at [auspice.us](https://auspice.us/) or in a local instance of [Auspice](https://github.com/nextstrain/auspice).  
If you plan on having the distance matrix in auspice again, I have made a [custom Auspice build](https://github.com/Iry63/custom_auspice_build) for that.  
  
  
## Run Auract  
  
For help on arguments:  
```bash  
auract -h  

optional arguments:  -h, --help
show this help message and exit  
	-c CSV, --csv CSV     		path to csv file  
	-n NEWICK, --newick NEWICK  	path to newick file needed for auspice  
	-m MATRICE, --matrice MATRICE  	path to matrice csv or tsv file  
	--no_microreact 		if call cancel microreact process  
	--no_auspice 			if call cancel auspice process  
	-nll, --no_addlatlong 		if call cancel latlong process  
	--no_clearfile 			if call cancel secondfile clear
	--output OUTPUT 		path for Auract output files

```  
  
Basic command:  
```bash  
auract -c data_test/metadata.csv -n data_test/newick_tree.nwk
```  
  
Add matrix:    
Adding matrix will only give you a color filter base on minimum distance in classic Auspice but if you plan on using my [custom Auspice build](https://github.com/Iry63/custom_auspice_build) the matrix will also be display in Auspice.  
```bash  
auract -c data_test/metadata.csv -n data_test/newick_tree.nwk -m data_test/matrix.tsv
``` 
More complexe command:
```bash  
auract -c data_test/metadata.csv \
	-n data_test/newick_tree.nwk \
	-m data_test/matrix.tsv \
	--output path_to/auract/result/ \
	--no_clearfile \
	-nll \
	--no_microreact
``` 
This command for example will give result at path_to/auract/result/ , plus will not clear second file in auract folder so will see every file created during Auract process. There will be no geocoding. And microreact result will not be created you will only have the .json file for Auspice. 

[![License GPL v3](https://img.shields.io/badge/license-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.en.html)
