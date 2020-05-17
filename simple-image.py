#!/usr/bin/env python

import argparse
import io
import os
import uuid
import sys
import webbrowser

import boto3
from jinja2 import Template
from PIL import Image, ImageGrab
from flask import Flask, render_template


def getUploadArgs(args):
    parser = argparse.ArgumentParser(
        prog="simple-image upload",
        description='Resize image and upload it to given s3 bucket')
    parser.add_argument(
        '--resolution', help="The resolution of uploaded image, default is -1 which means keep the original size",
        default=-1,
        choices=[480, 720, 1080, -1],
        type=int)
    parser.add_argument(
        '--domain', help="The domain of image server, if this value is given, the full image url will be generated")
    parser.add_argument(
        '--open', help="Open the image in browser after uploaded the image", action='store_true')
    parser.add_argument(
        'image', help="The image which will be uploaded, if the value is -, the image in clipboard will be used.")
    parser.add_argument('bucket', help="The s3 bucket which host the image")

    args = parser.parse_args(args)
    return args


def getBrowseArgs(args):
    parser = argparse.ArgumentParser(
        prog="simple-image browse",
        description='Browse all the images in the s3 bucket')
    parser.add_argument(
        'domain', help="The domain of image server, if this value is given, the image url will use this domain")
    parser.add_argument('bucket', help="The s3 bucket which host the image")

    args = parser.parse_args(args)
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


def uploadImage():
    args = getUploadArgs(sys.argv[2:])
    size = getResolutionSize(args.resolution)
    image = getImage(args.image)
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
                        Bucket=args.bucket, Key=randomName, StorageClass='STANDARD_IA', ContentType=contentType)
    url = randomName if args.domain == None else args.domain+'/'+randomName

    webbrowser.open(url, new=0) if args.open else print(url)


def browseImages():
    args = getBrowseArgs(sys.argv[2:])
    s3Client = boto3.client("s3")
    app = Flask(__name__, template_folder='template')

    @ app.route('/')
    def index():
        response = s3Client.list_objects(Bucket=args.bucket)
        images = list(map(lambda x: args.domain+'/'+x['Key'],
                          sorted(response['Contents'],
                                 key=lambda x: x['LastModified'], reverse=True)))
        return render_template('index.html', images=images)
    app.run(debug=False)


def main():
    parser = argparse.ArgumentParser(
        description='Simple image tool to upload/browse image on remote server.',
        usage='''simple-image <command> [<args>]

    The most commonly used git commands are:
       upload      Upload image to remote server
       browse      Browse all images on remote server
    ''')
    parser.add_argument('command', choices=[
                        'upload', 'browse'], help='Subcommand to run')
    args = parser.parse_args(sys.argv[1:2])
    if args.command == 'browse':
        browseImages()
    else:
        uploadImage()


if __name__ == '__main__':
    main()
