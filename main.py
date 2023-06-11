#!usr/bin/env python3
# -*- coding: utf-8 -*-
# @Software : PyCharm
import sys

from PyQt5 import QtWidgets
from utils import MainWindow


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


main()
