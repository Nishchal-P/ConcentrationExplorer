from presentation_tier import Form_user_feedback_process
import datetime,time

class UserfeedbackTracker():
    teller_duration_iterations_sec = 0.0
    interval_feedback_form = 0.0
    datetime_last_userfeedback_asked = datetime.datetime.now()
    time_last_notified = time.clock()

    def __init__(self,interval_feedback_form):
        self.interval_feedback_form = interval_feedback_form

    def notify(self):
        if self.interval_feedback_form >= 0:
            time_now = time.clock()
            duration_iteration_sec = time_now - self.time_last_notified
            self.time_last_notified = time.clock()
            self.teller_duration_iterations_sec += duration_iteration_sec

            if (self.teller_duration_iterations_sec >= self.interval_feedback_form):
                #user_feedback_process.launch_feedback_form()
                #threading.Thread(form_user_feedback_process.call_form(self.datetime_last_userfeedback_asked)).start()

                Form_user_feedback_process.call_form(self.datetime_last_userfeedback_asked)

                self.teller_duration_iterations_sec = 0
                self.datetime_last_userfeedback_asked = datetime.datetime.now()


