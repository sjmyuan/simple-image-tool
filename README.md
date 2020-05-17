# [Simple Image Tool](https://pypi.org/project/simple-image-tool/)

## Assumtion

* This tool is used to upload image to image server which is based on s3 bucket.
* You already set up the s3 bucket.
* The image in this s3 bucket is public, which mean anyone can access it by `https://<domain>/<image name>`. You can achieve this by public read permission or cloudfront.
* You already get the `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`

## Feature

* Upload local image to S3 bucket with specified resolution.
* Upload image in clipboard to S3 bucket with specified resolution.
* Generate random name for uploaded image.
* Generate full url for uploaded image if domain is given

## How to install

```sh
pip install simple-image-tool
simple-image-tool --help
simple-image-tool upload --help
simple-image-tool browse --help
```

## Usage

### Upload existing image to s3 bucket

```sh
AWS_DEFAULT_REGION=<region> AWS_ACCESS_KEY_ID=<key id> AWS_SECRET_ACCESS_KEY=<access key> simple-image-tool upload --domain <domain> --resolution 480 --open <image path> <bucket>
```

### Upload image in clipboard to s3 bucket

```sh
AWS_DEFAULT_REGION=<region> AWS_ACCESS_KEY_ID=<key id> AWS_SECRET_ACCESS_KEY=<access key> simple-image-tool upload --domain <domain> --resolution 480 --open - <bucket>
```

### Browse all images in the s3 bucket

```sh
AWS_DEFAULT_REGION=<region> AWS_ACCESS_KEY_ID=<key id> AWS_SECRET_ACCESS_KEY=<access key> simple-image-tool browse <domain> <bucket>
```
