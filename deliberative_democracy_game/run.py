# run.py

from app import create_app, socketio

# Create the Flask app instance
app = create_app()

# Main entry point for Heroku
if __name__ == "__main__":
    # Use eventlet or gevent for production if you're using SocketIO
    socketio.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
