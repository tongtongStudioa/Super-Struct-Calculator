# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 18:44:22 2024

@author: La famille tong
"""

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QMessageBox, QTabWidget
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt

from shear_force_calculation import ShearCalculator
from steel_section_calculation import ArmatureCalculator
class MainApp(QTabWidget):
    def __init__(self):
        super().__init__()

        # Configuration de la fenêtre principale
        self.setWindowTitle("Application de Calcul Structuré")
        self.setMinimumSize(900, 900)  # Taille minimale de la fenêtre
        
        # Ajouter les calculateurs comme onglets
        self.addTab(ArmatureCalculator(), "Calcul Section Armatures")
        self.addTab(ShearCalculator(), "Calcul Cisaillement")
        self.addTab(MomentCalculator(), "Moment Quadratique")
        
        # Appliquer un thème professionnel
        self.apply_theme()

    def apply_theme(self):
        app.setStyle("Fusion")
        
        # Personnalisation de la palette
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        #palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        
        app.setPalette(palette)

class MomentCalculator(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Calcul Moment Quadratique"))
        # Ajoute ici les widgets spécifiques
        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Appliquer le style Fusion et personnaliser la palette
    window = MainApp()
    window.show()
    
    sys.exit(app.exec_())

