# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 09:28:00 2024

@author: axel
"""

import sys
from PyQt5.QtWidgets import QApplication, QCheckBox, QWidget, QComboBox, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

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
        self.profile_combobox.addItem("Rectangulaire")
        self.profile_combobox.addItem("Profil en I")
        self.profile_combobox.addItem("Profil en T")

        
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
        
        vbox_input = QVBoxLayout()
        vbox_input.addLayout(input_layout1)
        vbox_input.addWidget(self.auto_moment_checkbox)
        vbox_input.addLayout(input_layout4)
        vbox_input.addWidget(self.auto_stiffness_center_checkbox)
        vbox_input.addWidget(self.input_forms_frame)
        #vbox_input.addLayout(input_layout5)
        #vbox_input.addLayout(input_layout6)
        input_frame.setLayout(vbox_input)



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
        intermediate_layout.addWidget(input_frame)
        intermediate_layout.addWidget(self.canvas)
        main_layout.addLayout(intermediate_layout)
        main_layout.addWidget(calculate_button, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.result_label, alignment=Qt.AlignCenter)
        
        self.setLayout(main_layout)
    
    def createProfileInputs(self):
        """Crée les champs d'entrée pour les dimensions en fonction du profilé."""
       
        self.clearLayout(self.input_forms_frame.layout())
        layout = QVBoxLayout()

        profile_type = self.profile_combobox.currentText()
        
        # Dimensions pour un profilé rectangulaire
        if profile_type == "Rectangulaire":
            self.entry_hauteur = self.createInputField("Hauteur (mm):", layout)
            self.entry_largeur = self.createInputField("Largeur (mm):", layout)
        
        # Dimensions pour un profilé en H
        elif profile_type == "Profilé en H":
            self.entry_hauteur_totale = self.createInputField("Hauteur totale (mm):", layout)
            self.entry_largeur_totale = self.createInputField("Largeur totale (mm):", layout)
            self.entry_hauteur_ame = self.createInputField("Hauteur de l'âme (mm):", layout)
            self.entry_epaisseur_ame = self.createInputField("Épaisseur de l'âme (mm):", layout)
            self.entry_largeur_ailes = self.createInputField("Largeur des ailes (mm):", layout)
            self.entry_epaisseur_ailes = self.createInputField("Épaisseur des ailes (mm):", layout)
        
        # Dimensions pour un profilé en T
        elif profile_type == "Profilé en T":
            self.entry_hauteur_totale = self.createInputField("Hauteur totale (mm):", layout)
            self.entry_largeur_ame = self.createInputField("Largeur de l'âme (mm):", layout)
            self.entry_epaisseur_ame = self.createInputField("Épaisseur de l'âme (mm):", layout)
            self.entry_largeur_ailes = self.createInputField("Largeur de l'aile (mm):", layout)
            self.entry_epaisseur_ailes = self.createInputField("Épaisseur de l'aile (mm):", layout)

        self.input_forms_frame.setLayout(layout)

    def createInputField(self, label_text, layout):
        """Crée un champ d'entrée avec un label et l'ajoute à la mise en page."""
        hbox = QHBoxLayout()
        label = QLabel(label_text)
        line_edit = QLineEdit(self)
        hbox.addWidget(label)
        hbox.addWidget(line_edit)
        layout.addLayout(hbox)
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
        self.createProfileInputs()
        
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
            
    def update_input_fields(self):
        """Mettre à jour les champs d'entrée en fonction du profil sélectionné."""
        selected_profile = self.profile_combobox.currentText()
        
            
    # Fonction de calcul de la section d'acier
    def calculs_cisaillement_points_critiques(self):
        try:
            # Récupérer les entrées utilisateur
            h = float(self.entry_hauteur.text()) / 1000  # hauteur poutre en m
            b = float(self.entry_largeur.text()) / 1000  # largeur poutre en m
            
            if self.auto_moment_checkbox.isChecked():
                I_z = (b * h**3) / 12  # Calcul du moment quadratique (m^4)
                self.entry_quadratic_moment.setText(f"{I_z*10**12:.0f}")
            else:
                I_z = float(self.entry_quadratic_moment.text())  # Moment quadratique en mm4
                I_z = I_z * 10**-12  # Convertir en m^4
                
            q = float(self.entry_charge.text()) * 1000 # charge linéaire en N/m
            longueur = float(self.entry_portee.text())  # en m
            V = q*longueur/2 # Effort tranchant en N
            
            if self.auto_stiffness_center_checkbox.isChecked():
                y_g = h/2  # Centre d'inertie en mm
                self.entry_stiffness_center.setText(f"{y_g * 1000:.2f}")
            else:
                y_g = int(self.entry_stiffness_center.text())  # position y du centre de rigidité en mm
                y_g = y_g / 1000  # Convertir en m^4
                
            distribution_cisaillement = self.distribution_cisaillement(h, V, I_z, b, b)
            self.display_graph(distribution_cisaillement["y"], distribution_cisaillement["tau"])
            t_max = self.calcul_cisaillement(V,I_z,b,b,h/2-y_g,h/2)
            self.result_label.setText(f"Contrainte de cisaillement max Txy = {t_max:.2f} MPa")
        except ValueError:
            QMessageBox.critical(self, "Erreur", "Veuillez entrer des valeurs numériques valides.")
    
    
    def calcul_cisaillement(self,V,I_z,b_u,b_y,y0,ymax ):
        """Calcul cisaillement considérant que la largeur b ne change pas sur un dy donnée"""
        integral = b_y * (ymax**2/2-y0**2/2)
        if I_z == 0 or b_y == 0:
            QMessageBox.critical(self, "Erreur", "Veuillez entrer des valeurs numériques valides : I_z ne peut pas être égal à 0 et b non plus")
            return None
        return -V/(I_z*b_u)*integral / 10**6 # contrainte de cisaillement en MPa
    
    
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
            
    def distribution_cisaillement(self,h,V,I_z,b_u,b_y):
        "Distribution du cisaillement sur pour une largeur constante."
        # Calcul de la contrainte de cisaillement à différentes hauteurs
        y = np.linspace(h/2, -h/2, 1000)  # Discrétisation de la hauteur
        tau = np.zeros_like(y)
        
        for i, y_val in enumerate(y):
            # Cisaillement dans l'âme
            if -h/2 <= y_val <= h/2 :
                tau[i] = self.calcul_cisaillement(V,I_z,b_u,b_y,y_val,h/2)
                
        return {"y":y,"tau":tau}
    
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
        
# Lancer l'application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ShearCalculator()
    window.show()
    sys.exit(app.exec_())

