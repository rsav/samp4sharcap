# samp4sharcap

## Installation

### Python

- Retrieve the latest Miniconda installer for your architecture from https://docs.anaconda.com/free/miniconda/miniconda-other-installer-links/
- With conda, setup a python-3.4 environment to install astropy for using in SharpCap

```
    conda create -n sharpcap-py3.4 python=3.4 -c free
    conda activate sharpcap-py3.4
    pip install colorama==0.4.1 # because dependency version 0.4.2 won't install
    pip install --only-binary :all: astropy # NB: remove "--only-binary :all:" to build it if Visual Studio (Build Tools) is installed
```

- Note the python path in your conda env, this will be refered later as PPATH

```
    conda activate sharpcap-py3.4
    python -c "import sys; print(sys.path)" # copy result to clipboard => PPATH  
```

### NumSharp

- Install NumSharp.0.20.5.zip from github https://github.com/SciSharp/NumSharp: extract the zip file into a directory that we will refer later as NLIB

### Modifications of astropy

We need to modify astropy.samp to use NumSharp by editing the astropy __init__.py file which was installed by conda (example: C:\USERS\USER\\.conda\envs\sharpcap-py3.4\Lib\site-packages\astropy\__init__.py)

1. Make 2 changes in the function check_numpy

- set requirement_met = True
- comment the else block

It will look as below:
             
```     
def _check_numpy():
    """
    Check that Numpy is installed and it is of the minimum version we
    require.
    """
    # Note: We could have used distutils.version for this comparison,
    # but it seems like overkill to import distutils at runtime.
    requirement_met = True

    try:
        import NumSharp.np as numpy
    except ImportError:
        pass
    #else:
    #    from .utils import minversion
    #    requirement_met = minversion(numpy, __minimum_numpy_version__)

    if not requirement_met:
        msg = ("Numpy version {0} or later must be installed to use "
               "Astropy".format(__minimum_numpy_version__))
        raise ImportError(msg)

    return numpy
```


2. Comment the line with _initialize_astropy()


```
#_initialize_astropy()  
```


### Test

- Launch a SAMP hub (for example by launching Aladin Desktop)
- Start SharpCap-4.1 and open “Show Console” in the Scripting menu to open the Python Console
- Load the file samp.py (from this repo) in the Python editor (button load at the bottom of Python Console)
- Customize the script:

1. Set the path for padc_icon (the file is in this repo)
2. Set the path for NumSharp to NLIB as noted above in the line

```
clr.AddReferenceToFileAndPath(...)
```
3. Change sys.path to use modified astropy.samp installed with conda in the line

```
sys.path.append(...)
```

- Run samp_init() (in the Python Console) to init SAMP in IronPython

```
samp_init()
```

- Create the client 

```
c=SampClient()
```

- Interact with other SAMP Apps using the client Examples:

```
c.get_coords(‘c1’) # get reticle coordinates from Aladin
```

## Usage

After the Installation step above is performed you can 
 
- Launch a SAMP-enabled application with an embedded hub such a Aladin Desktop
- Run the customized samp.py script (Scripting/Run Script...) to see the new "SAMP" button that is setup at the right of the toolbar (below the menu).
- Click on the SAMP button to display the SAMP control Panel
- Send coordinates from a SAMP-enabled application 
- The coordinates will be displayed in the SAMP control panel
- You can click on the Slew button to slew the current mount to the position pointed
  
See screenshot Screenshot_SharpCap+Aladin.jpg in this repo.

