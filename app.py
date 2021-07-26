### Avalition test for NAMA
#> Receive dados.txt file from web form
#> Parse the file
#> Create and populate DB
#> Display on records
#
# Author: Luca CG
# 2021-Jul-25

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import sqlite3

# Server Port
srv_port = 9000

# Database file
db_file = 'nama-avail.db'

# Dictionary for imported data
dataDict = dict()

# Register as string for DB results
dbRegisters = str()


def database_relay():
    global dataDict
    global dbRegisters
    # 'Connect' to database, in this case; a file
    conn = sqlite3.connect(db_file)
    # Check if table exists
    if conn.execute("SELECT name FROM sqlite_master WHERE type='table';") == "DADOS":
        print("Table DADOS exists")
    else:
        # Create table
        conn.execute('''CREATE TABLE DADOS
        (ID INT PRIMARY KEY     NOT NULL,
        "%s"  TEXT                NOT NULL,
        "%s"  TEXT                NOT NULL,
        "%s"  TEXT                NOT NULL,
        "%s"  TEXT                NOT NULL,
        "%s"  TEXT                NOT NULL,
        "%s"  TEXT                NOT NULL);
        ''' %(dataDict[1][0], dataDict[1][1], dataDict[1][2], dataDict[1][3], \
                dataDict[1][4], dataDict[1][5]))
        print("Table DADOS created in database: %s" %db_file)
        # Populate new table
        id_count = 1
        dataHeader = dataDict[1]
        dataDict.pop(1)
        for ndata in dataDict:
            if len(dataDict[ndata]) < 2: break
            conn.execute('INSERT INTO DADOS (ID, "%s","%s","%s","%s","%s","%s") \
                    VALUES ("%i", "%s","%s",%s,%s,"%s","%s")' %(dataHeader[0], dataHeader[1], \
                    dataHeader[2], dataHeader[3], dataHeader[4], dataHeader[5], \
                    id_count, dataDict[ndata][0], dataDict[ndata][1], dataDict[ndata][2], \
                    dataDict[ndata][3], dataDict[ndata][4], dataDict[ndata][5]))
            id_count += 1
        conn.commit()
    # Adjust, display and save registers
    c = conn.cursor()
    c.execute('SELECT * FROM DADOS')
    dbRegisters = c.fetchall()
    for row in dbRegisters: print(row)
    print("Records created into database")
    conn.close()


# Parse file to dictionary
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


    print("File parse success")



# Simple flask app to receive the file
app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "receveid/"

@app.route('/')
def upload_file():
    return render_template('index.html')


@app.route('/display', methods = ['GET', 'POST'])
def save_file():
    global dbRegisters
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)

        f.save(app.config['UPLOAD_FOLDER'] + filename)

        file = open(app.config['UPLOAD_FOLDER'] + filename,"r")
        content = file.read()
        print("File receveid\n"+content)
        parse_to_array(content)

        database_relay()
        fullDisplay = "[RAW file]\n"+content+"\n[DATABASE Registers]\n"+str(dbRegisters)
        
    return render_template('content.html', content=fullDisplay) 

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=srv_port, debug = True)

