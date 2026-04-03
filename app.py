import io
import os
import logging

os.environ.setdefault("SDL_AUDIODRIVER", "alsa")
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame
from flask import Flask, render_template, request, jsonify, Response
from flask_socketio import SocketIO, emit

from models import db, Button, init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///soundboard.db"
app.config["SECRET_KEY"] = os.urandom(24)

db.init_app(app)
socketio = SocketIO(app, async_mode="threading")

# In-memory sound cache: {button_id: pygame.mixer.Sound}
sound_cache = {}


def init_audio():
    try:
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        pygame.mixer.set_num_channels(16)
        logger.info("Audio initialized")
    except Exception as e:
        logger.warning("Could not initialize audio: %s", e)


def load_sound_cache():
    """Load all sound BLOBs from DB into pygame Sound objects."""
    sound_cache.clear()
    with app.app_context():
        buttons = Button.query.filter(Button.sound_data.isnot(None)).all()
        for btn in buttons:
            try:
                sound_cache[btn.id] = pygame.mixer.Sound(
                    io.BytesIO(btn.sound_data)
                )
                logger.info("Cached sound for button %d (%s)", btn.id, btn.label)
            except Exception as e:
                logger.warning(
                    "Failed to load sound for button %d: %s", btn.id, e
                )


def play_sound(button_id):
    sound = sound_cache.get(button_id)
    if sound:
        sound.play()
        return True
    logger.info("No sound cached for button %d", button_id)
    return False


# --- Routes ---


@app.route("/")
def index():
    buttons = Button.query.order_by(Button.position).all()
    return render_template("index.html", buttons=buttons)


@app.route("/api/buttons")
def api_buttons():
    buttons = Button.query.order_by(Button.position).all()
    return jsonify([b.to_dict() for b in buttons])


@app.route("/api/buttons/<int:button_id>", methods=["PUT"])
def update_button(button_id):
    btn = db.session.get(Button, button_id)
    if not btn:
        return jsonify({"error": "not found"}), 404

    data = request.get_json()
    if "label" in data:
        btn.label = data["label"]
    if "color" in data:
        btn.color = data["color"]
    if "gpio_pin" in data:
        btn.gpio_pin = data["gpio_pin"]

    db.session.commit()
    return jsonify(btn.to_dict())


@app.route("/api/buttons/<int:button_id>/sound", methods=["POST"])
def upload_sound(button_id):
    btn = db.session.get(Button, button_id)
    if not btn:
        return jsonify({"error": "not found"}), 404

    if "sound" not in request.files:
        return jsonify({"error": "no file provided"}), 400

    f = request.files["sound"]
    btn.sound_data = f.read()
    btn.sound_filename = f.filename
    db.session.commit()

    # Refresh cache for this button
    try:
        sound_cache[btn.id] = pygame.mixer.Sound(io.BytesIO(btn.sound_data))
    except Exception as e:
        logger.warning("Failed to cache uploaded sound: %s", e)

    return jsonify(btn.to_dict())


@app.route("/api/buttons/<int:button_id>/sound", methods=["DELETE"])
def delete_sound(button_id):
    btn = db.session.get(Button, button_id)
    if not btn:
        return jsonify({"error": "not found"}), 404

    btn.sound_data = None
    btn.sound_filename = ""
    db.session.commit()
    sound_cache.pop(btn.id, None)
    return jsonify(btn.to_dict())


@app.route("/api/buttons/<int:button_id>/sound", methods=["GET"])
def get_sound(button_id):
    btn = db.session.get(Button, button_id)
    if not btn or not btn.sound_data:
        return jsonify({"error": "no sound"}), 404

    filename = btn.sound_filename.lower()
    if filename.endswith(".mp3"):
        mimetype = "audio/mpeg"
    elif filename.endswith(".ogg"):
        mimetype = "audio/ogg"
    else:
        mimetype = "audio/wav"

    return Response(btn.sound_data, mimetype=mimetype)


# --- SocketIO ---


@socketio.on("button_press")
def handle_button_press(data):
    button_id = data.get("button_id")
    if button_id is None:
        return

    logger.info("Button press: %s", button_id)
    play_sound(int(button_id))
    emit("button_feedback", {"button_id": button_id}, broadcast=True)


@socketio.on("connect")
def handle_connect():
    logger.info("Client connected")


if __name__ == "__main__":
    init_audio()
    init_db(app)
    load_sound_cache()
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
