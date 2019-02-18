from improvisor import app, socketio

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(debug=True)


if __name__ == '__main__':
    print("")
    print("--- --- --- --- --- --- ---")
    print("-- Improvisor Web Server --")
    print("--- --- --- --- --- --- ---")
    print("")
    socketio.run(app, port=5000)
