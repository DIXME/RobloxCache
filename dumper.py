import sys
from traceback import extract_stack
from PySide6.QtWidgets import QApplication, QWidget, QGridLayout, QListWidget, QPushButton, QLabel, QHBoxLayout, QVBoxLayout
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt  # <-- needed for AlignmentFlag
from patcher import init, cache_files, exatract, find, write, dumpAll, view, dump
from PIL import Image
import os
from enums import SigText, broad
from get import get

class CacheManagerWidget(QWidget):
    def init_(self):
        global cache_files
        self.list_images.clear()
        self.list_sounds.clear()
        self.list_others.clear()
        cache_files.clear()
        init()
        for file in cache_files:
            match broad[file.type]:
                case "image":
                    self.list_images.addItem(f'[{file.type.value}] ' + file.hash)
                case "sound":
                    self.list_sounds.addItem(f'[{file.type.value}] ' + file.hash)
                case _:
                    self.list_others.addItem(f'[{file.type.value}] ' + file.hash)
    
    def __init__(self):
        global cache_files
        super().__init__()

        # Font for the whole widget
        manager_font = QFont("Small Fonts", 10)
        self.setFont(manager_font)

        # Header label
        self.header_label = QLabel("Roblox Cache Manager")
        self.header_label.setFont(manager_font)
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # List widgets
        self.list_sounds = QListWidget()
        self.list_images = QListWidget()
        self.list_others = QListWidget()

        

        # Labels for lists
        self.label_sounds = QLabel("Sounds")
        self.label_images = QLabel("Images & KTX")
        self.label_others = QLabel("Others")
        for lbl in [self.label_sounds, self.label_images, self.label_others]:
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setFont(manager_font)

        # Buttons
        dump_button = QPushButton("Dump")
        self.redownload_button = QPushButton("Refetch")

        # --- NEW VIEW BUTTON ---
        self.view_button = QPushButton("View")
        self.view_button.clicked.connect(self.on_view_clicked)

        # --- NEW RE-FETCH BUTTON ---
        self.refetch_button = QPushButton("ReloadFiles")
        self.refetch_button.clicked.connect(self.on_refetch_clicked)

        dump_all_button = QPushButton("Dump All")

        # Layout
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.header_label)

        grid_layout = QGridLayout()
        grid_layout.addWidget(self.label_sounds, 0, 0)
        grid_layout.addWidget(self.label_images, 0, 1)
        grid_layout.addWidget(self.label_others, 0, 2)

        grid_layout.addWidget(self.list_sounds, 1, 0)
        grid_layout.addWidget(self.list_images, 1, 1)
        grid_layout.addWidget(self.list_others, 1, 2)

        main_layout.addLayout(grid_layout)

        # Buttons row
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(dump_button)

        # --- PUT VIEW BUTTON HERE ---
        buttons_layout.addWidget(self.view_button)

        # --- PUT RE-FETCH BUTTON HERE ---
        buttons_layout.addWidget(self.refetch_button)
        buttons_layout.addWidget(self.redownload_button)

        buttons_layout.addWidget(dump_all_button)
        main_layout.addLayout(buttons_layout)

        # Connect buttons
        dump_button.clicked.connect(self.on_dump)
        dump_all_button.clicked.connect(self.on_dump_all)
        self.redownload_button.clicked.connect(self.redownload)

        self.recent = ""

        self.list_images.itemClicked.connect(self.imageSelect)
        self.list_sounds.itemClicked.connect(self.soundSelect)
        self.list_others.itemClicked.connect(self.otherSelect)

        self.init_()

    def redownload(self):
        get()

    def on_refetch_clicked(self):
        self.init_()
    
    def imageSelect(self):
        self.recent = "image"
    
    def soundSelect(self):
        self.recent = "sound"
    
    def otherSelect(self):
        self.recent = "other"
    
    def removeType(self,label):
        return label[label.find(']')+2:]

    def on_dump(self):
        selected_items = [
            lst.currentItem().text()
            for lst in [self.list_sounds, self.list_images, self.list_others]
            if lst.currentItem() is not None
        ]
        match self.recent:
            case "image":
                item = selected_items[1]
            case "sound":
                item = selected_items[0]  
            case "other":
                item = selected_items[2]  
        
        hash = self.removeType(item)
        file = find(hash)
        dump(file)
        

    def on_dump_all(self):
        # fs
        # one folder called dumps that will have three folders
        # images, sounds, others
        # file names will be {[Foldername]Filename} Filename being the hash from roblox
        dumpAll()
            

    # --- VIEW BUTTON CALLBACK ---
    def on_view_clicked(self):
        selected_items = [
            lst.currentItem().text()
            for lst in [self.list_sounds, self.list_images, self.list_others]
            if lst.currentItem() is not None
        ]

        match self.recent:
            case "image":
                item = selected_items[1]
            case "sound":
                item = selected_items[0]  
            case "other":
                item = selected_items[2]  
        
        hash = self.removeType(item)
        file = find(hash)
        view(file)
                

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CacheManagerWidget()
    window.setWindowTitle("Roblox Cache Manager")
    window.resize(700, 400)
    window.show()
    sys.exit(app.exec())
