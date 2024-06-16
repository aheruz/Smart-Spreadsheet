from flask import Flask
from controllers.upload_controller import UploadController
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
app.register_blueprint(UploadController()())
CORS(app)

if __name__ == '__main__':
    app.run(debug=True)