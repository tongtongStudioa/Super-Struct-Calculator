# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 09:28:00 2024

@author: axel
"""

import sys
from PyQt5.QtWidgets import (
    QApplication, QCheckBox, QWidget, QComboBox, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QMessageBox, QScrollArea
    )
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


PROFILE_H = "Profilé en H" 
PROFILE_RECT = "Rectangulaire"
PROFILE_T = "Profilé en T"
 
# Classe principale pour l'application
class ShearCalculator(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Définir le titre et la taille minimale de la fenêtre
        self.setWindowTitle("Calcul contrainte de cisaillement")

        # Styles pour l'interface professionnelle
        self.setStyleSheet("""
            QWidget {
                background-color: #f4f4f4;
            }
            QLabel {
                color: #2E4053;
                font-size: 16px;
                word-wrap: break-word;
            }
            QLineEdit {
                padding: 10px;
                border: 1px solid #2E4053;
                border-radius: 4px;
                font-size: 14px;
                max-width: 100px;  /* Largeur maximale */
                word-wrap: break-word;
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
            QFrame {
                border: 1px solid #2E4053;
                padding: 20px;
                border-radius: 8px;
            }
            QComboBox {
                background-color: #f0f0f0;
                color: #333;
                border-radius: 5px;
                padding: 5px;
                min-width: 120px;
            }
            QComboBox::down-arrow {
                width: 12px;
                height: 12px;
            }
            QComboBox QAbstractItemView {
                background-color: #ffffff;
                selection-background-color: #2874A6;
                selection-color: #ffffff;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 5px;
                }
        """)

        # Explication des hypothèses
        hypothese_label = QLabel("""
        Ce programme calcule les efforts tranchants dans une section. 
        Hypothèses : 
            - h et b de même ordre de grandeurs. (Calculs non valables avec profilés minces)
        """)
        
        hypothese_label.setWordWrap(True)
        hypothese_label.setAlignment(Qt.AlignLeft)
        hypothese_label.setFont(QFont('Arial', 12))


        # Menu déroulant pour choisir le profil de la poutre
        self.profile_combobox = QComboBox(self)
        self.profile_combobox.addItems([PROFILE_RECT, PROFILE_H, PROFILE_T])
        self.profile_type = self.profile_combobox.currentText()


        
        # Disposition des champs d'entrée et des labels
        input_frame = QFrame(self)
        # Ajout des champs d'entrée pour les paramètres de calcul
        I_label = QLabel("Moment quadratique (mm4):")
        I_label.setFixedWidth(250)
        self.entry_quadratic_moment = QLineEdit(self)
        
        # Case à cocher pour calculer automatiquement le moment quadratique
        self.auto_moment_checkbox = QCheckBox("Calculer le moment quadratique automatiquement", self)
        self.auto_moment_checkbox.stateChanged.connect(self.toggle_moment_input)
        self.auto_moment_checkbox.setChecked(True)

        charge_label = QLabel("Effort tranchant (kN):")
        charge_label.setFixedWidth(200) # Limite de largeur
        self.entry_charge = QLineEdit(self)
        self.entry_charge.setText("35")

        portee_label = QLabel("Portée (m):")
        portee_label.setFixedWidth(170)
        self.entry_portee = QLineEdit(self)
        self.entry_portee.setText("10")

        stiffness_center_label = QLabel("Centre de rigidité sur la haueur (mm)")
        stiffness_center_label.setFixedWidth(330)
        self.entry_stiffness_center = QLineEdit(self)
        
        self.auto_stiffness_center_checkbox = QCheckBox("Calculer le centre de rigidité automatiquement", self)
        self.auto_stiffness_center_checkbox.stateChanged.connect(self.toggle_stiffness_center_input)
        self.auto_stiffness_center_checkbox.setChecked(True)
        
        """ hauteur_label = QLabel("Hauteur de la poutre (mm):")
        hauteur_label.setFixedWidth(210)
        self.entry_hauteur = QLineEdit(self)
        self.entry_hauteur.setText("600")

        largeur_label = QLabel("Largeur de la poutre (mm):")
        largeur_label.setFixedWidth(210)
        self.entry_largeur = QLineEdit(self)
        self.entry_largeur.setText("250")"""

        # Organisation horizontale des labels et des champs de saisie
        input_layout2 = QHBoxLayout()
        input_layout2.addWidget(charge_label)
        input_layout2.addWidget(self.entry_charge)

        input_layout3 = QHBoxLayout()
        input_layout3.addWidget(portee_label)
        input_layout3.addWidget(self.entry_portee)

        input_layout1 = QHBoxLayout()
        input_layout1.addWidget(I_label)
        input_layout1.addWidget(self.entry_quadratic_moment)

        input_layout4 = QHBoxLayout()
        input_layout4.addWidget(stiffness_center_label)
        input_layout4.addWidget(self.entry_stiffness_center)

        # Champs d'entrée pour les dimensions, changent en fonction du profilé
        self.input_forms_frame = QFrame(self)
        self.createProfileInputs()
        
        # Ajouter la connexion avec l'adaptateur de vue une fois la valeur "input_forms_frame" créé
        self.profile_combobox.currentIndexChanged.connect(self.updateLayout)
        
        combo_layout = QHBoxLayout()
        combo_box_label = QLabel("Sélectionnez le profil :")
        combo_layout.addWidget(combo_box_label)
        combo_layout.addWidget(self.profile_combobox)
        
        """input_layout5 = QHBoxLayout()
        input_layout5.addWidget(hauteur_label)
        input_layout5.addWidget(self.entry_hauteur)

        input_layout6 = QHBoxLayout()
        input_layout6.addWidget(largeur_label)
        input_layout6.addWidget(self.entry_largeur)"""


        # Ajout des entrées dans le frame
        vbox_input = QVBoxLayout()
        vbox_input.addLayout(input_layout2)
        vbox_input.addLayout(input_layout3)
        
        vbox_input.addLayout(input_layout1)
        vbox_input.addWidget(self.auto_moment_checkbox)
        vbox_input.addLayout(input_layout4)
        vbox_input.addWidget(self.auto_stiffness_center_checkbox)
        vbox_input.addWidget(self.input_forms_frame)
        #vbox_input.addLayout(input_layout5)
        #vbox_input.addLayout(input_layout6)
        
        input_frame.setLayout(vbox_input)
        # Ajouter input_frame dans un QScrollArea
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(input_frame)

        # Créer un widget de graphique avec matplotlib
        self.canvas = FigureCanvas(plt.Figure(figsize=(9, 6)))

        # Bouton pour calculer la section d'acier
        calculate_button = QPushButton("Calculer la contrainte de cisaillement", self)
        calculate_button.clicked.connect(self.calculs_cisaillement_points_critiques)

        # Affichage des résultats
        self.result_label = QLabel("Résultat de la contrainte de cisaillement")
        self.result_label.setFixedWidth(500)
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setWordWrap(True)
        self.result_label.setFont(QFont('Arial', 18))

        # Mise en page principale
        main_layout = QVBoxLayout()
        main_layout.addWidget(hypothese_label)
        main_layout.addLayout(combo_layout)
        intermediate_layout = QHBoxLayout()
        # Ajouter la scroll_area à la main_layout
        intermediate_layout.addWidget(self.scroll_area)
        #intermediate_layout.addWidget(input_frame)
        intermediate_layout.addWidget(self.canvas)
        main_layout.addLayout(intermediate_layout)
        main_layout.addWidget(calculate_button, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.result_label, alignment=Qt.AlignCenter)
        
        self.setLayout(main_layout)
    
    def createProfileInputs(self):
        """Crée les champs d'entrée pour les dimensions en fonction du profilé."""
       
        self.clearLayout(self.input_forms_frame.layout())
        if self.input_forms_frame.layout() is  None:
            layout = QVBoxLayout()
            self.input_forms_frame.setLayout(layout)
        
        # Dimensions pour un profilé rectangulaire
        if self.profile_type == PROFILE_RECT :
            self.entry_hauteur = self.createInputField("Hauteur (mm):", 600)
            self.entry_largeur = self.createInputField("Largeur (mm)", 250)
        
        # Dimensions pour un profilé en H
        elif self.profile_type == PROFILE_H :
            self.entry_hauteur = self.createInputField("Hauteur totale (mm):", 600)
            self.entry_largeur = self.createInputField("Largeur totale (mm):", 250)
            self.entry_hauteur_ame = self.createInputField("Hauteur de l'âme (mm)", 500)
            self.entry_epaisseur_ame = self.createInputField("Épaisseur de l'âme (mm):", 50)
            self.entry_largeur_ailes = self.createInputField("Largeur des ailes (mm)", 250)
            self.entry_epaisseur_ailes = self.createInputField("Épaisseur des ailes (mm):", 50)
        
        # Dimensions pour un profilé en T
        elif self.profile_type == PROFILE_T :
           self.entry_hauteur = self.createInputField("Hauteur totale (mm):", 600)
           self.entry_largeur = self.createInputField("Largeur totale (mm):", 250)
           self.entry_hauteur_ame = self.createInputField("Hauteur de l'âme (mm):", 500)
           self.entry_epaisseur_ame = self.createInputField("Épaisseur de l'âme (mm):", 50)
           self.entry_largeur_ailes = self.createInputField("Largeur des ailes (mm):", 250)
           self.entry_epaisseur_ailes = self.createInputField("Épaisseur des ailes (mm):", 50)

        self.input_forms_frame.update()
        
    def createInputField(self, label_text, default_value):
        """Crée un champ d'entrée avec un label et l'ajoute à la mise en page."""
        hbox = QHBoxLayout()
        label = QLabel(label_text)
        line_edit = QLineEdit(self)
        line_edit.setText(f"{default_value}")

        hbox.addWidget(label)
        hbox.addWidget(line_edit)
        self.input_forms_frame.layout().addLayout(hbox)
        return line_edit

    def clearLayout(self, layout):
        """Efface tous les widgets d'une mise en page."""
        if layout is not None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

    def updateLayout(self):
        """Met à jour les champs d'entrée lorsque le profilé change."""
        self.profile_type = self.profile_combobox.currentText()
        self.createProfileInputs()
        self.scroll_area.update()
        self.update()
        
    # Activer/désactiver la saisie du moment quadratique selon la case à cocher
    def toggle_moment_input(self, state):
        if state == Qt.Checked:
            self.entry_quadratic_moment.setDisabled(True)
        else:
            self.entry_quadratic_moment.setDisabled(False)
    # Activer/désactiver la saisie du centre de rigidité selon la case à cocher
    def toggle_stiffness_center_input(self, state):
        if state == Qt.Checked:
            self.entry_stiffness_center.setDisabled(True)
        else:
            self.entry_stiffness_center.setDisabled(False)
               
    # Fonction de calcul de la section d'acier
    def calculs_cisaillement_points_critiques(self):
        try:
            h = 0
            b = 0
            h_ame = 0
            b_ame = 0
            h_aile = 0
            b_aile = 0
            
            # Récupérer les entrées utilisateur
            if self.profile_type == PROFILE_RECT:
                h = float(self.entry_hauteur.text()) / 1000  # hauteur poutre en m
                b = float(self.entry_largeur.text()) / 1000 # largeur poutre en m
        
            elif self.profile_type == PROFILE_H:
                h = float(self.entry_hauteur.text()) / 1000
                b = float(self.entry_largeur.text()) / 1000
                h_ame = float(self.entry_hauteur_ame.text()) / 1000
                b_ame = float(self.entry_epaisseur_ame.text()) / 1000
                b_aile = float(self.entry_largeur_ailes.text()) / 1000
                h_aile = float(self.entry_epaisseur_ailes.text()) / 1000
    
            elif self.profile_type == PROFILE_T:
                h = float(self.entry_hauteur.text()) / 1000
                b = float(self.entry_largeur.text()) / 1000
                h_ame = float(self.entry_hauteur_ame.text()) / 1000
                b_ame = float(self.entry_epaisseur_ame.text()) / 1000
                b_aile = float(self.entry_largeur_ailes.text()) / 1000
                h_aile = float(self.entry_epaisseur_ailes.text()) / 1000                
                
            # Calcul de l'effort tranchant
            q = float(self.entry_charge.text()) * 1000 # charge linéaire en N/m
            longueur = float(self.entry_portee.text())  # en m
            V = q*longueur/2 # Effort tranchant en N aux points critiques sur la poutre (aux appuis)
            
            # Calcul du centre de rigidité 
            if self.auto_stiffness_center_checkbox.isChecked():
                y_g = self.calcul_Y_g(h,b,h_ame,b_ame,h_aile,b_aile)  # Centre d'inertie en mm
                self.entry_stiffness_center.setText(f"{y_g * 1000:.2f}")
            else:
                y_g = int(self.entry_stiffness_center.text())  # position y du centre de rigidité en mm
                y_g = y_g / 1000  # Convertir en m^4
                
            # Calcul du moment quadratique
            if self.auto_moment_checkbox.isChecked():
                I_z = self.calcul_I_z(y_g,h,b,h_ame,b_ame,h_aile,b_aile) # Calcul du moment quadratique (m^4)
                self.entry_quadratic_moment.setText(f"{I_z*10**12:.0f}")
            else:
                I_z = float(self.entry_quadratic_moment.text())  # Moment quadratique en mm4
                I_z = I_z * 10**-12  # Convertir en m^4
        
                
            y, tau = self.distribution_cisaillement(V, I_z, y_g, h,b,h_ame,b_ame,h_aile,b_aile)
            self.display_graph(y, tau)
            #t_max = self.calcul_cisaillement(V,I_z,b,b,h/2-y_g,h/2)
            #self.result_label.setText(f"Contrainte de cisaillement max Txy = {t_max:.2f} MPa")
        except ValueError:
            QMessageBox.critical(self, "Erreur", "Veuillez entrer des valeurs numériques valides.")
    
    def calcul_Y_g(self,h,b,h_ame,b_ame,h_aile,b_aile):
        if self.profile_type == PROFILE_RECT:
            return h/2 
        elif self.profile_type == PROFILE_H:
            return (h_ame * b_ame * (h_ame/2 + h_aile)+ h_aile * b_aile * (h_aile / 2 + h_aile/2 + h_aile + h_ame)) / (h_ame * b_ame + h_aile * b_aile *2)
        elif self.profile_type == PROFILE_T:
            return (h_ame * b_ame * h_ame/2 + h_aile * b_aile * (h_aile/2 + h_ame)) / (h_ame * b_ame + h_aile * b_aile )
        
    def calcul_I_z(self,y_g,h,b,h_ame,b_ame,h_aile,b_aile):
        """Calcul de moment quadratique pour une differents types de section (rectangulaire, type H et T)"""
        if self.profile_type == PROFILE_RECT:
            return self.I_z_rect(h,b)
        elif self.profile_type == PROFILE_H:
            return (self.I_z_rect(h_aile,b_aile) + b_aile * h_aile * (h_aile - y_g)**2)*2 + self.I_z_rect(h_ame,b_ame) + h_ame * b_ame * (h_ame /2 - y_g)**2     
        elif self.profile_type == PROFILE_T:
            return self.I_z_rect(h_aile,b_aile) + b_aile * h_aile * (h_aile - y_g)**2 + self.I_z_rect(h_ame,b_ame) + h_ame * b_ame * (h_ame /2 - y_g)**2
        
    def I_z_rect(self,h,b):
        """Calcul de moment quadratique pour une section rectangulaire"""
        return b*h**3/12
    
    def calculer_cisaillement(self,V,I_z,b_u,b_y,y0,ymax ):
        """Calcul cisaillement considérant que la largeur b ne change pas sur un dy donnée"""
        integral = b_y * (ymax**2/2-y0**2/2)
        if I_z == 0 or b_y == 0:
            QMessageBox.critical(self, "Erreur", "Veuillez entrer des valeurs numériques valides : I_z ne peut pas être égal à 0 et b non plus")
            return None
        return -V/(I_z*b_u)*integral / 10**6 # contrainte de cisaillement en MPa
            
    def distribution_cisaillement(self,V, I_z, y_g, h,b,h_ame,b_ame,h_aile,b_aile):
        # Calcul de la contrainte de cisaillement à différentes hauteurs
        y_vals = np.linspace(h/2, -h/2, 1000)  # Discrétisation de la hauteur
        cisaillements_tau = np.zeros_like(y_vals)
        if self.profile_type == PROFILE_T:
            for i, y in enumerate(y_vals):
                if y > h/2 - h_aile:
                    cisaillements_tau[i] = self.calculer_cisaillement(V,I_z,b_aile,b_aile,y,h/2)
                else:
                    cisaillements_tau[i] = self.calculer_cisaillement(V,I_z,b_ame,b_aile,y,h/2)
        elif self.profile_type == PROFILE_RECT:
            cisaillements_tau = [self.calculer_cisaillement(V,I_z,b,b,y,h/2) for y in y_vals]
        elif self.profile_type == PROFILE_H:
            for i, y in enumerate(y_vals):
                if y > h/2 - h_aile or y < -h/2 + h_aile:
                    cisaillements_tau[i] = self.calculer_cisaillement(V,I_z,b_aile,b_aile,y,h/2)
                else:
                    cisaillements_tau[i] = self.calculer_cisaillement(V,I_z,b_ame,b_aile,y,h/2)
        return (y_vals, cisaillements_tau)
    
        """def distribution_cisaillement(self,y,V,I_z,b_u,b_y,y_max):
        "Distribution du cisaillement pour une largeur constante."
        tau = np.zeros_like(y)
        
        for i, y_val in enumerate(y):
            # Cisaillement dans l'âme
            tau[i] = self.calcul_cisaillement(V,I_z,b_u,b_y,y_val,y_max)
                
        return tau"""
    
        # Tracé du graphique
        """plt.figure(figsize=(8, 6))
        plt.plot(tau, y, label='Contrainte de cisaillement')
        plt.axhline(0, color='gray', linewidth=0.5)
        plt.xlabel('Contrainte de cisaillement (MPa)')
        plt.ylabel('Hauteur dans la section (mm)')
        plt.title('Distribution de la contrainte de cisaillement dans une section en H')
        plt.legend()
        plt.grid(True)
        plt.show()"""
        
    def display_graph(self,y,tau):
        try:
            # Nettoyer la figure actuelle et dessiner le graphique
            self.canvas.figure.clear()
            ax = self.canvas.figure.add_subplot(111)
            ax.plot(tau, y, label='Contrainte de cisaillement')
            ax.set_xlabel('Contrainte de cisaillement (MPa)')
            ax.set_ylabel('Hauteur dans la section (mm)')
            ax.set_title('Distribution de la contrainte de cisaillement')
            ax.legend()
            ax.grid(True)

            # Mettre à jour l'affichage du graphique
            self.canvas.draw()
        except ValueError:
            QMessageBox.critical(self, "Erreur", "Problèmes lors de la mise en page")
# Lancer l'application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ShearCalculator()
    window.show()
    sys.exit(app.exec_())

