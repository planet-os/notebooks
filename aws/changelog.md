# List of changes

## Releases

|    | Release date | Description                                               |
|:---|:-------------|:----------------------------------------------------------|
| v2 |              | Dimension and other changes due to changes in data source |
| v1 |              | Initial release                                           |
|    |              |                                                           |


| Version | Change                 | Description                                                                                                           |
|:--------|:-----------------------|:----------------------------------------------------------------------------------------------------------------------|
| v2      | start year 1979        | change start year from 2008, as it was previously, to 1979                                                            |
| v2      | CDS API                | Change data download source from ECMWF API to CDS API                                                                 |
| v2      | resolution 0.25 degree | Data resolution change caused by resolution change in distribution source                                             |
| v2      | Analysis vs forecast   | In v1, all the variables where forecast variables. In v2, they can be either, but not from both for the same variable |
| v2      | Data start time        | In v1, all the files started on the hour 7 of a day, in v2, it is 00                                                  |
| v2      | Object versioning      |                                                                                                                       |

## Accessing previous versions
When we release a new version of data, like in the change from v1 to v2, the v1 version will remain available for three month period. For separation of versions, [AWS S3 object versioning](https://docs.aws.amazon.com/AmazonS3/latest/dev/ObjectVersioning.html) is used. In order to get other than latest versions of object, one has to specify the `VersionId` parameter.

`aws s3api get-object --bucket bucketname --key <prefix + filename> --version-id <something like Cu9ksraX_OOpbAtobdlYuNPCoJFY4N3S>`

However, as the `version-id` cannot be set by user, we define the version in a separate metadata field `Planet OS version`, so another steps are needed to actually find the `version-id`.

List object versions for all object at once `aws s3api list-object-versions --bucket era5-pds --prefix <>`

List object tags, for each object separately, defining versions found in previous step `aws s3api get-object-tagging --bucket era5-pds --key <prefix + filename> --version-id <something like IjLAMp_1ZfuarZ9bYbzXIWtb7yYdpqou>`
