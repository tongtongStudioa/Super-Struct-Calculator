# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 10:21:05 2024

@author: axel
"""
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFormLayout, QComboBox, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from steel_section.beams_def import RectangularBeam, TéBeam

PROFILE_RECT = "Rectangulaire"
PROFILE_T = "Profilé en T"

# Classe principale pour l'application
class ArmatureCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Définir le titre et la taille minimale de la fenêtre
        self.setWindowTitle("Calcul Section Acier pour Poutre Béton")

        # Styles pour l'interface professionnelle
        self.setStyleSheet("""
            QWidget {
                background-color: #f4f4f4;
            }
            QLabel {
                color: #2E4053;
                font-size: 16px;
            }
            QLineEdit {
                padding: 10px;
                border: 1px solid #2E4053;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #2E86C1;
                color: white;
                border-radius: 4px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2874A6;
            }
            QComboBox {
                background-color: #f0f0f0;
                color: #333;
                border-radius: 5px;
                padding: 5px;
                min-width: 120px;
            }
            QFrame {
                border: 1px solid #2E4053;
                padding: 20px;
                border-radius: 8px;
            }
        """)

        # Explication des hypothèses
        hypothese_label = QLabel("""
        Ce programme calcule la section d'armature longitudinale nécessaire pour une poutre en béton armé.
        Les hypothèses de calcul sont basées sur l'Eurocode 2 :
        - fyk : Limite élastique de l'acier, typiquement 500 MPa.
        - Section rectangulaire ou en Té.
        - Coefficients de sécurité appliqués selon les charges (ELS et ELU).
        """)
        hypothese_label.setWordWrap(True)
        hypothese_label.setAlignment(Qt.AlignLeft)
        hypothese_label.setFont(QFont('Arial', 12))

        
        
        # Formulaire pour les entrées utilisateur
        self.form_layout = QFormLayout()

        # Ajout des champs au formulaire
        
        # Menu déroulant pour choisir le profil de la poutre
        self.profile_combobox = QComboBox(self)
        self.profile_combobox.addItems([PROFILE_RECT, PROFILE_T])
        self.profile_type = self.profile_combobox.currentText()
        self.profile_combobox.currentIndexChanged.connect(self.update_form_visibility)
        self.form_layout.addRow(self.profile_combobox)
        
        self.entry_mg = QLineEdit()
        self.entry_mg.setText("70")
        self.form_layout.addRow(QLabel("Mg (kNm) :"), self.entry_mg)

        self.entry_mq = QLineEdit()
        self.entry_mq.setText("130")
        self.form_layout.addRow(QLabel("Mq (kNm) :"), self.entry_mq)

        self.entry_fck = QLineEdit()
        self.entry_fck.setText("30")
        self.form_layout.addRow(QLabel("Résistance béton (MPa) :"), self.entry_fck)

        self.entry_cmin = QLineEdit()
        self.entry_cmin.setText("30")
        self.form_layout.addRow(QLabel("Cmin (mm) :"), self.entry_cmin)

        self.entry_hauteur = QLineEdit()
        self.entry_hauteur.setText("500")
        self.form_layout.addRow(QLabel("Hauteur de la poutre (mm) :"), self.entry_hauteur)

        self.entry_largeur = QLineEdit()
        self.entry_largeur.setText("300")
        self.form_layout.addRow(QLabel("Largeur (bw en mm) :"), self.entry_largeur)

        self.entry_beff = QLineEdit()
        self.entry_beff.setText("600")
        self.form_layout.addRow(QLabel("beff (mm) :"), self.entry_beff)

        self.entry_heff = QLineEdit()
        self.entry_heff.setText("100")
        self.form_layout.addRow(QLabel("heff (mm) :"), self.entry_heff)

        # Bouton pour calculer la section d'acier
        calculate_button = QPushButton("Calculer la section d'acier", self)
        calculate_button.clicked.connect(self.calculer_section_acier)

        # Affichage des résultats
        self.result_label = QLabel("Section d'acier nécessaire : ")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setWordWrap(True)
        self.result_label.setFont(QFont('Arial', 18))

        # Mise en page principale
        main_layout = QHBoxLayout()
        part1_layout = QVBoxLayout()
        part1_layout.addWidget(hypothese_label)
        part1_layout.addWidget(self.profile_combobox)
        part1_layout.addLayout(self.form_layout)
        part2_layout = QVBoxLayout()
        part2_layout.addWidget(calculate_button)
        part2_layout.addWidget(self.result_label)
        main_layout.addLayout(part1_layout)
        main_layout.addLayout(part2_layout)
        self.setLayout(main_layout)
        
        # Mise à jour initiale pour masquer les champs spécifiques aux poutres en Té
        self.update_form_visibility()

    def update_form_visibility(self):
        is_t_beam = self.profile_combobox.currentText() == PROFILE_T
        self.entry_beff.setVisible(is_t_beam)
        self.entry_heff.setVisible(is_t_beam)
        
    # Fonction de calcul de la section d'acier
    def calculer_section_acier(self):
        try:
            # Récupérer les entrées utilisateur
            f_ck = int(self.entry_fck.text())  # Résistance caractéristique du béton en MPa
            f_yk = 500  # Résistance caractéristique de l'acier en MPa

            
            M_q = float(self.entry_mq.text())   # en kN/m
            M_g = float(self.entry_mg.text()) # en kN/m
            c_min = int(self.entry_cmin.text())  # en mm
            c_nom = c_min + 10
            h = float(self.entry_hauteur.text()) / 1000  # hauteur poutre en m
            bw = float(self.entry_largeur.text()) / 1000  # largeur poutre en m

            if self.profile_combobox.currentText() == PROFILE_RECT :
                beam = RectangularBeam(h, bw, c_nom, f_ck, f_yk)
            else:
                beff = float(self.entry_beff.text()) / 1000
                heff = float(self.entry_heff.text()) / 1000
                beam = TéBeam(h,bw,c_nom,f_ck,f_yk,beff,heff)

            # Calcul spécifique à la poutre sélectionnée
            result = beam.section_armature_longitudinale_ELU(M_g, M_q)
            self.result_label.setText(result)
            
        except ValueError:
            QMessageBox.critical(self, "Erreur", "Veuillez entrer des valeurs numériques valides.")

# Lancer l'application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ArmatureCalculator()
    window.show()
    sys.exit(app.exec_())

