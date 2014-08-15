import wx #, wx.html
from logical_tier.image_processing import Image_operations

class Frame(wx.Frame):
    brightness=0.0
    contrast=0.0
    frame = None
    miniframe = None
    def __init__(self, title, frame, miniframe):
        wx.Frame.__init__(self, None, title=title, pos=(150,150), size=(350,500))
       # self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.frame = frame
        self.miniframe = miniframe

        panel = wx.Panel(self)
        box = wx.BoxSizer(wx.VERTICAL)


        # Brightness
        labelSliderBrightness =  wx.StaticText(panel,-1,"Brightness")
        box.Add(labelSliderBrightness,0,wx.ALL,10)
        boxSliderBrightness = wx.BoxSizer(wx.HORIZONTAL)
        labelBrightnessValue = wx.StaticText(panel,-1,"")

        slSliderBrightness = wx.Slider(panel,minValue=0,maxValue=100,size=(150,40))
        slSliderBrightness.Bind(wx.EVT_SLIDER, lambda event : self.EvtSliderBrightness(event,labelBrightnessValue),slSliderBrightness)
        boxSliderBrightness.Add(slSliderBrightness,0,wx.ALL,10)

        boxSliderBrightness.Add(labelBrightnessValue,0,wx.ALL,10)
        box.Add(boxSliderBrightness,0,wx.ALL,10)

        # Contrast
        labelSliderContrast =  wx.StaticText(panel,-1,"Contrast")
        box.Add(labelSliderContrast,0,wx.ALL,10)
        boxSliderContrast = wx.BoxSizer(wx.HORIZONTAL)
        labelContrastValue = wx.StaticText(panel,-1,"")

        slSliderContrast = wx.Slider(panel,minValue=0,maxValue=100,size=(150,40))
        slSliderContrast.Bind(wx.EVT_SLIDER, lambda event : self.EvtSliderContrast(event,labelContrastValue),slSliderContrast)
        boxSliderContrast.Add(slSliderContrast,0,wx.ALL,10)


        boxSliderContrast.Add(labelContrastValue,0,wx.ALL,10)

        box.Add(boxSliderContrast,0,wx.ALL,10)

        # Meditation
        #label_rbMeditation = "How relaxed were you during the past 10 minutes ?"
        #radioListMeditation = ['low', 'medium low', 'medium', 'medium high', 'high']
        #rbMeditation = wx.RadioBox(panel, label=label_rbMeditation, pos=(20, 120), choices=radioListMeditation,  majorDimension=5, style=wx.RA_SPECIFY_ROWS)
        #rbMeditation.Bind(wx.EVT_RADIOBOX, self.EvtRadioBoxMeditation, rbMeditation)
        #box.Add(rbMeditation,0,wx.ALL,10)

        # A button
        button =wx.Button(panel, wx.ID_CLOSE,"Save")
        button.Bind(wx.EVT_BUTTON, lambda event : self.OnClick(event),button)
        box.Add(button,0,wx.ALL,10)


        panel.SetSizer(box)
        panel.Layout()

    def EvtSliderBrightness(self,event,labelBrightnessValue):
        self.brightness = event.GetInt()
        labelBrightnessValue.SetLabel(str(event.GetInt()) + " %")

    def EvtSliderContrast(self,event,labelContrastValue):
        self.contrast = event.GetInt()
        labelContrastValue.SetLabel(str(event.GetInt()) + " %")

    def EvtRadioBoxAttention(self, event):
        self.attention_value = (event.GetInt() / 4.0)

    def EvtRadioBoxMeditation(self, event):
        self.meditation_value = (event.GetInt() / 4.0)

    def OnClick(self,event):
        roi_eye =  Image_operations.detect_face_eyes(self.frame, self.miniframe)
        Image_operations.detect_center_eye(roi_eye[0],roi_eye[1],roi_eye[2],self.brightness,self.contrast)



def call_form(frame, miniframe) :
    app = wx.App(False)   # Error messages go to popup window
    top = Frame("test form image processing",frame,miniframe)
    top.Show()
    app.MainLoop()