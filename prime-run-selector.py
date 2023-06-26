import csv
import subprocess
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSettings, QCoreApplication
from gi.repository import Gio
import PyQt5.QtGui as QtGui
import os

all_apps = []
search_res = []
current_dir = os.getcwd()


class Ui_MainWindow(object):
    def __init__(self):
        self.get_all_apps()
        self.save = all_apps
        self.state = False
        call = Ui_Dialog_add_exe_file()
        Ui_Dialog_add_exe_file.load_files(call)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(500, 490)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        MainWindow.setFont(font)
        MainWindow.setIconSize(QtCore.QSize(22, 22))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.buttonBox = QtWidgets.QDialogButtonBox(self.centralwidget)
        self.buttonBox.setGeometry(QtCore.QRect(310, 410, 174, 34))
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.accepted.connect(self.start_app)
        self.buttonBox.rejected.connect(self.exit_app)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.searchbar = QtWidgets.QLineEdit(self.centralwidget)
        self.searchbar.returnPressed.connect(self.search_list)
        self.searchbar.setGeometry(QtCore.QRect(10, 20, 301, 32))
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(320, 20, 81, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.search_list)
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(410, 20, 81, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.reset)
        self.pushButton_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(10, 60, 481, 341))
        self.listWidget.setObjectName("listWidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 500, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuSetting = QtWidgets.QMenu(self.menubar)
        self.menuSetting.setObjectName("menuSetting")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionAdd_Executable_File = QtWidgets.QAction(MainWindow)
        self.actionAdd_Executable_File.triggered.connect(self.add_file_window)
        self.actionAdd_Executable_File.setObjectName("actionAdd_Executable_File")
        self.actionMode = QtWidgets.QAction(MainWindow)
        self.actionMode.setObjectName("actionMode")
        self.actionMode.triggered.connect(self.run_mode_dialog)
        self.actionAbout_Prime_Selector = QtWidgets.QAction(MainWindow)
        self.actionAbout_Prime_Selector.triggered.connect(self.run_help_dialog)
        self.actionAbout_Prime_Selector.setObjectName("actionAbout_Prime_Selector")
        self.menuFile.addAction(self.actionAdd_Executable_File)
        self.menuSetting.addAction(self.actionMode)
        self.menuHelp.addAction(self.actionAbout_Prime_Selector)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSetting.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.settings = QSettings("prime_run_selector", QCoreApplication.organizationName())
        self.gpu_mode = self.settings.setValue('gpu_mode', self.settings.value('gpu_mode'))

        self.retranslateUi(MainWindow)
        self.appUi(all_apps)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Prime Run Selector"))
        MainWindow.setWindowIcon(QtGui.QIcon('{}/icon/icon.png'.format(os.path.dirname(__file__))))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.pushButton.setText(_translate("MainWindow", "Search"))
        self.pushButton_2.setText(_translate("MainWindow", "reset"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuSetting.setTitle(_translate("MainWindow", "Setting"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionAdd_Executable_File.setText(_translate("MainWindow", "Add Executable File"))
        self.actionMode.setText(_translate("MainWindow", "Mode..."))
        self.actionAbout_Prime_Selector.setText(_translate("MainWindow", "About Prime Selector"))

    def appUi(self, selected_list):
        _translate = QtCore.QCoreApplication.translate
        loop = -1
        for app in selected_list:
            item = QtWidgets.QListWidgetItem()
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(QtGui.QIcon.fromTheme(app['icon']).pixmap(64, 64)))
            item.setIcon(icon)
            self.listWidget.addItem(item)
            loop = loop + 1
            item = self.listWidget.item(loop)
            item.setText(_translate("MainWindow", app['name']))

    def get_all_apps(self):
        apps = Gio.AppInfo.get_all()
        app_names = list()
        for app in apps:
            icon = app.get_icon()
            if icon:
                name = app.get_display_name()
                app_names.append(name)
                item = {'name': name, 'icon': icon.to_string(), 'command': app.get_commandline()}
                all_apps.append(item)

    def selected_app(self):
        if self.state is False:
            return all_apps[self.listWidget.currentRow()]['command']
        else:
            return search_res[self.listWidget.currentRow()]['command']

    def start_app(self):
        selected = self.selected_app()
        if self.settings.value('gpu_mode') == 'true':
            subprocess.Popen(['prime-run', *selected.split(' ')], stdout=sys.stdout, stderr=sys.stdout, stdin=sys.stdout)
        else:
            subprocess.Popen([*selected.split(' ')], stdout=sys.stdout, stderr=sys.stdout, stdin=sys.stdout)

    def exit_app(self):
        sys.exit(app.exec_())

    def search_list(self):
        search = self.searchbar.text().lower()
        search_res.clear()
        for app in self.save:
            if search.__len__() >= 2:
                if search in app['name'].lower():
                    search_res.append(app)
                    self.listWidget.clear()
                    self.listWidget.repaint()
                    self.appUi(search_res)
                    self.state = True

    def reset(self):
        self.state = False
        self.listWidget.clear()
        self.appUi(all_apps)

    def add_file_window(self):
        dialog = QtWidgets.QDialog()
        dialog.ui = Ui_Dialog_add_exe_file()
        dialog.ui.setupUi(dialog)
        dialog.exec_()
        dialog.show()

    def run_help_dialog(self):
        dialog = QtWidgets.QDialog()
        dialog.ui = Ui_Dialog_help()
        dialog.ui.setupUi(dialog)
        dialog.exec_()
        dialog.show()

    def run_mode_dialog(self):
        dialog = QtWidgets.QDialog()
        dialog.ui = Ui_Dialog_mode()
        dialog.ui.setupUi(dialog)
        dialog.exec_()
        dialog.show()


class Ui_Dialog_add_exe_file(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setFixedSize(400, 306)
        self.addFileButton = QtWidgets.QPushButton(Dialog)
        self.addFileButton.setGeometry(QtCore.QRect(20, 30, 151, 31))
        self.addFileButton.setObjectName("addFileButton")
        self.addFileButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.addFileButton.clicked.connect(self.add_file)
        self.filesList = QtWidgets.QListWidget(Dialog)
        self.filesList.setGeometry(QtCore.QRect(20, 90, 361, 161))
        self.filesList.setObjectName("filesList")
        self.dialog_label = QtWidgets.QLabel(Dialog)
        self.dialog_label.setGeometry(QtCore.QRect(20, 70, 221, 18))
        self.dialog_label.setObjectName("dialog_label")
        self.removeFileButton = QtWidgets.QPushButton(Dialog)
        self.removeFileButton.setGeometry(QtCore.QRect(290, 260, 88, 31))
        self.removeFileButton.setObjectName("removeFileButton")
        self.removeFileButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.removeFileButton.clicked.connect(self.remove_file)

        self.retranslateUi(Dialog)
        self.file_manager()
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Add File"))
        self.addFileButton.setText(_translate("Dialog", "Add Executable File"))
        __sortingEnabled = self.filesList.isSortingEnabled()
        self.filesList.setSortingEnabled(False)

        self.filesList.setSortingEnabled(__sortingEnabled)
        self.dialog_label.setText(_translate("Dialog", "Current executable files:"))
        self.removeFileButton.setText(_translate("Dialog", "Remove"))

    def file_manager(self):
        _translate = QtCore.QCoreApplication.translate
        loop = -1
        with open('{}/executable_files.csv'.format(os.path.dirname(__file__)), 'r') as f:
            data = csv.reader(f)
            for app in data:
                item = QtWidgets.QListWidgetItem()
                item.setCheckState(QtCore.Qt.Unchecked)
                self.filesList.addItem(item)
                loop = loop + 1
                item = self.filesList.item(loop)
                item.setText(_translate("Dialog", app[0]))

    def add_file(self):
        file = QtWidgets.QFileDialog.getOpenFileName(QtWidgets.QDialog(), 'Hey! Select a File')
        if not file[0] == "":
            with open('{}/executable_files.csv'.format(os.path.dirname(__file__)), 'a') as f:
                data = csv.DictWriter(f, fieldnames=['path'])
                data.writerow({'path': file[0]})
            self.repaint_list()
        self.load_files()
        ui.reset()

    def remove_file(self):
        remove_list = list()
        for item in range(0, self.filesList.count()):
            state = self.filesList.item(item).checkState()
            if state == 2:
                remove_list.append(item)

        with open('{}/executable_files.csv'.format(os.path.dirname(__file__)), 'r') as f:
            data = csv.reader(f)
            rows = list(data)
            new_rows = [row for index, row in enumerate(rows) if index not in remove_list]

        with open('{}/executable_files.csv'.format(os.path.dirname(__file__)), 'w', newline='') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerows(new_rows)
        self.repaint_list()

    def load_files(self):
        with open('{}/executable_files.csv'.format(os.path.dirname(__file__)), 'r') as f:
            data = csv.reader(f)
            for file in data:
                item = {'name': file[0], 'icon': 'configurator', 'command': file[0]}
                if item not in all_apps:
                    all_apps.append(item)

    def repaint_list(self):
        self.filesList.clear()
        self.file_manager()


class Ui_Dialog_help(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setEnabled(True)
        Dialog.setFixedSize(400, 300)
        Dialog.setAcceptDrops(False)
        Dialog.setAccessibleName("")
        Dialog.setAutoFillBackground(False)
        Dialog.setSizeGripEnabled(False)
        Dialog.setModal(False)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 20, 191, 21))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.textEdit = QtWidgets.QTextEdit(Dialog)
        self.textEdit.setGeometry(QtCore.QRect(20, 50, 361, 221))
        font = QtGui.QFont()
        font.setUnderline(False)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.textEdit.setFont(font)
        self.textEdit.setAutoFillBackground(False)
        self.textEdit.setStyleSheet("background-color: #121212; border: 0px;")
        self.textEdit.setTabChangesFocus(False)
        self.textEdit.setUndoRedoEnabled(True)
        self.textEdit.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.textEdit.setReadOnly(True)
        self.textEdit.setOverwriteMode(False)
        self.textEdit.setObjectName("textEdit")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Help"))
        self.label.setText(_translate("Dialog", "Prime Run Selector"))
        self.textEdit.setHtml(_translate("Dialog",
                                         "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                         "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                         "p, li { white-space: pre-wrap; }\n"
                                         "</style></head><body style=\" font-family:\'Noto Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">When you want to use your laptop\'s dedicated graphics, </p>\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">you may have to use the Prime Run command over and </p>\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">over again, and this may be a bit difficult.</p>\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Prime Run selector is here, in addition to running the </p>\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">programs installed on the system, has the ability to run </p>\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">your chosen executable files to save your time.</p>\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">To add an executable file to File &gt; Add Executable File</p>\n"
                                         "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#0000ff;\">Github: daninouai</span></p>\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#0000ff;\">Website: danirahimi.ir</span></p></body></html>"))


class Ui_Dialog_mode(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setFixedSize(302, 124)
        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.setGeometry(QtCore.QRect(120, 20, 81, 31))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 20, 91, 31))
        self.label.setObjectName("label")
        self.textEdit = QtWidgets.QTextEdit(Dialog)
        self.textEdit.setGeometry(QtCore.QRect(20, 60, 261, 51))
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setStyleSheet("background-color: #121212; border: 0px;")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(210, 20, 71, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.change_mode)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        if ui.settings.value('gpu_mode') == 'true':
            self.comboBox.setItemText(0, _translate("Dialog", "dGPU"))
            self.comboBox.setItemText(1, _translate("Dialog", "iGPU"))
        else:
            self.comboBox.setItemText(0, _translate("Dialog", "iGPU"))
            self.comboBox.setItemText(1, _translate("Dialog", "dGPU"))
        self.label.setText(_translate("Dialog", "App run mode:"))
        self.textEdit.setHtml(_translate("Dialog",
                                         "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                         "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                         "p, li { white-space: pre-wrap; }\n"
                                         "</style></head><body style=\" font-family:\'Noto Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">dGPU : discrete gpu to best perfomance.</p>\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">iGPU : integerated gpu to save power.</p></body></html>"))
        self.pushButton.setText(_translate("Dialog", "OK"))
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

    def change_mode(self):
        _translate = QtCore.QCoreApplication.translate
        mode = self.comboBox.currentText()
        if mode == 'iGPU':
            ui.settings.setValue('gpu_mode', 'false')
        else:
            ui.settings.setValue('gpu_mode', 'true')



if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
