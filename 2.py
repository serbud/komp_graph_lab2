import sys
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication, QPushButton, QLineEdit, QLabel
from PyQt5.QtCore import QCoreApplication, pyqtSlot
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageDraw

imageroute = sys.argv[1]
imageroute2 = "temp5.jpg"
def RGBtoHSL(R,G,B):
    R = R/255
    G = G/255
    B = B/255
    Cmax = max(R,G,B)
    Cmin = min(R,G,B)
    delta = Cmax-Cmin
    L = (Cmin+Cmax)/2
    if delta == 0:
        H = 0
        S = 0
    else:
        S = delta / (1-abs(2*L-1))
        if R == Cmax:
            H = 60*(((G-B)/delta)%6)
        elif G == Cmax:
            H = 60*(((B-R)/delta)+2)
        else:
            H = 60*(((R-G)/delta)+4)
    return H, S, L
def RGBtoHSV(R,G,B):
    R = R/255
    G = G/255
    B = B/255
    Cmax = max(R,G,B)
    Cmin = min(R,G,B)
    delta = Cmax - Cmin
    V = Cmax
    if delta == 0:
        H = 0
        S = 0
    else:
        S = delta / V
        if R == Cmax:
            H = 60*(((G-B)/delta)%6)
        elif G == Cmax:
            H = 60*(((B-R)/delta)+2)
        else:
            H = 60*(((R-G)/delta)+4)
    return H, S, V
def HSLtoRGB(H,S,L):
    C = (1-abs(2*L-1))*S
    X = C * (1-abs((H/60)%2 -1))
    m = L - C/2
    R = 0
    G = 0
    B = 0
    if (H >= 0 and H < 60):
        R = C
        G = X
        B = 0
    elif (H >= 60 and H < 120):
        R = X
        G = C
        B = 0
    elif (H >= 120 and H < 180):
        R = 0
        G = C
        B = X
    elif (H >= 180 and H < 240):
        R = 0
        G = X
        B = C
    elif (H >= 240 and H < 300):
        R = X
        G = 0
        B = C
    elif (H >= 300 and H < 360):
        R = C
        G = 0
        B = X

    R = (R + m) * 255
    G = (G + m) * 255
    B = (B + m) * 255

    return R, G, B
def HSVtoRGB(H,S,V):
    C = V*S
    X = C * (1-abs((H/60)%2 -1))
    m = V - C
    R = 0
    G = 0
    B = 0
    if (H >= 0 and H < 60):
        R = C
        G = X
        B = 0
    elif (H >= 60 and H < 120):
        R = X
        G = C
        B = 0
    elif (H >= 120 and H < 180):
        R = 0
        G = C
        B = X
    elif (H >= 180 and H < 240):
        R = 0
        G = X
        B = C
    elif (H >= 240 and H < 300):
        R = X
        G = 0
        B = C
    elif (H >= 300 and H < 360):
        R = C
        G = 0
        B = X

    R = (R + m) * 255
    G = (G + m) * 255
    B = (B + m) * 255

    return R,G,B


class Example(QWidget):



    def __init__(self):
        super().__init__()
        self.initUI()
        # self.applyChanges()


    def applyChanges1(self):
        global imageroute
        image = Image.open(imageroute)  # Открываем изображение.
        draw = ImageDraw.Draw(image)  # Создаем инструмент для рисования.
        width = image.size[0]  # Определяем ширину.
        height = image.size[1]  # Определяем высоту.
        pix = image.load()  # Выгружаем значения пикселей.
        if type(pix[0,0]) != int:
            gist = [0 for i in range(256)]
            for i in range(width):
                for j in range(height):
                    R = pix[i, j][0]
                    G = pix[i, j][1]
                    B = pix[i, j][2]
                    Y = 0.299 * R + 0.587 * G + 0.114 * B
                    gist[round(Y)] += 1


            f1 = True
            f2 = True
            mins = 255
            maxs = 0

            for i in range(256):
                if (not gist[i] == 0 and f1):
                    f1 = False
                    mins = i

                if (not gist[256 - i - 1] == 0 and f2):
                    f2 = False
                    maxs = 256 - i - 1



            b = 255 / (maxs - mins)
            a = -b * mins

            for i in range(width):
                for j in range(height):
                    R = pix[i, j][0]
                    G = pix[i, j][1]
                    B = pix[i, j][2]
                    Y = 0.299 * R + 0.587 * G + 0.114 * B
                    Ynew = a + b * Y
                    if Y == 0:
                        k = Ynew/0.001
                    else:
                        k = Ynew / Y


                    R = pix[i, j][0] * k
                    G = pix[i, j][1] * k
                    B = pix[i, j][2] * k
                    draw.point((i, j), (round(R), round(G), round(B)))
        else:
            gist = [0 for i in range(256)]
            for i in range(width):
                for j in range(height):
                    Y = pix[i,j]
                    gist[Y] += 1
            f1 = True
            f2 = True
            mins = 255
            maxs = 0

            for i in range(256):
                if (not gist[i] == 0 and f1):
                    f1 = False
                    mins = i

                if (not gist[256 - i - 1] == 0 and f2):
                    f2 = False
                    maxs = 256 - i - 1

            b = 255 / (maxs - mins)
            a = -b * mins


            for i in range(width):
                for j in range(height):

                    Y = pix[i,j]
                    Ynew = a + b * Y
                    draw.point((i, j), (round(Ynew)))

        image.save(imageroute2, "JPEG")
        del draw

        self.pixmap = QPixmap(imageroute2)
        self.imageLabel.setPixmap(self.pixmap)
        self.show()
        print("finish load")




    def applyChanges2(self):
        global imageroute
        image = Image.open(imageroute)  # Открываем изображение.
        draw = ImageDraw.Draw(image)  # Создаем инструмент для рисования.
        width = image.size[0]  # Определяем ширину.
        height = image.size[1]  # Определяем высоту.
        pix = image.load()  # Выгружаем значения пикселей.
        if type(pix[0,0]) == int:
            gist = [0 for i in range(256)]
            for i in range(width):
                for j in range(height):
                    Y = pix[i,j]
                    gist[Y] += 1

            f1 = True
            f2 = True
            mins = 255
            maxs = 0
            tmp = 0
            for i in range(256):
                if gist[i] * 3 < gist[i + 1]:
                    tmp = i
                    break
            for i in range(256):
                if (not gist[i] < tmp and f1):
                    f1 = False
                    mins = i

                print(gist[i], gist[256 - i - 1])
                if (not gist[256 - i - 1] < tmp and f2):
                    f2 = False
                    maxs = 256 - i - 1


            # sr = maxot - minot

            b = 255 / (maxs - mins)
            a = -b * mins
            for i in range(width):
                for j in range(height):
                    Y = pix[i,j]
                    Ynew = a + b * Y

                    draw.point((i, j), (round(Ynew)))
        else:
            gist = [0 for i in range(256)]
            for i in range(width):
                for j in range(height):
                    R = pix[i, j][0]
                    G = pix[i, j][1]
                    B = pix[i, j][2]
                    Y = 0.299 * R + 0.587 * G + 0.114 * B
                    gist[round(Y)] += 1



            f1 = True
            f2 = True
            mins = 255
            maxs = 0
            tmp = 0
            for i in range(256):
                if gist[i] * 3 < gist[i + 1]:
                    tmp = i
                    break
            for i in range(256):
                if (not gist[i] < tmp and f1):
                    f1 = False
                    mins = i

                if (not gist[256 - i - 1] < tmp and f2):
                    f2 = False
                    maxs = 256 - i - 1

            # sr = maxot - minot

            b = 255 / (maxs - mins)
            a = -b * mins

            for i in range(width):
                for j in range(height):
                    R = pix[i, j][0]
                    G = pix[i, j][1]
                    B = pix[i, j][2]
                    Y = 0.299 * R + 0.587 * G + 0.114 * B
                    Ynew = a + b * Y
                    if Y == 0:
                        k = Ynew / 0.001
                    else:
                        k = Ynew / Y

                    R = pix[i, j][0] * k
                    G = pix[i, j][1] * k
                    B = pix[i, j][2] * k
                    draw.point((i, j), (round(R), round(G), round(B)))

        image.save(imageroute2, "JPEG")
        del draw

        self.pixmap = QPixmap(imageroute2)
        self.imageLabel.setPixmap(self.pixmap)
        self.show()
        print("finish load")

    def applyChanges3(self):
        global imageroute
        image = Image.open(imageroute)  # Открываем изображение.
        draw = ImageDraw.Draw(image)  # Создаем инструмент для рисования.
        width = image.size[0]  # Определяем ширину.
        height = image.size[1]  # Определяем высоту.
        pix = image.load()  # Выгружаем значения пикселей.
        if type(pix[0, 0]) == int:
            h = [0 for i in range(256)]

            for i in range(width):
                for j in range(height):
                    L = pix[i, j]
                    h[L] += 1
            for i in range(255):
                h[i] = h[i] / (height * width)

            for i in range(1, 255, 1):
                h[i] = h[i - 1] + h[i]
            for i in range(width):
                for j in range(height):
                    L = pix[i, j]
                    Lnew = h[L]
                    draw.point((i, j), (round(Lnew * 255)))
        else:
            h = [0 for i in range(256)]

            for i in range(width):
                for j in range(height):
                    H, S, L = RGBtoHSL(pix[i, j][0], pix[i, j][1], pix[i, j][2])
                    h[round(L * 255)] += 1


            for i in range(255):
                h[i] = h[i] / (height * width)

            for i in range(1, 255, 1):
                h[i] = h[i - 1] + h[i]
            for i in range(width):
                for j in range(height):
                    H, S, L = RGBtoHSL(pix[i, j][0], pix[i, j][1], pix[i, j][2])

                    Lnew = h[round(255 * L)]
                    R, G, B = HSLtoRGB(H, S, Lnew)
                    draw.point((i, j), (round(R), round(G), round(B)))

        image.save(imageroute2, "JPEG")
        del draw

        self.pixmap = QPixmap(imageroute2)
        self.imageLabel.setPixmap(self.pixmap)
        self.show()
        print("finish load")


    @pyqtSlot()
    def on_click(self):
        self.applyChanges1()

        self.show()

    @pyqtSlot()
    def on_click1(self):

        self.applyChanges2()
        self.show()

    @pyqtSlot()
    def on_click2(self):

        self.applyChanges3()
        self.show()


    def initUI(self):
        global imageroute
        self.imageLabel = QLabel(self)
        self.pixmap = QPixmap(imageroute)
        self.imageLabel.setPixmap(self.pixmap)
        self.imageLabel.move(220, 50)
        self.resize(220+self.pixmap.width()+50, 50+self.pixmap.height()+50)
        self.center()

        self.qbtn = QPushButton('линейное контрастирование', self)
        self.qbtn.clicked.connect(self.on_click)
        self.qbtn.resize(self.qbtn.sizeHint())
        self.qbtn.move(50, 170)
        self.qbtn1 = QPushButton('нормализация', self)
        self.qbtn1.clicked.connect(self.on_click1)
        self.qbtn1.resize(self.qbtn1.sizeHint())
        self.qbtn1.move(50, 200)
        self.qbtn1 = QPushButton('эквализация', self)
        self.qbtn1.clicked.connect(self.on_click2)
        self.qbtn1.resize(self.qbtn1.sizeHint())
        self.qbtn1.move(50, 230)





        self.setWindowTitle('Center')
        self.show()


    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()



    sys.exit(app.exec_())