import unittest
import cv2
from logical_tier.image_processing import Image_operations, Iris_detection


class TestBinaryImageMethod(unittest.TestCase):
    path_to_main = ''
    imageOperations = Image_operations.ImageOperations(path_to_main)
    def test_median(self):
        irisDetection = Iris_detection.IrisDetection()
        list = [5,9,3,4,8,6,1,2]
        median = irisDetection.calculate_median(list)

        self.assertEqual(median,4.5)
        list2 = [44,56,85,45,25,32,33,1,7,85,9]
        median2 = irisDetection.calculate_median(list2)
        self.assertEqual(median2,33)

    """
    def test_x_y_verhoudingen(self):
        image = cv2.imread("test_images/webcam/test16.jpg",cv2.CV_LOAD_IMAGE_COLOR)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        y = 0.0
        teller = 0.0
        total = len(gray_image) * len(gray_image[0])

        while y < len(gray_image):
            x = 0.0
            while x < len(gray_image[0]):
                pixelwaarde = float(teller / total) * 255
                gray_image[y][x] = pixelwaarde
                teller += 1.0
                x += 1.0
            y += 1.0
        cv2.imshow("test x y verhoudingen",gray_image)
        cv2.waitKey(0) ## Wait for keystroke
        cv2.destroyAllWindows() ## Destroy all windows

    def test_calculate_treshold_binarize_gray_image(self):
        frame = cv2.imread("test_images/do_not_remove/test_image_treshold_calculation.jpg",cv2.CV_LOAD_IMAGE_COLOR)
        irisDetection = binary_image_method.IrisDetection()
        if frame == None: ## Check for invalid input
            print "Could not open or find the image"
        else:
            gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            #print len(gray_image)
            #print len(gray_image[0])
            treshold = irisDetection.calculate_treshold_binarize_gray_image(gray_image)

            self.assertEqual(int(treshold),196)
            #print gray_image
    """
    """
    def test_image_paper(self):
        DOWNSCALE = 4

        #Dit deel staat in voor de webcam
        #webcam = cv2.VideoCapture(0)
        #if webcam.isOpened(): # try to get the first frame
        #    rval, frame = webcam.read()
        #else:
        #    rval = False

        frame = cv2.imread("test_images/test_image_van_paper.JPG",cv2.CV_LOAD_IMAGE_COLOR)
        if frame == None: ## Check for invalid input
            print "Could not open or find the image"
        else:
            minisize = (frame.shape[1] / DOWNSCALE, frame.shape[0] / DOWNSCALE)
            miniframe = cv2.resize(frame, minisize)

            cv2.namedWindow('Display Window') ## create window for display
            cv2.imshow('Display Window', frame) ## Show image in the window
            binary_image_method.detect_eyes(frame,frame,0,0,len(frame),len(frame[0]))
            cv2.imshow('Display Window', frame) ## Show image in the window
            print "size of image: ", frame.shape ## print size of image
            cv2.waitKey(0) ## Wait for keystroke
            cv2.destroyAllWindows() ## Destroy all windows
    """

    def test_image_paper_2(self):
        irisDetection = Iris_detection.IrisDetection()
        frame = cv2.imread("test_images/webcam/test16.jpg",cv2.CV_LOAD_IMAGE_COLOR)
        #frame = cv2.imread("test_images/DSC_1872.JPG",cv2.CV_LOAD_IMAGE_COLOR)
        if frame == None: ## Check for invalid input
            print "Could not open or find the image"
        else:

            face,coordinates = self.imageOperations.get_face(frame)
            #cv2.namedWindow('Display Window') ## create window for display
            #cv2.imshow('Display Window', face) ## Show image in the window
            irisDetection.detect_eyes(face,frame,coordinates,irisDetection.BOTH_EYES)

            cv2.namedWindow('Display Window') ## create window for display
            cv2.imshow('Display Window', frame) ## Show image in the window
            print "size of image: ", frame.shape ## print size of image

            cv2.waitKey(0) ## Wait for keystroke
            cv2.destroyAllWindows() ## Destroy all windows

if __name__ == '__main__':
    unittest.main()