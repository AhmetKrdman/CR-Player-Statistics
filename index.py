import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
import PyQt5.QtCore
import PyQt5.QtGui
from bs4 import BeautifulSoup
import requests

def search(self):
    _translate = QtCore.QCoreApplication.translate
    if (self.NameInput.text() == ""):
        noName = QtWidgets.QMessageBox()
        noName.setWindowTitle("Error")
        noName.setIcon(QtWidgets.QMessageBox.Warning)
        noName.setText("Please enter a player name!")
        noName.exec_()
    else:
        url = "https://www.craftrise.com.tr/oyuncu/" + self.NameInput.text()
        response = requests.get(url,headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36 Edg/86.0.622.58',}).text.encode("utf-8")
        soup = BeautifulSoup(response, 'html.parser')

        playerName = soup.select_one(".profileHeader-name")
        if (playerName == "" or playerName == None):
            noPlayer = QtWidgets.QMessageBox()
            noPlayer.setWindowTitle("Error")
            noPlayer.setIcon(QtWidgets.QMessageBox.Warning)
            noPlayer.setText("The entered player was not found!")
            noPlayer.exec_()
        else:
            playerRanks = soup.select(".rankButton p")
            playerStatusDiv = str(soup.find_all("div", {"class": "rankButton socialMedia"}))
            playerStatus = ""
            if (playerStatusDiv.find("ÇEVRİMDIŞI") != -1):
                playerStatus = "Offline"
            else:
                playerStatus = "Online"
            self.treeWidget.topLevelItem(0).setText(0, _translate("MainWindow", str(playerStatus)))
            self.treeWidget.topLevelItem(0).setText(1, _translate("MainWindow", str(playerRanks[0]).replace('<p class="rainbow rainbow_text_animated">', '').replace('<p>', '').replace('</p>', '')))
            gameStats(self)


def gameStats(self):
    _translate = QtCore.QCoreApplication.translate
    if (self.NameInput.text() == ""):
        return
    else:
        url = "https://www.craftrise.com.tr/oyuncu/" + self.NameInput.text()
        response = requests.get(url,headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36 Edg/86.0.622.58',}).text.encode("utf-8")
        soup = BeautifulSoup(response, 'html.parser')
        playerName = soup.select_one(".profileHeader-name")
        if (playerName == "" or playerName == None):
            return
        else:
            gameStatistic = soup.select(".riseStats p")
            self.label_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">" + str(self.GameSelection.currentText()) + " Statistics</p></body></html>"))
            self.GameStatistic.topLevelItem(0).setText(0, _translate("MainWindow", str(gameStatistic[self.GameSelection.currentIndex()]).replace('<p style="text-align:center; font-family: \'Mikado-Medium\'; margin-top: -40px;">', '').split(',')[0].replace('puan', '') + " Point"))
            self.GameStatistic.topLevelItem(0).setText(1, _translate("MainWindow", str(gameStatistic[self.GameSelection.currentIndex()]).replace('<p style="text-align:center; font-family: \'Mikado-Medium\'; margin-top: -40px;">', '').split(',')[1].replace('kazanma', '').replace('</p>', '') + " Win"))

def resetAll(self):
    _translate = QtCore.QCoreApplication.translate
    self.treeWidget.topLevelItem(0).setText(0, _translate("MainWindow", "..."))
    self.treeWidget.topLevelItem(0).setText(1, _translate("MainWindow", "..."))
    self.GameStatistic.topLevelItem(0).setText(0, _translate("MainWindow", "0 Point"))
    self.GameStatistic.topLevelItem(0).setText(1, _translate("MainWindow", "0 Win"))
    self.NameInput.setText("")


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(540, 274)
        MainWindow.setMinimumSize(QtCore.QSize(540, 274))
        MainWindow.setMaximumSize(QtCore.QSize(540, 274))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.SearchGroup = QtWidgets.QGroupBox(self.centralwidget)
        self.SearchGroup.setGeometry(QtCore.QRect(20, 20, 241, 101))
        self.SearchGroup.setFlat(False)
        self.SearchGroup.setCheckable(False)
        self.SearchGroup.setChecked(False)
        self.SearchGroup.setObjectName("SearchGroup")
        self.NameInput = QtWidgets.QLineEdit(self.SearchGroup)
        self.NameInput.setGeometry(QtCore.QRect(10, 60, 121, 31))
        self.NameInput.setText("")
        self.NameInput.setObjectName("NameInput")
        self.ResetButton = QtWidgets.QPushButton(self.SearchGroup)
        self.ResetButton.setGeometry(QtCore.QRect(150, 60, 81, 31))
        self.ResetButton.clicked.connect(lambda: resetAll(self))
        self.ResetButton.setObjectName("ResetButton")
        self.SearchButton = QtWidgets.QPushButton(self.SearchGroup)
        self.SearchButton.setGeometry(QtCore.QRect(150, 20, 81, 31))
        self.SearchButton.setFlat(False)
        self.SearchButton.clicked.connect(lambda: search(self))
        self.SearchButton.setObjectName("SearchButton")
        self.PlayerNameLabel = QtWidgets.QLabel(self.SearchGroup)
        self.PlayerNameLabel.setGeometry(QtCore.QRect(10, 30, 121, 21))
        self.PlayerNameLabel.setObjectName("PlayerNameLabel")
        self.GeneralGroup = QtWidgets.QGroupBox(self.centralwidget)
        self.GeneralGroup.setGeometry(QtCore.QRect(20, 130, 241, 131))
        self.GeneralGroup.setObjectName("GeneralGroup")
        self.treeWidget = QtWidgets.QTreeWidget(self.GeneralGroup)
        self.treeWidget.setGeometry(QtCore.QRect(10, 30, 222, 91))
        self.treeWidget.setStyleSheet("background: transparent")
        self.treeWidget.setObjectName("treeWidget")
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        self.GameGroup = QtWidgets.QGroupBox(self.centralwidget)
        self.GameGroup.setGeometry(QtCore.QRect(280, 20, 241, 241))
        self.GameGroup.setObjectName("GameGroup")
        self.GameSelection = QtWidgets.QComboBox(self.GameGroup)
        self.GameSelection.setGeometry(QtCore.QRect(120, 30, 101, 22))
        self.GameSelection.currentIndexChanged.connect(lambda: gameStats(self))
        self.GameSelection.setObjectName("GameSelection")
        self.GameSelection.addItem("")
        self.GameSelection.addItem("")
        self.GameSelection.addItem("")
        self.GameSelection.addItem("")
        self.GameSelection.addItem("")
        self.GameSelection.addItem("")
        self.GameSelection.addItem("")
        self.GameSelection.addItem("")
        self.GameSelection.addItem("")
        self.GameSelection.addItem("")
        self.GameSelection.addItem("")
        self.GameSelection.addItem("")
        self.GameSelection.addItem("")
        self.GameSelection.addItem("")
        self.GameSelection.addItem("")
        self.GameSelection.addItem("")
        self.GameSelection.addItem("")
        self.label = QtWidgets.QLabel(self.GameGroup)
        self.label.setGeometry(QtCore.QRect(10, 30, 101, 21))
        self.label.setObjectName("label")
        self.GameStatistic = QtWidgets.QTreeWidget(self.GameGroup)
        self.GameStatistic.setGeometry(QtCore.QRect(10, 140, 222, 91))
        self.GameStatistic.setStyleSheet("background: transparent")
        self.GameStatistic.setObjectName("GameStatistic")
        item_0 = QtWidgets.QTreeWidgetItem(self.GameStatistic)
        self.label_2 = QtWidgets.QLabel(self.GameGroup)
        self.label_2.setGeometry(QtCore.QRect(10, 80, 221, 60))
        self.label_2.setObjectName("label_2")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "CraftRise Player Stats"))
        self.SearchGroup.setTitle(_translate("MainWindow", "Player Search"))
        self.NameInput.setToolTip(_translate("MainWindow", "<html><head/><body><p><br/></p></body></html>"))
        self.NameInput.setPlaceholderText(_translate("MainWindow", "Enter Player Name"))
        self.ResetButton.setText(_translate("MainWindow", "Reset"))
        self.SearchButton.setText(_translate("MainWindow", "Search"))
        self.PlayerNameLabel.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:9pt;\">Player Name :</span></p></body></html>"))
        self.GeneralGroup.setTitle(_translate("MainWindow", "General Information"))
        self.treeWidget.headerItem().setText(0, _translate("MainWindow", "Status"))
        self.treeWidget.headerItem().setText(1, _translate("MainWindow", "Rank"))
        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        self.treeWidget.topLevelItem(0).setText(0, _translate("MainWindow", "..."))
        self.treeWidget.topLevelItem(0).setText(1, _translate("MainWindow", "..."))
        self.treeWidget.topLevelItem(0).setText(2, _translate("MainWindow", "..."))
        self.treeWidget.setSortingEnabled(__sortingEnabled)
        self.GameGroup.setTitle(_translate("MainWindow", "Game Stats"))
        self.GameSelection.setItemText(0, _translate("MainWindow", "Bomb Lobbers"))
        self.GameSelection.setItemText(1, _translate("MainWindow", "Sky Wars"))
        self.GameSelection.setItemText(2, _translate("MainWindow", "Katil Kim"))
        self.GameSelection.setItemText(3, _translate("MainWindow", "The Bridge"))
        self.GameSelection.setItemText(4, _translate("MainWindow", "Build Battle"))
        self.GameSelection.setItemText(5, _translate("MainWindow", "UHC Meetup"))
        self.GameSelection.setItemText(6, _translate("MainWindow", "Speed Builders"))
        self.GameSelection.setItemText(7, _translate("MainWindow", "Egg Wars"))
        self.GameSelection.setItemText(8, _translate("MainWindow", "Tnt Run"))
        self.GameSelection.setItemText(9, _translate("MainWindow", "Dragon Escape"))
        self.GameSelection.setItemText(10, _translate("MainWindow", "Bed Wars"))
        self.GameSelection.setItemText(11, _translate("MainWindow", "Survival Games"))
        self.GameSelection.setItemText(12, _translate("MainWindow", "UHC Run"))
        self.GameSelection.setItemText(13, _translate("MainWindow", "Turf Wars"))
        self.GameSelection.setItemText(14, _translate("MainWindow", "Arena PvP"))
        self.GameSelection.setItemText(15, _translate("MainWindow", "Herobrine Chamber"))
        self.GameSelection.setItemText(16, _translate("MainWindow", "OITC"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:9pt;\">Select Game</span></p></body></html>"))
        self.GameStatistic.headerItem().setText(0, _translate("MainWindow", "Point"))
        self.GameStatistic.headerItem().setText(1, _translate("MainWindow", "Win"))
        __sortingEnabled = self.GameStatistic.isSortingEnabled()
        self.GameStatistic.setSortingEnabled(False)
        self.GameStatistic.topLevelItem(0).setText(0, _translate("MainWindow", "0 Point"))
        self.GameStatistic.topLevelItem(0).setText(1, _translate("MainWindow", "0 Win"))
        self.GameStatistic.setSortingEnabled(__sortingEnabled)
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">The Bridge Statistics</p></body></html>"))

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon("./logo.ico"))
    MainWindow = QtWidgets.QWidget()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
