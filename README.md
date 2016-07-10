## Notebooks

A collection of Planet OS Jupyter notebooks.

## Requirements

### [Python 3](https://www.python.org/)

The notebooks included in this repository are intended for use with Python 3. Please refer to the [python downloads page](https://www.python.org/downloads/) for an appropriate version for your OS.

### [Jupyter Notebook](http://jupyter.org/)

The Jupyter Notebook is a web application that allows you to create and share documents that contain live code, equations, visualizations and explanatory text.

Please refer to the [Jupyter documentation](http://jupyter.readthedocs.org/en/latest/) for [installation instructions](http://jupyter.readthedocs.org/en/latest/install.html).

### [virtualenv](https://virtualenv.pypa.io/en/latest/) and [pip](https://pip.pypa.io/en/stable/)

Some notebooks may require additional python modules. If you attempt to run a notebook and receive an import error, it is likely that your local python installation is missing a requirement.

We recommend using [virtualenv](https://virtualenv.pypa.io/en/latest/) and [pip](https://pip.pypa.io/en/stable/) to create an environment for running the notebooks.

When creating your virtualenv, be sure to do so using python 3. Some systems ship with python 2 and will use that version as the default.

A requirements.txt file is included with the required notebook dependencies. To install them, activate your virtual environment and run the following command:

`pip install -r requirements.txt`

## Getting Started

### Have Your API Key Ready

The example notebooks will require a Planet OS API key to run. If you do not have an account, you'll need to [sign up for one](http://data.planetos.com/plans).

You can view your API key on the [Planet OS account settings page](http://data.planetos.com/account/settings/). You'll need to insert your key in the notebook to authorize the API calls, so keep it handy in your clipboard or a browser tab.

### Launch Jupyter Notebook

Launch Jupyter with the following command:

`jupyter notebook` or `ipython3 notebook`

By default, the command above will open a new browser tab at http://127.0.0.1:8888 which lists the available notebooks in a directory view.

### Select a Notebook

The example notebooks are organized into directories. A good place to begin is the `/api-examples` directory. Using the Jupyter web UI, navigate into the directory and select a notebook to view it.
