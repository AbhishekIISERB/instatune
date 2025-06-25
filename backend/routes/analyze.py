from flask import Blueprint, request, jsonify
from services.blip import get_image_caption
from services.gemini import get_moods_from_caption, get_songs_for_moods

analyze_bp = Blueprint('analyze', __name__)

@analyze_bp.route('/analyze', methods=['POST'])
def analyze():
    file = request.files.get('image')
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    caption = get_image_caption(file)
    moods = get_moods_from_caption(caption)

    return jsonify({
        "caption": caption,
        "mood_options": moods
    })

@analyze_bp.route('/generate_songs', methods=['POST'])
def generate_songs():
    moods = request.json.get('selected_moods', [])
    if not moods:
        return jsonify({"error": "No moods selected"}), 400

    result = get_songs_for_moods(moods)
    return jsonify(result)