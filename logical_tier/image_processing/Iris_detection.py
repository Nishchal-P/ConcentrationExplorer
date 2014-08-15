from exception import Exception
from logical_tier.image_processing import Image_operations, Projection_function_method
import cv2

import math
class IrisDetection():
    DOWNSCALE = 4
    LEFT_EYE = 0
    RIGHT_EYE = 1
    BOTH_EYES = 2
    brightness_correction_value = 0
    contrast_correction_value = 0
    treshold_max_avg_intensity = 200
    treshold_min_avg_intensity = 10
    imageOperations = Image_operations.ImageOperations('')
    """
    def __init__(self):
        cv2.namedWindow("left_eye")
        cv2.namedWindow("right_eye")
    """

    def detect_iris_from_eye_boundaries(self, eye_boundaries_color, frame, min_x_positions_eye_boundaries_in_frame,
                                        min_y_positions_eye_boundaries_in_frame):
        self.imageOperations.update_brightcont(eye_boundaries_color, self.brightness_correction_value,
                                           self.contrast_correction_value)

        eye_YCbCr = cv2.cvtColor(eye_boundaries_color, cv2.COLOR_RGB2YCR_CB)
        if eye_YCbCr is None:
            return None

        eye_boundaries_gray = cv2.cvtColor(eye_boundaries_color,cv2.COLOR_RGB2GRAY)
        #cv2.imshow("gray before hist eq",eye_boundaries_color)
        eye_boundaries_gray = cv2.equalizeHist(eye_boundaries_gray)
        eye_boundaries_color = cv2.cvtColor(eye_boundaries_gray,cv2.COLOR_GRAY2RGBA)

#        cv2.imshow("gray before hist eq",eye_YCbCr)
        eye_YCbCr = cv2.cvtColor(eye_boundaries_color, cv2.COLOR_RGB2YCR_CB)
 #       cv2.imshow("gray after hist eq",eye_YCbCr)
        """
        channels = cv2.split(eye_YCbCr) #split the image into channels

        channels[0] = cv2.equalizeHist(channels[0]) #equalize histogram on the 1st channel (Y)

        eye_YCbCr = cv2.merge(channels) #merge 3 channels including the modified 1st channel into one image
        eye_boundaries_color = cv2.cvtColor(eye_YCbCr, cv2.COLOR_YCR_CB2RGB)
        cv2.imshow("eye YCbCr",eye_YCbCr)
        """
        list_irisPixels_x = []
        list_irisPixels_y = []
        y = 0
        while y < len(eye_YCbCr):
            x = 0
            while x < len(eye_YCbCr[0]):
                if int(eye_YCbCr[y][x][0]) <= 10:
                    frame[y + min_y_positions_eye_boundaries_in_frame][x + min_x_positions_eye_boundaries_in_frame] = [255,0,0]
                    list_irisPixels_x.append(x + min_x_positions_eye_boundaries_in_frame)
                    list_irisPixels_y.append(y + min_y_positions_eye_boundaries_in_frame)
                x += 1
            y += 1

        """
        if len(list_irisPixels_x) < 3:
            self.brightness_correction_value -= 5
        else:
            #print str("percentage iris pixels gedetecteerd: " + str((float(len(list_irisPixels_x)) / (float(len(eye_boundaries_color)) * float(len(eye_boundaries_color[0]))))))
            if (float(len(list_irisPixels_x)) / (
                float(len(eye_boundaries_color)) * float(len(eye_boundaries_color[0])))) > 0.1:
                self.brightness_correction_value += 5
        """
        """
        eye_gray = cv2.cvtColor(eye_boundaries_color, cv2.COLOR_BGR2GRAY)
        avg_intensity = self.imageOperations.calcuate_avg_intensity_image(eye_gray)
        if avg_intensity <= self.treshold_min_avg_intensity or avg_intensity >= self.treshold_max_avg_intensity:
            self.brightness_correction_value = 0
            self.contrast_correction_value = 0
        """

        #cv2.imshow("right_eye YCbCr",eye_YCbCr)
        #cv2.imshow("frame after iris detection",frame)
        #cv2.imshow("frame after iris detection",eye_boundaries_color)
        #cv2.namedWindow("binarized face image")
        #cv2.imshow("binarized face image",eye_gray)

        if len(list_irisPixels_x) == 0:
            return None
        center_x = int(self.calculate_median(list_irisPixels_x))
        center_y = int(self.calculate_median(list_irisPixels_y))
        #    center_y = int(round((min_y_positions_right_eye_boundaries_in_frame + max_y_positions_right_eye_boundaries_in_frame) / 2.0,0))
        self.mark_center(frame, center_x, center_y)
        return [center_x, center_y]

    def detect_eyes(self,face_image,frame,f,which_eye):
        gray_image = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)

        x, y, w, h = [ v*self.DOWNSCALE for v in f ]
        if which_eye == self.LEFT_EYE:
            #left_eye_area,left_eye_area_coordinates = self.get_left_eye_area(gray_image)
            left_eye_area,left_eye_area_coordinates = self.imageOperations.get_left_eye_area(gray_image,f)
            if left_eye_area is None:
                return None
            else:
                y_max_left = len(left_eye_area)
                self.remove_reflections(left_eye_area,y_max_left)
                self.binarize_gray_image(left_eye_area)

                x_position_eye_in_frame = x + left_eye_area_coordinates[0][0]
                y_position_eye_in_frame = y + left_eye_area_coordinates[0][1]

                try:
                    eye_location = Projection_function_method.detect_eye_boundaries(left_eye_area,x + left_eye_area_coordinates[0][0],y + left_eye_area_coordinates[0][1],0,0)
                    eye_boundaries_color = frame[(eye_location[0][1] + y_position_eye_in_frame) : (eye_location[1][1] + y_position_eye_in_frame),(eye_location[0][0] + x_position_eye_in_frame) : (eye_location[1][0] + x_position_eye_in_frame)]

                    min_x_positions_eye_boundaries_in_frame = x_position_eye_in_frame + eye_location[0][0]
                    min_y_positions_eye_boundaries_in_frame = y_position_eye_in_frame + eye_location[0][1]
                    #cv2.imshow("left_eye",left_eye_area)
                    return self.detect_iris_from_eye_boundaries(eye_boundaries_color, frame,
                                                            min_x_positions_eye_boundaries_in_frame,
                                                            min_y_positions_eye_boundaries_in_frame)
                except Exception.NoEyesDetected:
                    return None
        if which_eye == self.RIGHT_EYE:
            right_eye_area, right_eye_area_coordinates = self.imageOperations.get_right_eye_area(gray_image,f)
            if right_eye_area is None:
                return None
            else:

                y_max_right = len(right_eye_area)
                self.remove_reflections(right_eye_area,y_max_right)
                self.binarize_gray_image(right_eye_area)

                x_position_eye_in_frame = x + right_eye_area_coordinates[0][0]
                y_position_eye_in_frame = y + right_eye_area_coordinates[0][1]
                try:
                    eye_location = Projection_function_method.detect_eye_boundaries(right_eye_area,x + right_eye_area_coordinates[0][0],y + right_eye_area_coordinates[0][1],0,0)
                    eye_boundaries_color = frame[(eye_location[0][1] + y_position_eye_in_frame) : (eye_location[1][1] + y_position_eye_in_frame),(eye_location[0][0] + x_position_eye_in_frame) : (eye_location[1][0] + x_position_eye_in_frame)]

                    min_x_positions_eye_boundaries_in_frame = x_position_eye_in_frame + eye_location[0][0]
                    min_y_positions_eye_boundaries_in_frame = y_position_eye_in_frame + eye_location[0][1]
                    #cv2.imshow("right_eye",rigt_eye_area)

                    return self.detect_iris_from_eye_boundaries(eye_boundaries_color, frame,
                                                            min_x_positions_eye_boundaries_in_frame,
                                                            min_y_positions_eye_boundaries_in_frame)
                except Exception.NoEyesDetected:
                    return None

        if which_eye == self.BOTH_EYES:
            #Left
            #left_eye_area,left_eye_area_coordinates = self.get_left_eye_area(gray_image)
            left_eye_area,left_eye_area_coordinates = self.imageOperations.get_left_eye_area(gray_image,f)

            if left_eye_area is None:
                left_result = None
            else:
                y_max_left = len(left_eye_area)
                self.remove_reflections(left_eye_area,y_max_left)
                self.binarize_gray_image(left_eye_area)

                right_eye_area, left_eye_area_coordinates = self.get_left_eye_area(gray_image)
                y_max_left = len(right_eye_area)
                self.remove_reflections(right_eye_area,y_max_left)
                self.binarize_gray_image(right_eye_area)

                x_position_left_eye_in_frame = x + left_eye_area_coordinates[0][0]
                y_position_left_eye_in_frame = y + left_eye_area_coordinates[0][1]

                try:
                    left_eye_location = Projection_function_method.detect_eye_boundaries(right_eye_area,x + left_eye_area_coordinates[0][0],y + left_eye_area_coordinates[0][1],0,0)
                    left_eye_boundaries_color = frame[(left_eye_location[0][1] + y_position_left_eye_in_frame) : (left_eye_location[1][1] + y_position_left_eye_in_frame),(left_eye_location[0][0] + x_position_left_eye_in_frame) : (left_eye_location[1][0] + x_position_left_eye_in_frame)]

                    min_x_positions_left_eye_boundaries_in_frame = x_position_left_eye_in_frame + left_eye_location[0][0]
                    min_y_positions_left_eye_boundaries_in_frame = y_position_left_eye_in_frame + left_eye_location[0][1]
                    #cv2.imshow("left_eye",rigt_eye_area)
                    left_result = self.detect_iris_from_eye_boundaries(left_eye_boundaries_color, frame,
                                                        min_x_positions_left_eye_boundaries_in_frame,
                                                        min_y_positions_left_eye_boundaries_in_frame)
                except(Exception.NoEyesDetected):
                    left_result = None

            #Right
            right_eye_area, right_eye_area_coordinates = self.imageOperations.get_right_eye_area(gray_image,f)
            y_max_right = len(right_eye_area)
            self.remove_reflections(right_eye_area,y_max_right)
            self.binarize_gray_image(right_eye_area)

            x_position_right_eye_in_frame = x + right_eye_area_coordinates[0][0]
            y_position_right_eye_in_frame = y + right_eye_area_coordinates[0][1]

            try:
                right_eye_location = Projection_function_method.detect_eye_boundaries(right_eye_area,x + right_eye_area_coordinates[0][0],y + right_eye_area_coordinates[0][1],0,0)
                right_eye_boundaries_color = frame[(right_eye_location[0][1] + y_position_right_eye_in_frame) : (right_eye_location[1][1] + y_position_right_eye_in_frame),(right_eye_location[0][0] + x_position_right_eye_in_frame) : (right_eye_location[1][0] + x_position_right_eye_in_frame)]

                min_x_positions_right_eye_boundaries_in_frame = x_position_right_eye_in_frame + right_eye_location[0][0]
                min_y_positions_right_eye_boundaries_in_frame = y_position_right_eye_in_frame + right_eye_location[0][1]
                #cv2.imshow("right_eye",rigt_eye_area)
                right_result = self.detect_iris_from_eye_boundaries(right_eye_boundaries_color, frame,
                                                    min_x_positions_right_eye_boundaries_in_frame,
                                                    min_y_positions_right_eye_boundaries_in_frame)
            except Exception.NoEyesDetected:
                right_result = None
            """
            if right_eye_area is not None:
                cv2.imshow("right eye boundaries color",right_eye_area)
            if left_eye_area is not None:
                cv2.imshow("left eye boundaries color",left_eye_area)
            """
            return left_result,right_result
        return None


       # max_y_positions_right_eye_boundaries_in_frame = y_position_right_eye_in_frame + right_eye_location[1][1]


        #projection_function_method.detect_center_eye(left_eye_area,0,0,0,0)





    def mark_center(self,frame, center_x,center_y):
        y = -7
        while y <= 7:
            frame[y + center_y][center_x] = [0,255,0]
            y += 1

        x = -7
        while x <= 7:
            frame[center_y][x + center_x] = [0,255,0]
            x += 1

    def get_left_eye_area(self,gray_image):
        width = len(gray_image)
        height = len(gray_image[0])
        x = 1.0
        y = 1.0
        min_x = int(round(width * (x / 5.0)))
        max_x = int(round(width * ((x + 1) / 5.0)))

        min_y = int(round(height * (y / 3.0)))
        max_y = int(round(height * ((y + 1) / 3.0)))

        return gray_image[ min_y : max_y , min_x : max_x ],[[min_x,min_y],[max_x,max_y]]

    def get_right_eye_area(self,gray_image):
        width = len(gray_image)
        height = len(gray_image[0])
        x = 3.0
        y = 1.0
        min_x = int(round(width * (x / 5.0)))
        max_x = int(round(width * ((x + 1) / 5.0)))

        min_y = int(round(height * (y / 3.0)))
        max_y = int(round(height * ((y + 1) / 3.0)))

        return gray_image[ min_y : max_y , min_x : max_x ],[[min_x,min_y],[max_x,max_y]]

    """
    def face_division(gray_image):
        result = [5][3]
        width = len(gray_image)
        height = len(gray_image[0])
        x = 0.0
        while x < 5:
            y = 0.0
            while y < 3:
                min_x = int(round(width * (x / 5.0)))
                max_x = int(round(width * ((x + 1) / 5.0)))

                min_y = int(round(height * (y / 3.0)))
                max_y = int(round(height * ((y + 1) / 3.0)))

                result[x][y] = gray_image[ min_y : max_y , min_x : max_x ]


                cv2.rectangle(gray_image,(min_x,min_y),(max_x,max_y),(0,255,0))
                y += 1
            x += 1
        return result
    """


    def remove_reflections(self,gray_image,y_max):
        m = self.calculate_reflection_removal_treshold(gray_image,y_max)
        y = 0
        while y < len(gray_image):
            x = 0
            while x < len(gray_image[0]):
                if int(gray_image[y][x]) > m:
                    gray_image[y][x] = m
                x += 1
            y += 1

    def calculate_reflection_removal_treshold(self,gray_face,y_max):
        y = 0
        list_pixelvalues = []
        while y < y_max:
            x = 0
            while x < len(gray_face[0]):
                list_pixelvalues.append(int(gray_face[y][x]))
                #gray_face[y][x] = 0
                x += 1
            y += 1
        list_pixelvalues.sort()
        median = self.calculate_median(list_pixelvalues)
        #print str("median: " + str(median))
        return median

    def calculate_median(self,list):
        if len(list) == 0:
            return None
        list.sort()
        middle = 0
        if (len(list) % 2) == 0:
            middle = len(list) / 2
            median = float(list[middle - 1] + list[(middle)]) / 2.0
        else:
            middle = int(math.floor(len(list)/ 2.0))
            median = list[middle]
        return median


    def calculate_treshold_binarize_gray_image(self,gray_image):
        teller = 0.0
        noemer = 0.0
        x = 1
        while x < (len(gray_image) - 1):
            y = 1
            while y < (len(gray_image[x]) - 1):
                Sn = 0.0
                Sn_x = 0.0
                Sn_y = 0.0
                Sn_x = abs(int(gray_image[x][y - 1]) - int(gray_image[x][y + 1]))
                Sn_y = abs(int(gray_image[x - 1][y]) - int(gray_image[x + 1][y]))

                if Sn_x > Sn_y:
                    Sn = Sn_x
                else:
                    Sn = Sn_y

                teller += (int(gray_image[x][y]) * Sn)
                noemer += Sn

                y += 1
            x += 1
        treshold = round(teller / noemer)
        return treshold


    def binarize_gray_image(self,gray_image):
        treshold = self.calculate_treshold_binarize_gray_image(gray_image)

        y = 0
        while y < len(gray_image):
            x = 0
            while x < len(gray_image[y]):
                if int(gray_image[y][x]) < treshold:
                    gray_image[y][x] = 0
                else:
                    gray_image[y][x] = 255
                x += 1
            y += 1
