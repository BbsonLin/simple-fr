import os
import logging
import cognitive_face as MS_CF

from flask import Flask, request, redirect, session, render_template, send_from_directory
from livereload import Server
from utils import export_ms_result_images

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
# file_handler = logging.FileHandler('debug.log')
# file_handler.setFormatter(logging.Formatter(
#     '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
# ))
# app.logger.addHandler(file_handler)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    target = os.path.join(app.root_path, 'images')

    if not os.path.isdir(target):
        os.mkdir(target)
    else:
        app.logger.info("Couldn't create upload directory: {}".format(target))
    app.logger.info(request.files.getlist("file"))
    for upload in request.files.getlist("file"):
        app.logger.info(upload)
        app.logger.info("{} is the file name".format(upload.filename))
        filename = upload.filename
        destination = "/".join([target, filename])
        app.logger.info("Accept incoming file: {}".format(filename))
        app.logger.info("Save it to: {}".format(destination))
        upload.save(destination)
        session['filename'] = filename
        session['destination'] = destination

    return redirect('analyze')


@app.route('/upload/<filename>')
def send_image(filename):
    target = os.path.join(app.root_path, 'images/')
    return send_from_directory(target, filename)


@app.route('/analyze', methods=['GET'])
def analyze():
    if os.getenv('MS_KEY'):
        MS_CF.Key.set(os.getenv('MS_KEY'))
    else:
        raise AssertionError('Please set your Microsoft Face API Key')

    if os.getenv('MS_URL'):
        MS_CF.BaseUrl.set(os.getenv('MS_URL'))
    else:
        raise AssertionError('Please set your Microsoft Face API URL')

    faces = MS_CF.face.detect(session['destination'],
                              attributes='age,gender,headPose,smile,facialHair,glasses,emotion' +
                              ',hair,makeup,occlusion,accessories,blur,exposure,noise')
    app.logger.debug("Get Result: {}".format(faces))
    export_ms_result_images(session['destination'], faces)
    return render_template('result.html',
                           image_name='{}_result{}'.format(
                                os.path.splitext(session['filename'])[0],
                                os.path.splitext(session['filename'])[1]))


@app.cli.command('serve', help='Run a live reload server for development.')
def serve_app():
    server = Server(app.wsgi_app)
    # server.watch
    server.serve()
