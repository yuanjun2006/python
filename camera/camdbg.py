#!/usr/bin/python

from socket import socket, AF_INET, SOCK_STREAM
import cv2
import time

_sock = None

def init(host, port):
    global _sock
    if not _sock:
        _sock = socket(AF_INET, SOCK_STREAM)
        _sock.connect((host, port))
    
def im_show_jpg(title, jpgbuf):
    global _sock
    if (len(title) <= 0 or len(title) > 19):
        return

    title += " " * (19 - len(title))
    
    # data = bytearray(encimg)
    
    buf = bytearray(32)
    width = 640
    height = 480
    buf  = (width).to_bytes(4, 'little', signed=True)
    buf += (height).to_bytes(4, 'little', signed=True)
    buf += (len(jpgbuf)).to_bytes(4, 'little', signed=True)
    buf += title.encode()
    buf += b'\0'
    _sock.send(buf)
    _sock.sendall(jpgbuf)
    return
    
def im_show(title, img, remote=True):
    if (len(title) <= 0 or len(title) > 19):
        return

    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    ret, encimg = cv2.imencode('.jpg', img, encode_param)
    if not ret:
        return

    im_show_jpg('Remote', bytearray(encimg))
