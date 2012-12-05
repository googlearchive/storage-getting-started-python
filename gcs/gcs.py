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

"""Google Cloud Storage client abstract class."""

__author__ = 'kbrisbin@google.com (Kathryn Hurley)'


class Gcs(object):
  """Gcs class used for making Google Cloud Storage API calls.

  Attributes:
    auth_http: An authorized instance of httplib2.Http.
    project_id: The string project id of the Cloud Storage project.
    default_origin: The default request origin.
    default_method: The default HTTP method.
    default_response_header: The default response header.
    default_max_age_sec: The default max age in seconds.
  """

  def __init__(self, auth_http, project_id):
    """Inits Gcs with credentials, project id, and API version.

    Args:
      auth_http: An authorized instance of httplib2.Http.
      project_id: The string project id of the Cloud Storage project.
    """
    self.auth_http = auth_http
    self.project_id = project_id
    self.default_origin = '*'
    self.default_method = 'GET'
    self.default_response_header = 'gcs-demo'
    self.default_max_age_sec = 1800

  def get_buckets(self):
    """Get a list of Cloud Storage buckets.

    Raises:
      NotImplementedError if the method is not implemented in the subclass.
    """
    raise NotImplementedError('You need to override this function')

  def get_bucket(self, bucket_name):
    """Get the info for a specific bucket.

    Args:
      bucket_name: String name of the bucket.

    Raises:
      NotImplementedError if the method is not implemented in the subclass.
    """
    raise NotImplementedError('You need to override this function')

  def get_bucket_cors(self, bucket_name):
    """Get CORS for the specified bucket.

    Args:
      bucket_name: String name of the bucket.

    Raises:
      NotImplementedError if the method is not implemented in the subclass.
    """
    raise NotImplementedError('You need to override this function')

  def get_bucket_location(self, bucket_name):
    """Get location of the specified bucket.

    Args:
      bucket_name: String name of the bucket.

    Raises:
      NotImplementedError if the method is not implemented in the subclass.
    """
    raise NotImplementedError('You need to override this function')

  def insert_bucket(self, bucket_name, acl=None, location_constraint=None):
    """Get a list of Cloud Storage buckets.

    Args:
      bucket_name: The name of the bucket to insert.
      acl: A string predefined Google ACL, as defined here:
          developers.google.com/storage/docs/reference-headers#xgoogacl.
          Defaults to private.
      location_constraint: The location for the bucket (EU or US). Defaults to
          US.

    Raises:
      NotImplementedError if the method is not implemented in the subclass.
    """
    raise NotImplementedError('You need to override this function')

  def set_bucket_cors(self, bucket_name, origins=None, methods=None,
                      response_headers=None, max_age_sec=None):
    """Sets CORS on the specified bucket.

    Args:
      bucket_name: String name of the bucket to set the cors on.
      origins: List of string origins.
      methods: List of string methods (GET, POST, etc).
      response_headers: List of string response headers.
      max_age_sec: String or number max age.

    Raises:
      NotImplementedError if the method is not implemented in the subclass.
    """
    raise NotImplementedError('You need to override this function')

  def delete_bucket(self, bucket_name):
    """Deletes the given bucket.

    Args:
      bucket_name: The string name of the bucket to delete.

    Raises:
      NotImplementedError if the method is not implemented in the subclass.
    """
    raise NotImplementedError('You need to override this function')

  def get_object(self, bucket_name, object_name):
    """Gets an object in a Cloud Storage bucket.

    Args:
      bucket_name: String name of the bucket to set the cors on.
      object_name: The name of the object.

    Raises:
      NotImplementedError if the method is not implemented in the subclass.
    """
    raise NotImplementedError('You need to override this function')

  def get_object_acls(self, bucket_name, object_name):
    """Gets an object's ACLs in a Cloud Storage bucket.

    Args:
      bucket_name: String name of the bucket to set the cors on.
      object_name: The name of the object.

    Raises:
      NotImplementedError if the method is not implemented in the subclass.
    """
    raise NotImplementedError('You need to override this function')

  def get_object_metadata(self, bucket_name, object_name):
    """Gets an object's ACLs in a Cloud Storage bucket.

    Args:
      bucket_name: String name of the bucket to set the cors on.
      object_name: The name of the object.

    Raises:
      NotImplementedError if the method is not implemented in the subclass.
    """
    raise NotImplementedError('You need to override this function')

  def insert_object(self, bucket_name, file_path=None, object_name=None,
                    content_type=None, content_encoding=None, acl=None):
    """Insert an object into a Cloud Storage bucket.

    Args:
      bucket_name: The name of the bucket to insert.
      file_path: The local file path to the file to upload.
      object_name: An optional string name for the object. Defaults to the file
          name.
      content_type: An optional content type string value for the Content-Type
          header. Defaults to using python mimetype.guess_type.
      content_encoding: An optional encoding string value for the
          Content-Encoding header. Defaults to using python mimetype.guess_type.
      acl: A string predefined Google ACL, as defined here:
          developers.google.com/storage/docs/reference-headers#xgoogacl.
          Defaults to private.

    Raises:
      NotImplementedError if the method is not implemented in the subclass.
    """
    raise NotImplementedError('You need to override this function')

  def copy_object(self, original_bucket_name, original_object_name,
                  new_bucket_name, new_object_name=None, acl=None):
    """Copy an existing Cloud Storage object.

    Args:
      original_bucket_name: The bucket of the original object.
      original_object_name: The name of the original object.
      new_bucket_name: The name of the new bucket to copy to.
      new_object_name: The name of the new bucket to copy to.
      acl: A string predefined Google ACL, as defined here:
          developers.google.com/storage/docs/reference-headers#xgoogacl.
          Defaults to private.

    Raises:
      NotImplementedError if the method is not implemented in the subclass.
    """
    raise NotImplementedError('You need to override this function')

  def delete_object(self, bucket_name, object_name):
    """Delete an existing Cloud Storage object.

    Args:
      bucket_name: The name of the bucket.
      object_name: The name of the object.

    Raises:
      NotImplementedError if the method is not implemented in the subclass.
    """
    raise NotImplementedError('You need to override this function')
