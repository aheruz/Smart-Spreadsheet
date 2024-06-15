from flask import Flask
from controllers.upload_controller import upload_bp

app = Flask(__name__)
app.register_blueprint(upload_bp)

if __name__ == '__main__':
    app.run(debug=True)