import os
from flask import Flask, flash, request, redirect, render_template, url_for
from werkzeug.utils import secure_filename

app=Flask(__name__)

app.secret_key = "dorina's secret key"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Get current path
path = os.getcwd()
# file Upload
UPLOAD_FOLDER = os.path.join(path, 'static/uploads')

# Make directory if uploads is not exists
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Pictures allowed extentions
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('upload.html')


@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':

        if 'imgs' not in request.files:
            flash('No image found')
            return redirect(request.url)

        files = request.files.getlist('imgs')
        file_names = []
        for file in files:
            if file and allowed_file(file.filename):
                file_name = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
                file_names.append(file_name)
            else:
                flash('file type not accepted please only upload images files with extenstions - png, jpg, jpeg')
                return redirect('/')

        flash('File(s) successfully uploaded')
        return render_template('upload.html', filenames = file_names)
    else:
        return 'upload faileds'

@app.route('/display/<filename>')
def display_image(filename):
	return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000)