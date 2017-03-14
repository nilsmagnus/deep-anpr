import cv2
import numpy as np

def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )

def find_squares(img):
    img = cv2.GaussianBlur(img, (5, 5), 0)
    squares = []
    for gray in cv2.split(img):
        for thrs in xrange(0, 255, 26):
            if thrs == 0:
                bin = cv2.Canny(gray, 0, 50, apertureSize=5)
                bin = cv2.dilate(bin, None)
            else:
                retval, bin = cv2.threshold(gray, thrs, 255, cv2.THRESH_BINARY)
                bin, contours, hierarchy = cv2.findContours(bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
                for cnt in contours:
                    cnt_len = cv2.arcLength(cnt, True)
                    cnt = cv2.approxPolyDP(cnt, 0.05*cnt_len, True)
                    if len(cnt) == 4 and cv2.contourArea(cnt) > 100 and cv2.isContourConvex(cnt):
                        cnt = cnt.reshape(-1, 2)
                        max_cos = np.max([angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in xrange(4)])
                        if max_cos < 0.1:
                            squares.append(cnt)
    return squares

def showtime():
    cam = cv2.VideoCapture(0)
    while True:
        ret_val, img = cam.read()
        squares = find_squares(img)
        cv2.drawContours( img, squares, -1, (0, 255, 0), 3 )
        cv2.imshow('squares', img)
        ch = cv2.waitKey(1)
        if ch == 27:
            cv2.destroyAllWindows()
            break
    
     
showtime()
    
