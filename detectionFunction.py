import cv2,time,thread,threading
import numpy as np,pygame
from collections import Counter

clk = pygame.time.Clock()

def fingerCount(cap,openSecs):

    ret,img = cap.read()

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    ret,thresh1 = cv2.threshold(blur,130,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
  
    i,contours, hierarchy = cv2.findContours(thresh1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    output = np.zeros(img.shape,np.uint8)

    max_area=0
   
    for i in range(len(contours)):
            cnt=contours[i]
            area = cv2.contourArea(cnt)
            if(area>max_area):
                max_area=area
                ci=i

    cnt=contours[ci]
    hull = cv2.convexHull(cnt)
    moments = cv2.moments(cnt)
    
    if moments['m00']!=0:
                cx = int(moments['m10']/moments['m00']) # cx = M10/M00
                cy = int(moments['m01']/moments['m00']) # cy = M01/M00
              
    centr=(cx,cy)       
    cv2.circle(img,centr,5,[0,0,255],2)
    cv2.drawContours(output,[cnt],0,(0,255,0),2)
    cv2.drawContours(output,[hull],0,(0,0,255),2) 
          
    cnt = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
    hull = cv2.convexHull(cnt,returnPoints = False)
    
    defects = cv2.convexityDefects(cnt,hull)

    for i in range(defects.shape[0]):
        s,e,f,d = defects[i,0]
        start = tuple(cnt[s][0])
        end = tuple(cnt[e][0])
        far = tuple(cnt[f][0])
        dist = cv2.pointPolygonTest(cnt,centr,True)
        cv2.line(img,start,end,[0,255,0],2)
        
        cv2.circle(img,far,5,[0,0,255],-1)

    # print "fingers1 = %d"%(i)

    # i=0
    
    # cv2.imshow('output',output)
    # cv2.imshow('input',img)
                
    k = cv2.waitKey(10)
    # if k == 27:
    #     break
    cv2.imwrite("output.png",output)
    cv2.imwrite("input.png",img)

    return i


def fingerCount1(cap,openSecs):
    dfcts = []

    ori = time.time()
    clk = time.time()

    while clk-ori<openSecs:
        clk = time.time()
        
        ret,img = cap.read()

        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray,(5,5),0)
        ret,thresh1 = cv2.threshold(blur,130,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
      
        i,contours, hierarchy = cv2.findContours(thresh1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        output = np.zeros(img.shape,np.uint8)

        max_area=0
       
        for i in range(len(contours)):
                cnt=contours[i]
                area = cv2.contourArea(cnt)
                if(area>max_area):
                    max_area=area
                    ci=i

        cnt=contours[ci]
        hull = cv2.convexHull(cnt)
        moments = cv2.moments(cnt)
        
        if moments['m00']!=0:
                    cx = int(moments['m10']/moments['m00']) # cx = M10/M00
                    cy = int(moments['m01']/moments['m00']) # cy = M01/M00
                  
        centr=(cx,cy)       
        cv2.circle(img,centr,5,[0,0,255],2)       
        cv2.drawContours(output,[cnt],0,(0,255,0),2) 
        cv2.drawContours(output,[hull],0,(0,0,255),2) 
              
        cnt = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
        hull = cv2.convexHull(cnt,returnPoints = False)
        
        defects = cv2.convexityDefects(cnt,hull)

        for i in range(defects.shape[0]):
            s,e,f,d = defects[i,0]
            start = tuple(cnt[s][0])
            end = tuple(cnt[e][0])
            far = tuple(cnt[f][0])
            dist = cv2.pointPolygonTest(cnt,centr,True)
            cv2.line(img,start,end,[0,255,0],2)
            
            cv2.circle(img,far,5,[0,0,255],-1)

        # print "fingers = %d"%(i)

        dfcts.append(i)
        i=0
        
        # cv2.imshow('output',output)
        # cv2.imshow('input',img)
                    
        k = cv2.waitKey(10)
        if k == 27:
            break

    data = Counter(dfcts)
    
    # cap.release()
    # del(cap)
    return data.most_common(1)[0][0]

# cap = cv2.VideoCapture(0)
# fingerCount(cap,660)

# cap = cv2.VideoCapture(0)

# ori = time.time()
# clk = time.time()

# while clk-ori<500:
#     clk = time.time()
#     fingerCount1(cap,5)
