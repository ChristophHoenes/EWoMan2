# EWoMan  
Evolutionary Computing: Group Assignment Task 2 (multi-objective)

## Disclaimer  
Note thet the folder 'evoman' and all its contents were taken from the evoman framework (https://github.com/karinemiras/evoman_framework) and hence those contents must be treated under their lcense.

## Setup  
Install required packages by installing the environment:  
```shell
conda env create -f environment.yml
```  
## Running the algorithm  
To run the algorithm specify which evolutionary modules and parameters you want to use in a .json file (see example default_config.json).  
Then run the main of evolution.py by executing:  
```shell
python evolution.py
```  
For multiprocessing on multiple CPUs run the following comand:  
```shell
python -m scoop evolution.py --multiprocessing True
```  
