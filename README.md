# Algorithm Energy Complexity Analysis

This project investigates the **energy complexity** of classical
Divide and Conquer algorithms by experimentally measuring
execution time and energy consumption for different input sizes.

## Algorithms
- Merge Sort
- Quick Sort

## Energy Measurement Approach
Energy consumption is calculated using the following priority:
1. **pyRAPL** (Intel RAPL – CPU & DRAM)
2. **pyJoules** (RAPL-based energy measurement)
3. **Model-based estimation** using CPU utilization (psutil)

Energy is defined as:
E(n) = P_avg × T(n)

## Experimental Setup
- Programming Language: Python 3
- Libraries: psutil, matplotlib
- Input sizes: user-defined (low / medium / high)
- Each experiment is averaged over 5 runs

## How to Run
```bash
pip install -r requirements.txt
python main.py
