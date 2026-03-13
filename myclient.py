import socket
import ssl
from threading import Thread
from time import sleep
import datetime

class myclient:
    def __init__(self):
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        self.context.load_verify_locations('cert/ca.crt')
        self.context.load_cert_chain('cert/client.crt', 'cert/client.key')
        self.context.check_hostname = False

    def receive_messages(self, ssock):
        while True:
            msg = ssock.recv(1024).decode("utf-8")
            if len(msg) >= 0:
                print('\n'+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+f" Server> {msg}")

    def connect(self):
        with socket.create_connection(('127.0.0.1', 23333)) as sock:
            with self.context.wrap_socket(sock, server_hostname='myserver') as ssock:
                receive_thread = Thread(target=self.receive_messages, args=(ssock,))
                receive_thread.setDaemon(True)
                receive_thread.start()

                while True:
                    send_msg = input("\nClient> ") or "exit"
                    if send_msg == "exit":
                        break
                    ssock.send(send_msg.encode("utf-8"))

if __name__ == "__main__":
    client = myclient()
    client.connect()
