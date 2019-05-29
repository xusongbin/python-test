
import os, time
from win32com.client import Dispatch
import pythoncom


# 启用win32模块导出excel的图表，图表需要打开加载缓存才能导出
class Pyxlchart(object):
    # This class exports charts in an Excel Spreadsheet to the FileSystem
    # win32com libraries are required.
    def __init__(self):
        # 初始化图表
        pythoncom.CoInitialize()
        self.WorkbookDirectory = ''     # excel文件所在目录
        self.WorkbookFilename = ''      # 文件名称
        self.GetAllWorkbooks = False    # 获取所有book
        self.SheetName = ''         # sheet名称
        self.ChartName = ''         # 导出单张图表时，指定图表名称
        self.GetAllWorkbookCharts = False
        self.GetAllWorksheetCharts = True
        self.ExportPath = ''        # 导出的文件路径
        self.ImageFilename = ''     # 导出的图片名称
        self.ReplaceWhiteSpaceChar = '_'
        self.ImageType = 'jpg'

    def __del__(self):
        pass

    def start_export(self,_visible=False):
        if self.WorkbookDirectory == '':
            return "WorkbookDirectory not set"
        else:
            self._export(_visible)

    def _export(self, _visible):
        # Exports Charts as determined by the settings in class variabels.
        excel = Dispatch("excel.application")
        # 启用独立的进程调用excel，Dispatch容易冲突【会强行关闭正在打开的excel】
        # 使用 DispatchEx为单独调用线程，不影响已经打开的excel

        excel.Visible = _visible
        wb = excel.Workbooks.Open(os.path.join(self.WorkbookDirectory, self.WorkbookFilename))

        if self.SheetName != "" and self.ChartName != "":
            while True:
                time.sleep(0.5)
                sht = self._change_sheet(wb, self.SheetName)
                cht = sht.ChartObjects(self.ChartName)
                if cht:
                    break
        '''
        time.sleep(3)  # 等5秒等待进程打开加载文档
        # 使用打开excel的方式，则模拟键盘事件触发加载所有图表
        if excel.Visible == 1 or excel.Visible is True:
            win32api.keybd_event(17, 0, 0, 0)  # 键盘按下  ctrl键
            time.sleep(1)
            for k in range(4):
                win32api.keybd_event(34, 0, 0, 0)  # ctrl+pageDown的组合会跳转sheet，20次跳转可以到最后的图表
            win32api.keybd_event(36, 0, 0, 0)  # 键盘按下  home键，和上个按键形成组合键，回到第一行开头
            win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)
            win32api.keybd_event(36, 0, win32con.KEYEVENTF_KEYUP, 0)

            # 当表格过大时，只能保存到页面显示的图标，故此需要先循环翻页将所有图片加载
            for i in range(15):  # 翻页加载所有图表
                win32api.keybd_event(34, 0, 0, 0)  # 每次读取之后翻页
                win32api.keybd_event(34, 0, win32con.KEYEVENTF_KEYUP, 0)
                time.sleep(0.5)
        '''

        # 图片加载完成，好了，导出图片继续进行
        self._get_Charts_In_Worksheet(wb, self.SheetName, self.ChartName)
        wb.Close(True)
        excel.Quit()

    def _get_Charts_In_Worksheet(self, wb, worksheet="", chartname=""):
        if worksheet != "" and chartname != "":
            sht = self._change_sheet(wb, worksheet)
            cht = sht.ChartObjects(chartname)

            self._save_chart(cht)
            return
        if worksheet == "":  # 导出表格中所有图表
            for sht in wb.Worksheets:
                for cht in sht.ChartObjects():
                    if chartname == "":
                        self._save_chart(cht)
                    else:
                        if chartname == cht.Name:
                            self._save_chart(cht)
        else:   # 导出指定sheet中的图标
            sht = wb.Worksheets(worksheet)
            for cht in sht.ChartObjects():
                if chartname == "":
                    self._save_chart(cht)
                else:
                    if chartname == cht.Name:
                        self._save_chart(cht)

    def _change_sheet(self, wb, worksheet):
        try:
            return wb.Worksheets(worksheet)
        except:
            raise NameError('Unable to Select Sheet: ' + worksheet + ' in Workbook: ' + wb.Name)

    def _save_chart(self, chartObject):
        # 保存图标到指定路径
        # :param chartObject: 图表名称
        # :return:
        imagename = self._get_filename(chartObject.Name)
        savepath = os.path.join(self.ExportPath, imagename)
        # print(savepath)

        chartObject.Chart.Export(savepath, self.ImageType)

    def _get_filename(self, chartname):
        # 获取导出图表的文件名称
        # Replaces white space in self.WorkbookFileName with the value given in self.ReplaceWhiteSpaceChar
        # If self.ReplaceWhiteSpaceChar is an empty string then self.WorkBookFileName is left as is
        if self.ReplaceWhiteSpaceChar != '':
            chartname.replace(' ', self.ReplaceWhiteSpaceChar)
        if self.ImageFilename == '':    # 未指定导出的图片名称，则与图表名称一致
            return chartname + "." + self.ImageType
        else:   # 指定了导出图片的命名格式
            return self.ImageFilename + "_" + chartname + "." + self.ImageType


docPath = r'C:\Users\Administrator\Desktop\银行.xlsx'
docSheet = '5分钟'

if __name__ == '__main__':
    print(docPath)
    path = docPath[:docPath.rfind('\\')]
    print(path)
    file = docPath[docPath.rfind('\\')+1:]
    print(file)
    Ect = Pyxlchart()
    Ect.WorkbookDirectory = path
    Ect.WorkbookFilename = file
    Ect.SheetName = docSheet  # 图表所在的sheet名称
    Ect.ExportPath = path  # 图片的导出路径
    Ect.start_export()
