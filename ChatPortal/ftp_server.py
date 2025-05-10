from pyftpdlib.servers import FTPServer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.authorizers import DummyAuthorizer

def start_ftp():
    authorizer = DummyAuthorizer()
    authorizer.add_user("user", "12345", "./ftp_files", perm="elradfmwMT")
    handler = FTPHandler
    handler.authorizer = authorizer

    server = FTPServer(("0.0.0.0", 2121), handler)  # Listen on all IPs (0.0.0.0) and port 2121
    server.serve_forever()

if __name__ == "__main__":
    start_ftp()