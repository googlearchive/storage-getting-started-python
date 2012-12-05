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

"""Command line for Cloud Storage demo.

Retrieves input from user, runs Cloud Storage API request, displays output.
"""

import logging
import os

import gcs_error


class UserInput(object):
  """Input from the user.

  Attributes:
    parameters: Dictionary of parameters to control user input.
    values: A dictionary mapping a key to the value entered by the user.
  """

  def __init__(self, parameters):
    """Initialize UserInput with parameters.

    Parameters is a dictionary, mapping a key to a dictionary of input
    requirements. Input requirements include text, default, and processing.
    The structure is as follows:

    {
        <key>: {
            'text': <visible-text>
            'default': <default-value>
            'processing': <processing-method>
        }
    }

    <ul>
    <li>key: The key value gives access to the user-entered value stored
    in the values class attribute.</li>
    <li>'text': Displays a name for the input at the console.</li>
    <li>'default': Displays an optional default value if left blank.</li>
    <li>'processing': An optional method for post-processing the entered user
    input.</li>
    </ul>

    'text' and 'default' are used in the display prompt, with the format:

    "Enter <text> (defaults to <default> if blank):"

    Args:
      parameters: Dictionary of parameters to control user input.
    """
    self.parameters = parameters
    self.values = {}

  def get_user_input_values(self):
    """Gets input from the user at the command prompt.

    Maps the keys from the parameters class attribute to the user-entered
    values in the values class attribute.
    """
    if self.parameters:
      for key in self.parameters:
        user_input = self.parameters[key]
        input_value = self._get_input(
            user_input['text'],
            default=user_input.get('default', None))
        processing_method = user_input.get('processing', None)
        if processing_method:
          input_value = processing_method(input_value)
        self.values[key] = input_value

  def _get_input(self, text, default=None):
    """Get input from the user.

    Displays as "Enter <text> (defaults to <default> if blank):"

    Args:
      text: String value to display to user when asking for input.
      default: The string default value if left blank. If none, the value is
          required.

    Returns:
      The string value entered by the user.
    """
    default_string = ''
    if default:
      default_string = ' (defaults to %s if blank)' % default
    input_value = raw_input('Enter %s%s: ' % (text, default_string))
    required = not default
    while not input_value and required:
      logging.error('%s cannot be blank.', text)
      input_value = raw_input('Please enter a %s: ' % text)
    return input_value


class GcsCommand(object):
  """Retrieves command line input, calls Cloud Storage API, handles output.

  Attributes:
    description: The description for the user menu.
  """

  UPLOAD_FILE_NAME = 'cloud-storage-upload-test.txt'
  DEFAULT_BUCKET_USER_INPUT = {'text': 'Bucket Name'}
  DEFAULT_OBJECT_USER_INPUT = {'text': 'Object Name'}

  def __init__(self, description, gcs_client, parameters=None):
    """Initialize GcsCommand with description, gcs_client, and parameters.

    Args:
      description: The description for the user menu.
      gcs_client: An instance of gcs.Gcs.
      parameters: Dictionary of parameters to control user input.
    """
    self.description = description
    self._gcs_client = gcs_client
    self._input = UserInput(parameters)

  def run_command(self):
    """Retrieve command line input, call Cloud Storage API, handle output.

    Raises:
      gcs_error.GcsError if API call fails.
      ValueError if user entered an invalid value.
    """
    self._input.get_user_input_values()
    try:
      result = self._run_api_command()
    except gcs_error.GcsError, ge:
      logging.error('%s failed: %s', self.description, ge)
      raise
    except ValueError, ve:
      logging.error('%s failed: %s', self.description, ve.message)
      raise
    self._process_result(result)

  def _run_api_command(self):
    """Run the appropriate Cloud Storage API call."""
    raise NotImplementedError('You need to override this function')

  def _process_result(self, result=None):
    """Process the results.

    Args:
      result: The string results of the API call.
    """
    if result: logging.info(result)


class GetBucketsCommand(GcsCommand):
  """Get all Cloud Storage buckets for a project."""

  def _run_api_command(self):
    """Get all Cloud Storage buckets for a project.

    Returns:
      The string API call results.
    """
    results = self._gcs_client.get_buckets()
    return results


class GetBucketCommand(GcsCommand):
  """Get the Cloud Storage bucket."""

  def __init__(self, description, gcs_client):
    """Initialize GetBucketCommand with description and gcs_client.

    Args:
      description: The description for the user menu.
      gcs_client: An instance of gcs.Gcs.
    """
    params = {'bucket': self.DEFAULT_BUCKET_USER_INPUT}
    super(GetBucketCommand, self).__init__(description, gcs_client, params)

  def _run_api_command(self):
    """Get the Cloud Storage bucket.

    Returns:
      The string API call results.
    """
    results = self._gcs_client.get_bucket(self._input.values['bucket'])
    return results


class GetBucketCorsCommand(GcsCommand):
  """Get the Cloud Storage bucket CORS info."""

  def __init__(self, description, gcs_client):
    """Initialize GetBucketCorsCommand with description and gcs_client.

    Args:
      description: The description for the user menu.
      gcs_client: An instance of gcs.Gcs.
    """
    params = {'bucket': self.DEFAULT_BUCKET_USER_INPUT}
    super(GetBucketCorsCommand, self).__init__(description, gcs_client, params)

  def _run_api_command(self):
    """Get the Cloud Storage bucket CORS info.

    Returns:
      The string API call results.
    """
    results = self._gcs_client.get_bucket_cors(self._input.values['bucket'])
    return results


class GetBucketLocationCommand(GcsCommand):
  """Get the Cloud Storage bucket location."""

  def __init__(self, description, gcs_client):
    """Initialize GetBucketLocationCommand with description and gcs_client.

    Args:
      description: The description for the user menu.
      gcs_client: An instance of gcs.Gcs.
    """
    params = {'bucket': self.DEFAULT_BUCKET_USER_INPUT}
    super(GetBucketLocationCommand, self).__init__(
        description, gcs_client, params)

  def _run_api_command(self):
    """Get the Cloud Storage bucket location.

    Returns:
      The string API call results.
    """
    results = self._gcs_client.get_bucket_location(
        self._input.values['bucket'])
    return results


class InsertBucketCommand(GcsCommand):
  """Create a new bucket."""

  def __init__(self, description, gcs_client):
    """Initialize InsertBucketCommand with description and gcs_client.

    Args:
      description: The description for the user menu.
      gcs_client: An instance of gcs.Gcs.
    """
    params = {'bucket': self.DEFAULT_BUCKET_USER_INPUT}
    super(InsertBucketCommand, self).__init__(description, gcs_client, params)

  def _run_api_command(self):
    """Create a new bucket.

    Returns:
      The Bucket created successfully string message.
    """
    self._gcs_client.insert_bucket(self._input.values['bucket'])
    return 'Bucket "%s" created' % self._input.values['bucket']


class SetBucketCorsCommand(GcsCommand):
  """Set the CORS on a bucket."""

  def __init__(self, description, gcs_client):
    """Initialize SetBucketCorsCommand with description and gcs_client.

    Args:
      description: The description for the user menu.
      gcs_client: An instance of gcs.Gcs.
    """
    params = {}
    params['bucket'] = self.DEFAULT_BUCKET_USER_INPUT
    params['origins'] = {
        'text': 'a comma-separated list of origins',
        'default': gcs_client.default_origin,
        'processing': lambda origins: origins.split(',')
    }
    params['methods'] = {
        'text': 'a comma-separated list of methods',
        'default': gcs_client.default_method,
        'processing': lambda methods: methods.split(',')
    }
    params['headers'] = {
        'text': 'a comma-separated list of headers',
        'default': gcs_client.default_response_header,
        'processing': lambda headers: headers.split(',')
    }
    params['age'] = {
        'text': 'max cache time in seconds',
        'default': gcs_client.default_max_age_sec
    }
    super(SetBucketCorsCommand, self).__init__(description, gcs_client, params)

  def _run_api_command(self):
    """Set the CORS on a bucket.

    Returns:
      The CORS set successfully string message.
    """
    self._gcs_client.set_bucket_cors(
        self._input.values['bucket'],
        self._input.values['origins'],
        self._input.values['methods'],
        self._input.values['headers'],
        self._input.values['age'])
    return 'Cors set successfully'


class DeleteBucketCommand(GcsCommand):
  """Delete a bucket."""

  def __init__(self, description, gcs_client):
    """Initialize DeleteBucketCommand with description and gcs_client.

    Args:
      description: The description for the user menu.
      gcs_client: An instance of gcs.Gcs.
    """
    params = {'bucket': self.DEFAULT_BUCKET_USER_INPUT}
    super(DeleteBucketCommand, self).__init__(description, gcs_client, params)

  def _run_api_command(self):
    """Delete a bucket.

    Returns:
      The Bucket deleted string message.
    """
    self._gcs_client.delete_bucket(self._input.values['bucket'])
    return self._input.values['bucket'] + ' deleted.'


class GetObjectCommand(GcsCommand):
  """Get an object."""

  def __init__(self, description, gcs_client):
    """Initialize GetObjectCommand with description and gcs_client.

    Args:
      description: The description for the user menu.
      gcs_client: An instance of gcs.Gcs.
    """
    params = {}
    params['bucket'] = self.DEFAULT_BUCKET_USER_INPUT
    params['object'] = self.DEFAULT_OBJECT_USER_INPUT
    super(GetObjectCommand, self).__init__(description, gcs_client, params)

  def _run_api_command(self):
    """Get an object.

    Returns:
      The string API call results.
    """
    results = self._gcs_client.get_object(
        self._input.values['bucket'],
        self._input.values['object'])
    return results

  def _process_result(self, result=None):
    """Saves API call results to file.

    Args:
      result: The string API call results.
    """
    object_name = self._input.values['object']
    if object_name.count('/'):
      object_name = object_name.split('/')[-1]
    downloaded_file = open(object_name, 'w')
    downloaded_file.write(result)
    logging.info('File downloaded locally to ' + object_name)


class GetObjectAclsCommand(GcsCommand):
  """Get an object's ACLs."""

  def __init__(self, description, gcs_client):
    """Initialize GetObjectAclsCommand with description and gcs_client.

    Args:
      description: The description for the user menu.
      gcs_client: An instance of gcs.Gcs.
    """
    params = {}
    params['bucket'] = self.DEFAULT_BUCKET_USER_INPUT
    params['object'] = self.DEFAULT_OBJECT_USER_INPUT
    super(GetObjectAclsCommand, self).__init__(description, gcs_client, params)

  def _run_api_command(self):
    """Get an object's ACLs.

    Returns:
      The string API call results.
    """
    results = self._gcs_client.get_object_acls(
        self._input.values['bucket'],
        self._input.values['object'])
    return results


class GetObjectMetadataCommand(GcsCommand):
  """Get an object's metadata."""

  def __init__(self, description, gcs_client):
    """Initialize GetObjectMetadataCommand with description and gcs_client.

    Args:
      description: The description for the user menu.
      gcs_client: An instance of gcs.Gcs.
    """
    params = {}
    params['bucket'] = self.DEFAULT_BUCKET_USER_INPUT
    params['object'] = self.DEFAULT_OBJECT_USER_INPUT
    super(GetObjectMetadataCommand, self).__init__(
        description, gcs_client, params)

  def _run_api_command(self):
    """Get an object's metadata.

    Returns:
      The string API call results.
    """
    results = self._gcs_client.get_object_metadata(
        self._input.values['bucket'],
        self._input.values['object'])
    return results


class InsertObjectCommand(GcsCommand):
  """Insert a new object."""

  def __init__(self, description, gcs_client):
    """Initialize InsertObjectCommand with description and gcs_client.

    Args:
      description: The description for the user menu.
      gcs_client: An instance of gcs.Gcs.
    """
    params = {}
    params['file-path'] = {
        'text': 'path to file',
        'default': self.UPLOAD_FILE_NAME,
        'processing': self._process_input
    }
    params['bucket'] = self.DEFAULT_BUCKET_USER_INPUT
    params['object'] = {'text': 'new name', 'default': 'file name'}
    params['content-type'] = {'text': 'content-type', 'default': 'best guess'}
    params['encoding'] = {'text': 'encoding', 'default': 'best guess'}
    params['acl'] = {
        'text': 'an acl (private, public-read, etc)',
        'default': 'private'
    }
    super(InsertObjectCommand, self).__init__(description, gcs_client, params)

  def _process_input(self, file_path):
    """Checks to make sure that the entered file path exists.

    Args:
      file_path: The string path to a local file.

    Returns:
      The string file path.
    """
    if not file_path:
      file_path = self._create_new_file()
    else:
      f = None
      try:
        f = open(file_path, 'r')
      except IOError:
        logging.error(
            'File does not exist, creating %s file.', self.UPLOAD_FILE_NAME)
        file_path = self._create_new_file()
      finally:
        if f: f.close()
    return file_path

  def _create_new_file(self):
    """Creates a new test file if one doesn't already exist.

    Returns:
      The string file path.
    """
    file_path = os.path.join(os.path.dirname(__file__), self.UPLOAD_FILE_NAME)
    f = None
    try:
      f = open(file_path, 'r')
    except IOError:
      f = open(file_path, 'w')
      f.write('This is a test file for the Cloud Storage demo.')
    finally:
      f.close()
    return file_path

  def _run_api_command(self):
    """Insert a new object.

    Returns:
      The successful file upload string message.
    """
    self._gcs_client.insert_object(
        self._input.values['bucket'],
        self._input.values['file-path'],
        self._input.values['object'],
        self._input.values['content-type'],
        self._input.values['encoding'],
        self._input.values['acl'])
    return 'File %s was uploaded.' % self._input.values['file-path']


class CopyObjectCommand(GcsCommand):
  """Copy an object."""

  def __init__(self, description, gcs_client):
    """Initialize CopyObjectCommand with description and gcs_client.

    Args:
      description: The description for the user menu.
      gcs_client: An instance of gcs.Gcs.
    """
    params = {}
    params['original-bucket'] = {'text': 'current bucket'}
    params['original-object'] = {'text': 'object to copy'}
    params['new-bucket'] = {'text': 'new bucket'}
    params['new-object'] = {
        'text': 'new object name',
        'default': 'original object name'
    }
    super(CopyObjectCommand, self).__init__(description, gcs_client, params)

  def _run_api_command(self):
    """Copy an object.

    Returns:
      The successful file copy string message.
    """
    self._gcs_client.copy_object(
        self._input.values['original-bucket'],
        self._input.values['original-object'],
        self._input.values['new-bucket'],
        self._input.values['new-object'])

    return '%s has been copied to %s.' % (
        self._input.values['new-object'],
        self._input.values['new-bucket'])


class DeleteObjectCommand(GcsCommand):
  """Delete an object."""

  def __init__(self, description, gcs_client):
    """Initialize DeleteObjectCommand with description and gcs_client.

    Args:
      description: The description for the user menu.
      gcs_client: An instance of gcs.Gcs.
    """
    params = {}
    params['bucket'] = self.DEFAULT_BUCKET_USER_INPUT
    params['object'] = self.DEFAULT_OBJECT_USER_INPUT
    super(DeleteObjectCommand, self).__init__(description, gcs_client, params)

  def _run_api_command(self):
    """Delete an object.

    Returns:
      The successful delete file string message.
    """
    self._gcs_client.delete_object(
        self._input.values['bucket'],
        self._input.values['object'])
    return '%s deleted.' % self._input.values['object']
