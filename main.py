from network.app import app, check_peer_availability
from model.__main__ import main as model_main
import threading


def application(environ, start_resp):
    # Start the thread for checking peer availability
    threading.Thread(target=check_peer_availability).start()
    threading.Thread(target=model_main).start()
    # Run Flask app
    app.run()