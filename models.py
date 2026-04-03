from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_BUTTONS = [
    {"position": 0, "label": "Sound 1", "color": "#e74c3c", "gpio_pin": 17},
    {"position": 1, "label": "Sound 2", "color": "#e67e22", "gpio_pin": 27},
    {"position": 2, "label": "Sound 3", "color": "#f1c40f", "gpio_pin": 22},
    {"position": 3, "label": "Sound 4", "color": "#2ecc71", "gpio_pin": 23},
    {"position": 4, "label": "Sound 5", "color": "#3498db", "gpio_pin": 24},
    {"position": 5, "label": "Sound 6", "color": "#9b59b6", "gpio_pin": 25},
    {"position": 6, "label": "Sound 7", "color": "#1abc9c", "gpio_pin": 5},
    {"position": 7, "label": "Sound 8", "color": "#e84393", "gpio_pin": 6},
]


class Button(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.Integer, unique=True, nullable=False)
    label = db.Column(db.String(50), default="")
    color = db.Column(db.String(7), default="#888888")
    gpio_pin = db.Column(db.Integer, nullable=True)
    sound_data = db.Column(db.LargeBinary, nullable=True)
    sound_filename = db.Column(db.String(100), default="")

    def to_dict(self):
        return {
            "id": self.id,
            "position": self.position,
            "label": self.label,
            "color": self.color,
            "gpio_pin": self.gpio_pin,
            "sound_filename": self.sound_filename,
            "has_sound": self.sound_data is not None,
        }


def init_db(app):
    with app.app_context():
        db.create_all()
        if Button.query.count() == 0:
            for btn in DEFAULT_BUTTONS:
                db.session.add(Button(**btn))
            db.session.commit()
