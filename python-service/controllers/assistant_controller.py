from flask import Blueprint, jsonify
from app.openai_service import OpenAiService

class AssistantController:
    def __init__(self):
        self._assistant_bp = Blueprint('assistant', __name__)
        self._openai_service = OpenAiService()
        self._assistant_bp.add_url_rule('/assistant', 'get_or_create_assistant', self.get_or_create_assistant, methods=['GET'])

    def get_or_create_assistant(self):
        assistant_id = self._openai_service.get_or_create_assistant()
        return jsonify(assistant_id), 200

    def __call__(self):
        return self._assistant_bp