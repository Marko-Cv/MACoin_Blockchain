# MACoin Blockchain
## A Python based Cryptocurrency
**Skills: Programming with Advanced Computer Languages (7,789 | 8,789)**

Project Link: **xyz**

## Creators
- Marko Cvijic (18-607-903)
- Robert Josua Michels (18-615-286)
- Anne Strunz (22-601-595)
- Julia Vogt (16-933-582)

## About the Project
This MACoin group project aimed to develop a basic blockchain simulation to provide practical insights into how blockchain technology operates, particularly in the context of cryptocurrency transactions. The objective was to build a functional prototype that would allow for the creation and management of digital wallets, the execution of secure transactions, and the ability to track these transactions through a ledger system. Additionally, the prototype provides the basic infrastructure to implement smart contracts. This simulation was designed to demystify the technology behind cryptocurrencies and offer a clear, hands-on experience of its potential applications.

The team comprised students at various skill levels, from beginners to more experienced coders, which enriched the learning experience. Those with advanced skills shared their knowledge, helping to elevate the group's overall understanding and capabilities. This collaborative environment not only boosted our Python programming skills but also fostered a spirit of teamwork and peer-to-peer education.

The team’s motivation for choosing this project was driven by a collective curiosity about blockchain technology and a desire to strengthen our technical skills in a highly relevant area. Recognizing the growing importance of blockchain and cryptocurrencies in the digital economy, the decision was made to align the team’s skills with these trends. By building this blockchain simulation, a foundational understanding was sought that could support future projects and professional opportunities in technology and finance.


## Files
This repository includes all documents related to the MACoin Blockchain group project.
Specifically, it includes:
- The `MACoin.ipynb` Jupyter Notebook which contains the code and explanations of the blockchain
- A `MACoin.py` python file with the raw code necessary for the blockchain
- A `MACoin.pdf` file consisting of the documentation, explaining the reasoning and details of the blockchain

## Getting Started
The entire Blockchain can be controlled via the User Interface function. This will enable the user to navigate between the different functionalities provided on the blockchain.
To begin, the interface and blockchain must be initialized with the following code.
```python
UI = UserInterface()
```
Following initial instantiation, the user is prompted whether to activate the testing interface. This testing interface enables the creation of multiple wallets simultaneously, as well as generating transactions and smart contracts between these testing wallets. These testing wallets are identical to wallets created normally on the blockchain, except for lacking any password security measure. To invoke the testing interface, after instantiation, use the following command.
```python
UI.testing_UI()
```
Subsequent interactions with the blockchain can be made via the following interface. If the blockchain contains testing wallets, these will also appear as they are saved on the blockchain, provided the blockchain has not been erased and instantiated again.
```python
UI.menu()
```
For more detailed information about the blockchain, it is recommended to consult the documentation file, `MACoin.pdf`. The documentation additionally also covers the blockchain limitations.

### Prerequisites
While this code does not require any specifics, certain libraries must be loaded or installed, for the code to run as intended.
Specifically, the following libraries are required:
```python
import hashlib
import datetime
import secrets
import pandas as pd
from IPython.display import display, HTML
import requests
import matplotlib.pyplot as plt
import yfinance as yf
from graphviz import Digraph
```
If any of the above library is not installed or not certain, the following code checks whether the libraries are already installed and otherwise installs them.
```python
import subprocess
import sys
# Function to install a package using pip
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
# List of required libraries
required_libraries = [
    'hashlib',
    'datetime',
    'secrets',
    'pandas',
    'IPython.display',
    'requests',
    'matplotlib',
    'yfinance',
    'graphviz']
# Dictionary to map module names to pip install names (for modules where they differ)
pip_names = {
    'IPython.display': 'ipython',
    'matplotlib': 'matplotlib',
    'pandas': 'pandas',
    'requests': 'requests',
    'yfinance': 'yfinance',
    'graphviz': 'graphviz',}
# Check and install missing libraries
for lib in required_libraries:
    try:
        exec(f"import {lib.split('.')[0]}")
        print(f"{lib} is already installed.")
    except ImportError:
        print(f"{lib} not found. Installing...")
        install(pip_names.get(lib, lib.split('.')[0]))
# Now import all libraries (this ensures they are available for use)
import hashlib
import datetime
import secrets
import pandas as pd
from IPython.display import display, HTML
import requests
import matplotlib.pyplot as plt
import yfinance as yf
from graphviz import Digraph
```
