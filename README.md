# amazon-s3-upload-static-site

Uploads a static site, such as a Jekyll generated site, to Amazon S3, with
built in pretty url handling.

## Usage

    python amazon-s3-upload-static-site.py --bucket s3_bucket_name --dir /path/to/directory/to/upload

## Notes

The upload directory defaults to "_site" in the current working directory.

Pretty URLs: For .html files, a second file will be upload without the .html
extension. The file will be uploaded with the "text/html" content type, so
that I can have pretty URLs with my Amazon S3 hosted static websites.

Example: The local file about.html will be upload to the S3 bucket as both
about.html and "about". The "about" file has no .html extension, but the
text/html content type is set, allowing Amazon S3 to serve the file as HTML.
Otherwise, the file will default to the "binary/octet-stream" content type,
and the browser will attempt to download it rather than render it.
