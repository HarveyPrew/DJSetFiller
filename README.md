# DJ Set Filler


## Setup your python environnment

Use `pipenv` !! https://pipenv.readthedocs.io/en/latest/

## Setup the project

`pipenv install --dev`

To install tables (pytables) (taken from [Stack Overflow](https://stackoverflow.com/questions/73029883/could-not-find-hdf5-installation-for-pytables-on-m1-mac/74276925#74276925)):
* pip install cython
* brew install hdf5 
* brew install c-blosc 
* export HDF5_DIR=/opt/homebrew/opt/hdf5 
* export BLOSC_DIR=/opt/homebrew/opt/c-blosc 
* pip install --user tables
 


## Run the tests with coverage
`pytest`

## Lint the project

`flake8`

## Run continual testing

`ptw`



## Setting up mixesDB
What to get from spotify:
* artist uri 
* album uri 
* album name 
* total duration
not included:
* collaborative
* pid
* modified_at
* num_edits



# Usage
The code was adapted from [the third place solution in RecSys Challenge 2018](https://github.com/VasiliyRubtsov/recsys2018).

To start it is necessary to have a folder 'data' with data in json and an input.json file.

The order of execution:
1) json_to_dataframe.ipynb
2) validation_strategy.ipynb
3) lightfm.ipynb
4) lightfm_text.ipynb
5) candidate_selection.ipynb
6) lightfm_features.ipynb
7) co_occurence_features.ipynb
8) xgboost.ipynb
