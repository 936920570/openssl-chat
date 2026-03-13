import datetime
import os.path
import socket
import ssl
import threading
from Crypto.Cipher import AES
recorder = None
clientNumber=0
class chat_recorder:
    def __init__(self, passwd="123"):
        self.passwd = passwd.encode('utf-8')
        while len(self.passwd) <= 16:
            self.passwd = self.passwd + b'\x00'
        self.passwd = self.passwd[0:16]
        self.buff = ""

    def record(self, sender, content):
        msg = "[ {} ] {} --> {}".format(datetime.datetime.now(), sender, content)
        self.buff = "{}\n{}".format(self.buff, msg)

    def writefile(self, file):
        aes = AES.new(self.passwd, AES.MODE_ECB)
        text = self.buff.encode('utf-8')
        while len(text) % AES.block_size != 0:
            text = text + b'\x00'
        file.write(aes.encrypt(text))

class ssl_client:
    def __init__(self, ssl_client, ssl_client_address,cn):
        self.client = ssl_client
        self.addr = ssl_client_address
        self.number=cn

    def send_messages(self, ssl_client):
        global recorder
        while True:
            send_msg = input("\nServer> ".format(self.addr)).encode("utf-8")
            recorder.record("Server", send_msg.decode())
            try:
                ssl_client.send(send_msg)
            except:
                print("Connection from "+str(self.number)+"closed.")

    def setup(self):
        ssl_client = self.client
        send_thread = threading.Thread(target=self.send_messages, args=(ssl_client,))
        send_thread.setDaemon(True)
        send_thread.start()

        global recorder
        while True:
            recv_data = ssl_client.recv(1024)
            if recv_data:
                print('\n'+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" Client> ".format(self.addr), recv_data.decode())
                recorder.record("Client",recv_data.decode())
            else:
                break
        print("\nClient:{} Log out.\nChatting records saved under /chat_records.".format(self.number))
        if not os.path.exists("./chat_records"):
            os.mkdir("./chat_records")
        filename=str(self.number)+" time:"+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file = open("./chat_records/{}".format(filename),"wb")
        recorder.writefile(file)
        ssl_client.close()
        
            
class myserver:
    def __init__(self, port, client_num=100):
        self.port = port
        self.client_num = client_num

    def setup(self):
        global clientNumber
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER, )
        context.verify_mode = ssl.CERT_REQUIRED

        context.load_cert_chain('cert/server.crt', 'cert/server.key')
        context.load_verify_locations('cert/ca.crt')

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
            sock.bind(('0.0.0.0', self.port))
            sock.listen(self.client_num)
            print("Listening to client...")

            with context.wrap_socket(sock, server_side=True, ) as ssock:
                while True:

                    try:
                        client_socket, addr = ssock.accept()
                    except:
                        print("Connection failed.")
                        continue

                    client = ssl_client(client_socket, addr,clientNumber)

                    thd = threading.Thread(target=client.setup, args=())
                    thd.setDaemon(True)
                    thd.start()
                    print("Connected to client.\nNumber:"+str(clientNumber))
                    clientNumber+=1


if __name__ == "__main__":
    passwd = input("input passwd:") or "123"
    recorder = chat_recorder(passwd)
    server = myserver(port=23333)
    server.setup()
