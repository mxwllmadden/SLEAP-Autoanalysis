# SLEAP-Autoanalysis
 
## Installation

Create a new conda environment that contains autosleap with the following command

```console
conda create -n autosleap -c mxwllmadden -c conda-forge autosleap
```

Alternatively, autosleap can be installed into an existing environment using 

```console
conda activate my-environment
conda install -c mxwllmadden autosleap
```

## Using Autosleap

### Using Autosleap (Command Line)

To use the autosleap CLI use the `autosleap` keyword from inside the autosleap environment

### Using Autosleap Wizard

The autosleap GUI wizard can be run using `autosleap wizard`

### Using Autosleap as a python package

Autosleap includes some useful utility and visualization functions in addition to the autosleap utility. Access these via

```python
import autosleap
```
 
## Build Instructions (for my own reference)

If you would like to build from source, you may do so using these commands.

```console
python -m build --sdist
```

```console
twine upload --respository pypi dist
```

```console
grayskull pypi autosleap
```

add ffmpeg to run dependancies and ensure that all run dependancies are in test requires

```console
conda build -c conda-forge autosleap
```
