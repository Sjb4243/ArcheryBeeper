from flask import Flask, render_template, redirect, request, url_for
import threading
import queue
import pygame
from flask_socketio import SocketIO, emit
import dbus

def queue_watcher(commqueue, socketio, state_store, state_lock):
    while True:
        try:
            state = commqueue.get(timeout=0.5)
            print(f"STATE IS {state}")
            with state_lock:
                state_store["current_state"] = state
            # Emit an event to all connected clients
            socketio.emit("update_ui", {"state": state})
        except queue.Empty:
            continue
        except Exception as e:
            print("Error emitting state:", e)

def start_flask(commqueue):
    global iface
    bus = dbus.SessionBus()
    spotify = bus.get_object("org.mpris.MediaPlayer2.spotify",
                             "/org/mpris/MediaPlayer2")
    iface = dbus.Interface(spotify, "org.mpris.MediaPlayer2.Player")
    app = Flask(__name__, static_url_path='/static')
    global socketio
    socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")  # Allow JS from any origin

    state_store = {"current_state": "main_menu"}
    state_lock = threading.Lock()

    threading.Thread(
        target=queue_watcher,
        daemon=True,
        args=(commqueue, socketio, state_store, state_lock),
    ).start()
    key_map = {
        "f": pygame.K_f,
        "space": pygame.K_SPACE,
        "d": pygame.K_d,
        "p": pygame.K_p,
        "escape": pygame.K_ESCAPE,
        "1": pygame.K_1,
        "c": pygame.K_c,
    }

    @app.route("/control_music", methods=["POST"])
    def control_music():
        iface.PlayPause()
        return ("", 204)

    @app.route("/")
    def index():
        return render_template("base.js")

    @socketio.on("connect")
    def handle_connect():
        print("Socket client connected")
        with state_lock:
            current_state = state_store["current_state"]
        emit("update_ui", {"state": current_state})

    @socketio.on("disconnect")
    def handle_disconnect():
        print("Socket client disconnected")


    @app.route("/send_pygame", methods=["POST"])
    def send_pygame():
        key = request.form.get("key")
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=key_map[key]))
        return ("", 204)
    socketio.run(app, host="0.0.0.0", port=8000, allow_unsafe_werkzeug=True)





