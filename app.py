### Avalition test for NAMA
# 


from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

# Server Port
srv_port = 9000

# Dictionary for imported data
dataDict = dict()

# Parse file to a list
def parse_to_array(rec_file):
    global dataDict
    line_count = 1
    
    # Iterate and relay lines
    for line in rec_file.split('\n'):
        # Split lines from 'TAB'
        dataList = list()
        for dt in line.split('\t'):
            dataList.append(dt)
        
        dataDict[line_count] = dataList
        line_count += 1


    #dataList = rec_file.split('\t')
    print(dataDict)


# Simple flask app to receive the file
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
        parse_to_array(content)
        
        
    return render_template('content.html', content=content) 

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=srv_port, debug = True)

