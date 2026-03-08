"""
Mesh Networking for v5.0
Offline P2P communication via UDP Broadcast
"""
import socket
import threading

class MeshNetwork:
    def __init__(self, port=12345):
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def broadcast_message(self, message):
        """Send message to all devices on local network"""
        self.sock.sendto(message.encode(), ('<broadcast>', self.port))

    def listen(self, callback):
        """Listen for incoming mesh messages"""
        self.sock.bind(('', self.port))
        def _listen():
            while True:
                data, addr = self.sock.recvfrom(1024)
                callback(data.decode(), addr)

        threading.Thread(target=_listen, daemon=True).start()
