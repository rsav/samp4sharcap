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

We need to modify astropy.samp to use NumSharp by editing the astropy __init__.py file which was installed by conda (example: C:\USERS\USER\.conda\envs\sharpcap-py3.4\Lib\site-packages\astropy\__init__.py)

1. Change function check_numpy as below:
             
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
- Configure the script:

TBD

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

TBD


