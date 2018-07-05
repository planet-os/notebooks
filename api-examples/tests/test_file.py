import os
import subprocess
import tempfile
import nbformat

def _notebook_run(path):
    """Execute a notebook via nbconvert and collect output.
       :returns (parsed nb object, execution errors)
    """
    dirname, __ = os.path.split(path)
    os.chdir(dirname)
    with tempfile.NamedTemporaryFile(suffix=".ipynb") as fout:
        args = ["jupyter nbconvert", "--to", "notebook", "--execute",
          "--ExecutePreprocessor.timeout=1000",
          "--output", fout.name, path]

        command = ' '.join(args)
        print (command)

        subprocess.check_call([command],shell=True)

        fout.seek(0)
        nb = nbformat.read(fout, nbformat.current_nbformat)

    errors = [output for cell in nb.cells if "outputs" in cell
                     for output in cell["outputs"]\
                     if output.output_type == "error"]

    return nb, errors

def _listdir_ipynb(folder):
    files = [file for file in os.listdir(folder) if file.endswith('ipynb')]
    return files

def Test_ipynb(filename):
    nb, errors = _notebook_run(filename)
    assert errors == []

folder = '/Users/etoodu/desktop/planetOS/git/notebooks/api-examples/'

done = ['BOM_australia_demo.ipynb','PlanetOS_WAve_Models.ipynb','ARC2_CHIRPS_example.py.ipynb','fmi_hirlam_metno_and_gfs.ipynb','swan-oahu-api.ipynb',
        'rbsn_era5_comparison.ipynb','modis_snow_cover_demo.ipynb','dataset-metadata-api.ipynb','gfs-api.ipynb','model-comparisons.ipynb','cams_air_quality_demo.ipynb',
        'hycom-api.ipynb','cfsr_demo.ipynb','CHIRPS_example.ipynb','cams_air_quality_hawaii.ipynb','ndbc-wavewatch-iii.ipynb','ERA5_tutorial.ipynb','rtofs-reftime-vs-time.ipynb',
        'gefs-api.ipynb']

ignore = ['GFS_public_full_demo_main.ipynb','ndbc-spectral-wave-density-data-validation.ipynb',
          'Metno_wind_demo.ipynb','CFSv2_usage_example.ipynb','SMAP_brazil.ipynb','SMAP_package-api.ipynb',
          'URD-CONUS_CHIRP_with_package.ipynb']

notebooks = _listdir_ipynb(folder)
for file in notebooks:
    if not file in done and not file in ignore:
        print ('testing ' + file)
        filename = folder + file
        Test_ipynb(filename)