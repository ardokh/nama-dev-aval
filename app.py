### Avalition test for NAMA
# 


from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

# Server Port
srv_port = 9000

# Basic flask app to receive the file
app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "receveid/"

@app.route('/')
def upload_file():
    return render_template('index.html')


@app.route('/display', methods = ['GET', 'POST'])
def save_file():
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)

        f.save(app.config['UPLOAD_FOLDER'] + filename)

        file = open(app.config['UPLOAD_FOLDER'] + filename,"r")
        content = file.read()
        
        
    return render_template('content.html', content=content) 

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=srv_port, debug = True)

