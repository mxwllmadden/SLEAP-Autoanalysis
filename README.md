# SLEAP-Autoanalysis
 
## Installation

Create a new conda environment that contains autosleap with the following command

<pre> conda create -n autosleap -c mxwllmadden -c conda-forge autosleap </pre>

 ## Use

 autosleap can be imported as a python package using

 '''python
 import autosleap
 '''
 
## Build Instructions (for my own reference)

If you would like to build from source, you may do so using these commands.

<pre> python -m build --sdist </pre>

<pre> twine upload --respository pypi dist </pre>

<pre> grayskull pypi autosleap </pre>

add ffmpeg to run dependancies and ensure that all run dependancies are in test requires

<pre> conda build -c conda-forge autosleap </pre>
