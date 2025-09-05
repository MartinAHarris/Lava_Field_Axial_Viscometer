# README.txt

## Overview
This project contains three Python scripts for processing force–distance–time data, selecting regions of interest, and calculating viscosity. 
The scripts use Tkinter for file dialogs, Pandas and NumPy for data handling, and Matplotlib for plotting and interactive selection.

The workflow is:
1. First script – Load raw data and interactively select the first region of interest.
2. Second script – Process the selected data, calculate velocity, viscosity, and export results.
3. Third script – Refine the selection with another interactive region of interest.

---

## Requirements

### Python version
- Python 3.8 or higher (recommended 3.10+)

### Required packages

The scripts depend on the following packages:

**Standard library (no installation required):**
- os
- sys
- warnings

**External packages (must be installed with pip):**
- numpy
- pandas
- matplotlib
- tk (Tkinter)

### Installation

1. Make sure you have Python installed:
   - Download from: https://www.python.org/downloads/

2. (Optional but recommended) Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate   # On Linux/Mac
   venv\Scripts\activate    # On Windows
   ```

3. Install the required packages:
   ```
   pip install numpy pandas matplotlib
   ```

   > Note: Tkinter is included with most Python distributions. 
   > If it is missing, install it with your system package manager:
   > - Ubuntu/Debian: `sudo apt-get install python3-tk`
   > - macOS (Homebrew): `brew install python-tk`
   > - Windows: Tkinter is included in the standard installer.

---

## Running the scripts

1. Place your `.txt` data files into a working directory.
2. Run each script in order:
   ```
   python script1.py
   python script2.py
   python script3.py
   ```
3. Follow the on-screen file dialog prompts to select input files.
4. Processed data will be saved as `.txt` and `.csv` files in the same directory.

---

## Output files

- `_first_selected_dat.txt` → Output of the first selection.
- `_second_selected_dat.txt` → Output of the second selection.
- `_processed_dat.txt` and `_processed_dat.csv` → Final processed data including calibrated viscosity, smoothed viscosity, depth, and velocity.
