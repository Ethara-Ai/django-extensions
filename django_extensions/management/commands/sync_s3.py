"""
Sync Media to S3
================

Django command that scans all files in your settings.MEDIA_ROOT and
settings.STATIC_ROOT folders and uploads them to S3 with the same directory
structure.

This command can optionally do the following but it is off by default:
* gzip compress any CSS and Javascript files it finds and adds the appropriate
  'Content-Encoding' header.
* set a far future 'Expires' header for optimal caching.
* upload only media or static files.
* use any other provider compatible with Amazon S3.
* set other than 'public-read' ACL.

Note: This script requires the Python boto library and valid Amazon Web
Services API keys.

Required settings.py variables:
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
AWS_BUCKET_NAME = ''

When you call this command with the `--renamegzip` param, it will add
the '.gz' extension to the file name. But Safari just doesn't recognize
'.gz' files and your site won't work on it! To fix this problem, you can
set any other extension (like .jgz) in the `SYNC_S3_RENAME_GZIP_EXT`
variable.

Command options are:
  -p PREFIX, --prefix=PREFIX
                        The prefix to prepend to the path on S3.
  --gzip                Enables gzipping CSS and Javascript files.
  --expires             Enables setting a far future expires header.
  --force               Skip the file mtime check to force upload of all
                        files.
  --filter-list         Override default directory and file exclusion
                        filters. (enter as comma separated line)
  --renamegzip          Enables renaming of gzipped files by appending '.gz'.
                        to the original file name. This way your original
                        assets will not be replaced by the gzipped ones.
                        You can change the extension setting the
                        `SYNC_S3_RENAME_GZIP_EXT` var in your settings.py
                        file.
  --invalidate          Invalidates the objects in CloudFront after uploading
                        stuff to s3.
  --media-only          Only MEDIA_ROOT files will be uploaded to S3.
  --static-only         Only STATIC_ROOT files will be uploaded to S3.
  --s3host              Override default s3 host.
  --acl                 Override default ACL settings ('public-read' if
                        settings.AWS_DEFAULT_ACL is not defined).

TODO:
 * Use fnmatch (or regex) to allow more complex FILTER_LIST rules.

"""

import datetime
import email
import gzip
import mimetypes
import os
import time
from typing import List  # NOQA

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from io import StringIO

from django_extensions.management.utils import signalcommand


try:
    import boto
except ImportError:
    HAS_BOTO = False
else:
    HAS_BOTO = True


class Command(BaseCommand):
    # Extra variables to avoid passing these around
    AWS_ACCESS_KEY_ID = ""
    AWS_SECRET_ACCESS_KEY = ""
    AWS_BUCKET_NAME = ""
    AWS_CLOUDFRONT_DISTRIBUTION = ""
    SYNC_S3_RENAME_GZIP_EXT = ""

    DIRECTORIES = ""
    FILTER_LIST = [".DS_Store", ".svn", ".hg", ".git", "Thumbs.db"]
    GZIP_CONTENT_TYPES = (
        "text/css",
        "application/javascript",
        "application/x-javascript",
        "text/javascript",
    )

    uploaded_files = []  # type: List[str]
    upload_count = 0
    skip_count = 0

    help = "Syncs the complete MEDIA_ROOT structure and files to S3 into the given bucket name."  # noqa: E501
    args = "bucket_name"

    can_import_settings = True

    def add_arguments(self, parser):
        pass

    @signalcommand
    def handle(self, *args, **options):
        pass

    def open_cf(self):
        """Return an open connection to CloudFront"""
        pass

    def invalidate_objects_cf(self):
        """Split the invalidation request in groups of 1000 objects"""
        pass

    def sync_s3(self):
        """Walk the media/static directories and syncs files to S3"""
        pass

    def compress_string(self, s):
        """Gzip a given string."""
        pass

    def get_s3connection_kwargs(self):
        """Return connection kwargs as a dict"""
        pass

    def open_s3(self):
        """Open connection to S3 returning bucket and key"""
        pass

    def upload_s3(self, arg, dirname, names, dirs):
        pass
