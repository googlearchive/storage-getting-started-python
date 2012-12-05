Summary:

This demo allows you to test many of the API features of the Google Cloud
Storage XML API. For example, you can list project buckets, list objects within
a bucket, and upload an object to a bucket. For more information about the
Cloud Storage API, please see the documentation:

https://developers.google.com/storage/docs/developer-guide

Before running the application, install the dependencies (listed below) and
update the information in the client_secrets.json file with your client id and
secret available in the Google API Console:

https://code.google.com/apis/console#access

When running the application for the first time you will be asked to authorize
to the Google Cloud Storage API. The demo uses OAuth2.0 for authorization and
stores credentials locally in a file called gcs_credentials.dat.

You will then be asked for your Google Cloud Storage project ID, a numerical
value found in the API console. More information about projects can be found
here:

https://developers.google.com/storage/docs/projects

The demo stores your Cloud Storage project ID in a local file called
project_info.


Dependencies:

  * google-api-python-client-1.0
    Installation: https://developers.google.com/api-client-library/python/start/installation
  * httplib2-0.7.7
    Installation: http://code.google.com/p/httplib2/wiki/Install
  * python_gflags-2.0
    Download: http://code.google.com/p/python-gflags/downloads/list


Usage:

  $ python main.py [--logging_level=<log-level>]

Log levels include:

  * DEBUG
  * INFO
  * WARNING
  * ERROR
  * CRITICAL

Each log level shows the corresponding level of log messages.
