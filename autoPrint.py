#python批量打印word文件
#pip install pypiwin32
import tempfile
import win32api
import win32print
import os


#成批打印word文件
def printer_loading(filename):
    open(filename, "r")
    win32api.ShellExecute(
        0,
        "print",
        filename,
        #
        # If this is None, the default printer will
        # be used anyway.
        #
        '/d:"%s"' % win32print.GetDefaultPrinter(),
        ".",
        0
    )

path=r'I:\PycharmProjects\aboutWorkGit\ok'
for a, b, c in os.walk(path):
    print(c)
for i in c:
    f = os.path.join(path, i)
    if f.endswith("docx"):
        print(f)
        printer_loading(f)
