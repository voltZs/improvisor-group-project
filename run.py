from improvisor import app, socketio

if __name__ == '__main__':
    print("")
    print("--- --- --- --- --- --- ---")
    print("-- Improvisor Web Server --")
    print("--- --- --- --- --- --- ---")
    print("")
    socketio.run(app, port=5000)
