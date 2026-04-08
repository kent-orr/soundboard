from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_BUTTONS = [
    # Row 1: left to right
    {"position": 0, "label": "R1", "color": "#e74c3c", "gpio_pin": 17},
    {"position": 1, "label": "G1", "color": "#2ecc71", "gpio_pin": 27},
    {"position": 2, "label": "B1", "color": "#3498db", "gpio_pin": 22},
    {"position": 3, "label": "Y1", "color": "#f1c40f", "gpio_pin": 23},
    {"position": 4, "label": "W1", "color": "#ecf0f1", "gpio_pin": 24},
    # Row 2: left to right
    {"position": 5, "label": "R2", "color": "#e74c3c", "gpio_pin": 25},
    {"position": 6, "label": "G2", "color": "#2ecc71", "gpio_pin": 5},
    {"position": 7, "label": "B2", "color": "#3498db", "gpio_pin": 6},
    {"position": 8, "label": "Y2", "color": "#f1c40f", "gpio_pin": 16},
    {"position": 9, "label": "W2", "color": "#ecf0f1", "gpio_pin": 26},
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
