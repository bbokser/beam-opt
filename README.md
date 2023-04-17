# Beam Optimization

## Table of Contents

- [Intro](#intro)
- [Setup](#setup)
- [Info](#info)

---
## Intro

This repository contains Python code for mass optimization of a cantilever beam.

---

## Setup

1. Clone this directory wherever you want.

2. Make sure both Python 3.8 and pip are installed.

```shell
sudo apt install python3.8
sudo apt-get install python3-pip
python3.8 -m pip install --upgrade pip
```

2. I recommend setting up a virtual environment for this, as it requires the use of a number of specific Python packages.

```shell
sudo apt-get install python3.8-venv
cd beam-opt
python3.8 -m venv env
```
For more information on virtual environments: https://docs.python.org/3/library/venv.html
    
3. Activate the virtual environment, and then install the following packages.

```shell
source env/bin/activate
python3.8 -m pip install numpy nlopt matplotlib argparse
```
Don't use sudo here if you can help it, because it may modify your path and install the packages outside of the venv.

---

## Info

To run the optimization:

```shell
cd src
python3.8 main.py titanium 30 0.3 0.05 0.001 0.0004064
```

### Argparse Arguments

- Material
    - `titanium`, `aluminum`, or `cfrp`.
- Mass
    - The mass of the end-effector in kg.
- $L_x$
    - The length of the beam in meters.
- $L_y$
    - The axial offset distance of the end-effector mass from the beam axis.
- Max Deflection
    - Maximum beam deflection in meters.
- Minimum Wall Thickness
    - Minimum wall thickness in meters.
