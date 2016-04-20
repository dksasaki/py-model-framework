Short guide to install python using Virtual Environment(linux)

1)to install python

Okey, go to the following link: 

<http://conda.pydata.org/miniconda.html>

Download the proper miniconda installer for your system (linux is awesome for this)!

2)using the installer file, install Miniconda

>cd download_directory/
>chmod +x Miniconda2-latest-Linux-x86_64.sh
>./Miniconda2-latest-Linux-x86_64.sh

You may choose the directory miniconda will be installed, while the script is running.
The following lines will appear at the end of the installation - choose yes (it's a little more simple).


>Do you wish the installer to prepend the Miniconda2 install location
>to PATH in your /home/otel/.bashrc ? [yes|no]
>yes

Close and reopen your Terminal tab (or type 'source ~/.bashrc').
Now you will create a locally installed Virtual Environment using miniconda:

>conda install -name YourVirtualEnvironmentName python=2.7

Okey, your YourVirtualEnvironmentName environment is ready!
You need to activate by typing on terminal:

>source activate YourVirtualEnvironmentName

Your terminal line will look like:

>(YourVirtualEnvironmentName)YourUser@YourMachine:~$ 

Finally install the desired packages (in our case ipython matplotlib basemap xray scipy numpy)!

>conda install ipython matplotlib basemap xray scipy numpy

Don't know what is anaconda and virtual environment? Research a little bit, but you can begin at:
<https://www.continuum.io/content/conda-data-science>