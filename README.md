# SLEAP-Autoanalysis
 
## Installation

Create a new conda environment that contains autosleap with the following command

<pre> ```console $ conda create -n autosleap -c mxwllmadden -c conda-forge autosleap``` </pre>
 
 
## Build Instructions

If you would like to build from source, you may do so using these commands.

<pre> ```console $ python -m build --sdist``` </pre>

<pre> ```console $ twine upload --respository pypi dist/*``` </pre>

<pre> ```console $ grayskull pypi autosleap``` </pre>

add ffmpeg to run dependancies

<pre> ```console $ conda build -c conda-forge autosleap``` </pre>