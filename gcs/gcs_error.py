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

"""Google Cloud Storage error class."""

__author__ = 'kbrisbin@google.com (Kathryn Hurley)'


class GcsError(Exception):
  """Exception raised when API call does not return a 20x status.

  Attributes:
    status: The string status of the HTTP response.
    message: A string message explaining the error.
  """

  def __init__(self, status, message):
    """Inits GcsError with status and message.

    Args:
      status: String status of the HTTP response.
      message: A string message explaining the error.
    """
    self.status = status
    self.message = message

  def __str__(self):
    """Displays the error as <status>: <error message>.

    Returns:
      The string representation of the error.
    """
    return '%s: %s' % (repr(self.status), repr(self.message))
