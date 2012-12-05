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

"""Google Cloud Storage client for the XML API."""

__author__ = 'kbrisbin@google.com (Kathryn Hurley)'

import mimetypes
import os
import re
import xml.etree.ElementTree as xml

import httplib2

import gcs
import gcs_error

DEFAULT_VERSION = '2'
NOT_FOUND = 404


class GcsXml(gcs.Gcs):
  """Gcs class used for making Google Cloud Storage API calls.

  Attributes:
    api_version: The version of the API.
  """

  def __init__(self, auth_http, project_id, api_version=DEFAULT_VERSION):
    """Inits Gcs with credentials, project id, and API version.

    Args:
      auth_http: An authorized instance of httplib2.Http.
      project_id: The string project id of the Cloud Storage project.
      api_version: The version of the API.
    """
    super(GcsXml, self).__init__(auth_http, project_id)
    self.api_version = api_version
    self._base_url = 'storage.googleapis.com'

  def get_buckets(self):
    """Get a list of Cloud Storage buckets.

    Returns:
      The string XML representation of the buckets.

    Raises:
      gcs_error.GcsError if the API request did not succeed.
    """
    try:
      response, content = self._api_request(self._base_url)
    except gcs_error.GcsError:
      raise
    return content

  def get_bucket(self, bucket_name):
    """Get the info for a specific bucket.

    Args:
      bucket_name: String name of the bucket.

    Returns:
      The string XML representation of the bucket.

    Raises:
      gcs_error.GcsError if the API request did not succeed.
    """
    try:
      response, content = self._api_request(
          '%s.%s' % (bucket_name, self._base_url))
    except gcs_error.GcsError:
      raise
    return content

  def get_bucket_cors(self, bucket_name):
    """Get CORS for the specified bucket.

    Args:
      bucket_name: String name of the bucket.

    Returns:
      The string XML representation of the CORS.

    Raises:
      gcs_error.GcsError if the API request did not succeed.
    """
    try:
      response, content = self._api_request(
          '%s.%s/?cors' % (bucket_name, self._base_url))
    except gcs_error.GcsError:
      raise
    return content

  def get_bucket_location(self, bucket_name):
    """Get location of the specified bucket.

    Args:
      bucket_name: String name of the bucket.

    Returns:
      The string XML representation of the location.

    Raises:
      gcs_error.GcsError if the API request did not succeed.
    """
    try:
      response, content = self._api_request(
          '%s.%s/?location' % (bucket_name, self._base_url))
    except gcs_error.GcsError:
      raise
    return content

  def insert_bucket(self, bucket_name, acl=None, location_constraint=None):
    """Get a list of Cloud Storage buckets.

    Args:
      bucket_name: The name of the bucket to insert.
      acl: A string predefined Google ACL, as defined here:
          developers.google.com/storage/docs/reference-headers#xgoogacl.
          Defaults to private.
      location_constraint: The location for the bucket (EU or US). Defaults to
          US.

    Returns:
      The string response from the API call.

    Raises:
      gcs_error.GcsError if the API request did not succeed.
      ValueError: If the bucket name does not conform to Cloud Storage
          constraints (https://developers.google.com/storage/docs/bucketnaming).
    """
    if not re.match(r'^[\w\-\.]+$', bucket_name):
      raise ValueError(
          'Bucket names can only contain letters, numbers, -, _, or .')
    if not re.match(r'^[a-zA-Z0-9]+.*', bucket_name):
      raise ValueError(
          'Bucket names can only start with letters or numbers.')
    if not re.match(r'.*[a-zA-Z0-9]+$', bucket_name):
      raise ValueError(
          'Bucket names can only end with letters or numbers. ' + bucket_name)
    if len(bucket_name) < 3 or len(bucket_name) > 63:
      raise ValueError('Bucket names must contain 3 to 63 letters.')
    body = None
    if location_constraint and (
        location_constraint == 'EU' or location_constraint == 'US'):
      body = self._get_location_constraint_body(location_constraint)
    headers = {}
    if acl: headers['x-goog-acl'] = acl
    try:
      response, content = self._api_request(
          '%s.%s' % (bucket_name, self._base_url), 'PUT', headers=headers,
          body=body)
    except gcs_error.GcsError:
      raise
    return content

  def set_bucket_cors(self, bucket_name, origins=None, methods=None,
                      response_headers=None, max_age_sec=None):
    """Sets CORS on the specified bucket.

    Args:
      bucket_name: String name of the bucket to set the cors on.
      origins: List of string origins.
      methods: List of string methods (GET, POST, etc).
      response_headers: List of string response headers.
      max_age_sec: String or number max age.

    Returns:
      The string response from the API call.

    Raises:
      gcs_error.GcsError if the API request did not succeed.
    """
    if not origins: origins = [self.default_origin]
    if not methods: methods = [self.default_method]
    if not response_headers: response_headers = [self.default_response_header]
    if not max_age_sec: max_age_sec = self.default_max_age_sec

    body = self._get_cors_body(origins, methods, response_headers, max_age_sec)
    try:
      response, content = self._api_request(
          '%s.%s/?cors' % (bucket_name, self._base_url), 'PUT', body=body)
    except gcs_error.GcsError:
      raise
    return content

  def delete_bucket(self, bucket_name):
    """Deletes the given bucket.

    Args:
      bucket_name: The string name of the bucket to delete.

    Returns:
      The string response from the API call.

    Raises:
      gcs_error.GcsError if the API request did not succeed.
    """
    try:
      response, content = self._api_request(
          '%s.%s' % (bucket_name, self._base_url), 'DELETE')
    except gcs_error.GcsError:
      raise
    return content

  def get_object(self, bucket_name, object_name):
    """Gets an object in a Cloud Storage bucket.

    Args:
      bucket_name: String name of the bucket to set the cors on.
      object_name: The name of the object.

    Returns:
      The object content.

    Raises:
      gcs_error.GcsError if the API request did not succeed.
    """
    try:
      response, content = self._api_request(
          '%s.%s/%s' % (bucket_name, self._base_url, object_name))
    except gcs_error.GcsError:
      raise
    return content

  def get_object_acls(self, bucket_name, object_name):
    """Gets an object's ACLs in a Cloud Storage bucket.

    Args:
      bucket_name: String name of the bucket to set the cors on.
      object_name: The name of the object.

    Returns:
      The string XML representation of the object's ACLs.

    Raises:
      gcs_error.GcsError if the API request did not succeed.
    """
    try:
      response, content = self._api_request(
          '%s.%s/%s?acl' % (bucket_name, self._base_url, object_name))
    except gcs_error.GcsError:
      raise
    return content

  def get_object_metadata(self, bucket_name, object_name):
    """Gets an object's ACLs in a Cloud Storage bucket.

    Args:
      bucket_name: String name of the bucket to set the cors on.
      object_name: The name of the object.

    Returns:
      The httplib2.Response object from the API call.

    Raises:
      gcs_error.GcsError if the API request did not succeed.
    """
    try:
      response, content = self._api_request(
          '%s.%s/%s' % (bucket_name, self._base_url, object_name), 'HEAD')
    except gcs_error.GcsError:
      raise
    return response

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

    Returns:
      The string response from the API call.

    Raises:
      gcs_error.GcsError if the API request did not succeed.
    """
    upload_file = open(file_path, 'r')
    upload_file_contents = upload_file.read()
    if not object_name: object_name = os.path.basename(file_path)
    if not content_type or not content_encoding:
      guess_type, guess_encoding = mimetypes.guess_type(file_path)
      if not content_type: content_type = guess_type
      if not content_encoding: content_encoding = guess_encoding
    headers = {}
    if content_type: headers['Content-Type'] = content_type
    if content_encoding: headers['Content-Encoding'] = content_encoding
    if acl: headers['x-goog-acl'] = acl
    try:
      response, content = self._api_request(
          '%s.%s/%s' % (bucket_name, self._base_url, object_name), 'PUT',
          headers=headers, body=upload_file_contents)
    except gcs_error.GcsError:
      raise
    return content

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

    Returns:
      The string response from the API call.

    Raises:
      gcs_error.GcsError if the API request did not succeed.
    """
    copy_source = '/%s/%s' % (original_bucket_name, original_object_name)
    headers = {
        'x-goog-copy-source': copy_source
    }
    if acl: headers['x-goog-acl'] = acl
    if not new_object_name: new_object_name = original_object_name
    print '%s.%s/%s' % (new_bucket_name, self._base_url, new_object_name)
    try:
      response, content = self._api_request(
          '%s.%s/%s' % (new_bucket_name, self._base_url, new_object_name),
          'PUT',
          headers=headers)
    except gcs_error.GcsError:
      raise
    return content

  def delete_object(self, bucket_name, object_name):
    """Delete an existing Cloud Storage object.

    Args:
      bucket_name: The name of the bucket.
      object_name: The name of the object.

    Returns:
      The string response from the API call.

    Raises:
      gcs_error.GcsError if the API request did not succeed.
    """
    try:
      response, content = self._api_request(
          '%s.%s/%s' % (bucket_name, self._base_url, object_name), 'DELETE')
    except gcs_error.GcsError:
      raise
    return content

  def _get_location_constraint_body(self, location_constraint):
    """Create the XML document for the location constraint object request.

    Args:
      location_constraint: The location of the bucket (EU or US).

    Returns:
      The string XML representation of the location constraint body.

    Raises:
      gcs_error.GcsError if the API request did not succeed.
    """
    bucket_config_elem = xml.Element('CreateBucketConfiguration')
    location_elem = xml.SubElement(bucket_config_elem, 'LocationConstraint')
    location_elem.text = location_constraint
    return self._xml_tostring(bucket_config_elem)

  def _get_cors_body(self, origins, methods, response_headers, max_age_sec):
    """Create the XML document for the cors request.

    Args:
      origins: List of string origins.
      methods: List of string methods (GET, POST, etc).
      response_headers: List of string response headers.
      max_age_sec: String or number max age.

    Returns:
      The string XML representation of the CORS body.
    """
    cors_config_elem = xml.Element('CorsConfig')
    cors_elem = xml.SubElement(cors_config_elem, 'Cors')

    origins_elem = xml.SubElement(cors_elem, 'Origins')
    for origin in origins:
      origin_elem = xml.SubElement(origins_elem, 'Origin')
      origin_text = origin.strip()
      if not origin_text: origin_text = self.default_origin
      origin_elem.text = origin_text

    methods_elem = xml.SubElement(cors_elem, 'Methods')
    for method in methods:
      method_elem = xml.SubElement(methods_elem, 'Method')
      method_text = method.strip()
      if not method_text: method_text = self.default_method
      method_elem.text = method_text

    response_headers_elem = xml.SubElement(cors_elem, 'ResponseHeaders')
    for response_header in response_headers:
      response_header_elem = xml.SubElement(
          response_headers_elem, 'ResponseHeader')
      response_header_text = response_header.strip()
      if not response_header_text:
        response_header_text = self.default_response_header
      response_header_elem.text = response_header_text

    max_age_sec_elem = xml.SubElement(cors_elem, 'MaxAgeSec')
    if type(max_age_sec) is int:
      max_age_sec_elem.text = '%d' % max_age_sec
    elif type(max_age_sec) is float:
      max_age_sec_elem.text = '%f' % max_age_sec
    else:
      max_age_sec_elem.text = max_age_sec

    return self._xml_tostring(cors_config_elem)

  def _xml_tostring(self, root_elem):
    """Converts an xml.etree.ElementTree to string.

    Args:
      root_elem: An xml.etree.ElementTree object.

    Returns:
      A string representation of the XML.
    """
    body = xml.tostring(root_elem, 'utf-8')
    body = '<?xml version="1.0" encoding="UTF-8"?>' + body
    return body

  def _api_request(self, url, method=None, headers=None, body=None):
    """Send an authorized HTTP request to the Cloud Storage API.

    Args:
      url: The API URL endpoint.
      method: The HTTP request method (GET, POST, etc).
      headers: Any additional headers to send.
      body: The request body.

    Returns:
      The response dictionary and string content.

    Raises:
      gcs_error.GcsError if the API request did not succeed.
    """
    if not method: method = self.default_method
    if not headers: headers = {}
    headers['x-goog-project-id'] = self.project_id
    headers['x-goog-api-version'] = self.api_version

    if method == 'POST' or method == 'PUT' or body:
      if body:
        headers['Content-Length'] = '%d' % (len(body))
      else:
        headers['Content-Length'] = '0'

    try:
      response, content = self.auth_http.request(
          'http://' + url, method=method, headers=headers, body=body)
    except httplib2.ServerNotFoundError, se:
      raise gcs_error.GcsError(NOT_FOUND, 'Server not found.')

    if response.status >= 300:
      raise gcs_error.GcsError(response.status, response.reason)

    return response, content
