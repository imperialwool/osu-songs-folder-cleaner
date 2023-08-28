# █ █▀▄▀█ █▀█ █▀█ █▀█ ▀█▀
# █ █░▀░█ █▀▀ █▄█ █▀▄ ░█░
import os
import sys
import shutil
import urllib3
import platform
import webbrowser
from PyQt6 import QtCore, QtGui, QtWidgets, uic
# DONT FORGET TO CHANGE THIS VAR U STOOPIT TOASTER
BUILD_VERSION = 11


# █░░ █▀█ █▀▀   █░█░█ █ █▄░█ █▀▄ █▀█ █░█░█
# █▄▄ █▄█ █▄█   ▀▄▀▄▀ █ █░▀█ █▄▀ █▄█ ▀▄▀▄▀
class LogWindow(QtWidgets.QMainWindow):
    # initing window
    def __init__(self, logs: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("ui/logs.ui", self)
        self.setWindowIcon(QtGui.QIcon('o!sfc.ico'))
        self.logs.setPlainText(logs)
        self.close_button.clicked.connect(self.close)



# █░█░█ █ █▄░█ █▀▄ █▀█ █░█░█
# ▀▄▀▄▀ █ █░▀█ █▄▀ █▄█ ▀▄▀▄▀
class MainWindow(QtWidgets.QMainWindow):
    # initin window
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # load ui
        uic.loadUi("ui/main.ui", self)
        self.setWindowIcon(QtGui.QIcon('o!sfc.ico'))
        self.start_clean_button.setEnabled(False)

        # trying to guess where is osu
        defaultOsuPath = "C:/Users/{}/AppData/Local/osu!".format(os.getlogin()) if platform.system() == "Windows" else ("/Applications/osu!.app/Contents/Resources/drive_c/osu!" if platform.system() == "Darwin" else "")
        if os.path.exists(defaultOsuPath) and os.path.exists(defaultOsuPath+"/Songs"):
            self.path_to_songs_folder.text = defaultOsuPath
        
        # givin events to needed things
        self.scan_folder.clicked.connect(self.scan_songs_folder)
        self.start_clean_button.clicked.connect(self.clean_proceed)
        self.update_available.mousePressEvent = self.open_github_repo

        # actions :) 
        self.toolbar.addAction(self.bake_action(self, "how to", self.howto_popup))
        self.toolbar.addAction(self.bake_action(self, "about", self.about_popup))

        # check version
        http = urllib3.PoolManager()
        version = http.request("GET", "https://raw.githubusercontent.com/imperialwool/osu-songs-folder-cleaner/main/VERSION").data.decode('utf-8')
        if not version.isnumeric() or (version.isnumeric() and int(version) < BUILD_VERSION):
            self.update_available.setText("ඞ SUS ඞ")
        elif version.isnumeric() and int(version) == BUILD_VERSION: pass
        else:
            self.update_available.setText("new update available!")

    # additional stuff n' functions
    @staticmethod
    def path_invalid(path: str) -> bool:
        return path.strip() in [None, ""] or not os.path.exists(path) or not os.path.exists(path+"/Songs")
    @staticmethod
    def multiEndsWith(text, folder) -> bool:
        return any(item.lower().endswith(text) for item in folder)
    @staticmethod
    def doubleEndsWith(lst, folder) -> bool:
        return any(MainWindow.multiEndsWith(item.lower(), folder) for item in lst)
    
    # checkin for files
    def find_osu(self, beatmapFiles) -> bool:
        return self.multiEndsWith(".osu", beatmapFiles)
    def find_mp3(self, beatmapFiles) -> bool:
        # REFACTOR TO READ .OSU AND FIND AUDIO THAT WROTE IN .OSU
        return self.doubleEndsWith(['.mp3', '.ogg'], beatmapFiles)
    def find_images(self, beatmapFiles) -> bool:
        return self.doubleEndsWith(['.jpg', '.jpeg', '.png'], beatmapFiles)
    def song_folder_verification(self, dir_files):
        bmf, af, bg = self.find_osu(dir_files), self.find_mp3(dir_files), self.find_images(dir_files)
        if (
            self.audio_file_check.isChecked() and not af 
            or
            self.beatmap_files_check.isChecked() and not bmf 
            or
            self.bg_images_check.isChecked() and not bg
        ):
            return True, str(bmf), str(af), str(bg) 
        else:
            return False, str(bmf), str(af), str(bg)

    # force choicing path
    def choice_path(self) -> None:
        while True:
            path = QtWidgets.QFileDialog.getExistingDirectory(
                None,
                'Select a folder:'
            )
            if not self.path_invalid(path):
                self.path_to_songs_folder.setText(path)
                break

    # bake helpers
    @staticmethod 
    def bake_action(window, name: str, function = None):
        action = QtGui.QAction(name, window)
        action.triggered.connect(function)
        return action
    @staticmethod
    def bake_table_cell(name: str, checkboxed: bool = False, checked: bool = False):
        item = QtWidgets.QTableWidgetItem(name)
        item.setText(name)
        if checkboxed:
            item.setFlags(QtCore.Qt.ItemFlag.ItemIsUserCheckable | QtCore.Qt.ItemFlag.ItemIsEnabled)
            item.setCheckState(QtCore.Qt.CheckState.Checked if checked else QtCore.Qt.CheckState.Unchecked)
        return item

    # howto popup
    def howto_popup(self):
        dlg = QtWidgets.QMessageBox(self)
        dlg.setWindowTitle("How to use this")
        dlg.setText("1. Find game's root folder and paste it into input field (you can skip it, but window will pop up to find ur game's folder).\n2. Click \"scan songs folder!\" to start scanning.\n3. The table will be filled with maps, checked one will be deleted (you can uncheck them if you want).\n4. Click on \"clean useless stuff!\" to clean songs folder.\n5. Wait.\n6. Done!\n\nAlso you can select checks that you need.")
        dlg.exec()
    
    # about popup
    def about_popup(self):
        dlg = QtWidgets.QMessageBox(self)
        dlg.setWindowTitle("About")
        dlg.setText("osu! Songs Folder Cleaner\n\ncode by imperialwool (toaster61)\nused python3.11, pyqt6\ngithub repo: https://github.com/imperialwool/osu-songs-folder-cleaner\nfeel free to suggest new ideas!\n\nt61.link")
        dlg.setIcon(QtWidgets.QMessageBox.Icon.Information)
        dlg.exec()

    # label event that on click opens github repo
    def open_github_repo(self, *args):
        webbrowser.open('https://github.com/imperialwool/osu-songs-folder-cleaner')
        return

    # scan songs folder
    # returns result into table
    def scan_songs_folder(self) -> None:
        # why user should touch smth when processing?
        self.main_party.setEnabled(False)

        # path check
        path = self.path_to_songs_folder.text()
        if self.path_invalid(path):
            self.choice_path()
            path = self.path_to_songs_folder.text()

        # getting folders
        with os.scandir(path+"/Songs") as it:
            dirs = [entry.name for entry in it if entry.is_dir()]

        if self.only_delpending_maps.isChecked():
            newDirs = []
            for dir in dirs:
                dir_files = os.listdir(path+"/Songs/"+dir)
                should_be_removed, beatmap_file, mp3, bg = self.song_folder_verification(dir_files)
                if should_be_removed: newDirs.append(dir)
            dirs = newDirs

        # clean table
        self.songs_list.clearContents()

        # making table
        headers = ["Folder name", "Beatmap files", "Background images", "Beatmap music"]
        self.songs_list.setHorizontalHeaderLabels(headers)
        self.songs_list.horizontalHeader().setVisible(True)
        self.songs_list.setRowCount(len(dirs))
        for number, dir_name in enumerate(dirs, 0):
            item = QtWidgets.QTableWidgetItem(dir_name)
            item.setText(dir_name)
            item.setFlags(QtCore.Qt.ItemFlag.ItemIsUserCheckable | QtCore.Qt.ItemFlag.ItemIsEnabled)
            item.setCheckState(QtCore.Qt.CheckState.Unchecked)
    
            if not self.only_delpending_maps.isChecked():
                dir_files = os.listdir(path+"/Songs/"+dir_name)
                should_be_removed, beatmap_file, mp3, bg = self.song_folder_verification(dir_files)
                self.songs_list.setItem(number, 0, self.bake_table_cell(dir_name, True, should_be_removed))
                self.songs_list.setItem(number, 1, self.bake_table_cell(beatmap_file))
                self.songs_list.setItem(number, 2, self.bake_table_cell(bg))
                self.songs_list.setItem(number, 3, self.bake_table_cell(mp3))
            else:
                dir_files = os.listdir(path+"/Songs/"+dir_name)
                self.songs_list.setItem(number, 0, self.bake_table_cell(dir_name, True, True))
                self.songs_list.setItem(number, 1, self.bake_table_cell(str(self.find_osu(dir_files))))
                self.songs_list.setItem(number, 2, self.bake_table_cell(str(self.find_images(dir_files))))
                self.songs_list.setItem(number, 3, self.bake_table_cell(str(self.find_mp3(dir_files))))

        self.main_party.setEnabled(True)
        self.start_clean_button.setEnabled(True)

    def clean_proceed(self):
        logs = str()
        path = self.path_to_songs_folder.text()
        for i in range(self.songs_list.rowCount()):
            item = self.songs_list.item(i, 0)
            if item.checkState() == QtCore.Qt.CheckState.Checked:
                try:
                    shutil.rmtree(path+"/Songs/"+item.text())
                    logs += "[V] {} deleted successfully!\r\n".format(item.text())
                except Exception as e:
                    logs += "[X] {} NOT deleted!! -> {}\r\n".format(item.text(), str(e).replace("\n", " | "))
            elif not self.only_important_logs.isChecked():
                logs += "[ ] {} skipped.\r\n".format(item.text())
        global logwin
        logwin = LogWindow(logs=logs)
        logwin.show()




# █▀█ █░█ █▄░█   ▄▀█ █▀█ █▀█
# █▀▄ █▄█ █░▀█   █▀█ █▀▀ █▀▀
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()