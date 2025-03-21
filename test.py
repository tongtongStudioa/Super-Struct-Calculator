# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 00:10:30 2024

@author: La famille tong
"""

import sys
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
import matplotlib
matplotlib.use('Qt5Agg')  # Ajoute cette ligne avant d'importer matplotlib.pyplot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialisation de la fenêtre principale
        self.setWindowTitle('PyQt5 avec Matplotlib')
        self.setGeometry(100, 100, 800, 600)

        # Création d'un widget central pour la fenêtre
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Layout principal
        layout = QVBoxLayout(central_widget)

        # Création d'une figure Matplotlib
        self.figure = plt.figure(figsize=(5, 4))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Dessin d'un graphique simple
        self.plot_graph()

    def plot_graph(self):
        # Créer un graphique
        ax = self.figure.add_subplot(111)
        ax.plot([1, 2, 3, 4], [1, 4, 9, 16], label="y = x^2")
        ax.set_title("Graphique Simple")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.legend()

        # Rafraîchir le canvas pour afficher le graphique
        self.canvas.draw()

# Fonction principale pour lancer l'application
def main():
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
