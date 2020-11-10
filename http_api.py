import os
from flask import Flask, render_template, request, send_from_directory
from glob import glob
from hashlib import md5

# File upload directories
UPLOAD_STORE = os.getcwd() + '\\store'
TEMPORARY_STORE = os.getcwd() + '\\tmp'
# Instantiating a class Flask
app = Flask(__name__)
app.config['UPLOAD_STORE'] = UPLOAD_STORE
app.config['TEMPORARY_STORE'] = TEMPORARY_STORE


# Start page
@app.route('/')
def index():
    return render_template('start_page.html')


# Hash function
def hash_file(file):
    hash = md5()
    for segment in iter(lambda: file.read(4096), b""):
        hash.update(segment)
    return hash.hexdigest()


# File upload function
@app.route('/upload', methods=['POST'])
def upload():
    # Checking for the presence of a file in an HTTP request
    if 'file' not in request.files:
        return 'No file selected'
    # Saving and hashing a file
    file = request.files['file']
    path_tmp = os.path.join(app.config['TEMPORARY_STORE'], file.filename)
    file.save(path_tmp)
    ext = '.' + file.filename.split('.')[-1]

    with open(path_tmp, 'rb') as f:
        hash = hash_file(f)
    file.close()

    path = os.path.join(app.config['UPLOAD_STORE'], str(hash)[0:2])
    # Check for duplicates
    if os.path.exists(os.path.join(path, hash + ext)):
        os.remove(path_tmp)
        return 'The file is already uploaded'
    try:
        os.mkdir(path)
    except FileExistsError:
        pass
    # Saving in UPLOAD_STORE
    os.rename(path_tmp, os.path.join(path, hash + ext))
    # Returns a hash to the client
    return app.make_response('File hash: {0}'.format(hash))


# File download function
@app.route('/download/<hash>', methods=['GET'])
def download(hash):
    try:
        # Search for a file by hash
        path = os.path.join(app.config['UPLOAD_STORE'], hash[0:2])
        file_name = glob(os.path.join(path, hash + '.*'))[0].split("\\")[-1]
        # Returns the file to the client
        return send_from_directory(path, file_name)
    except IndexError:  # If the file is not found -> glob(os.path.join (path, hash + '. *')) = []
        return 'File not found'


# File delete function
@app.route('/delete/<hash>', methods=['DELETE'])
def delete(hash):
    # Search for a file by hash
    path = os.path.join(os.path.join(app.config['UPLOAD_STORE'], hash[0:2]))
    file_name = glob(os.path.join(path, hash + '.*'))[0]
    try:
        # Deleting a file
        os.remove(os.path.join(path, file_name))
        # Removing an empty subdirectory
        if not os.listdir(path):
            os.rmdir(path)
    except FileNotFoundError:
        return 'File not found'
    return 'File deleted'


if __name__ == "__main__":
    try:
        os.mkdir(UPLOAD_STORE)
        os.mkdir(TEMPORARY_STORE)
    except FileExistsError:
        pass
    app.run(debug=True)
