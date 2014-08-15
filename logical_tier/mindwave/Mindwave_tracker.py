from NeuroPy import NeuroPy
import time, datetime
from data_tier import DAMindwave_SQLite
import tkMessageBox

class MindwaveTracker:
    com = "COM16"

    time_last_notified = time.clock()
    MAX_ZERO_VALUES_BEFORE_WARNING = 10
    attention_value = 0
    meditation_value = 0
    poorSignal = 0
    blinkStrength = 0
    index = 0
    aantal_avg = 0
    interval = 0
    teller_duration_iteration_sec = 0.0
    datetime_from = datetime.datetime.today()
    teller_zero_values = 0
    mindwave_instance = None

    def __init__(self,aantal_avg, interval, com_port_mindwave):
        self.aantal_avg = aantal_avg
        self.interval = interval
        self.com = com_port_mindwave
        self.mindwave_instance = NeuroPy(self.com)
        self.mindwave_instance.start()

    def notify(self):
        time_now = time.clock()
        duration_iteration_sec = time_now - self.time_last_notified
        self.time_last_notified = time.clock()
        self.teller_duration_iteration_sec += duration_iteration_sec
        if self.teller_duration_iteration_sec >= self.interval:
            self.teller_duration_iteration_sec = 0.0
            self.record_measurement()

    def record_measurement(self):
        print str(str('attention: ' + str(self.mindwave_instance.attention)) + '\t' + str('meditation: ' + str(self.mindwave_instance.meditation)))
        if(self.index == self.aantal_avg):
            print str('avg attention: ' + str(float(self.attention_value / self.aantal_avg)))
            average_attention = float(self.attention_value / self.aantal_avg)/100
            average_meditation = float(self.meditation_value / self.aantal_avg)/100
            average_poorSignal = float(self.poorSignal / self.aantal_avg)
            average_blinkStrength = float(self.blinkStrength / self.aantal_avg)
            datetime_to = datetime.datetime.today()
            DAMindwave_SQLite.insert_row_mindwave(self.datetime_from,datetime_to,average_attention,average_meditation,average_poorSignal,average_blinkStrength)

            self.attention_value = self.mindwave_instance.attention
            self.meditation_value = self.mindwave_instance.meditation
            self.poorSignal = self.mindwave_instance.poorSignal
            self.blinkStrength = self.mindwave_instance.blinkStrength

            self.index = 1
            self.datetime_from = datetime.datetime.today()

        else:
            if self.mindwave_instance.attention !=  0 and self.mindwave_instance.meditation != 0:
                self.attention_value += self.mindwave_instance.attention
                self.meditation_value += self.mindwave_instance.meditation
                self.poorSignal += self.mindwave_instance.poorSignal
                self.blinkStrength += self.mindwave_instance.blinkStrength

                self.index += 1
            else:
                self.teller_zero_values += 1
                if self.teller_zero_values == self.MAX_ZERO_VALUES_BEFORE_WARNING:
                    tkMessageBox.showinfo(title="Warning", message="The attention and meditation values are 0 for a long time. Possible problem with the device")
                    self.teller_zero_values = 0


    def stop_device(self) :
        try:
            self.mindwave_instance.stop()
        except Exception, e:
            raise Exception(e)