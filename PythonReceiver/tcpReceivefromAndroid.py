import socket
import cv2
import numpy as np


MAX_DGRAM = 6550

JPEGSTART = bytearray(b'\xff\xd8')
JPEGEND = bytearray(b'\xff\xd9')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 8888))
s.listen(1)
conn, addr = s.accept()
print("connected to ", addr[0])
##---------------------------------------------------------------------------------------------------



def getFrameFromSocket():
    rBytes = bytearray()
    streamIsOpen = False
    seg= conn.recv(MAX_DGRAM)
    rBytes.extend(bytearray(seg))
    streamIsOpen = True
    while(streamIsOpen == True):
        
        if((rBytes[:2] == JPEGSTART)):
            rBytes = bytearray(seg)
        else:
            seg= conn.recv(MAX_DGRAM)
            rBytes.extend(bytearray(seg))



        if (rBytes[-2:] == JPEGEND):
            streamIsOpen = False
            buffer = bytes(rBytes[4:])
            _image = cv2.imdecode(np.frombuffer(buffer, dtype=np.uint8), cv2.IMREAD_COLOR)
            return _image

    

while 1:
    color_image = getFrameFromSocket()    
    if(color_image is not None):

        scale_percent = 40 # percent of original size
        width = int(color_image.shape[1] * scale_percent / 100)
        height = int(color_image.shape[0] * scale_percent / 100)
        dim = (width, height)

        # resize image
        resized = cv2.resize(color_image, dim, interpolation = cv2.INTER_AREA)
        resized = cv2.rotate(resized, cv2.ROTATE_90_CLOCKWISE)
        cv2.imshow(" ", resized)
        cv2.waitKey(0)
        s.close()
    