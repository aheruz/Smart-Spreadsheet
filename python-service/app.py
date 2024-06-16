from flask import Flask
from controllers.upload_controller import UploadController
from controllers.assistant_controller import AssistantController
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
app.register_blueprint(UploadController()())
app.register_blueprint(AssistantController()())
CORS(app)

if __name__ == '__main__':
    app.run(debug=True)