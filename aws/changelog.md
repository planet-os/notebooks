# List of ERA5 data changes

## v2

> TBD

### Dimensions & Grid Update. Longer Time Range.

 - New time range covering 1979 - 2019
 - Data is sourced from CDS API (previously from ECMWF API)
 - New grid resolution – 0.25 degree
 - Both – analysis and forecast variables are now available
   (previously only forecast variables were distributed)
 - Data start time changed to beging at 00 hour (comparing to 07 hour in v1)

## v1

> Jul 12, 2018

Initial dataset release covering years 2008-2018.



# Accessing previous versions
With every data release, like in the update from v1 to v2, the previous version will remain available for three months. Data versioning is implemented according to [AWS S3 object versioning](https://docs.aws.amazon.com/AmazonS3/latest/dev/ObjectVersioning.html). In order to get other than latest versions of object, one has to specify the `VersionId` parameter of AWS S3 API call.

`aws s3api get-object --bucket bucketname --key <prefix + filename> --version-id <aws_s3_version_hash>`

However, as the `version-id` cannot be set by user, there is a separate metadata field – `Planet OS version`, which contains with semantic version (like v1, v2, etc). Few more steps are required to find the right `version-id`:

 * List object versions hashes for all objects at once `aws s3api list-object-versions --bucket era5-pds --prefix <>`
 * List object tags, for each object separately, defining versions found in previous step `aws s3api get-object-tagging --bucket era5-pds --key <prefix + filename> --version-id <aws_s3_version_hash>`
