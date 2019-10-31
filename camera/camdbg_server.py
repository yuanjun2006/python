import cv2
import numpy as np
import socket
import threading
import struct
import time

CHAR_q = 113
CHAR_Q = 81

HEADER_SIZE = 32

client = None
def decode_jpg(jpgbuf):
    '''@jpgbuf is bytearray, jpeg data'''
    
    #jpgdata = np.frombuffer(frame)
    #rgb = cv2.imdecode(np.fromstring(bytes(jpgbuf), dtype=np.uint8), cv2.IMREAD_COLOR)
    rgb = cv2.imdecode(np.asarray(jpgbuf, dtype=np.uint8), cv2.IMREAD_COLOR)
    return rgb

class Camera():
    '''camera sending jpg by tcp'''
    def __init__(self, sock):
        self._sock = sock
        self._rbuf = bytearray()
        pass

    def recv(self):
        chunk = self._sock.recv(64 * 1024)
        if chunk == b'':
            return 0
#            raise RuntimeError("socket peer closed")

        self._rbuf += chunk
        return len(chunk)
    
    def get_image(self):
        if len(self._rbuf) < HEADER_SIZE:
            return False, 0, 0, "   ", None
    
        print("_rbuf %d" % (len(self._rbuf)))

        w, h, size = struct.unpack('<III', self._rbuf[0:12])
        print('get_image [%d, %d, %d]' % (w, h, size))

        if len(self._rbuf) < (size + HEADER_SIZE): # not complete packet
            return False, 0, 0, "   ", None
        
        frame = self._rbuf[HEADER_SIZE: HEADER_SIZE + size]
        
        # remove this packet
        del self._rbuf[0:HEADER_SIZE + size]
        
        return True, w, h, '   ', frame
        
class CamdbgServer():
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._sock = None
    
    def start(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind((self._host, self._port))
        self._sock.listen(1)
        return True
    
    def accept(self):
        return self._sock.accept()
    
    def close(self):
        self._sock.close()        
        
def clients_thread():
    sleep_time = 0
    
    while True:
        time.sleep(sleep_time)
        print('clients_thread loop')
        if not client:
            sleep_time = 0.5
            continue
        
        ret = client.recv()
        if ret < 0:
            client.close()
            client = None
            sleep_time = 0.5
            continue
        
        sleep_time = 0.1

        if ret == 0:
            continue
        
        ret, w, h, title, frame = client.get_image()
        if not ret:
            continue
        
        
def main():
    # t = threading.Thread(target=clients_thread)
    # t.start()
    
    serv = CamdbgServer('192.168.10.152', 5000)
    serv.start()
    
    print('main start...')
    
    while True:
        sock, addr = serv.accept()
        if not sock:
            continue

        print('new client')

        c = Camera(sock)
        while True:
            ret = c.recv()
            if not ret:
                cv2.destroyAllWindows()
                print('Client closed')
                break

            r, w, h, title, frame = c.get_image()
            if not r:
                continue
            print('[%dx%d, %d]' % (w, h, len(frame)))
            rgb = decode_jpg(frame)
            cv2.imshow('Frame', rgb)
            key = cv2.waitKey(33)
            if key == CHAR_q or key == CHAR_Q:
                print('User interruptted')
                break
    
if __name__ == '__main__':
    main()

'''
im1 = cv2.imread("d:/test.jpg")
im2 = cv2.imread("d:/test1.jpg")

while True:
    cv2.imshow('Frame', im1)
    key = cv2.waitKey(33)
    if key == 113:
        break

    cv2.imshow('Frame', im2)
    key = cv2.waitKey(33)
    print(key)
    if key == 113: # key 'q' == 113, 'Q' == 81
        break

cv2.destroyAllWindows()

print('Quit')
'''