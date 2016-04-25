#Short guide to install python using Virtual Environment(linux)

### Install python

Okey, go to the following link: 

<http://conda.pydata.org/miniconda.html>

Download the proper miniconda installer for your system (linux is awesome for this)!

### INSTALL MINICONDA

On terminal, install Miniconda:

>cd download_directory/

>chmod +x Miniconda2-latest-Linux-x86_64.sh

>./Miniconda2-latest-Linux-x86_64.sh

while the script is running, you may choose the directory where miniconda will be installed.

The following lines will appear at the end of the installation - choose yes (it's a little more simple).


>Do you wish the installer to prepend the Miniconda2 install location

>to PATH in your /home/otel/.bashrc ? [yes|no]

>yes

Close and reopen your Terminal tab (or type 'source ~/.bashrc').

Now you will create a locally installed Virtual Environment using miniconda:

>conda install -name YourVirtualEnvironmentName python=2.7

###Activating miniconda virtual environment and installing python packages
Okey, your YourVirtualEnvironmentName environment is ready!

You need to activate by typing on terminal:

>source activate YourVirtualEnvironmentName

Your terminal line will look like:

>(YourVirtualEnvironmentName)YourUser@YourMachine:~$ 

Finally install the desired packages (in our case ipython matplotlib basemap xray scipy numpy)!

>conda install ipython matplotlib basemap xray scipy numpy

### What is anaconda and virtual environment?
Don't know what is anaconda and virtual environment? Research a little bit, but you can begin at:
<https://www.continuum.io/content/conda-data-science>