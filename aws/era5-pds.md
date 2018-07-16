# ERA5 Data on S3 via AWS Public Dataset Program

To provide cloud-based access to ERA5 reanalysis data, Planet OS is working in conjunction with the [AWS Public Dataset Program](https://aws.amazon.com/opendata/public-datasets/) to publish and maintain regular updates of ERA5 data in S3.

This documentation outlines the dataset's details, available parameters, location and structure on S3, and includes examples of how to access and work with the data.

Please refer to the ECMWF website for the [official ERA5 data documentation.](https://confluence.ecmwf.int/display/CKB/ERA5+data+documentation)

## Introduction

ERA5 Climate reanalysis provides a numerical assessment of the modern climate. It is produced by a similar process as regular numerical weather forecast, a data assimilation and forecast loop, taking into account most of the available meteorological observations and analyses them with state of the art numerical model, producing a continuous, spatially consistent and homogeneous dataset.

The dataset provides all essential atmospheric meteorological parameters like, but not limited to, air temperature, pressure and wind at different altitudes, along with surface parameters like rainfall, soil moisture content and sea parameters like sea-surface temperature and wave height. ERA5 provides data at a considerably higher spatial and temporal resolution than its legacy counterpart ERA-Interim. ERA5 consists of high resolution version with 31 km horizontal resolution, and a reduced resolution ensemble version with 10 members.

Data is currently available since 2008, but will be continuously extended backwards, first until 1979 and then to 1950.

## Overview

<table>
  <tr>
    <td>Source</td>
    <td><a href="http://apps.ecmwf.int/data-catalogues/era5/">ECMWF WebAPI</a></td>
  </tr>
  <tr>
    <td>Category</td>
    <td>Climate Reanalysis</td>
  </tr>
  <tr>
    <td>Format</td>
    <td>NetCDF</td>
  </tr>
  <tr>
    <td>License</td>
    <td>Generated using Copernicus Climate Change Service Information 2018. See <a href="http://apps.ecmwf.int/datasets/licences/copernicus/">http://apps.ecmwf.int/datasets/licences/copernicus/</a> for additional information.</td>
  </tr>
  <tr>
    <td>Storage</td>
    <td>Amazon S3</td>
  </tr>
  <tr>
    <td>Location</td>
    <td><strong>Amazon Resource Name (ARN)</strong><br/>arn:aws:s3:::era5-pds<br/><br/>
        <strong>AWS Region</strong><br/>us-east-1<br/><br/>
        <strong>URL</strong><br/><a href="http://era5-pds.s3.amazonaws.com/">http://era5-pds.s3.amazonaws.com/</a>
    </td>
  </tr>
  <tr>
    <td>Update Frequency</td>
    <td>New data is published monthly. The ERA5 Public Release Plan is available at <a href="http://climate.copernicus.eu/products/climate-reanalysis">http://climate.copernicus.eu/products/climate-reanalysis</a></td>
  </tr>
</table>

## Variables

The table below lists the 18 ERA5 variables that are available on S3. All variables are surface or single level parameters sourced from the HRES sub-daily forecast stream.

<table>
  <tr>
    <th>Variable Name</th>
    <th>File Name</th>
  </tr>
  <tr>
    <td>10 metre U wind component</td>
    <td>eastward_wind_at_10_metres.nc</td>
  </tr>
  <tr>
    <td>10 metre V wind component</td>
    <td>northward_wind_at_10_metres.nc</td>
  </tr>
  <tr>
    <td>100 metre U wind component</td>
    <td>eastward_wind_at_100_metres.nc</td>
  </tr>
  <tr>
    <td>100 metre V wind component</td>
    <td>northward_wind_at_100_metres.nc</td>
  </tr>
  <tr>
    <td>2 metre dew point temperature</td>
    <td>dew_point_temperature_at_2_metres.nc</td>
  </tr>
  <tr>
    <td>2 metre temperature</td>
    <td>air_temperature_at_2_metres.nc</td>
  </tr>
  <tr>
    <td>2 metres maximum temperature since previous post-processing</td>
    <td>air_temperature_at_2_metres_1hour_Maximum.nc</td>
  </tr>
  <tr>
    <td>2 metres minimum temperature since previous post-processing</td>
    <td>air_temperature_at_2_metres_1hour_Minimum.nc</td>
  </tr>
  <tr>
    <td>Mean sea level pressure</td>
    <td>air_pressure_at_mean_sea_level.nc</td>
  </tr>
  <tr>
    <td>Sea surface temperature</td>
    <td>sea_surface_temperature.nc</td>
  </tr>
  <tr>
    <td>Mean wave period</td>
    <td>sea_surface_wave_mean_period.nc</td>
  </tr>
  <tr>
    <td>Mean direction of wind waves</td>
    <td>sea_surface_wind_wave_from_direction.nc</td>
  </tr>
  <tr>
    <td>Significant height of combined wind waves and swell</td>
    <td>significant_height_of_wind_and_swell_waves.nc</td>
  </tr>
  <tr>
    <td>Snow density</td>
    <td>snow_density.nc</td>
  </tr>
  <tr>
    <td>Snow depth</td>
    <td>lwe_thickness_of_surface_snow_amount.nc</td>
  </tr>
  <tr>
    <td>Surface pressure</td>
    <td>surface_air_pressure.nc</td>
  </tr>
  <tr>
    <td>Surface solar radiation downwards</td>
    <td>integral_wrt_time_of_surface_direct_downwelling_shortwave_flux_in_air_1hour_Accumulation.nc</td>
  </tr>
  <tr>
    <td>Total precipitation</td>
    <td>precipitation_amount_1hour_Accumulation.nc</td>
  </tr>
</table>

The date and time of the variable data is the valid time, with a mapping from forecast time to valid time corresponding to that outlined in [Table 0 of the ECMWF ERA5 documentation.](https://software.ecmwf.int/wiki/display/CKB/ERA5+data+documentation#ERA5datadocumentation-Dataorganisationandaccess) In this mapping, the first 12 forecast hours are used from each forecast run, which occur at 06:00 and 18:00 UTC. A sample highlighting key times of this mapping is included below for reference.

<table>
  <tr>
    <th colspan=2>Valid Time</th>
    <th colspan=3>ERA5 HRES Sub-Daily Forecast</th>
  </tr>
  <tr>
    <td>Date</td>
    <td>Time</td>
    <td>Date</td>
    <td>Forecast Run</td>
    <td>Step</td>
  </tr>
  <tr>
    <td>date</td>
    <td>00:00</td>
    <td>date - 1</td>
    <td>18:00</td>
    <td>6</td>
  </tr>
  <tr>
    <td>date</td>
    <td>06:00</td>
    <td>date - 1</td>
    <td>18:00</td>
    <td>12</td>
  </tr>
  <tr>
    <td>date</td>
    <td>07:00</td>
    <td>date</td>
    <td>06:00</td>
    <td>1</td>
  </tr>
  <tr>
    <td>date</td>
    <td>18:00</td>
    <td>date</td>
    <td>06:00</td>
    <td>12</td>
  </tr>
  <tr>
    <td>date</td>
    <td>19:00</td>
    <td>date</td>
    <td>18:00</td>
    <td>1</td>
  </tr>
  <tr>
    <td>date</td>
    <td>23:00</td>
    <td>date</td>
    <td>18:00</td>
    <td>5</td>
  </tr>
</table>

If there are specific variables you would like to recommend for future inclusion, please contact [datahub@intertrust.com](mailto:datahub@intertrust.com).

## Data Structure

The ERA5 dataset has been transformed to optimize access by specific variables and temporal ranges. To accommodate this, data is divided into distinct NetCDF granules organized by year, month, and variable name.

The data is structured as follows:

```
/{year}/{month}/main.nc
               /data/{var1}.nc
                    /{var2}.nc
                    /{....}.nc
                    /{varN}.nc
```

where **year** is expressed as four digits (e.g. YYYY) and **month** as two digits (e.g. MM). Individual data variables (**var1** through **varN**) use names corresponding to [NetCDF CF standard names convention](http://cfconventions.org) plus any applicable additional info, such as vertical coordinate.

Granule variable structure and metadata attributes are stored in **main.nc**. This file contains coordinate and auxiliary variable data, and is also annotated using NetCDF CF metadata conventions.

A sample path for air temperature would take the following form:

```
/2008/01/data/air_temperature_at_2_metres.nc
```

Note that due to the nature of the ERA5 forecast timing, which is run twice daily at 06:00 and 18:00 UTC, monthly data files begins with data from 07:00 on the first of the month and continue through 06:00 of the following month. This means the first six hours of data for each month are contained in the previous month’s file.

## Versioning

To provide a means for correcting potential processing errors in individual granule files, [bucket versioning](https://docs.aws.amazon.com/AmazonS3/latest/dev/Versioning.html) will be used. This solution allows for consistent S3 file paths for end users of the data, and also allows for recovery of previous file versions if necessary. Should an issue occur that requires the rewriting of data granules, we will publish details of the incident as well as the affected files on the ERA5 dataset page.

In the unlikely event that a major update impacting the data structure or its dimensionality be required, such changes would be published as a distinct version of the dataset.

## Data Access

The data is publicly available in the ERA5 S3 bucket (era5-pds) and may be directly accessed there. Please note that the best transfer speeds will be achieved by accessing the data from an EC2 instance located in the same AWS region as the S3 bucket (us-east-1).

Data may be accessed via http using the S3 REST API. To make a GET request, use the bucket name and the full key name for the object. For example, to download air temperature at 2 meters for January, 2008, submit a GET request to the following url: [http://era5-pds.s3.amazonaws.com/2008/01/data/air_temperature_at_2_metres.nc](http://era5-pds.s3.amazonaws.com/2008/01/data/air_temperature_at_2_metres.nc)

Another option is to use the [AWS SDK or CLI.](https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingAWSSDK.html) We’ve published a jupyter notebook on GitHub that provides an example of [how to access ERA5 data in python using boto](https://github.com/planet-os/notebooks/blob/master/aws/era5-s3-via-boto.ipynb).

This dataset is also accessible via the [Planet OS Datahub](https://data.planetos.com/datasets/ecmwf_era5), which provides a RESTful API that supports JSON and CSV responses to point and polygon based queries.

## Use Cases & Examples

* [Accessing ERA5 Data on S3 Using Boto](https://github.com/planet-os/notebooks/blob/master/aws/era5-s3-via-boto.ipynb)
* [Analyzing wind speed and temperature relation in Estonia](https://medium.com/planet-os/too-cold-for-more-wind-e6fa6038ec41)
* [Using the Planet OS Datahub API to work with ERA5 data in python](https://github.com/planet-os/notebooks/blob/master/api-examples/ERA5_tutorial.ipynb)
* [ERA5: The new champion of wind power modelling?](https://doi.org/10.1016/j.renene.2018.03.056)
* [Evaluation of global horizontal irradiance estimates](https://doi.org/10.1016/j.solener.2018.02.059)
