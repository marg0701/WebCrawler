from api import app

def start_app():
    app.run(
        host='0.0.0.0',
        port='5000',
        debug=True,
        use_reloader=False
    )
