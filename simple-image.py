#!/usr/bin/env python

from PIL import Image
from PIL import ImageGrab
import boto3
import argparse
import uuid
import os
import io


def getArgs():
    parser = argparse.ArgumentParser(
        description='Resize image and upload it to given s3 bucket')
    parser.add_argument(
        '--resolution', help="The resolution of uploaded image, default is -1 which means keep the original size",
        default=-1,
        choices=[480, 720, 1080, -1],
        type=int)
    parser.add_argument(
        '--domain', help="The domain of image server, if this value is given, the full image url will be generated")
    parser.add_argument(
        'image', help="The image which will be uploaded, if the value is -, the image in clipboard will be used.")
    parser.add_argument('bucket', help="The s3 bucket which host the image")

    args = parser.parse_args()
    print(args)
    return args


def getResolutionSize(resolution):
    if resolution == 480:
        return (720, 480)
    elif resolution == 720:
        return (1280, 720)
    elif resolution == 1080:
        return (1920, 1080)
    else:
        return (1000000, 1000000)


def getImage(imagePath):
    return Image.open(imagePath) if imagePath != '-' else ImageGrab.grabclipboard()


def uploadToS3(image, bucket, size):
    if(image == None):
        raise Exception('The image is not available.')

    targetImage = image.copy()
    targetImage.thumbnail(size)

    randomName = str(uuid.uuid4()) + '.' + image.format.lower()
    contentType = 'image/'+image.format.lower()

    s3Client = boto3.client("s3")

    imgByteArr = io.BytesIO()
    targetImage.save(imgByteArr, format=image.format)
    s3Client.put_object(Body=imgByteArr.getvalue(),
                        Bucket=bucket, Key=randomName, StorageClass='STANDARD_IA', ContentType=contentType)
    return randomName


def main():
    args = getArgs()
    size = getResolutionSize(args.resolution)
    image = getImage(args.image)
    name = uploadToS3(image, args.bucket, size)
    print(name) if args.domain == None else print(
        args.domain+'/'+name)


if __name__ == '__main__':
    main()
