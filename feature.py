import numpy as np
import cv2
import glob
import matplotlib.pyplot as plt
import xlsxwriter

import csv


                

 
def extract(filename):
                
                        '''with open('test1.csv', 'w', newline='') as csvfile:
                        fieldnames = ['class', 'area','perimeter','maxdia','mindia','h_asym','v_asym','maxr','maxg','maxb','minr','ming','minb','maxh','maxs','maxv']
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                        writer.writeheader()'''
    
                        img=cv2.imread(filename)
                        r=img[..., 0].min()
                        g=img[..., 1].min()
                        b=img[..., 2].min()
                        r1=img[..., 0].max()
                        g1=img[..., 1].max()
                        b1=img[..., 2].max()
                        gray = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY)

                        blur = cv2.GaussianBlur(gray, (17, 17), 32)

                        ret,thresh = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
                        '''
                        ret,thresh = cv2.threshold(blur,127,255,0)
                        cv2.imshow('sgmented',thresh)
                        contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)'''
                        contours,hierarchy = cv2.findContours(thresh, 1, 2)
                        c = contours[0]

                        cnt = max(contours, key=cv2.contourArea)


                        M = cv2.moments(c)
                        if(M['m00']!=0):
                                cx = int(M['m10']/M['m00'])
                                cy = int(M['m01']/M['m00'])
                        else:
                                cx=cy=0
                        centroid=(cx,cy)
                        perimeter = round(cv2.arcLength(c, True),2)


                        area=cv2.countNonZero(thresh)
                        if len(c)>5:
                                rect = cv2.fitEllipse(c)
                                cv2.ellipse(img,rect,(0,255,0),2)

                                cv2.drawContours(img, contours, -1, (0, 0, 255), 3)


                                cv2.circle(img, (cx, cy), 7, (255, 255, 255), -1)
                                cv2.putText(img, "center", (cx - 25, cy - 25),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                                cv2.imwrite('fimage.jpg',img)

                                (x, y) = rect[0]
                                (w, h) = rect[1]
                                angle = rect[2]

                                if w < h:
                                            if angle < 90:
                                                angle -= 90
                                else:
                                                angle += 90

                                rows,cols=thresh.shape
                                rot = cv2.getRotationMatrix2D((x, y), angle, 1)

                                cos = np.abs(rot[0, 0])
                                sin = np.abs(rot[0, 1])

                                nW = int((rows * sin) + (cols * cos))
                                nH = int((rows * cos) + (cols * sin))

                                rot[0, 2] += (nW / 2) - cols / 2
                                rot[1, 2] += (nH / 2) - rows / 2


                                warp_mask=cv2.warpAffine(thresh,rot,(nH,nW))
                                warp_img = cv2.warpAffine(img, rot, (nH, nW))
                                warp_img_segmented = cv2.bitwise_and(warp_img, warp_img,
                                                                             mask=warp_mask)

                                xx, yy, nW, nH = cv2.boundingRect(cnt)

                                warp_mask = warp_mask[yy:yy + nH, xx:xx + nW]

                                
                                flipContourHorizontal = cv2.flip(warp_mask, 1)
                                flipContourVertical = cv2.flip(warp_mask, 0)


                                diff_horizontal = cv2.compare(warp_mask, flipContourHorizontal,
                                                                      cv2.CV_8UC1)
                                diff_vertical = cv2.compare(warp_mask, flipContourVertical,
                                                                    cv2.CV_8UC1)

                                diff_horizontal = cv2.bitwise_not(diff_horizontal)
                                diff_vertical = cv2.bitwise_not(diff_vertical)


                                h_asym = round(cv2.countNonZero(diff_horizontal)/area,3)
                                v_asym = round(cv2.countNonZero(diff_vertical)/area,3)
                                D1=max([nH,nW])
                                D2=min([nH,nW])
                                hsv = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2HSV)
                                


                                
                                low=np.array([0, 0,0])
                                high=np.array([15,140,90])
                                mask = cv2.inRange(hsv,low,high)
                                imask = mask>0
                                black = np.zeros_like(img, np.uint8)
                                black[imask] = img[imask]
                                

                                hsvv=cv2.cvtColor(black.copy(), cv2.COLOR_BGR2HSV)
                                h = hsvv[:,:,0].max()
                                s = hsvv[:,:,1].max()
                                v = hsvv[:,:,2].max()
                                        
                                
                        
                                if D1>600 or D1<600:
                                        h=s=v=0
                        
                                elif(h!=0 and s!=0 and v!=0):
                                      x='severe'  
                                        
                                        
                                else:
                                        low=low=np.array([0, 80,0])
                                        high=np.array([15,255,147])
                                        mask = cv2.inRange(hsv,low,high)
                                        imask = mask>0
                                        brown = np.zeros_like(img, np.uint8)
                                        brown[imask] = img[imask]
                                

                                        hsvv=cv2.cvtColor(brown.copy(), cv2.COLOR_BGR2HSV)
                                        h = hsvv[:,:,0].max()
                                        s = hsvv[:,:,1].max()
                                        v = hsvv[:,:,2].max()
                                        
                                        if h!=0 and s!=0 and v!=0:
                                                x='oderate'
                                                 
                                                 
                                        elif h!=0 or s!=0 or v!=0:
                                                x='mild'
                                        else:
                                                h=s=v=0
                                                 
                                                 
                                
                                return(area,perimeter,D1,D2,h_asym,v_asym,r1,g1,b1,r,g,b,h,s,v)
                        else:
                                return('non',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
                                
             
                






                                                       
