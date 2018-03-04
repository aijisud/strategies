# -*- coding: utf-8 -*-
import wx
from wx import adv
import tushare as ts
import pandas as pd

class Dialog(wx.Dialog):
    def __init__(self, *args, **kwargs):
        super(Dialog, self).__init__(*args, **kwargs)
        self.button = wx.Button(self, label='OK')
        self.button.SetDefault()
        self.button.Bind(wx.EVT_BUTTON, self.onButton)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.datepicker)
        sizer.Add(self.button)
        self.SetSizerAndFit(sizer)

    def onButton(self, event):
        print(self.datepicker.GetValue())
        self.Close()

class StatisticsPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.tips = wx.StaticText(self, label='输入6位股票代码，选择日期', pos=(50, 30))

        self.datepicker = wx.adv.DatePickerCtrl(self, id=wx.ID_ANY, dt=wx.DefaultDateTime,
                                                pos=(50,100), size=wx.DefaultSize, style=wx.adv.DP_DEFAULT | wx.adv.DP_SHOWCENTURY,
                                                validator=wx.DefaultValidator)
        dt = wx.DateTime.FromDMY(15, wx.DateTime.Sep, 2017)
        self.datepicker.SetValue(dt)

        self.stockcode = wx.TextCtrl(self, value='601988', pos=(50, 60), size=(140, -1))

        self.button = wx.Button(self, label='Start', pos=(50, 325))
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.button)

        self.result = wx.TextCtrl(self, pos=(300,20), size=(400, 300),
                                  style=wx.TE_MULTILINE | wx.TE_READONLY)

        """
        # 仅有1行的编辑控件
        self.lblname = wx.StaticText(self, label='Your name:', pos=(20, 60))
        self.editname = wx.TextCtrl(self, value='Enter here your name:',
                                    pos=(150, 60), size=(140, -1))
        self.Bind(wx.EVT_TEXT, self.EvtText, self.editname)
        self.Bind(wx.EVT_CHAR, self.EvtChar, self.editname)

        # 一个ComboBox控件（下拉菜单）
        self.sampleList = ['friends', 'advertising', 'web search', \
                           'Yellow Pages']
        self.lblhear = wx.StaticText(self, label="How did you hear from us ?",
                                     pos=(20, 90))
        self.edithear = wx.ComboBox(self, pos=(150, 90), size=(95, -1),
                                    choices=self.sampleList,
                                    style=wx.CB_DROPDOWN)
        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, self.edithear)
        # 注意ComboBox也绑定了EVT_TEXT事件
        self.Bind(wx.EVT_TEXT, self.EvtText, self.edithear)

        # 复选框
        self.insure = wx.CheckBox(self, label="Do you want Insured Shipment ?",
                                  pos=(20,180))
        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox, self.insure)

        # 单选框
        radioList = ['blue', 'red', 'yellow', 'orange', 'green', 'purple', \
                     'navy blue', 'black', 'gray']
        self.rb = wx.RadioBox(label="What color would you like ?",
                              pos=(20, 210), choices=radioList, \
                              majorDimension=3, style=wx.RA_SPECIFY_COLS)
        self.Bind(wx.EVT_RADIOBOX, self.EvtRadioBox, self.rb)
        """

    """
               date  open  close  high   low     volume    code
173  2017-09-15   4.1   4.06  4.11  4.02  1935670.0  601988
<class 'pandas.core.series.Series'>-----2017-09-15	4.1
    """

    def OnClick(self, event):

        code = self.stockcode.GetValue()
        start_end = self.datepicker.GetValue().Format('%Y-%m-%d')
        try:
            df=ts.get_k_data(code, start=start_end, end=start_end)
        except Exception as e:
            self.result.AppendText('%s\n' % str(e))

        to_be_appended = ''
        for index, row in df.iterrows():
            to_be_appended = to_be_appended + \
                             "%s\t%s\t%s\t%s\t%s\t%s" % (str(row['date']), str(row['code']),
                             str(row['open']), str(row['close']), str(row['high']), str(row['low']))

        self.result.AppendText(to_be_appended)

    """
    def EvtText(self, event):
        self.logger.AppendText(self, 'EvtText: %s\n' % event.GetString())
    def EvtChar(self, event):
        self.logger.AppendText('EvtChar: %d\n' % event.GetKeyCode())
        event.Skip()
    def EvtComboBox(self, event):
        self.logger.AppendText('EvtComboBox: %s\n' % event.GetString())
    def EvtCheckBox(self, event):
        self.logger.AppendText('EvtCheckBox: %d\n' % event.Checked())
    def EvtRadioBox(self, event):
        self.logger.AppendText('EvtRadioBox: %d\n' % event.GetInt())
    """


app = wx.App(False)
frame = wx.Frame(None, title = "小停牌工具", size = (800, 450))
panel = StatisticsPanel(frame)
frame.Show()
app.MainLoop()


#end
