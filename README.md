![status: inactive](https://img.shields.io/badge/status-inactive-red.svg)

This project is no longer actively developed or maintained.  

For more information about Cloud Storage, refer to our [documentation](https://cloud.google.com/storage).

# Getting Started with Google Cloud Storage API

Google Cloud Storage features a RESTful API that allows developers to
access their Cloud Storage objects and buckets.

## Summary

This demo allows you to test many of the API features of the Google Cloud
Storage XML API. For example, you can list project buckets, list objects within
a bucket, and upload an object to a bucket. For more information about the
Cloud Storage API, please see the [documentation][1].

Before running the application, install the dependencies (listed below) and
update the information in the client_secrets.json file with your client id and
secret available in the [Google API Console][2].

When running the application for the first time you will be asked to authorize
to the Google Cloud Storage API. The demo uses OAuth2.0 for authorization and
stores credentials locally in a file called gcs_credentials.dat.

You will then be asked for your Google Cloud Storage project ID, a numerical
value found in the API console. More information about projects can be found
in the [Cloud Storage documentation][3].

The demo stores your Cloud Storage project ID in a local file called
project_info.


## Dependencies

- [google-api-python-client-1.0][4]
- [httplib2-0.7.7][5]
- [python_gflags-2.0][6]

## Usage

  $ python main.py [--logging_level=log-level]

### Log levels include

- DEBUG
- INFO
- WARNING
- ERROR
- CRITICAL

Each log level shows the corresponding level of log messages.

[1]: https://developers.google.com/storage/docs/developer-guide
[2]: https://code.google.com/apis/console#access
[3]: https://developers.google.com/storage/docs/projects
[4]: https://developers.google.com/api-client-library/python/start/installation
[5]: http://code.google.com/p/httplib2/wiki/Install
[6]: http://code.google.com/p/python-gflags/downloads/list
