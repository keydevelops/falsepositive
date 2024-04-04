try:
    import minecraft_launcher_lib as mcll
    import subprocess

    from uuid import uuid1
    from random_username.generate import generate_username
    from PyQt5 import QtCore, QtGui, QtWidgets

    class LaunchTread(QtCore.QThread):
        launch_setup_signal = QtCore.pyqtSignal(str, str)
        progress_update_signal = QtCore.pyqtSignal(int, int)
        state_update_signal = QtCore.pyqtSignal(bool)

        version_id = ''
        username = ''
        mcdir = mcll.utils.get_minecraft_directory()

        progress = 0
        progress_max = 0

        def __init__(self):
            super().__init__()

            self.launch_setup_signal.connect(self.launch_setup)

        def launch_setup(self, version_id, username):
            self.version_id = version_id
            self.username = username

        def update_progress_label(self, value):
            self.progress_label = value
            self.progress_update_signal.emit(self.progress, self.progress_max)

        def update_progress(self, value):
            self.progress = value
            self.progress_update_signal.emit(self.progress, self.progress_max)


        def update_progress_max(self, value):
            self.progress_max = value
            self.progress_update_signal.emit(self.progress, self.progress_max)


        def run(self):
            self.state_update_signal.emit(True)

            version = self.version_id
            username = self.username

            callback = {
                'setStatus': self.update_progress_label,
                'setProgress': self.update_progress,
                'setMax': self.update_progress_max,
            }

            mcll.install.install_minecraft_version(versionid=version, minecraft_directory=self.mcdir, callback=callback)
            
            if not username:
                username = generate_username()[0]
                    
            options = {
                'username': username,
                'uuid': str(uuid1()),
                'token': ''
            }

            minecraftcmd = mcll.command.get_minecraft_command(version=version, minecraft_directory=self.mcdir, options=options)
            subprocess.call(minecraftcmd, shell=True)

            self.state_update_signal.emit(False)


    class Ui_MainWindow(object):
        def setupUi(self, MainWindow):
            MainWindow.setObjectName("MainWindow")
            MainWindow.resize(309, 326)
            MainWindow.setWindowTitle('FalsePositive')
            self.centralwidget = QtWidgets.QWidget(MainWindow)
            self.centralwidget.setObjectName("centralwidget")
            self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
            self.horizontalLayout.setObjectName("horizontalLayout")
            self.verticalLayout = QtWidgets.QVBoxLayout()
            self.verticalLayout.setObjectName("verticalLayout")
            self.launchername = QtWidgets.QLabel(self.centralwidget)
            font = QtGui.QFont()
            font.setPointSize(24)
            self.launchername.setFont(font)
            self.launchername.setText('FalsePositive')
            self.verticalLayout.addWidget(self.launchername, 0, QtCore.Qt.AlignHCenter)
            self.launcherversion = QtWidgets.QLabel(self.centralwidget)
            font = QtGui.QFont()
            font.setPointSize(10)
            self.launcherversion.setFont(font)
            self.launcherversion.setObjectName("launcherversion")
            self.launcherversion.setText('PRE-Alpha 0.0.1')
            self.verticalLayout.addWidget(self.launcherversion, 0, QtCore.Qt.AlignHCenter)
            spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
            self.verticalLayout.addItem(spacerItem)
            self.username = QtWidgets.QLineEdit(self.centralwidget)
            self.username.setObjectName("username")
            self.username.setPlaceholderText('Username')
            self.verticalLayout.addWidget(self.username)
            self.versions = QtWidgets.QComboBox(self.centralwidget)
            self.versions.setObjectName("versions")
            try:
                for version in mcll.utils.get_version_list():
                    self.versions.addItem(version['id'])
            except Exception as e:
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setText("Unable to get versions of minecraft")
                msg.setWindowTitle("Launcher error")
                sys.exit(msg.exec_())

            self.verticalLayout.addWidget(self.versions)
            spacerItem1 = QtWidgets.QSpacerItem(20, 30, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
            self.verticalLayout.addItem(spacerItem1)
            self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
            self.progressBar.setEnabled(True)
            self.progressBar.setVisible(False)
            self.progressBar.setProperty("value", 24)
            self.progressBar.setObjectName("progressBar")
            self.verticalLayout.addWidget(self.progressBar)
            self.runminecraft = QtWidgets.QPushButton(self.centralwidget)
            self.runminecraft.setObjectName("runminecraft")
            self.runminecraft.clicked.connect(self.launchgame)
            self.runminecraft.setText('Play')

            self.launch_thread = LaunchTread()
            self.launch_thread.state_update_signal.connect(self.state_update)
            self.launch_thread.progress_update_signal.connect(self.update_progress)

            self.verticalLayout.addWidget(self.runminecraft)
            self.horizontalLayout.addLayout(self.verticalLayout)
            MainWindow.setCentralWidget(self.centralwidget)

            QtCore.QMetaObject.connectSlotsByName(MainWindow)

        def launchgame(self):
            self.launch_thread.launch_setup_signal.emit(self.versions.currentText(), self.username.text())
            self.launch_thread.start()

        def update_progress(self, progress, maxProgress):
            self.progressBar.setValue(progress)
            self.progressBar.setMaximum(maxProgress)

        def state_update(self, value):
            self.runminecraft.setDisabled(value)
            self.progressBar.setVisible(value)

    if __name__ == "__main__":
        import sys
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)
        MainWindow.show()
        app.exec_()
        #sys.exit(app.exec_())
    else:
        import sys
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText("Cannot start launcher")
        msg.setWindowTitle("Protection")
        sys.exit(msg.exec_()) 
except Exception as e:
    try:
        import sys
        from PyQt5 import QtCore, QtGui, QtWidgets 
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText("An unknown error occurred")
        msg.setWindowTitle("Launcher error")
        sys.exit(msg.exec_())
    except Exception as e:
        print('No PyQt5 module installed')
        
