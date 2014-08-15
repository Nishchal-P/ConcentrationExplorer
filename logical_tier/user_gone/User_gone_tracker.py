from logical_tier.image_processing import Image_operations, Iris_detection
from logical_tier.read_detection import Read_detection_tracking
from presentation_tier import Form_user_gone

import datetime, time
from data_tier import DAEyesDetected_SQLite


class UserGoneTracker():
    time_last_notified = time.clock()
    logging_seconds = 0.0
    amount_of_webcam_images = 0
    # Moet groter zijn dan amount_of_webcam_images / logging_seconds
    interval_unable_to_detect_eyes = 0

    teller_eyesdetected = 0
    teller_eyesdetect_check = 0
    teller_unable_to_detect_eyes = 0
    teller_duration_iterations_sec = 0
    form_user_feedback_process_shown = False

    start_date_time = datetime.datetime.today()
    eyes_gone = False
    start_eyes_gone = datetime.datetime.today()
    datetime_last_eyes_detected = datetime.datetime.now()
    outputSTR_iris_coordinates = "iris coordinates: "

    irisDetection = Iris_detection.IrisDetection()

    radioListReden = None

    #parameters for switch eye
    which_eye = Iris_detection.IrisDetection.RIGHT_EYE
    threshold_min_eyes_detected_relative = 0.8
    eyes_detected_acc = 0.0
    total_eyes_detected = 0.0
    threshold_samples_for_check_switch_eye = 600

    #read detection
    readDetection = Read_detection_tracking.ReadDetection('')

    """
    # plot
    fig_right_eye = plt.figure("right eye")
    fig_left_eye = plt.figure("left eye")
    subplot = 111

    right_eye_x = []
    left_eye_x = []

    right_eye_y = []
    left_eye_y = []
    """
    image_operations = Image_operations.ImageOperations('')

    def __init__(self,logging_seconds, amount_of_webcam_images,interval_unable_to_detect_eyes,radioListReden):
        self.logging_seconds = logging_seconds
        self.amount_of_webcam_images = amount_of_webcam_images
        self.interval_unable_to_detect_eyes = interval_unable_to_detect_eyes / amount_of_webcam_images / logging_seconds
        self.radioListReden = radioListReden
    """
    @param eye
    @effect After every 'amount_of_webcam_images' iteration a row is added to the data_tier indicating whether the user was detected or not and eyes_detected_acc is set to 0.
    @effect During each iteration, if one of the eyes is detected, the 'eyes_detected_acc' is incremented.
    @effect if after amount_of_webcam_images iterations the eyes_detected_acc is larger than 0, the system will interpret this as 'eye detected'
    """
    def detect_user_gone(self,eye):
        if (eye is not None):
            eyes_detected = True
            self.eyes_detected_acc += 1
        else:
            eyes_detected = False
        self.total_eyes_detected += 1

        if (self.teller_eyesdetect_check == self.amount_of_webcam_images):
            self.teller_eyesdetect_check = 0
            currentDateTime = datetime.datetime.today()

            # time in seconds
            datetime_difference = currentDateTime - self.datetime_last_eyes_detected
            self.datetime_last_eyes_detected = currentDateTime

            if (self.teller_eyesdetected > 0):
                self.teller_eyesdetected = 0
                DAEyesDetected_SQLite.insert_row_action(currentDateTime, 1, datetime_difference.seconds)

                self.teller_unable_to_detect_eyes = 0
                if self.eyes_gone is True:
                    user_gone_period = currentDateTime - self.start_eyes_gone
                    Form_user_gone.call_form(self.radioListReden, user_gone_period.seconds, self.start_eyes_gone,
                                             datetime.datetime.today())
                    self.eyes_gone = False
            else:
                DAEyesDetected_SQLite.insert_row_action(currentDateTime, 0, datetime_difference.seconds)

                self.teller_unable_to_detect_eyes += 1
                if self.eyes_gone is False:
                    if self.teller_unable_to_detect_eyes >= self.interval_unable_to_detect_eyes:
                        self.start_eyes_gone = currentDateTime
                        self.eyes_gone = True
        else:
            self.teller_eyesdetect_check += 1
            self.teller_eyesdetected += eyes_detected

    """
    @param frame | current frame from webcam
    @param duration_iteration_sec | Amount of time between this and the last function call.
    @effect data will be written to the data_tier. When after 'amount_of_webcam_images' iterations, the eyes are detected at least once, the system will detect this as 'eyes detected'
    """
    def notify(self,frame):
        time_now = time.clock()
        duration_iteration_sec = time_now - self.time_last_notified
        self.time_last_notified = time.clock()
        self.teller_duration_iterations_sec += duration_iteration_sec

        face,face_coordinates = self.image_operations.get_face(frame)
        eye = None
        if face is not None :

            # If the face is detected, but hardly the current eye, it could be due to bad lightning. The solution is to try to detect the other eye
            if self.total_eyes_detected >= self.threshold_samples_for_check_switch_eye:
                eyes_detected_percentage = self.eyes_detected_acc / self.total_eyes_detected
                if eyes_detected_percentage < self.threshold_min_eyes_detected_relative:
                    self.switch_eye()

                self.total_eyes_detected = 0.0
                self.eyes_detected_acc = 0.0

            eye = self.irisDetection.detect_eyes(face,frame,face_coordinates,self.which_eye)
            self.readDetection.notify(eye,datetime.datetime.today())

        if self.teller_duration_iterations_sec >= self.logging_seconds:
            self.teller_duration_iterations_sec = 0
            self.detect_user_gone(eye)

    def switch_eye(self):
        if self.which_eye == Iris_detection.IrisDetection.RIGHT_EYE:
           self.which_eye =  Iris_detection.IrisDetection.LEFT_EYE
        else:
           self.which_eye =  Iris_detection.IrisDetection.RIGHT_EYE
        self.readDetection.eye_switched()

    def notify_stopping_application(self):
        self.readDetection.notify_stopping_application()
