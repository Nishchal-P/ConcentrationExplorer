import unittest
from logical_tier.image_processing import Image_operations, Projection_function_method, Iris_detection

import cv2

class TestImageProcessing(unittest.TestCase):
    path_to_main = ''
    """
    def test_record_video(self):
        DOWNSCALE = 4
        #Dit deel staat in voor de webcam
        webcam = cv2.VideoCapture(0)
        cv2.namedWindow("preview")
        if webcam.isOpened(): # try to get the first frame
            rval, frame = webcam.read()
        else:
            rval = False

        teller = 0
        stopWhile = False

        while not stopWhile:
            minisize = (frame.shape[1] / DOWNSCALE, frame.shape[0] / DOWNSCALE)
            miniframe = cv2.resize(frame, minisize)

            cv2.putText(frame, "Press ESC to close.", (5, 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255))
            cv2.imshow("preview", frame)
            file = "test_images/webcam/test_2_" + str(teller) + ".jpg"
            cv2.imwrite(file,frame)
            teller += 1

            # get next frame
            rval, frame = webcam.read()

            key = cv2.waitKey(20)
            if key in [27, ord('Q'), ord('q')]: # exit on ESC
                break
    """
    """
    def test_image(self):
        DOWNSCALE = 4
        imageOperations = image_operations.ImageOperations(self.path_to_main)
        #Dit deel staat in voor de webcam
        #webcam = cv2.VideoCapture(0)
        #if webcam.isOpened(): # try to get the first frame
        #    rval, frame = webcam.read()
        #else:
        #    rval = False

        frame = cv2.imread("../../test_images/webcam/test16.jpg",cv2.CV_LOAD_IMAGE_COLOR)
        if frame == None: ## Check for invalid input
            print "Could not open or find the image"
        else:
            minisize = (frame.shape[1] / DOWNSCALE, frame.shape[0] / DOWNSCALE)
            miniframe = cv2.resize(frame, minisize)

            cv2.namedWindow('Display Window') ## create window for display
            cv2.imshow('Display Window', frame) ## Show image in the window
            projection_function_method.detect_face_eyes(frame,miniframe,imageOperations)
            cv2.imshow('Display Window', frame) ## Show image in the window
            print "size of image: ", frame.shape ## print size of image
            cv2.waitKey(0) ## Wait for keystroke
            cv2.destroyAllWindows() ## Destroy all windows
    """
    def test_eye_center_for_thesis(self):
        DOWNSCALE = 4
        imageOperations = Image_operations.ImageOperations(self.path_to_main)
        irisDetection = Iris_detection.IrisDetection()
        frame = cv2.imread("../../test_images/webcam/test14.jpg",cv2.CV_LOAD_IMAGE_COLOR)

        if frame == None: ## Check for invalid input
            print "Could not open or find the image"
        else:
            minisize = (frame.shape[1] / DOWNSCALE, frame.shape[0] / DOWNSCALE)
            miniframe = cv2.resize(frame, minisize)

            cv2.namedWindow('Display Window') ## create window for display
            cv2.imshow('Display Window after', frame) ## Show image in the window
            #projection_function_method.detect_face_eyes(frame,frame,imageOperations)

            face,face_coordinates = imageOperations.get_face(frame)
            gray_image = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
            x, y, w, h = [ v*DOWNSCALE for v in face_coordinates]
            left_eye_area,left_eye_area_coordinates = imageOperations.get_right_eye_area(gray_image,face_coordinates)

            cv2.destroyAllWindows() ## Destroy all windows
            y_max_left = len(left_eye_area)
            #irisDetection.remove_reflections(left_eye_area,y_max_left)
            #irisDetection.binarize_gray_image(left_eye_area)
            Projection_function_method.detect_center_eye(left_eye_area,0,0,0,0)

            cv2.imshow('Display Window', frame) ## Show image in the window

            x_position_eye_in_frame = x + left_eye_area_coordinates[0][0]
            y_position_eye_in_frame = y + left_eye_area_coordinates[0][1]


            eye_location = Projection_function_method.detect_eye_boundaries(left_eye_area,x + left_eye_area_coordinates[0][0],y + left_eye_area_coordinates[0][1],0,0)
            cv2.waitKey(0) ## Wait for keystroke
#            eye_boundaries_color = frame[(eye_location[0][1] + y_position_eye_in_frame) : (eye_location[1][1] + y_position_eye_in_frame),(eye_location[0][0] + x_position_eye_in_frame) : (eye_location[1][0] + x_position_eye_in_frame)]




    """
    def test_eye_center_calculation(self):
        frame = cv2.imread("test_images/test_4.jpg",cv2.CV_LOAD_IMAGE_COLOR)
        if frame == None: ## Check for invalid input
            print "Could not open or find the image"
        else:
            cv2.namedWindow('Display Window') ## create window for display
            user_gone.detect_center_eye(frame)
    """
    """
    def test_webcam(self):
        DOWNSCALE = 4

        #Dit deel staat in voor de webcam
        webcam = cv2.VideoCapture(0)
        cv2.namedWindow("preview")
        if webcam.isOpened(): # try to get the first frame
            rval, frame = webcam.read()
        else:
            rval = False

        stopWhile = False
        fps = 0
        teller = 0.0

        while not stopWhile:
            start_time = time.clock()

            cv2.imshow("preview", frame)

            # get next frame
            rval, frame = webcam.read()

            key = cv2.waitKey(20)
            if key in [27, ord('Q'), ord('q')]: # exit on ESC
                break

            teller += (time.clock() - start_time)
            fps += 1
            if (teller >= 1.0):
                print str('fps: ' + str(fps))
                teller = 0.0
                fps = 0


    """

if __name__ == '__main__':
    unittest.main()