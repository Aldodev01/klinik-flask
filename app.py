from flask import Flask, render_template, request, json
from flaskext.mysql import MySQL
app = Flask(__name__)

mysql = MySQL()
app.config["MYSQL_DATABASE_USER"] = "root"
app.config["MYSQL_DATABASE_PASSWORD"] = ""
app.config["MYSQL_DATABASE_DB"] = "klinik"
app.config["MYSQL_DATABASE_HOST"] = "localhost"
mysql.init_app(app)
con = mysql.connect()
mycursor = con.cursor()

@app.route("/<username>")
def index(username):
    return render_template('index.html', data = username)

@app.route('/request', methods = ['POST'])
def cobarequest():
    _data = request.json
    return json.dumps({"data" : _data})

@app.route("/obat")
def getAllObat():
    sql = "SELECT * FROM obat"
    mycursor.execute(sql)
    data = mycursor.fetchall()

    return json.dumps({"data" : data})

@app.route("/obat", methods=["POST"])
def masukinObat():
    sql = "INSERT INTO obat (nama, jumlah, deskripsi) VALUES (%s, %s, %s)"
    nama = request.json['nama']
    jumlah = int(request.json['jumlah'])
    deskripsi = request.json['deskripsi']
    value = (nama, jumlah, deskripsi)
    mycursor.execute(sql, value)
    return json.dumps({
        "pesan" : "obat sudah masuk",
        "kode" : 200
    })

@app.route("/obat<id>", methods=["PUT"])
def editObat(id):
    sql = "UPDATE obat SET (nama = %s, jumlah = %s WHERE id = %s"
    nama = request.json['nama']
    jumlah = request.json['jumlah']
    value = (nama, jumlah, id)
    mycursor.execute(sql, value)
    return json.dumps({
        "pesan" : "obat sudah diedit",
        "kode" : 200
    })

if __name__ == "__main__":
    app.run("127.0.0.1", "5000", True)