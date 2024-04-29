import sys
from PyQt5.QtWidgets import *
from PyQt5.QtNetwork import QTcpSocket, QHostAddress
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtGui, QtCore

#创建登录界面
class Login_Window(QWidget,QTcpSocket,QHostAddress):

    #设置槽函数信息名称，格式信息
    switch_window = QtCore.pyqtSignal(str,int)

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("河南科技学院-机器人团队")
        self.resize(1920,1080)
        self.setFixedSize(1920,1080)

        layout = QVBoxLayout()
        background_label = QLabel(self)
        pixmap = QPixmap("login_window.png")
        background_label.setPixmap(pixmap)
        layout.addWidget(background_label)
        self.setLayout(layout)
        
        self.iP_lineedit = QLineEdit(self)
        self.iP_lineedit.move(940,770)
        self.iP_lineedit.resize(268,58)
        self.iP_lineedit.setStyleSheet('border:2px groove white;border-radius:10px;padding:2px 4px;')

        
        self.port_lineedit = QLineEdit(self)
        self.port_lineedit.move(940,851)
        self.port_lineedit.resize(268,58)
        self.port_lineedit.setStyleSheet('border:2px groove white;border-radius:10px;padding:2px 4px;')

        #连接按钮
        self.connect_button = QPushButton(self)
        self.connect_button.move(1215, 915)
        self.connect_button.resize(90,60)  
        self.connect_button.setFont(QFont('宋体', 20))
        self.connect_button.setStyleSheet('border:2px groove blue;border-radius:10px;padding:2px 4px;background-color:rgba(255, 255, 0,0);')
        self.connect_button.clicked.connect(self.switch) #按钮关联方法，在方法中执行槽函数信息的发送
        self.showMaximized()

    def switch(self):
        text = self.iP_lineedit.text()
        number = int(self.port_lineedit.text())
        
        #点击按钮，槽函数信息发送
        self.switch_window.emit(text,number)


#指针组件
class RotatingNeedle(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)    #先初始化父类的初始化函数
        self.angle = -113   #设置指向0的时候的角度

    #更新角度的方法
    def update_angle(self,angle):
        self.angle = angle
        self.update()

    #定义一个画笔事件
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 设置指针颜色和形状
        needle_color = QColor(255, 0, 0)
        needle_polygon = QPolygonF([
            QPoint(-3, 0),
            QPoint(3, 0),
            QPoint(0, -120)
        ])
        painter.translate(self.width() / 2, self.height() / 2)  # 将原点移动到窗口中心
        painter.rotate(self.angle)  # 旋转指针

        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(needle_color))
        painter.drawPolygon(needle_polygon)

        painter.end()

#圆形按钮
class CircleButton(QPushButton):
    def __init__(self, text, parent=None):
        super(CircleButton, self).__init__(text, parent)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        path = QPainterPath()
        path.addEllipse(QRectF(self.rect()))  # 创建一个椭圆路径

        color = QColor(0, 0, 255)  # 蓝色

        palette = self.palette()
        palette.setBrush(QPalette.Button, QBrush(color))
        self.setPalette(palette)

        painter.fillPath(path, self.palette().button())

        pen = QPen(QColor(255, 0, 0))  # 红色边界
        painter.setPen(pen)
        painter.drawEllipse(self.rect())

        # 绘制文字
        font = QFont()
        font.setPointSize(20)
        painter.setFont(font)
        painter.drawText(self.rect(), Qt.AlignCenter, "停止")

#三角形按钮
class TriangleButton(QPushButton):
    def __init__(self, text, parent=None):
        super(TriangleButton, self).__init__(text, parent)
        self.angle = 0
        self.center = QPoint(40,40)
        self.color = QColor(0, 0, 255)  # 蓝色
        self.name = "前"
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.translate(self.center)
        painter.rotate(self.angle)

        painter.setBrush(self.color)  # 设置画刷颜色
        painter.setPen(self.color)  # 设置画笔颜色

        path = QPainterPath()
        path.moveTo(0, -40)  # 顶点
        path.lineTo(40, 40)  # 右下角点
        path.lineTo(-40,40)  # 左下角点
        path.lineTo(0, -40)  # 返回到顶点，形成闭合路径

        palette = self.palette()
        palette.setColor(QPalette.Button,self.color)
        self.setPalette(palette)

        painter.fillPath(path, self.palette().button())

        painter.setPen(self.palette().dark().color())
        painter.drawPath(path)
    def rotate_button(self, angle):
        self.angle = angle
        self.update()



#三角形组件
class Triangle(QWidget):
    def __init__(self, parent):
        super(Triangle, self).__init__(parent)
        self.angle = 100
        self.center = QPoint(0, 0)
        self.color = QColor(255,0,0)  # 三角形颜色


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.translate(self.center)
        painter.rotate(self.angle)

        painter.setBrush(self.color)  # 设置画刷颜色
        painter.setPen(self.color)  # 设置画笔颜色

        triangle_path = QPainterPath()
        triangle_path.moveTo(0, -15)  # 顶点
        triangle_path.lineTo(10, 10)  # 右下角点
        triangle_path.lineTo(-10, 10)  # 左下角点
        triangle_path.lineTo(0, -15)  # 返回到顶点，形成闭合路径

        painter.drawPath(triangle_path)

    def move(self, dx, dy):
        self.center = QPoint(dx, dy)
        self.update()

    def rotate(self, angle):
        self.angle = angle
        self.update()



#画板组件
class mylable(QLabel):
    def __init__(self, parent):
        super(mylable, self).__init__(parent)
        # self.setStyleSheet("background-color: gray")
        self.Color = Qt.green  # pen color: default: blue
        self.penwidth = 2  # pen width: default: 4
        self.previous_point = None
        self.lines = []
        self.mouse_point_change_x = 0
        self.mouse_point_change_y = 0

        #添加三角形
        self.triangle = Triangle(self)
    def Sizeof(self,size_x, size_y):
        self.triangle.setGeometry(0,0 ,size_x,size_y) #三角形活动区域

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(self.Color, self.penwidth, Qt.SolidLine))

        # 绘制背景图片
        if self.background_image:
            painter.drawPixmap(self.rect(), self.background_image)

        painter.setPen(QPen(self.Color, self.penwidth, Qt.SolidLine))




        # 绘制所有线条
        for line in self.lines:
            x0, y0, x1, y1 = line
            painter.drawLine(x0, y0, x1, y1)

        # 画网格图
        grid_size = 1  # 网格大小
        painter.setPen(QPen(Qt.lightGray, 1, Qt.DotLine))
        for x in range(grid_size, self.width(), grid_size):
            painter.drawLine(x, 0, x, self.height())
        for y in range(grid_size, self.height(), grid_size):
            painter.drawLine(0, y, self.width(), y)

    def drawLine(self, x0, y0, x1, y1):
        self.lines.append((x0, y0, x1, y1))
        self.update()


    def mousePressEvent(self, event):
        print("鼠标事件执行！")
        if event.button() == Qt.LeftButton:
            if self.lines:
                start_x, start_y, _, _ = self.lines[0]
                self.mouse_point_change_x = event.x() - start_x
                self.mouse_point_change_y = event.y() - start_y
                self.lines = []


                
    def receiveCoordinates(self, a, b):
        if self.previous_point is not None:
            x0, y0 = self.previous_point
            x1, y1 = int(a), int(b)
            self.drawLine(x0, y0, x1, y1)
        self.previous_point = (int(a), int(b))

    #移动旋转三角
    def L_move(self,dx,dy):
        self.triangle.move(dx,dy)

    def L_rotate(self,angle):
        self.triangle.rotate(angle)

    def clearLines(self):
        self.mouse_point_change_x = 0
        self.mouse_point_change_y = 0
        self.L_move(0,0)
        self.L_rotate(0)
        self.lines = []
        self.update()

    def set_background_image(self, image_path):
        pixmap = QPixmap(image_path)
        self.background_image = pixmap.scaled(self.size())
        self.update()

class MyWidget(Login_Window,QWidget,QTcpSocket,QHostAddress):
    switch_to_main = QtCore.pyqtSignal()
    def __init__(self,text,number):
        self.t = text
        self.n = number
        self.font = QtGui.QFont() # 创建字体设置对象
        self.font.setPointSize(16) # 设置字体大小
        self.speed = 6000
        self.accelerate = 999
        self.speed2 = 4000
        self.flag_speed = 1
        self.send_times = 0
        self.previous_point = None
        super().__init__()
        self.initUI()
        self.tcp_socket = QTcpSocket()
        self.stream = QDataStream(self.tcp_socket)
        self.stream.setVersion(QDataStream.Qt_5_15)
        self.tcp_socket.readyRead.connect(self.receive_data)
        self.tcp_socket.connected.connect(self.send_data)
        self.tcp_socket.error.connect(self.get_error)

    #加速
    def Accelerate(self):
        self.speed += self.accelerate
        self.speed2 -= self.accelerate
        if self.speed >9999 and self.speed2 < 1:
            QMessageBox.information(self, "警告！", "速度最大了")
            self.speed2 = 1
            self.speed = 9999


        if self.flag_speed == 2 :
            if self.speed2 <1000:
                strSpeed = "aicy 2009 000" +str(self.speed2)
            else: 
                strSpeed = "aicy 0029 " + str(self.speed2) + " 5000 aiyc"
        elif self.flag_speed == 1:
                strSpeed = "aicy 0029 " + str(self.speed) + " 5000 aiyc"
        elif self.flag_speed == 3 :
                if self.speed2 <1000:
                    strSpeed = "aicy 2009 5000 000" + str(self.speed2) + "aiyc"
                else: 
                    strSpeed = "aicy 0029 5000 " + str(self.speed2) + "aiyc"
        else:
            strSpeed = "aicy 0029 5000 " + str(self.speed) + "aiyc"
        self.tcp_socket.write(strSpeed.encode())
    
    #减速
    def slowDown(self):
        self.speed -= self.accelerate
        self.speed2 += self.accelerate
        if self.speed <5000 and self.speed2 >4000:
            QMessageBox.information(self, "警告！", "速度最小了")
            self.speed2 = 4999
            self.speed = 5999
        if self.flag_speed == 2 :
            if self.speed2 <1000:
                strSpeed = "aicy 2009 000" +str(self.speed2)
            else: 
                strSpeed = "aicy 0029 " + str(self.speed2) + " 5000 aiyc"
        elif self.flag_speed == 1:
            strSpeed = "aicy 0029 " + str(self.speed) + " 5000 aiyc"
        elif self.flag_speed == 3 :
            if self.speed2 <1000:
                strSpeed = "aicy 2009 5000 000" + str(self.speed2) + "aiyc"
            else: 
                strSpeed = "aicy 0029 5000 " + str(self.speed2) + "aiyc"
        else:
            strSpeed = "aicy 0029 5000 " + str(self.speed) + "aiyc"
        self.tcp_socket.write(strSpeed.encode())

    #主界面设计
    def initUI(self):
        self.setWindowTitle("河南科技学院-机器人团队")
        self.resize(1920,1080)
        self.setFixedSize(1920,1080)

        #在标签中显示图片
        background_label = QLabel(self)
        pixmap = QPixmap("main_window6.png")
        background_label.setPixmap(pixmap)

        #设置线条
        self.line = QFrame(self)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setGeometry(1150 ,450 , 3, 500)
        self.line.setStyleSheet("background-color: white;")

        self.line2 = QFrame(self)
        self.line2.setFrameShape(QFrame.HLine)
        self.line2.setFrameShadow(QFrame.Sunken)
        self.line2.setGeometry(460 ,320 , 550, 3)
        self.line2.setStyleSheet("background-color: white;")
        
        self.line3 = QFrame(self)
        self.line3.setFrameShape(QFrame.HLine)
        self.line3.setFrameShadow(QFrame.Sunken)
        self.line3.setGeometry(1250 ,320 , 550, 3)
        self.line3.setStyleSheet("background-color: white;")

        self.mybutton1 = TriangleButton("前进", self)
        self.mybutton1.setGeometry(1458, 500,80,80)
        
        self.mybutton1.clicked.connect(lambda: self.tool_button_clicked("aicy 0029 6000 5000 aiyc"))

        self.mybutton2 = TriangleButton("后退",self)
        self.mybutton2.setGeometry(1458, 790,80,80)
        self.mybutton2.rotate_button(180)
        self.mybutton2.clicked.connect(lambda: self.tool_button_clicked("aicy 0029 4000 5000 aiyc"))

        self.mybutton3 = TriangleButton("左转", self)
        self.mybutton3.setGeometry(1310, 645,80,80)
        self.mybutton3.rotate_button(-90)
        self.mybutton3.clicked.connect(lambda: self.tool_button_clicked("aicy 0029 5000 6000 aiyc"))

        self.mybutton4 = TriangleButton("右转", self)
        self.mybutton4.setGeometry(1610, 645,80,80)
        self.mybutton4.rotate_button(90)
        self.mybutton4.clicked.connect(lambda: self.tool_button_clicked("aicy 0029 5000 4000 aiyc"))

        self.mybutton5 = CircleButton("停止", self)
        self.mybutton5.setGeometry(1420, 605,160,160)
        self.mybutton5.clicked.connect(lambda: self.tool_button_clicked("aicy 0029 5000 5000 aiyc"))

        self.mybutton8 = QPushButton("加速", self)
        self.mybutton8.move(1630, 870)
        self.mybutton8.resize(160,60)
        self.mybutton8.setFont(self.font)
        self.mybutton8.setStyleSheet("QPushButton{font-family:'宋体';font-size:50px;color:white;}"
                             "QPushButton{background-color:blue;border:2px groove blue;border-radius:10px;padding:2px 4px;}"
                             "QPushButton:hover{background-color:blue;border:2px groove white;border-radius:10px;padding:2px 4px;}")
        self.mybutton8.clicked.connect(self.Accelerate)

        self.mybutton9 = QPushButton("减速", self)
        self.mybutton9.move(1190, 870)
        self.mybutton9.resize(160,60)
        self.mybutton9.setFont(self.font)
        self.mybutton9.setStyleSheet("QPushButton{font-family:'宋体';font-size:50px;color:white;}"
                             "QPushButton{background-color:blue;border:2px groove blue;border-radius:10px;padding:2px 4px;}"
                             "QPushButton:hover{background-color:blue;border:2px groove white;border-radius:10px;padding:2px 4px;}")
        self.mybutton9.clicked.connect(self.slowDown)

        self.mybutton7 = QPushButton("退出", self)
        self.mybutton7.move(1755, 15)
        self.mybutton7.resize(150,50)
        self.mybutton7.setFont(self.font)
        self.mybutton7.setStyleSheet("QPushButton{font-family:'宋体';font-size:50px;color:white;}"
                             "QPushButton{background-color:blue;border:2px groove blue;border-radius:10px;padding:2px 4px;}"
                             "QPushButton:hover{background-color:blue;border:2px groove red;border-radius:10px;padding:2px 4px;}")
        self.mybutton7.clicked.connect(self.switch2) 

        # 标签
        self.nameLabel = QLabel("前",self)
        self.nameLabel.move(1478, 535)
        self.nameLabel.resize(35,35)
        self.nameLabel.setStyleSheet("QLabel {font-family: '宋体'; font-size:35px; color: white; opacity: 0;}")
        self.nameLabel1 = QLabel("后",self)
        self.nameLabel1.move(1478, 800)
        self.nameLabel1.resize(35,35)
        self.nameLabel1.setStyleSheet("QLabel {font-family: '宋体'; font-size:35px; color: white; opacity: 0;}")
        
        self.nameLabel2 = QLabel("左",self)
        self.nameLabel2.move(1335, 665) 
        self.nameLabel2.resize(35,35)
        self.nameLabel2.setStyleSheet("QLabel {font-family: '宋体'; font-size:35px; color: white; opacity: 0;}")
        
        self.nameLabel3 = QLabel("右",self)
        self.nameLabel3.move(1620, 665) 
        self.nameLabel3.resize(35,35)
        self.nameLabel3.setStyleSheet("QLabel {font-family: '宋体'; font-size:35px; color: white; opacity: 0;}")
        

        self.myLabel = QLabel("100",self)
        self.myLabel.move(170,350)
        self.myLabel.resize(150,50)
        self.myLabel.setStyleSheet("QLabel {font-family: '宋体'; font-size: 50px; color: white; opacity: 0;}")
        self.myLabel3 = QLabel("X=",self)
        self.myLabel3.setStyleSheet("QLabel {font-family: '宋体'; font-size: 50px; color: white; opacity: 0;}")
        self.myLabel3.move(100,350)
        self.myLabel3.resize(50,50)
        
        self.myLabel2 = QLabel("990",self)
        self.myLabel2.move(170,450)
        self.myLabel2.resize(150,50)
        self.myLabel2.setStyleSheet("QLabel {font-family: '宋体'; font-size: 50px; color: white; opacity: 0;}")
        self.myLabel4 = QLabel("Y=",self)
        self.myLabel4.setStyleSheet("QLabel {font-family: '宋体'; font-size: 50px; color: white; opacity: 0;}")
        self.myLabel4.move(100,450)
        self.myLabel4.resize(50,50)
        

        self.myLabel6 = QLabel("角度",self)
        self.myLabel6.setStyleSheet("QLabel {font-family: '宋体'; font-size: 50px; color: white; opacity: 0;}")
        self.myLabel6.move(100,550)
        self.myLabel6.resize(150,50)
        self.myLabel7 = QLabel("145",self)
        self.myLabel7.setStyleSheet("QLabel {font-family: '宋体'; font-size: 50px; color: white; opacity: 0;}")
        self.myLabel7.move(250,550)
        self.myLabel7.resize(150,50)
        
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setGeometry(350, 350, 710, 360)
        self.custom_label = mylable(self.scroll_area)
        self.custom_label.set_background_image("map.png")  #导入地图图片
        self.map_width = pixmap.width()
        self.map_height = pixmap.height()
        self.custom_label.setGeometry(350,350,self.map_width,self.map_height)
        self.custom_label.Sizeof(self.map_width,self.map_height)

        self.scroll_area.setWidget(self.custom_label)
        self.scroll_area.setWidgetResizable(False)

        self.mybutton10 = QPushButton("清除", self)
        self.mybutton10.move(120,630)
        self.mybutton10.resize(150,50)
        self.mybutton10.setFont(self.font)
        self.mybutton10.setStyleSheet("QPushButton{font-family:'宋体';font-size:50px;color:white;}"
                             "QPushButton{background-color:blue;border:2px groove blue;border-radius:10px;padding:2px 4px;}"
                             "QPushButton:hover{background-color:blue;border:2px groove white;border-radius:10px;padding:2px 4px;}")
        self.mybutton10.clicked.connect(self.custom_label.clearLines) 

        #添加指针
        self.N_needle = RotatingNeedle(self)
        self.N_needle.setGeometry(97,700, 400, 400)

        self.N_needle1 = RotatingNeedle(self)
        self.N_needle1.setGeometry(407,700, 400, 400)

        self.N_needle2 = RotatingNeedle(self)
        self.N_needle2.setGeometry(710,700, 400, 400)

        #显示x,y,z
        self.myLabel9 = QLabel("0",self)
        self.myLabel9.setStyleSheet("QLabel {font-family: '宋体'; font-size: 20px; color: white; opacity: 0;}")
        self.myLabel9.move(290,950)
        self.myLabel9.resize(50,20)

        self.myLabel11 = QLabel("0",self)
        self.myLabel11.setStyleSheet("QLabel {font-family: '宋体'; font-size: 20px; color: white; opacity: 0;}")
        self.myLabel11.move(600,950)
        self.myLabel11.resize(50,20)

        self.myLabel13 = QLabel("0",self)
        self.myLabel13.setStyleSheet("QLabel {font-family: '宋体'; font-size: 20px; color: white; opacity: 0;}")
        self.myLabel13.move(900,950)
        self.myLabel13.resize(50,20)

        self.myLabel15 = QLabel("实时状态",self)
        self.myLabel15.setStyleSheet("QLabel {font-family: '宋体'; font-size: 50px; color: white; opacity: 0;}")
        self.myLabel15.move(600 ,250 )
        self.myLabel15.resize(200,50)

        self.myLabel16 = QLabel("控制按钮",self)
        self.myLabel16.setStyleSheet("QLabel {font-family: '宋体'; font-size: 50px; color: white; opacity: 0;}")
        self.myLabel16.move(1400,250)
        self.myLabel16.resize(200,50)

    #接收ip地址，端口号发起连接请求
    @pyqtSlot()
    def call_service_clicked(self):
        host_address = QHostAddress(self.t)
        port = int(self.n)
        print(host_address, port)
        self.tcp_socket.connectToHost(host_address, port)

    #连接成功激发的槽函数
    @pyqtSlot()
    def send_data(self):
        self.send_times = 0
        self.flag_tcp = True
        QMessageBox.about(self,'提示','连接成功！')
    
    #连接失败激发的槽函数
    @pyqtSlot()
    def get_error(self):
        self.flag_tcp = False
        QMessageBox.warning(self, "错误", self.tcp_socket.errorString(), QMessageBox.Ok)

    #按纽发送速度信号
    @pyqtSlot(str)  #确保发送的是str
    def tool_button_clicked(self, data: str):
        if self.flag_tcp:
            self.send_times += 1
        else:
            self.send_times = 0
        self.speed = 6000
        self.speed2 = 4000
        forword = "aicy 0029 6000 5000 aiyc"
        back = "aicy 0029 4000 5000 aiyc"
        right = "aicy 0029 5000 4000 aiyc"
        if data is forword:
            self.flag_speed = 1
        elif data is back :
            self.flag_speed = 2
        elif data is right:
            self.flag_speed = 3
        else :
            self.flag_speed = 4
        self.tcp_socket.write(data.encode())

    #接收数据
    @pyqtSlot()
    def receive_data(self):
        # 接收服务端发送的数据 
        data = self.tcp_socket.readAll()
        string = data.data().decode()
        print(data)
        try:
            my_list = string.split() 
            a = (int(my_list[2]) - 5000) / 10
            b = (int(my_list[3]) - 5000) / 10
            c = int(my_list[4])
            d = int(my_list[5])/1000
            e = int(my_list[6])
            f = int(my_list[7])
            self.myLabel.setNum(a)
            self.myLabel2.setNum(b)
            self.myLabel7.setNum(c)
            self.myLabel9.setNum(d)
            self.myLabel11.setNum(e)         
            self.myLabel13.setNum(f)


            pose_x = int(a) + self.custom_label.mouse_point_change_x
            pose_y = (self.map_height - int(b)) + self.custom_label.mouse_point_change_y
            print(pose_x,pose_y)
            self.custom_label.receiveCoordinates(pose_x,pose_y)
            self.custom_label.L_move(pose_x, pose_y)
            self.custom_label.L_rotate(-c-90)

            self.N_needle.update_angle(int(2.825*d)-113)
            self.N_needle1.update_angle(int(0.2825*e)-113) 
            self.N_needle2.update_angle(int(2.825*f)-113)
        except Exception as e:
            print(e)

    #转换窗口
    def switch2(self):
        print("退出")
        self.tcp_socket.close()
        self.switch_to_main.emit()
    

class Controller():

    def __init__(self):
        pass

    def show_login(self):
        self.login = Login_Window()       
        self.login.switch_window.connect(self.show_main) #接收槽函数信息，并绑定相应的方法
        self.login.show()

    #槽函数信号，激发执行方法。
    def show_main(self,text,number): 
        self.window = MyWidget(text,number)
        self.window.call_service_clicked()
        self.window.switch_to_main.connect(self.show_window_two)
        self.login.close()
        self.window.show()

    def show_window_two(self):
        self.window.close()
        self.login = Login_Window()
        self.login.show()       
        self.login.switch_window.connect(self.show_main)
        self.login.show()
    
app = QApplication(sys.argv)
controller = Controller()
controller.show_login() 
sys.exit(app.exec_())


       