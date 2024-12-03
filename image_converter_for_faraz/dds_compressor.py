from PIL import Image
from PySide6.QtWidgets import *
import sys, os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DDS Compressor"), self.setGeometry(100, 100, 400, 200)
        container = QWidget()
        layout = QVBoxLayout(container)
        self.label = QLabel("Select a DDS file to compress")
        layout.addWidget(self.label)
        layout.addWidget(QPushButton("Select File", clicked=lambda: self.process_file()))
        self.setCentralWidget(container)
        
    def process_file(self):
        if path := QFileDialog.getOpenFileName(self, "Select DDS", "", "DDS Files (*.dds)")[0]:
            Image.open(path).save(f"{os.path.splitext(path)[0]}_compressed.dds", format='DDS', dds_format='BC1')
            self.label.setText(f"Compressed: {path}")

if __name__ == "__main__": app = QApplication(sys.argv); MainWindow().show(); sys.exit(app.exec())