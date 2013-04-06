from flask import Flask, render_template, request, send_from_directory 
import random
import os
import pymongo

db = pymongo.MongoClient("localhost", 27017).upload
app = Flask(__name__)
if not os.path.exists("files"):
    os.mkdir("files")
@app.route("/", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        name = file.filename
        name = name.split(".")
        name_2 = ''
        while True:
            for x in range(10):
                name_2 = name_2 + random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890") 
            if os.path.exists("files/"+name_2+name[1]):
                continue
            else:
                break
        data = file.read()
        with open("files/"+name_2+"."+name[1], 'wb') as file:
            file.write(data)
        db.files.insert({"id":name_2, "extension":name[1], "name":name[0]})
        return name_2
    return render_template("index.html")

@app.route("/download/<file>")
def download(file):
    a = db.files.find_one({"id":file})
    return send_from_directory("files", file+"."+a['extension'])
app.run(debug=True)
