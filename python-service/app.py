from flask import Flask
from controllers.upload_controller import UploadController
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.register_blueprint(UploadController()())

if __name__ == '__main__':
    app.run(debug=True)