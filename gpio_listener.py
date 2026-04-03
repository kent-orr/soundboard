#!/usr/bin/env python3
"""
GPIO listener for the soundboard.
Runs as a separate process, monitors physical buttons and sends
press events to Flask via SocketIO.

Usage:
    python gpio_listener.py          # Real GPIO on Raspberry Pi
    python gpio_listener.py --mock   # Keyboard mock for development
"""

import argparse
import signal
import sys
import time
import logging

import socketio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

FLASK_URL = "http://localhost:5000"
BOUNCE_TIME_MS = 300


def get_button_config(sio_client):
    """Fetch button-to-pin mapping from Flask API."""
    import urllib.request
    import json

    try:
        with urllib.request.urlopen(FLASK_URL + "/api/buttons") as resp:
            buttons = json.loads(resp.read())
        pin_map = {}
        for btn in buttons:
            if btn.get("gpio_pin") is not None:
                pin_map[btn["gpio_pin"]] = btn["id"]
        return pin_map
    except Exception as e:
        logger.error("Failed to fetch button config: %s", e)
        return {}


def run_gpio(sio_client):
    """Run with real RPi.GPIO."""
    import RPi.GPIO as GPIO

    pin_map = get_button_config(sio_client)
    if not pin_map:
        logger.error("No button config available, exiting")
        sys.exit(1)

    logger.info("GPIO pin mapping: %s", pin_map)

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    for pin in pin_map:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def on_press(channel):
        button_id = pin_map.get(channel)
        if button_id is not None:
            logger.info("GPIO %d pressed -> button %s", channel, button_id)
            sio_client.emit("button_press", {"button_id": button_id})

    for pin in pin_map:
        GPIO.add_event_detect(
            pin, GPIO.FALLING, callback=on_press, bouncetime=BOUNCE_TIME_MS
        )

    logger.info("GPIO listener running. Press Ctrl+C to stop.")

    def cleanup(*_):
        GPIO.cleanup()
        sys.exit(0)

    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)
    signal.pause()


def run_mock(sio_client):
    """Mock mode: use keyboard number keys 1-8 to simulate button presses."""
    pin_map = get_button_config(sio_client)
    if not pin_map:
        logger.warning("No button config, using default IDs 1-8")

    # Fetch button IDs in position order
    import urllib.request
    import json

    button_ids = []
    try:
        with urllib.request.urlopen(FLASK_URL + "/api/buttons") as resp:
            buttons = json.loads(resp.read())
        buttons.sort(key=lambda b: b["position"])
        button_ids = [b["id"] for b in buttons]
    except Exception:
        button_ids = list(range(1, 9))

    print("\n--- Mock GPIO Mode ---")
    print("Press keys 1-8 to simulate button presses, 'q' to quit.\n")
    for i, bid in enumerate(button_ids):
        print(f"  Key {i + 1} -> Button ID {bid}")
    print()

    while True:
        try:
            key = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if key.lower() == "q":
            break

        try:
            idx = int(key) - 1
            if 0 <= idx < len(button_ids):
                bid = button_ids[idx]
                logger.info("Mock press -> button %s", bid)
                sio_client.emit("button_press", {"button_id": bid})
            else:
                print("Invalid key. Use 1-8.")
        except ValueError:
            print("Invalid input. Use 1-8 or 'q' to quit.")


def main():
    parser = argparse.ArgumentParser(description="Soundboard GPIO listener")
    parser.add_argument(
        "--mock", action="store_true", help="Use keyboard input instead of GPIO"
    )
    parser.add_argument("--url", default=FLASK_URL, help="Flask server URL")
    args = parser.parse_args()

    global FLASK_URL
    FLASK_URL = args.url

    sio = socketio.Client(reconnection=True, reconnection_delay=1)

    @sio.event
    def connect():
        logger.info("Connected to Flask server at %s", FLASK_URL)

    @sio.event
    def disconnect():
        logger.warning("Disconnected from Flask server")

    logger.info("Connecting to %s ...", FLASK_URL)
    try:
        sio.connect(FLASK_URL)
    except Exception as e:
        logger.error("Could not connect to Flask server: %s", e)
        sys.exit(1)

    if args.mock:
        run_mock(sio)
    else:
        run_gpio(sio)

    sio.disconnect()


if __name__ == "__main__":
    main()
