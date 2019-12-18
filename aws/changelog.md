# List of changes

## Data Updates

|    | Release date | Description                                               |
|:---|:-------------|:----------------------------------------------------------|
| v2 | TBD          | Dimensions, grid, and other changes due to changes at the data source |
| v1 |              | Initial release                                           |
|    |              |                                                           |

## Detailed update breakdown

| Version | Change                 | Description                                                                                                           |
|:--------|:-----------------------|:----------------------------------------------------------------------------------------------------------------------|
| v2      | start year 1979        | change start year from 2008, as it was previously, to 1979                                                            |
| v2      | CDS API                | Change data download source from ECMWF API to CDS API                                                                 |
| v2      | resolution 0.25 degree | Data resolution change caused by resolution change in distribution source                                             |
| v2      | Analysis vs forecast   | In v1, all the variables where forecast variables. In v2, they can be either, but not from both for the same variable |
| v2      | Data start time        | In v1, all the files started on the hour 7 of a day, in v2, it is 00                                                  |
| v2      | Object versioning      |                                                                                                                       |

## Accessing previous versions
With every data release, like in the update from v1 to v2, the previous version will remain available for three months. Data versioning is implemented according to [AWS S3 object versioning](https://docs.aws.amazon.com/AmazonS3/latest/dev/ObjectVersioning.html). In order to get other than latest versions of object, one has to specify the `VersionId` parameter of AWS S3 API call.

`aws s3api get-object --bucket bucketname --key <prefix + filename> --version-id <aws_s3_version_hash>`

However, as the `version-id` cannot be set by user, there is a separate metadata field – `Planet OS version`, which contains with semantic version (like v1, v2, etc). Few more steps are required to find the right `version-id`:

 * List object versions hashes for all objects at once `aws s3api list-object-versions --bucket era5-pds --prefix <>`
 * List object tags, for each object separately, defining versions found in previous step `aws s3api get-object-tagging --bucket era5-pds --key <prefix + filename> --version-id <aws_s3_version_hash>`
