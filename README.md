##Notebooks##

A collection of Planet OS Jupyter notebooks.

###Requirements###

####[Jupyter Notebook](http://jupyter.org/)####

The Jupyter Notebook is a web application that allows you to create and share documents that contain live code, equations, visualizations and explanatory text.

Please refer to the [Jupyter documentation](http://jupyter.readthedocs.org/en/latest/) for [installation instructions](http://jupyter.readthedocs.org/en/latest/install.html).

###Recommendations###

Some notebooks may require additional python modules. If you attempt to run a notebook and receive an import error, it is likely that your local python installation is missing a requirement.

If you're using [virtualenv](https://virtualenv.pypa.io/en/latest/) and [pip](https://pip.pypa.io/en/stable/), a requirements.txt file is included with the required dependencies. Create or activate your virtual environment and run the following command to install the dependencies.

`pip install -r requirements.txt`

###Getting Started###

####Launch Jupyter Notebook####

Launch Jupyter with the following command:

`jupyter notebook`

By default, the command above will open a new browser tab at http://127.0.0.1:8888 which lists the available notebooks in a directory view.

####Select a Notebook####

The example notebooks are organized into directories. A good place to begin is the `/api-examples` directory. Using the Jupyter web UI, navigate into the directory and select a notebook to view it.
