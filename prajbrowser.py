import wx
from wx import html2

class MainApp(wx.App):
    def OnInit(self):
        browser = WebPageFrame(None, "Browser", pos = (100, 100))
        browser.SetSize(900, 800)
        browser.Show()
        return True
    
class WebPageFrame(wx.Frame):
    def __init__(self, parent, title, pos):
        super().__init__(parent, title = title, pos = pos)

        self.browserFrame = html2.WebView.New(self)
        self.browserFrame.LoadURL("https://google.com")
        self._nav = NavigationPanel(self, self.browserFrame)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self._nav, 0, wx.EXPAND)
        sizer.Add(self.browserFrame, 1, wx.EXPAND)
        self.SetSizer(sizer)

        self.Bind(html2.EVT_WEBVIEW_TITLE_CHANGED, self.OnTitleChange)

    def OnTitleChange(self, event):
        self.Title = event.GetString()

class NavigationPanel(wx.Panel):
    def __init__(self, parent, browser):
        super().__init__(parent)

        self.browser = browser
        print("Current URL:", self.browser.GetCurrentURL())
        self._url = wx.TextCtrl(parent = self, style = wx.TE_PROCESS_ENTER)
        self._url.SetHint("Enter web address")
        self._url.Bind(wx.EVT_TEXT_ENTER, self.onEnter)

        back = wx.Button(self, style = wx.BU_EXACTFIT)
        back.Bitmap = wx.ArtProvider.GetBitmap(wx.ART_GO_BACK, wx.ART_TOOLBAR)

        forward = wx.Button(self, style = wx.BU_EXACTFIT)
        forward.Bitmap = wx.ArtProvider.GetBitmap(wx.ART_GO_FORWARD, wx.ART_TOOLBAR)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(back, proportion = 0, flag = wx.ALL, border = 5)
        sizer.Add(forward, proportion = 0, flag = wx.ALL, border = 5)
        sizer.Add(window = self._url, proportion = 1, flag = wx.EXPAND)
        self.SetSizer(sizer)

    def onEnter(self, event):
        self.browser.LoadURL(self._url.Value)

    def goBack(self, event):
        event.Enable(self.browser.CanGoBack())
        self.browser.GoBack()
    
    def goForward(self, event):
        event.Enable(self.browser.CanGoForward())
        self.browser.GoForward()

if __name__ == "__main__":
    app = MainApp()
    app.MainLoop()