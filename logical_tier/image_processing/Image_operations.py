#!/usr/bin/env python2


import cv2
import cv
import cv2.cv as cv

class ImageOperations():
    TRAINSET_frontal_face = 'logical_tier/image_processing/haarcascades/haarcascade_frontalface_default.xml'
    TRAINSET_eye = 'logical_tier/image_processing/haarcascades/haarcascade_eye.xml'

    DOWNSCALE = 4
    face_classifier = None
    eye_classifier = None
    mouth_classifier = None
    def __init__(self,path_to_main):
        self.TRAINSET_frontal_face = path_to_main + self.TRAINSET_frontal_face
        self.TRAINSET_eye = path_to_main + self.TRAINSET_eye

        self.face_classifier = cv2.CascadeClassifier(self.TRAINSET_frontal_face)
        self.eye_classifier = cv2.CascadeClassifier(self.TRAINSET_eye)


    def detect_face(self,miniframe):
        faces = self.face_classifier.detectMultiScale(miniframe)
        return faces

    def get_face(self,frame):
        minisize = (frame.shape[1] / self.DOWNSCALE, frame.shape[0] / self.DOWNSCALE)
        miniframe = cv2.resize(frame, minisize)

        faces = self.detect_face(miniframe)
        for f in faces:
            x, y, w, h = [ v*self.DOWNSCALE for v in f ]
            roi_color = frame[y:y+h, x:x+w]
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255))
            return roi_color,f
        return None, None

    def has_eyes_detected(self,face_image,frame,face_coordinates):
        if face_image is None:
            return False
        x, y, w, h = [ v*self.DOWNSCALE for v in face_coordinates ]
        eyes_detected = False
        eyes = self.eye_classifier.detectMultiScale(face_image)
        #eyes = eye_classifier.detectMultiScale(roi_color)
        gray_image = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
        #cv2.imshow("test remove reflections before",gray_image)

        #middle_face = (w / 2.0)
        for (ex,ey,ew,eh) in eyes:
            if(ew>0):
                if(eh>0):
                    eyes_detected=True
                    print 'eye detected'
                cv2.rectangle(face_image,(ex,ey),(ex+ew,ey+eh),(0,255,0))
                #roi_eye = frame[(y + ey):(y + ey) + eh, (x + ex):(x + ex) + ew]
                #return [roi_eye,(x + ex),(y + ey)]
                #eye_frame_gray = cv2.cvtColor(roi_eye, cv2.COLOR_BGR2GRAY)
                #projection_function_method.detect_center_eye(eye_frame_gray ,(x + ex),(y + ey),0.0,0.0)
                #detect_edges(roi_eye)
        return eyes_detected

    def get_eyes(self,face_image,face_coordinates):
        eyes = self.eye_classifier.detectMultiScale(face_image)
        return eyes


    def get_right_eye_area(self,face_image, face_coordinates):
        eyes = self.get_eyes(face_image,face_coordinates)
        x, y, w, h = [ v*self.DOWNSCALE for v in face_coordinates ]
        middle_face = w / 2.0

        for (ex,ey,ew,eh) in eyes:
            if ex > middle_face and (ew > (w * 0.19)):
                if(ew>0):
                    if(eh>0):
                        cv2.rectangle(face_image,(ex,ey),(ex+ew,ey+eh),(0,255,0))
                        return face_image[ey : (ey + eh),ex : (ex + ew)],[[ex,ey],[(ex + ew),(ey + eh)]]
        return None,None

    def get_left_eye_area(self,face_image, face_coordinates):
        eyes = self.get_eyes(face_image,face_coordinates)
        x, y, w, h = [ v*self.DOWNSCALE for v in face_coordinates ]
        middle_face = w / 2.0

        for (ex,ey,ew,eh) in eyes:
            if (ex + ew) < middle_face and (ew > (w * 0.09)):
                if(ew>0):
                    if(eh>0):
                        cv2.rectangle(face_image,(ex,ey),(ex+ew,ey+eh),(0,255,0))
                        return face_image[ey : (ey + eh),ex : (ex + ew)],[[ex,ey],[(ex + ew),(ey + eh)]]
        return None,None

    def detect_face_eyes(self,frame):
        minisize = (frame.shape[1] / self.DOWNSCALE, frame.shape[0] / self.DOWNSCALE)
        miniframe = cv2.resize(frame, minisize)
        faces = self.detect_face(miniframe)
        for f in faces:
            x, y, w, h = [ v*self.DOWNSCALE for v in f ]
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255))
            roi_color = frame[y:y+h, x:x+w]
            minWidth = int(w * 0.2)
            minHeight = int(minWidth * 0.2)
            print str("minWidth: " + str(minWidth))
            print str("minHeight: " + str(minHeight))
            if self.has_eyes_detected(roi_color,frame,f):
                return True

        return False



    # Not used
    #def detect_eyes(frame,miniframe):
    #    eyes_detected = False
    #    eyes = eye_classifier.detectMultiScale(frame)
    #    for (ex,ey,ew,eh) in eyes:
    #        if(ew>0):
    #            if(eh>0):
    #                eyes_detected=True
    #                print 'eye detected'
    #        cv2.rectangle(frame,(ex,ey),(ex+ew,ey+eh),(0,255,0))
    #    return eyes_detected

    # Not used
    #todo: optimise. Dus dat bv die faces niet opnieuw berekent moet worden
    #def detect_face_eyes_mouth(frame,miniframe):
    #    detect_edges(frame)
    #    faces = face_classifier.detectMultiScale(frame, 1.3, 5)
    #    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #    hasface = False
    #    for (x,y,w,h) in faces:
    #        if(w>0):
    #            if(h>0):
    #                hasface=True
    #        print 'face detected'
    #        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0))
    #        roi_gray = gray[y:y+h, x:x+w]
    #        roi_color = frame[y:y+h, x:x+w]
    #        eyes = eye_classifier.detectMultiScale(roi_color)
    #        for (ex,ey,ew,eh) in eyes:
    #            print 'eye detected'
    #            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0))
    #
    #
    #        mouth = mouth_classifier.detectMultiScale(roi_color)
    #        for(mx,my,mw,mh) in mouth:
    #            print 'mouth detected'
    #            cv2.rectangle(roi_color,(mx,my),(mx+mw,my+mh),(0,0,255))
    #
    #
    lowThreshold = 0
    max_lowThreshold = 100
    ratio = 3
    kernel_size = 3

    def detect_edges(self,frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        self.CannyThreshold(90,gray,frame) # initialization

    def CannyThreshold(self,lowThreshold,gray,img):
        detected_edges = cv2.GaussianBlur(gray,(3,3),0)
        detected_edges = cv2.Canny(detected_edges,lowThreshold,lowThreshold*self.ratio,apertureSize = self.kernel_size)
        dst = cv2.bitwise_and(img,img,mask = detected_edges) # just add some colours to edges from original image.
        print '**********************'
        #for edge in detected_edges:
           # print edge
        #print '**********************'
        cv2.imshow('canny demo',dst)

    #def change_contrast(frame,phi , theta , maxIntensity ):
    #    #x = arange(maxIntensity)
    #    #y = (maxIntensity/phi)*(x/(maxIntensity/theta))**0.5
    #    # Decrease intensity such that
    #    # dark pixels become much darker,
    #    # bright pixels become slightly dark
    #    newFrame = (maxIntensity/phi)*(frame/(maxIntensity/theta))**2
    #
    #    #newFrame = array(newFrame,dtype=uint8)
    #
    #    return newFrame

    #def change_contrast_3de_poging(frame):
    #
    #    bigmask = cv2.compare(frame,np.uint8([127]),cv2.CMP_GE)
    #    smallmask = cv2.bitwise_not(bigmask)
    #
    #    x = np.uint8([90])
    #    big = cv2.add(frame,x,mask = bigmask)
    #    small = cv2.subtract(frame,x,mask = smallmask)
    #    res = cv2.add(big,small)
    #    return res

    def update_brightcont(self,frame,brightness,contrast):
        # The algorithm is by Werner D. Streidt
        # (http://visca.com/ffactory/archives/5-99/msg00021.html)
        hist_size = 64
        range_0 = [0, 256]
        ranges = [ range_0 ]

        #self.dst_image = cv.CloneMat(src_image)
        hist_image = cv.CreateImage((320, 200), 8, 1)
        hist = cv.CreateHist([hist_size], cv.CV_HIST_ARRAY, ranges, 1)

        if contrast > 0:
            delta = 127. * contrast / 100
            a = 255. / (255. - delta * 2)
            b = a * (brightness - delta)
        else:
            delta = -128. * contrast / 100
            a = (256. - delta * 2) / 255.
            b = a * brightness + delta
        newFrame = frame
        cv2.convertScaleAbs(frame, newFrame,a,b)
        #cv.ConvertScale(frame, newFrame, a, b)
        """
        cv.CalcArrHist([newFrame], hist)
        (min_value, max_value, _, _) = cv.GetMinMaxHistValue(hist)
        cv.Scale(hist.bins, hist.bins, float(hist_image.height) / max_value, 0)

        cv.Set(hist_image, cv.ScalarAll(255))
        bin_w = round(float(hist_image.width) / hist_size)

        for i in range(hist_size):
            cv.Rectangle(hist_image, (int(i * bin_w), hist_image.height),
                         (int((i + 1) * bin_w), hist_image.height - cv.Round(hist.bins[i])),
                         cv.ScalarAll(0), -1, 8, 0)
        """
        return newFrame
        #cv.ShowImage("histogram", hist_image)

    #def change_contrast_2de_poging(frame, alpha, beta):
    #
    #    x = 0
    #    while x < len(frame):
    #        y = 0
    #        while (y < len(frame[x])):
    #            frame[y][x] = alpha * frame[y][x] + beta
    #            y += 1
    #        x += 1
    def calcuate_avg_intensity_image(self,gray_image):
        avg_intensity_acc = 0.0
        total_pixels = 0

        for y in range(0,len(gray_image)):
            for x in range(0,len(gray_image[y])):
                avg_intensity_acc += int(gray_image[y][x])
                total_pixels += 1
        if total_pixels >0:
            return float(avg_intensity_acc / total_pixels)
        else:
            return -1