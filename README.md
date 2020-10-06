# EWoMan  
Evolutionary Computing: Group Assignments  

## Setup  
Please clone the evoman framework into this project's root directory:  
```shell
git clone https://github.com/karinemiras/evoman_framework.git
```  
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
