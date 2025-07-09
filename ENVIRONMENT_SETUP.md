# Virtual Environment Setup Guide

## Prerequisites
- Python 3.x installed on your system
- pip package manager

## Virtual Environment Setup

### 1. Virtual Environment Creation
The virtual environment has been created with the name `snowpylot-env` and is located in the project root directory.

### 2. Activating the Virtual Environment

**On macOS/Linux:**
```bash
source snowpylot-env/bin/activate
```

**On Windows:**
```bash
snowpylot-env\Scripts\activate
```

When activated, you should see `(snowpylot-env)` at the beginning of your command prompt.

### 3. Deactivating the Virtual Environment
To deactivate the virtual environment, simply run:
```bash
deactivate
```

## Installed Packages

The following packages have been installed in the virtual environment:
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **matplotlib**: Plotting and visualization
- **seaborn**: Statistical data visualization
- **snowpylot**: Snow pit data analysis (CAAML parser)
- **jupyter**: Interactive notebook environment

## Running the Notebooks

1. Activate the virtual environment:
   ```bash
   source snowpylot-env/bin/activate
   ```

2. Navigate to the notebooks directory:
   ```bash
   cd notebooks
   ```

3. Start Jupyter:
   ```bash
   jupyter notebook
   ```

4. Open the desired notebook file (e.g., `weight_and_bending_stiffness_rosendahl.ipynb`)

## Requirements File

A `requirements.txt` file has been generated with all package versions. To recreate this environment on another machine:

1. Create a new virtual environment:
   ```bash
   python3 -m venv snowpylot-env
   ```

2. Activate it:
   ```bash
   source snowpylot-env/bin/activate
   ```

3. Install the requirements:
   ```bash
   pip install -r requirements.txt
   ```

## Testing the Installation

You can test if the snowpylot library is working correctly by running:
```python
from snowpylot import caaml_parser
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
```

If no errors occur, your environment is set up correctly!

## Data Files

The repository includes:
- **Snow pit data**: Located in `snowpits/` directory with seasonal organization
- **Geldsetzer table**: CSV file for density calculations (`notebooks/geldsetzer_table.csv`)
- **Notebooks**: Analysis notebooks in `notebooks/` directory 