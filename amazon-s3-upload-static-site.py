#!/usr/bin/env python
# Author: Nicholas Kuechler
# URL: http://nicholaskuechler.com
# Github: https://github.com/nicholaskuechler

import argparse
import boto3
import mimetypes
import os
import sys

from boto3.s3.transfer import S3Transfer


VERBOSE = False

DEFAULT_REGION = "us-west-2"


def main(args):
    bucket = args.bucket
    upload_dir = args.dir

    print "Uploading directory: %s" % (upload_dir)
    print "Uploading to bucket: %s" % (bucket)

    s3_client = boto3.client('s3', DEFAULT_REGION)
    transfer = S3Transfer(s3_client)

    for root, dirs, files in os.walk(upload_dir):
        for name in files:
            path = root.split(os.path.sep)[1:]
            path.append(name)
            key_id = os.path.join(*path)
            upload_file = os.path.join(root, name)

            if key_id == sys.argv[0]:
                if VERBOSE:
                    print "Skipping upload of this uploader script"
                continue

            mime_type = mimetypes.guess_type(upload_file)[0]

            # print "mime_type: %s" % (mime_type)
            if mime_type:
                content_type = {'ContentType': mime_type}
            else:
                mime_type = "text/html"

            # upload normal files
            if VERBOSE:
                print ("Uploading file: %s to %s:%s type: %s"
                       % (upload_file, bucket, key_id, mime_type))
            transfer.upload_file(upload_file, bucket, key_id,
                                 extra_args=content_type)

            # for .html files, excluding index.html, also upload the file
            # without .html extension for pretty urls
            if (upload_file.endswith('.html') and not
                    upload_file.endswith('index.html')):
                key_id_pretty_url = key_id.replace('.html', '')
                if VERBOSE:
                    print ("Uploading file WITHOUT HTML EXTENSION: "
                           "%s to %s:%s type: %s"
                           % (upload_file, bucket, key_id_pretty_url,
                              mime_type))
                transfer.upload_file(upload_file, bucket, key_id_pretty_url,
                                     extra_args=content_type)

    print "Upload completed."


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dir',
                        type=str,
                        required=False,
                        default="_site",
                        help='Directory to upload. Defaults to _site in the '
                             'current working directory.')
    parser.add_argument('-b', '--bucket',
                        type=str,
                        required=True,
                        help='S3 Bucket')
    parser.add_argument("-v", "--verbose", action="store_true",
                        default=False,
                        help="Increase output verbosity")
    args = parser.parse_args()

    VERBOSE = args.verbose

    main(args)
