import sys
from PyQt5.QtWidgets import QWidget

out = sys.stdout
sys.stdout = open(r'D:\dropbox\Dropbox\git_hnjyzdc\git_python\python_pyqt5\QWidget.txt','w')
help(QWidget)
sys.stdout.close()
sys.stdout = out