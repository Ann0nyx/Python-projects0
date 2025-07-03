# CITS1401 Project 2 — Population and Area Data Analysis

**Student:** Ann Maria Saji  
**Student ID:** 24529993  
**Semester:** 1, 2025  
**Date:** 19 May 2025  

---

## Project Aim

This Python 3 program reads and analyzes two CSV files containing Australian area and population data. It processes the data to provide three different analytical outputs based on population distribution across various geographical regions and age groups.

---

## Features

- Reads two input CSV files:  
  - Area data file (e.g., `SampleData_Areas_P2.csv`)  
  - Population data file (e.g., `SampleData_Populations_P2.csv`)  
- Cleans data by removing duplicates, invalid rows, and handling missing or negative values  
- Calculates:  
  1. Largest population area by age group for each state, SA3, and SA2 level  
  2. For each SA3 area with total population ≥ 150,000, finds the SA2 with largest population and calculates population standard deviation  
  3. Finds the pair of SA2 areas with the highest cosine similarity of age group population vectors within SA3 areas having at least 15 SA2 areas  
- Handles tie-breaking scenarios in calculations  
- No external modules required (only built-in Python functions used)  

---

## Usage

Run the main function with the two CSV files as arguments:

```python
from your_script_name import main

op1, op2, op3 = main('SampleData_Areas_P2.csv', 'SampleData_Populations_P2.csv')
print(op1)
print(op2)
print(op3)
