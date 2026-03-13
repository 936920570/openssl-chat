# OpenSSL Secure Chat System

A simple half-duplex secure chat system based on Python and OpenSSL. After the chat session ends, the chat records can be encrypted and saved locally.

## Instructions

### Dependencies
```bash
pip install pycryptodome==3.16.0
```

### Generate Certificates
```bash
cd cert
make cert
```

### Clean Certificates
```bash
cd cert
make clean
```

### Start the Server (Default port 23333)
```bash
python3 server.py
# or python3 myserver.py
```

Follow the prompts to configure a secret key. At the end of the session, chat logs will be encrypted and stored in the `record` or `chat_records` directory.

### Start the Client
```bash
python3 client.py
# or python3 myclient.py
```
It will automatically try to connect to the server (127.0.0.1:23333).

### Decrypt Chat Records
```bash
python3 decrypt.py <record_file_path>
```
Follow the prompts, provide the paths and the secret key to decrypt and read the plain records.

## Acknowledgements

Some structural ideas and logic were inspired by open-source projects on the internet.