import winsound
from data_tier import DASubjects_SQLite

import wx

class ScrollbarFrame(wx.Frame):
    daSubjects = None
    subjects = []
    link_to_main = ''

    list_activities = []
    list_activities_important = []
    combobox_activities = []

    def get_list_subjects(self):
        list_subjects = []
        list_subjects.append('')
        for item in self.subjects:
            list_subjects.append(item[1])

        return list_subjects

    def initialise_panel(self):
        panel = wx.Panel(self)
        box_checkbox_list = wx.BoxSizer(wx.VERTICAL)
        box = wx.BoxSizer(wx.HORIZONTAL)
        #panel.scroll = wx.ScrolledWindow(panel, -1)
        #panel.scroll.SetScrollbars(1, 1, 500, 400)
        self.list_activities = self.list_activities
        #label = wx.StaticText(panel,-1,"Welk van de volgende programma's/websites droegen bij tot de studies?",pos=(20,20))
        label = wx.StaticText(panel, -1, "Which of the following programs/websites contributed to your studies?",
                              pos=(20, 20))
        box_checkbox_list.Add(label, 0, wx.ALL, 10)
        checkboxListActivities = wx.CheckListBox(panel, 100, size=(300, 300 ), choices=self.list_activities,
                                                 style=wx.LB_HSCROLL, pos=(20, 40))
        box_checkbox_list.Add(checkboxListActivities, 0, wx.ALL, 10)
        # Combobox
        list_subjects = self.get_list_subjects()#list_subjects.append('other')
        box_horizontal = wx.BoxSizer(wx.VERTICAL)

        labels_combobox = []
        for activity in self.list_activities:
            self.combobox_activities.append(
                wx.ComboBox(panel, -1, value=list_subjects[0], size=wx.Size(120, 0), choices=list_subjects))

            index_c = len(self.combobox_activities) - 1
            #index_b = len(box_horizontal)-1
            box_h = wx.BoxSizer(wx.HORIZONTAL)

            self.combobox_activities[index_c].SetToolTip(wx.ToolTip("select unit from dropdown-list"))
            labels_combobox.append(wx.StaticText(panel, -1, str(activity)))

            box_h.Add(self.combobox_activities[index_c], 0, wx.ALL, 2)
            box_h.Add(labels_combobox[index_c], 0, wx.ALL, 2)

            box_horizontal.Add(box_h, 0, wx.ALL, 2)

            #box.Add(box_h,0,wx.ALL,2)
        # Add New
        box_h = wx.BoxSizer(wx.HORIZONTAL)
        label_other = wx.StaticText(panel, -1, 'New Subject:')
        box_h.Add(label_other, 0, wx.ALL, 2)
        text_other = wx.TextCtrl(panel, -1, '', style=wx.TE_RIGHT)
        box_h.Add(text_other, 0, wx.ALL, 2)
        button_new = wx.Button(panel, wx.ID_CLOSE, "Save")
        button_new.Bind(wx.EVT_BUTTON, lambda event: self.OnClickAddNew(event, text_other, self.link_to_main),
                        button_new)
        box_h.Add(button_new, 0, wx.ALL, 2)
        box_horizontal.Add(box_h, 0, wx.ALL, 10)
        # A button
        button = wx.Button(panel, wx.ID_CLOSE, "Save")
        button.Bind(wx.EVT_BUTTON, lambda event: self.OnClick(event, self.list_activities_important, checkboxListActivities,
                                                              self.combobox_activities), button)
        box_checkbox_list.Add(button, 0, wx.ALL, 10)
        box.Add(box_checkbox_list, 0, wx.ALL, 10)
        box.Add(box_horizontal, 0, wx.ALL, 10)
        panel.SetSizer(box)
        panel.Layout()

    def __init__(self,title, list_activities,list_activities_important,subjects,link_to_main):
        wx.Frame.__init__(self, None, -1, title, size=(700, 500))
        winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)
        self.subjects = subjects
        self.list_activities_important = list_activities_important
        self.list_activities = list_activities
        self.link_to_main = link_to_main

        self.daSubjects = DASubjects_SQLite.DASubjects(link_to_main)
        self.initialise_panel()

    def OnClick(self,event,list_activities_important,checkboxListActivities,combobox_activities):
        x = 0
        for choice in self.list_activities :
            id_subject = 1
            if checkboxListActivities.IsChecked(x):
                for item in self.subjects:
                    selectedValue = combobox_activities[x].GetValue()
                    if item[1] == selectedValue:
                        id_subject = item[0]
                list_activities_important.append([choice,id_subject])
            x = x + 1
        self.Close(True)


    def OnClickAddNew(self,event,subject,link_to_main):

        self.daSubjects.insert_subject([subject.GetValue()])
        self.subjects = self.daSubjects.get_subjects()
        for combobox in self.combobox_activities:
            combobox.Append(subject.GetValue())

def call_form(list_activities,list_activities_important,subjects,link_to_main) :
    app = wx.PySimpleApp()
    frame = ScrollbarFrame('Activities RescueTime',list_activities,list_activities_important,subjects,link_to_main)
    frame.Show()
    app.MainLoop()
