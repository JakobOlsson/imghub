import boto3
import logging
from os import getenv
from flask import Blueprint, render_template
from flask import request, redirect, jsonify
from werkzeug.utils import secure_filename
bucket_handler = Blueprint('bucket_handler', __name__, template_folder='templates')

LOG = logging.getLogger(__name__)

s3 = boto3.resource('s3',
                    endpoint_url=getenv('S3_URL', 'http://localhost:9000'),
                    config=boto3.session.Config(signature_version='s3v4'),
                    aws_access_key_id=getenv('AWS_ACCESS_KEY_ID', "AKIAIOSFODNN7EXAMPLE"),
                    aws_secret_access_key=getenv('AWS_SECRET_ACCESS_KEY', "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"))
'''
s3cl = boto3.client('s3',
                    aws_access_key_id=getenv('AWS_ACCESS_KEY_ID', "AKIAIOSFODNN7EXAMPLE"),
                    aws_secret_access_key=getenv('AWS_SECRET_ACCESS_KEY', "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"))
'''
s3_bucket_name = getenv('S3_BUCKET', 'images')
s3_prefix = getenv("S3_PREFIX", 'images')
s3_url = getenv('S3_URL', 'http://localhost:9000')
s3_full_url = getenv('S3_FULL_URL', '{}/{}'.format(s3_url, s3_bucket_name))


@bucket_handler.route('/upload')
def upload_file_page():
    return render_template('upload.html')

@bucket_handler.route('/listimages')
def listimages_page():
    return render_template('list.html')

@bucket_handler.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check we got a file
        if 'file' not in request.files:
            return redirect('/upload')
        rec_file = request.files['file']
        if rec_file.filename == '':
            return redirect('/upload')
        if rec_file:
            filename = secure_filename(rec_file.filename)
            bucket = s3.Bucket(s3_bucket_name)
            filetype = filename.split('.')[-1]
            if 3 > len(filetype) < 4:
                filetype = "jpeg"
            ContentType = 'image/{}'.format(filetype)
            Key = "{}/{}".format(s3_prefix, filename)
            LOG.info(f"uploading: {filename}")
            bucket.put_object(Body=rec_file,
                              Key=Key,
                              ContentType=ContentType)
    return redirect('/listimages')


@bucket_handler.route('/list')
def list_imgs():
    bucket = s3.Bucket(s3_bucket_name)
    objs = bucket.objects.filter(Prefix='images')
    ret = {"files": []}
    for x in objs:
        filename = x.key
        file_path = "{}/{}".format(s3_full_url, filename)
        file_inf = {'url': file_path, 'name': filename}
        ret['files'].append(file_inf)
    return jsonify(ret)

@bucket_handler.route('/delete/<path:image>')
def delete_img(image):
    LOG.info(f"delete: {image}")

    bucket = s3.Bucket(s3_bucket_name)
    bucket.delete_objects(
        Delete={
            'Objects': [
                {
                    'Key': image
                },
            ]
        }
    )
    return redirect('/listimages')


