import boto3
import logging
from flask import Blueprint, render_template
from flask import request, redirect, jsonify
from werkzeug.utils import secure_filename
from settings import S3_API_ENDPOINT, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
from settings import S3_PREFIX, S3_BUCKET_NAME, S3_FULL_URL


bucket_handler = Blueprint('bucket_handler',
                           __name__,
                           template_folder='templates')

LOG = logging.getLogger(__name__)

s3 = boto3.resource('s3',
                    endpoint_url=S3_API_ENDPOINT,
                    config=boto3.session.Config(signature_version='s3v4'),
                    aws_access_key_id=AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
if AWS_ACCESS_KEY_ID == '':
    s3 = boto3.resource('s3',
                        endpoint_url=S3_API_ENDPOINT,
                        config=boto3.session.Config(signature_version='s3v4'))


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
            bucket = s3.Bucket(S3_BUCKET_NAME)
            filetype = filename.split('.')[-1]
            if 3 > len(filetype) < 4:
                filetype = "jpeg"
            ContentType = 'image/{}'.format(filetype)
            Key = f"{S3_PREFIX}/{filename}"
            LOG.info(f"uploading: {filename}")
            bucket.put_object(Body=rec_file,
                              Key=Key,
                              ContentType=ContentType)
    return redirect('/listimages')


@bucket_handler.route('/list')
def list_imgs():
    bucket = s3.Bucket(S3_BUCKET_NAME)
    objs = bucket.objects.filter(Prefix=S3_PREFIX)
    ret = {"files": []}
    for x in objs:
        filename = x.key
        file_path = "{}/{}".format(S3_FULL_URL, filename)
        file_inf = {'url': file_path, 'name': filename}
        ret['files'].append(file_inf)
    return jsonify(ret)


@bucket_handler.route('/delete/<path:image>')
def delete_img(image):
    LOG.info(f"delete: {image}")

    bucket = s3.Bucket(S3_BUCKET_NAME)
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


@bucket_handler.route('/test/bucket/access')
def test_bucket():
    bucket = s3.Bucket(S3_BUCKET_NAME)
    try:
        bucket.objects.filter(Prefix=S3_PREFIX)
        return "ok"
    except:
        return "error"
