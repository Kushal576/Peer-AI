from network.app import app, check_peer_availability
import threading
if __name__ == '__main__':
    # Start the thread for checking peer availability
    threading.Thread(target=check_peer_availability).start()
    # Run Flask app
    app.run(host='0.0.0.0', port=8000)