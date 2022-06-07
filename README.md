## ProcAID Stage Two 

ProcAID stands for "Process Anomaly-based Intrusion Detection." The capability is made of two stages: 

1. Stage One: Unsupervised link prediction on a process creation log graph 
2. Stage Two: Inverse leadership and inverse density analysis  

The full explanation of ProcAID can be found here [ProcAID](https://www.proquest.com/openview/e4ce5ff777fc5943a8b4624677b3cad1/1.pdf?pq-origsite=gscholar&cbl=18750&diss=y). Presentations for ProcAID, including my thesis defense can be found [here](https://github.com/ajread4/procaid_presentations).

For convenience and use-case purposes, this repository contains the framework and algorithm to run Stage Two of ProcAID. Stage One can be found here [ProcAID Stage One](https://github.com/ajread4/procaid_stage1).


## Install
```
git clone https://github.com/ajread4/procaid_stage2.git
cd procaid_stage2
pip3 install -r requirements.txt
```

## Usage 
```
$ python3 analyze.py -h
usage: analyze.py [-h] [-e edges] [-v] [-i] [--ludacris] data

analyze - a capability to perform leadership and density graph analytics on information security data.

positional arguments:
  data                  specify the input data for graph creation, can be json file or folder of json files

optional arguments:
  -h, --help            show this help message and exit
  -e edges, --edges edges
                        specify the edges for the graph to create in the form of NodeX--NodeY,NodeY--NodeZ,...
  -v, --verbose         run analyze in verbose mode
  -i, --inverse         return inverse leadership and inverse density values
  --ludacris            create a graph using all possible nodes and edges in the dataset
```

## Example Usage 
1. Find the leadership and density value of a graph with edges between ```UserName``` and ```EventID``` using data from ```input_data.json```. 
```
$ python3 analyze.py input_data.json -e UserName--EventID
Leadership Value: 0.11818181818181818
Density Value: 0.16363636363636364
```
2. Find the inverse leadership and inverse density value of a graph with edges between ```UserName``` and ```EventID``` and ```UserName``` and ```LogHost``` using data from ```input_data.json```.
```
$ python3 analyze.py input_data.json -e UserName--EventID,UserName--LogHost -i
Inverse Leadership Value: 6.782608695652174
Inverse Density Value: 4.875
```
3. Find the inverse leadership and inverse density value of a graph with edges between ```UserName``` and ```EventID``` and ```UserName``` and ```LogHost``` using data from ```input_data.json``` and output in verbose mode. 
```
$ python3 analyze.py ../octopus_graph/tests/json_files/xab.json -e UserName--EventID,UserName--LogHost -i -v
Beginning ingestion of data at folder ../octopus_graph/tests/json_files/xab.json
Done walking folder ../octopus_graph/tests/json_files/xab.json
../octopus_graph/tests/json_files/xab.json is a single file.
Beginning ingestion of data at file ../octopus_graph/tests/json_files/xab.json
Found UserName in dataset
Found EventID in dataset
Feature check complete
Found UserName in dataset
Found LogHost in dataset
Feature check complete
Node: User529192 and id: 0
Node: 4634 and id: 1
Node: User529192 and id: 0
Node: ActiveDirectory and id: 2
Node: User529192 and id: 0
Node: 4624 and id: 3
Node: User529192 and id: 0
Node: ActiveDirectory and id: 2
Node: User124533 and id: 4
Node: 4624 and id: 3
Node: User124533 and id: 4
Node: ActiveDirectory and id: 2
Node: User529192 and id: 0
Node: 4624 and id: 3
Node: User529192 and id: 0
Node: ActiveDirectory and id: 2
Node: User529192 and id: 0
Node: 4634 and id: 1
Node: User529192 and id: 0
Node: ActiveDirectory and id: 2
Node: User529192 and id: 0
Node: 4624 and id: 3
Node: User529192 and id: 0
Node: ActiveDirectory and id: 2
Node: User529192 and id: 0
Node: 4634 and id: 1
Node: User529192 and id: 0
Node: ActiveDirectory and id: 2
Node: User529192 and id: 0
Node: 4624 and id: 3
Node: User529192 and id: 0
Node: ActiveDirectory and id: 2
Node: User529192 and id: 0
Node: 4634 and id: 1
Node: User529192 and id: 0
Node: ActiveDirectory and id: 2
Node: Comp649388$ and id: 5
Node: 4688 and id: 6
Node: Comp649388$ and id: 5
Node: Comp649388 and id: 7
Node: Comp067947$ and id: 8
Node: 4634 and id: 1
Node: Comp067947$ and id: 8
Node: ActiveDirectory and id: 2
Node: Comp067947$ and id: 8
Node: 4624 and id: 3
Node: Comp067947$ and id: 8
Node: ActiveDirectory and id: 2
Node: Comp447172$ and id: 9
Node: 4624 and id: 3
Node: Comp447172$ and id: 9
Node: ActiveDirectory and id: 2
Node: Comp916004$ and id: 10
Node: 4672 and id: 11
Node: Comp916004$ and id: 10
Node: ActiveDirectory and id: 2
Node: User529192 and id: 0
Node: 4624 and id: 3
Node: User529192 and id: 0
Node: ActiveDirectory and id: 2
Node: User529192 and id: 0
Node: 4634 and id: 1
Node: User529192 and id: 0
Node: ActiveDirectory and id: 2
Node: Comp715254$ and id: 12
Node: 4634 and id: 1
Node: Comp715254$ and id: 12
Node: ActiveDirectory and id: 2
Node: User529192 and id: 0
Node: 4624 and id: 3
Node: User529192 and id: 0
Node: ActiveDirectory and id: 2
Node: User529192 and id: 0
Node: 4634 and id: 1
Node: User529192 and id: 0
Node: ActiveDirectory and id: 2
Node: User529192 and id: 0
Node: 4624 and id: 3
Node: User529192 and id: 0
Node: ActiveDirectory and id: 2
Number of Training Nodes: 13
Number of Training Edges: 16
Inverse Leadership Value: 6.782608695652174
Inverse Density Value: 4.875
```
4. Find the leadership and density value of a graph using data from ```input_data.json``` in ```ludacris``` mode.
```
$ python3 analyze.py input_data.json --ludacris
Leadership Value: 0.34552845528455284
Density Value: 0.35772357723577236
```
## ProcAID Stage Two Parameters 
To fully emulate Stage Two of ProcAID, use the following edges and parameters: 
```
$ python3 analyze.py process_logs.json -i --ludacris
```
## File and Directory Information 

- ```analyze.py``` 
  - This is the main Python script that runs graph analyzer algorithm. 
- ```utils```
  - This directory contains ```leaderdensity.py``` and the ```LeaderDensity``` class which is used by ```analyze.py``` to create graphs and analyze them. 
- ```requirements.txt```
  - This file contains the requirements for running this script. 

## Dependencies 
This script uses Python 3.8.10 for operation. It has not been fully tested on other versions of Python.

## Publication
The full ProcAID publication is located here: [ProcAID](https://www.proquest.com/openview/e4ce5ff777fc5943a8b4624677b3cad1/1.pdf?pq-origsite=gscholar&cbl=18750&diss=y)

## Author
All of the code was written by me, AJ Read, for my thesis at GW.
- Twitter: [ajread3](https://twitter.com/ajread3)
- Github: [ajread4](https://github.com/ajread4)
- LinkedIn: [Austin Read](https://www.linkedin.com/in/austin-read-88953b189/)