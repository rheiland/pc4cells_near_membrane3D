"""
Authors:
Randy Heiland (heiland@iu.edu)
Adam Morrow, Michael Siler, Grant Waldrow, Drew Willis, Kim Crevecoeur
Dr. Paul Macklin (macklinp@iu.edu)

--- Versions ---
0.1 - initial version
"""
# https://doc.qt.io/qtforpython/gettingstarted.html

import os
import sys
import getopt
import shutil
from pathlib import Path
import xml.etree.ElementTree as ET  # https://docs.python.org/2/library/xml.etree.elementtree.html
from xml.dom import minidom

# from matplotlib.colors import TwoSlopeNorm

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *

from vis_tab_2views import Vis 

class QHLine(QFrame):
    def __init__(self, sunken_flag):
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameStyle(QFrame.NoFrame)
        if sunken_flag:
            self.setFrameShadow(QFrame.Sunken)

def SingleBrowse(self):
        # if len(self.csv) < 2:
    filePath = QFileDialog.getOpenFileName(self,'',".",'*.xml')

        #     if filePath != "" and not filePath in self.csv:
        #         self.csv.append(filePath)
        # print(self.csv)
  
#class PhysiCellXMLCreator(QTabWidget):
class PhysiCellXMLCreator(QWidget):
    # def __init__(self, parent = None):
    def __init__(self, show_vis_flag, parent = None):
        super(PhysiCellXMLCreator, self).__init__(parent)

        # self.nanohub = True
        self.nanohub_flag = False
        if( 'HOME' in os.environ.keys() ):
            self.nanohub_flag = "home/nanohub" in os.environ['HOME']

        self.title_prefix = "studio_2views"
        # self.title_prefix = "PhysiCell Studio"
        self.setWindowTitle(self.title_prefix)

        # Menus
        vlayout = QVBoxLayout(self)
        # vlayout.setContentsMargins(5, 35, 5, 5)  # left,top,right,bottom
        vlayout.setContentsMargins(-1, 10, -1, -1)
        # if not self.nanohub_flag:
        if True:
            menuWidget = QWidget(self.menu())
            vlayout.addWidget(menuWidget)
            vlayout.addWidget(QHLine(False))
        self.setLayout(vlayout)

        self.resize(950, 770)  # width, height (height >= Cell Types|Death params)
        self.setMinimumSize(750, 770)  # width, height (height >= Cell Types|Death params)
        # self.setMinimumSize(1200, 770)  # width, height (height >= Cell Types|Death params)

        #------------------
        tabWidget = QTabWidget()
        stylesheet = """
            QTabBar::tab:selected {background: orange;}   #  dodgerblue
            """
        tabWidget.setStyleSheet(stylesheet)
        if show_vis_flag:
            print("studio_2views.py: creating vis_tab (Plot tab)")
            self.vis_tab = Vis(self.nanohub_flag)
            tabWidget.addTab(self.vis_tab,"Plot")

        vlayout.addWidget(tabWidget)

    def menu(self):
        menubar = QMenuBar(self)
        menubar.setNativeMenuBar(False)

        #--------------
        # file_menu = menubar.addMenu('&Model')
        # file_menu.addAction("Save as mymodel.xml", self.save_as_cb)

        view_menu = menubar.addMenu('&View')
        view_menu.addAction("Toggle domain box", self.toggle_domain_box)

        menubar.adjustSize()  # Argh. Otherwise, only 1st menu appears, with ">>" to others!

    def toggle_domain_box(self):
        self.vis_tab.toggle_domain_box()

    def indent(elem, level=0):
        i = "\n" + level*"  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                indent(elem, level+1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

    def prettify(self, elem):
        """Return a pretty-printed XML string for the Element.
        """
        rough_string = ET.tostring(elem, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="",  newl="")  # newl="\n"

def main():
    inputfile = ''
    # show_vis_tab = False
    show_vis_tab = True
    try:
        # opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
        opts, args = getopt.getopt(sys.argv[1:],"hv:",["vis"])
    except getopt.GetoptError:
        # print 'test.py -i <inputfile> -o <outputfile>'
        print('getopt exception')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
        #  print 'test.py -i <inputfile> -o <outputfile>'
            print('bin/gui4xml.py [--vis]')
            sys.exit(1)
    #   elif opt in ("-i", "--ifile"):
        elif opt in ("--vis"):
            show_vis_tab = True
    # print 'Input file is "', inputfile
    # print("show_vis_tab = ",show_vis_tab)
    # sys.exit()

    app = QApplication(sys.argv)
    ex = PhysiCellXMLCreator(show_vis_tab)
    # ex.setGeometry(100,100, 800,600)
    ex.show()
    sys.exit(app.exec_())
	
if __name__ == '__main__':
    main()