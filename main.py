# Copyright 2012 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Command-line sample for Google Cloud Storage.

Usage:
  python main.py [--logging_level=<log-level>]
"""

__author__ = 'kbrisbin@google.com (Kathryn Hurley)'

import logging
import os
import sys

import gflags
import httplib2
import oauth2client.client as oauthclient
import oauth2client.file as oauthfile
import oauth2client.tools as oauthtools

import gcs.gcs_commands as gcs_commands
from gcs.gcs_xml import GcsXml as Gcs

FLAGS = gflags.FLAGS

# The gflags module makes defining command-line options easy for
# applications. Run this program with the '--help' argument to see
# all the flags that it understands.
LOG_LEVELS = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
gflags.DEFINE_enum(
    'logging_level', 'INFO', LOG_LEVELS, 'Set the level of logging detail.')

CLIENT_SECRETS = 'client_secrets.json'
CREDENTIALS_FILE = 'gcs_credentials.dat'
PROJECT_FILE = 'project_info'
SCOPE = 'https://www.googleapis.com/auth/devstorage.full_control'


def init_client(auth_http, project_id):
  """Initializes the gcs.Gcs client.

  Clients are available per module. To switch the client, update the import
  statement above.

  Args:
    auth_http: An authorized httplib2.Http instance.
    project_id: A string Cloud Storage project id, ex: '123456'.

  Returns:
    An instance of gcs.Gcs.
  """
  gcs_client = Gcs(auth_http, project_id)
  return gcs_client


def get_project_id():
  """Retrieves Cloud Storage project id from user or file.

  Returns:
    The string project id.
  """
  project_file = None
  project_id = None
  try:
    project_file = open(PROJECT_FILE, 'r')
    project_id = project_file.read()
  except IOError:
    project_file = open(PROJECT_FILE, 'w')
    project_id = raw_input(
        'Enter your Cloud Storage project id (found in the API console): ')
    project_file.write(project_id)
  project_file.close()
  return project_id


def get_auth_http():
  """Runs the OAuth 2.0 installed application flow.

  Returns:
    An authorized httplib2.Http instance.
  """

  message = ('Please configure OAuth 2.0 by populating the client_secrets.json '
             'file found at: %s' % (os.path.join(os.path.dirname(__file__),
                                                 CLIENT_SECRETS)))
  flow = oauthclient.flow_from_clientsecrets(
      CLIENT_SECRETS, scope=SCOPE, message=message)
  storage = oauthfile.Storage(CREDENTIALS_FILE)
  credentials = storage.get()
  if credentials is None or credentials.invalid:
    credentials = oauthtools.run(flow, storage)
  http = httplib2.Http()
  auth_http = credentials.authorize(http)
  return auth_http


def main(argv):
  """Main application control."""
  try:
    argv = FLAGS(argv)
  except gflags.FlagsError, e:
    logging.error('%s\\nUsage: %s ARGS\\n%s', e, argv[0], FLAGS)
    sys.exit(1)

  # Set the logging according to the command-line flag
  numeric_level = getattr(logging, FLAGS.logging_level.upper())
  if not isinstance(numeric_level, int):
    logging.error('Invalid log level: %s', FLAGS.logging_level)
  logging.basicConfig(level=numeric_level)
  if FLAGS.logging_level == 'DEBUG': httplib2.debuglevel = 1

  auth_http = get_auth_http()
  project_id = get_project_id()
  gcs_client = init_client(auth_http, project_id)

  commands = [
      gcs_commands.GetBucketsCommand('Get all buckets', gcs_client),
      gcs_commands.GetBucketCommand('Get a bucket', gcs_client),
      gcs_commands.GetBucketCorsCommand('Get bucket CORS', gcs_client),
      gcs_commands.GetBucketLocationCommand('Get bucket location', gcs_client),
      gcs_commands.InsertBucketCommand('Create a bucket', gcs_client),
      gcs_commands.SetBucketCorsCommand('Set bucket CORS', gcs_client),
      gcs_commands.DeleteBucketCommand('Delete a bucket', gcs_client),
      gcs_commands.GetObjectCommand('Download an object', gcs_client),
      gcs_commands.GetObjectAclsCommand('Get object ACLs', gcs_client),
      gcs_commands.GetObjectMetadataCommand('Get object metadata', gcs_client),
      gcs_commands.InsertObjectCommand('Upload an object', gcs_client),
      gcs_commands.CopyObjectCommand('Copy an object', gcs_client),
      gcs_commands.DeleteObjectCommand('Delete an object', gcs_client),
  ]

  while True:
    print 'What would you like to do? Enter the number.'
    for i in range(len(commands)):
      print '%d: %s' % (i, commands[i].description)
    print '%d: Quit' % len(commands)

    selection = raw_input('Enter your selection: ')
    try:
      selection = int(selection)
    except ValueError, e:
      logging.error('Enter a number.')
      continue

    if selection > len(commands) or selection < 0:
      logging.error('Selection not recognized.')
      continue

    if selection == len(commands): break

    try:
      commands[selection].run_command()
    except Exception, e:
      logging.error('Error running command. Please try again.')
      logging.error(e)

if __name__ == '__main__':
  main(sys.argv)
