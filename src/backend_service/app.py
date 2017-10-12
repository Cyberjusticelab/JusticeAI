from flask import Flask, request, jsonify
import database

app = Flask(__name__)


@app.route("/")
def hello():
    con, meta = database.connect('postgres', 'DEV_PASS_NOT_SECRET', 'postgres')

    con.execute("CREATE TABLE IF NOT EXISTS " +
                "testing (test_data text)")
    con.execute("INSERT INTO testing (test_data) " +
                "VALUES ('this works!')")
    results = con.execute("SELECT * FROM testing")
    result = ''
    for row in results:
        result += row['test_data'] + '\n'

    return result


@app.route("/newchat", methods=['GET', 'POST'])
def init_session():
    if request.method == 'GET':
        data = {'id': 12345}
        return jsonify({'session': data})
