
import wx
# from wxPtython.ui_frame import MyFrame1, MyFrame2
from ui_frame import MyFrame1, MyFrame2


class MyFrame(object):
    def __init__(self):
        self.root = MyFrame1(None)
        self.root.m_choice2.Clear()
        self.root.m_choice2.SetItems([u"qqq", u"www"])
        self.root.m_choice2.SetSelection(0)
        self.root.m_sdbSizer1OK.Bind(wx.EVT_BUTTON, self.m_sdbSizer1OnOKButtonClick)
        self.root.m_sdbSizer1Cancel.Bind(wx.EVT_BUTTON, self.m_sdbSizer1OnCancelButtonClick)
        self.root.Bind(wx.EVT_CLOSE, self.OnClose)

        self.sub = MyFrame2(None)
        self.sub.Bind(wx.EVT_CLOSE, self.OnClose)

    def m_sdbSizer1OnOKButtonClick(self, event):
        self.root.Destroy()
        event.Skip()
        self.sub.Show(True)

    def m_sdbSizer1OnCancelButtonClick(self, event):
        wx.Exit()
        event.Skip()

    def show(self):
        self.root.Show(True)

    def OnClose(self, event):
        wx.Exit()
        event.Skip()


def main():
    app = wx.App()
    frame = MyFrame()
    frame.show()
    app.MainLoop()


if __name__ == '__main__':
    main()
