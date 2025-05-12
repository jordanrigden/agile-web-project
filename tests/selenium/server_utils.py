from threading import Thread
from werkzeug.serving import make_server
from app import app 

class ServerThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.server = make_server("127.0.0.1", 5000, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        print("🚀 Starting Flask live server for tests...")
        self.server.serve_forever()

    def shutdown(self):
        print("🛑 Shutting down Flask test server...")
        self.server.shutdown()
