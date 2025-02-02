from flask import Flask
import uuid

app = Flask(__name__)

receipts = {}

@app.route("/receipts/process", methods=['POST'])
def process_receipt():
    uid = str(uuid.uuid4())
    receipts[uid] = 10000
    return {"id": uid}

@app.route("/receipts/<string:id>/points", methods=['GET'])
def get_receipt_points(id):
    return {"points": receipts[id]}
    

if __name__ == '__main__':
    app.run(debug=True)
