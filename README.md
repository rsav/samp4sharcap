# samp4sharcap

## Installation

- Retrieve the latest Miniconda installer for your architecture
- With conda, setup a python-3.4 environment to install astropy for using in SharpCap

```
    conda create -n sharpcap-py3.4 python=3.4 -c free
    conda activate sharpcap-py3.4
    pip install colorama==0.4.1 # because dependency version 0.4.2 won't install
    pip install --only-binary :all: astropy # NB: remove "--only-binary :all:" to build it if Visual Studio (Build Tools) is installed
```

- Get the python path in conda env

```
    conda activate sharpcap-py3.4
    python -c "import sys; print(sys.path)" # copy result to clipboard => PPATH  
```

- Install NumSharp.0.20.5.zip from github https://github.com/SciSharp/NumSharp
    - Extract zip into NLIB (example C:\USERS\USER\Lib)

- Modify astropy.samp to use NumSharp 
    - Edit the astropy __init__.py file which was installed by conda (example: C:\USERS\USER\.conda\envs\sharpcap-py3.4\Lib\site-packages\astropy\__init__.py) 
        - 1. Change function check_numpy as below:
             
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

        - 2. Comment the line with _initialize_astropy()
```
#_initialize_astropy()  
```

- Start SharpCap-4.1 and open “Show Console” in the Scripting menu
- Load file in the editor (bottom of Console): samp.py
- Init SAMP in IronPython
```
samp_init()
```

- Init the client 

```
c=SampClient()
```

- Interact with other SAMP Apps. Examples:

```
c.get_coords(‘c1’) # get reticle coordinates from Aladin
```


