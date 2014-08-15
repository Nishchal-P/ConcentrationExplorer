from logical_tier.user_gone import User_gone_tracker
from logical_tier.rescueTime import Rescuetime_tracker
from logical_tier.userfeedback import Userfeedback_tracker

import cv2
import datetime
import time

from data_tier import DASession_SQLite
from data_tier import DAErrorReport_SQLite
from presentation_tier import Output


# To prevent the system from crashing when the mindwave isn't connected, or when there is a problem with the connection
try:
    from logical_tier.mindwave import Mindwave_tracker
except Exception, e:
    DAErrorReport_SQLite.insert_row_action(datetime.datetime.today(),"Mindwave_tracker.py",str(e))
    print str(e)


class Tracking():
    def __init__(self,RescueTime_key):
        self.tracking(RescueTime_key)

    """
    @param RescueTime_key | this key will be used to retrieve RescueTime log information during the session. The RescueTime client application for logging should run on the background with the key specified
    """
    def tracking(self,key_RescueTime):
        # parameters system
        # Webcam
        webcam_id = 0

        # UserGone_tracker
        interval_unable_to_detect_eyes = 18 # Must be larger than 'amount_of_webcam_images * logging_seconds'
        logging_seconds = 0.5
        amount_of_webcam_images = 6

        # Userfeedback_tracker
        interval_feedback_form = -1

        # Mindwave_tracker
        samples_mindwave = 1
        interval_mindwave = 1
        com_port_mindwave = "COM3"

        # Output
        treshold_important_unimportant = 30


        if key_RescueTime == '' :
            raise Exception('The RescueTime key cannot be empty')

        radioListReden = [['Notes','I was taking notes',1], ['Document','I was searching/reading a document',1], ['Break','I took a break',0], ['Distracted','I was distracted',0],  ['Screen','I was looking to the screen',1],['Other','Other',0]]

        # Webcam initialisation
        webcam = cv2.VideoCapture(webcam_id)
        cv2.namedWindow("preview")
        if webcam.isOpened(): # try to get the first frame
            rval, frame = webcam.read()

        try:
            mindwaveTracker = Mindwave_tracker.MindwaveTracker(samples_mindwave,interval_mindwave,com_port_mindwave)
        except Exception, e:
            DAErrorReport_SQLite.insert_row_action(datetime.datetime.today(),"Mindwave_tracker.py",str(e))
            print str(e)
        userGoneTracker = User_gone_tracker.UserGoneTracker(logging_seconds, amount_of_webcam_images,interval_unable_to_detect_eyes,radioListReden)
        userfeedbackTracker = Userfeedback_tracker.UserfeedbackTracker(interval_feedback_form)

        start_date_time = datetime.datetime.today()
        # To prevent the system from exiting the while loop when an exception is thrown and catched in a try except statement.
        stopWhile = False


        while not stopWhile:
            start_time = time.clock()
            # MindwaveTracker
            try:
                mindwaveTracker.notify()
            except Exception, e:
                print str(e)
                DAErrorReport_SQLite.insert_row_action(datetime.datetime.today(),"Mindwave_tracker.py",str(e))

            # userGoneTracker
            try:
                userGoneTracker.notify(frame)

                cv2.putText(frame, "Press ESC to close.", (5, 25),cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255))
                cv2.imshow("preview", frame)
            except Exception, e:
                print str(e)
                DAErrorReport_SQLite.insert_row_action(datetime.datetime.today(),"User_gone_tracker.py",str(e))

            # userFeedbackTracker
            try:
                userfeedbackTracker.notify()
            except Exception, e:
                print str(e)
                DAErrorReport_SQLite.insert_row_action(datetime.datetime.today(),"Userfeedback_tracker.py",str(e))

            # get next frame
            rval, frame = webcam.read()
            key = cv2.waitKey(20)
            if key in [27, ord('Q'), ord('q')]: # exit on ESC
                break

            print str("fps: " + str(1.0 / (time.clock() - start_time)))



        end_date_time = datetime.datetime.today()

        try:
            mindwaveTracker.stop_device()
        except Exception, e:
            print "Unknown exception"
            DAErrorReport_SQLite.insert_row_action(datetime.datetime.today(),"Mindwave_tracker.py",str(e))

        # Reading
        userGoneTracker.notify_stopping_application()


        # RescueTime
        rescueTimeTracker = Rescuetime_tracker.RescueTimeTracker('',key_RescueTime)
        rescueTimeTracker.notify_stopping_application(start_date_time, end_date_time)

        # Session
        dasession = DASession_SQLite.DASession('')
        dasession.insert_row_session(start_date_time,end_date_time,"prototype testing")

        # Results
        Output.show_results(start_date_time, end_date_time, radioListReden,treshold_important_unimportant)



