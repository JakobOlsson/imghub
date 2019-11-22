import boto3
from os import getenv
from flask import Flask, render_template
from flask import request, redirect, jsonify
from werkzeug.utils import secure_filename
app = Flask(__name__)

# limit max payload to 50MB
app.config['MAX_CONTENT_LENGTH']

s3 = boto3.resource('s3',
                    endpoint_url=getenv('S3_URL', 'http://localhost:9000'),
                    config=boto3.session.Config(signature_version='s3v4'),
                    aws_access_key_id=getenv('AWS_ACCESS_KEY_ID', "AKIAIOSFODNN7EXAMPLE"),
                    aws_secret_access_key=getenv('AWS_SECRET_ACCESS_KEY', "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"))
s3cl = boto3.client('s3',
                    aws_access_key_id=getenv('AWS_ACCESS_KEY_ID', "AKIAIOSFODNN7EXAMPLE"),
                    aws_secret_access_key=getenv('AWS_SECRET_ACCESS_KEY', "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"))

s3_prefix = getenv("S3_PREFIX", 'images')


@app.route('/upload')
def upload_file_page():
    return render_template('upload.html')

@app.route('/listimages')
def listimages_page():
    return render_template('list.html')

@app.route('/uploader', methods=['GET', 'POST'])
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
            bucket = s3.Bucket(getenv("S3_BUCKET", "images"))
            filetype = filename.split('.')[-1]
            if 3 > len(filetype) > 4:
                filetype = "jpeg"
            ContentType = 'image/{}'.format(filetype)
            Key = "{}/{}".format(s3_prefix, filename)
            bucket.put_object(Body=rec_file,
                              Key=Key,
                              ContentType=ContentType)
    return redirect('/listimages')


@app.route('/list')
def list_imgs():
    bucket = s3.Bucket(getenv("S3_BUCKET", "images"))
    objs = bucket.objects.filter(Prefix='images')
    ret = {"files": []}
    for x in objs:
        filename = x.key
        ret['files'].append(filename)
    return jsonify(ret)


if __name__ == '__main__':
    debug = True if getenv('DEBUG', '').lower() == "true" else False
    print(debug)
    app.run(debug=debug, host='0.0.0.0')