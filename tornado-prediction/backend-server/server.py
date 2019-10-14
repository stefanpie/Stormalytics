from flask import Flask, request, send_from_directory
import os


app = Flask(__name__, static_url_path='/static')
prediction_file_name = "prediction.json"

@app.route('/api/tornado-prediction')
def hello_world():
    return app.send_static_file(prediction_file_name)
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)

