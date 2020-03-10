import sys
from WalkingPatternAnalyseTool import PdVisualization
from PyQt5.QtWidgets import QApplication, QMainWindow

import sys, os, subprocess, time, shutil, signal
import atexit


from PyQt5 import Qt, QtCore

# control start or stop for left and right
start_Left = 0
start_Right = 0
# folder to save frames
f1 = "frames_Left"
f2 = "frames_Right"
# process to control left, right
pro1 = None
pro2 = None
# timer to link the slider
# horizontalSlider_2
t1 = 0
t2 = 0

class VideoWindow(Qt.QGraphicsView):
    def __init__(self, viewWin, dirName, st, slider, parent=None):
        Qt.QGraphicsView.__init__(self, parent)
        self.scene  = Qt.QGraphicsScene()
        self.grview = viewWin
        self.timer = Qt.QTimer(self)
        self.n = 0
        self.timer.timeout.connect(self.on_timeout)
        self.timer.start(300)
        self.grview.show()
        self.dirname = dirName
        self.st = st
        self.slider = slider




    def on_timeout(self):
        global t1, t2
        self.listFiles = os.listdir(self.dirname)
        t = 0
        # print(len(self.listFiles))
        if self.st == 0:
            start = start_Left
            self.n = t1
        else:
            start = start_Right
            self.n = t2
        if start and len(self.listFiles)>0:
            # print("in", self.n)
            if self.n < len(self.listFiles):
                self.scene.clear()
                file = self.listFiles[self.n]
                pixmap = Qt.QPixmap(self.dirname +"\{}".format(file))
                self.scene.addPixmap(pixmap)
                self.grview.fitInView(self.scene.itemsBoundingRect(), QtCore.Qt.KeepAspectRatio)
                self.grview.setScene(self.scene)
                self.slider.setValue(self.n)
                self.n += 1
                if self.st == 0:
                    t1 = self.n
                else:
                    t2 = self.n
            elif self.n >= len(self.listFiles):
                self.scene.clear()
                pixmap = Qt.QPixmap('wait.png')
                self.scene.addPixmap(pixmap)
                self.grview.fitInView(self.scene.itemsBoundingRect())
                self.grview.setScene(self.scene)
                self.slider.setValue(self.n)
                print("wait", self.dirname)
                if self.n == len(self.listFiles):
                    time.sleep(2)
                # self.timer.stop()




def startVis():
    print("start!")

    if os.path.exists(f1):
        shutil.rmtree(f1)
    os.makedirs(f1)
    if os.path.exists(f2):
        shutil.rmtree(f2)
    os.makedirs(f2)

    global pro1, pro2, start_Left,start_Right, ui
    pro1 = subprocess.Popen("blender -b untitled.blend -x 1 -o //"+f1+"/render -s 10 -e 500 -a",  stdout=subprocess.DEVNULL)
    pro2 = subprocess.Popen("blender -b untitled2.blend -x 1 -o //"+f2+"/render -s 10 -e 500 -a",  stdout=subprocess.DEVNULL)
    ui.horizontalSlider.setMaximum(490)
    ui.horizontalSlider_2.setMaximum(490)




    time.sleep(5)

    start_Left = 1
    start_Right = 1


def exit_handler():
    if pro1 != None:
        time.sleep(0.1)
        pro1.kill()
    if pro2 != None:
        time.sleep(0.1)
        pro2.kill()

    if os.path.exists(f1):
        shutil.rmtree(f1)
    if os.path.exists(f2):
        shutil.rmtree(f2)


    print('My application is ending!')



def leftSliderReleased():
    global t1, ui
    t1 = ui.horizontalSlider.value()


def rightSliderReleased():
    global t2, ui
    t2 = ui.horizontalSlider_2.value()


def pauseLeft():
    print("inLeft")
    global start_Left, ui
    if start_Left == 1:
        start_Left = 0
    else:
        start_Left = 1


def pauseRight():
    print("inRight")
    global start_Right, ui
    if start_Right == 1:
        start_Right = 0
    else:
        start_Right = 1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()


    if os.path.exists(f1):
        shutil.rmtree(f1)
    os.makedirs(f1)
    if os.path.exists(f2):
        shutil.rmtree(f2)
    os.makedirs(f2)

    ui = PdVisualization.Ui_mainWindow()
    ui.setupUi(MainWindow)
    ui.graphicsView = VideoWindow( ui.graphicsView, f1, 0, ui.horizontalSlider)
    ui.graphicsView_2 = VideoWindow( ui.graphicsView_2, f2, 1, ui.horizontalSlider_2)

    #  start visualization
    ui.pushButton.clicked.connect(startVis)

    # read slider value
    ui.horizontalSlider.sliderReleased.connect(leftSliderReleased)
    ui.horizontalSlider_2.sliderReleased.connect(rightSliderReleased)

    # pause and release
    ui.toolButton_5.clicked.connect(pauseLeft)
    ui.toolButton_8.clicked.connect(pauseRight)


    MainWindow.show()

    atexit.register(exit_handler)
    sys.exit(app.exec_())



