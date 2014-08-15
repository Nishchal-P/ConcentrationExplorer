import winsound
import wx #, wx.html
import datetime

from data_tier import DAUserFeedback_SQLite


class Frame(wx.Frame):
    attention_value=0.0
    meditation_value=0.0
    def __init__(self, title,datetime_last_userfeedback_asked):
        winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)
        wx.Frame.__init__(self, None, title=title, pos=(150,150), size=(350,380))
       # self.Bind(wx.EVT_CLOSE, self.OnClose)


        panel = wx.Panel(self)
        box = wx.BoxSizer(wx.VERTICAL)
        # Radio Boxes
        # Attention
        label_rbAttention = "What was your attention during the past 10 minutes ?"
        #label_rbAttention = "Hoe geconcentreerd was je tijdens de laatste 10 minuten?"
        radioListAttention = ['very low (1% to 20%)', 'low (21% to 40%)', 'neutral (41% to 60%)', 'slightly elevated (61% to 80%)', 'elevated (81% to 100%)']
        #radioListAttention = ['laag', 'medium laag', 'gemiddeld', 'medium hoog', 'hoog']
        rbAttention = wx.RadioBox(panel, label=label_rbAttention, pos=(20, 40), choices=radioListAttention,  majorDimension=5,
                         style=wx.RA_SPECIFY_ROWS)
        rbAttention.Bind(wx.EVT_RADIOBOX, self.EvtRadioBoxAttention, rbAttention)
        box.Add(rbAttention,0,wx.ALL,10)

        labelSlider =  wx.StaticText(panel,-1,"You can also indicate your concentration with the slider below:")
        box.Add(labelSlider,0,wx.ALL,10)
        boxSlider = wx.BoxSizer(wx.HORIZONTAL)
        labelAttentionValue = wx.StaticText(panel,-1,"")

        slSliderAttention = wx.Slider(panel,minValue=0,maxValue=100,size=(150,40))
        slSliderAttention.Bind(wx.EVT_SLIDER, lambda event : self.EvtSliderAttention(event,labelAttentionValue),slSliderAttention)
        boxSlider.Add(slSliderAttention,0,wx.ALL,10)


        boxSlider.Add(labelAttentionValue,0,wx.ALL,10)

        box.Add(boxSlider,0,wx.ALL,10)

        # Meditation
        #label_rbMeditation = "How relaxed were you during the past 10 minutes ?"
        #radioListMeditation = ['low', 'medium low', 'medium', 'medium high', 'high']
        #rbMeditation = wx.RadioBox(panel, label=label_rbMeditation, pos=(20, 120), choices=radioListMeditation,  majorDimension=5, style=wx.RA_SPECIFY_ROWS)
        #rbMeditation.Bind(wx.EVT_RADIOBOX, self.EvtRadioBoxMeditation, rbMeditation)
        #box.Add(rbMeditation,0,wx.ALL,10)

        # A button
        button =wx.Button(panel, wx.ID_CLOSE,"Save")
        button.Bind(wx.EVT_BUTTON, lambda event : self.OnClick(event,datetime_last_userfeedback_asked),button)
        box.Add(button,0,wx.ALL,10)

        panel.SetSizer(box)
        panel.Layout()

    def EvtSliderAttention(self,event,labelAttentionValue):
        self.attention_value = (event.GetInt() / 100.0)
        labelAttentionValue.SetLabel(str(event.GetInt()) + " %")

    def EvtRadioBoxAttention(self, event):
        self.attention_value = (event.GetInt() / 4.0)

    def EvtRadioBoxMeditation(self, event):
        self.meditation_value = (event.GetInt() / 4.0)

    def OnClick(self,event,datetime_last_userfeedback_asked):
        dateTime = datetime.datetime.today()
        # time in seconds meten
        datetime_difference = dateTime - datetime_last_userfeedback_asked

        # data_tier
        DAUserFeedback_SQLite.insert_row_userFeedback(datetime_last_userfeedback_asked,self.attention_value,self.meditation_value,datetime_difference.seconds)
        # mongodb
        #DAUserFeedback_mongodb.insert_row_user_feedback(dateTime,self.attention_value,self.meditation_value)
        self.Close(True)


def call_form(datetime_last_userfeedback_asked) :
    app = wx.App(False)   # Error messages go to popup window
    top = Frame("Your concentration",datetime_last_userfeedback_asked)
    top.Show()
    app.MainLoop()