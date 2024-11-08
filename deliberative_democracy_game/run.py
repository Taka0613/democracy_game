from app import create_app, socketio
import os

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Bind to the Heroku $PORT
    socketio.run(app, host="0.0.0.0", port=port)
