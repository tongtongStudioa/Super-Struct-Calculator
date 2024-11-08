# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 10:21:05 2024

@author: axel
"""
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from numpy import sqrt
 
class Eurocode2:
    def __init__(self):
        self.c_min = []

# Fonction de résolution d'équation du 2nd degré
def resolution_equation2d(a, b, c):
    delta = b**2 - 4 * a * c
    if delta < 0:
        return None, None
    x1 = (-b - sqrt(delta)) / (2 * a)
    x2 = (-b + sqrt(delta)) / (2 * a)
    #print(f"x1 = {abs(x1)} et x2 = {abs(x2)}")
    return abs(x1), abs(x2)

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
        - Section rectangulaire.
        - Coefficients de sécurité appliqués selon les charges (ELS et ELU).
        """)
        
        hypothese_label.setWordWrap(True)
        hypothese_label.setAlignment(Qt.AlignLeft)
        hypothese_label.setFont(QFont('Arial', 12))

        # Disposition des champs d'entrée et des labels
        input_frame = QFrame(self)

        # Ajout des champs d'entrée pour les paramètres de calcul
        fck_label = QLabel("Résistance béton à 28j (MPa):")
        self.entry_f_ck = QLineEdit(self)
        self.entry_f_ck.setText("30")

        charge_label = QLabel("Charge (kN/m):")
        self.entry_charge = QLineEdit(self)
        self.entry_charge.setText("35")

        portee_label = QLabel("Portée (m):")
        self.entry_portee = QLineEdit(self)
        self.entry_portee.setText("10")

        cmin_label = QLabel("Enrobage nominal c nom (mm):")
        self.entry_c_min = QLineEdit(self)
        self.entry_c_min.setText("20")

        hauteur_label = QLabel("Hauteur de la poutre (mm):")
        self.entry_hauteur = QLineEdit(self)
        self.entry_hauteur.setText("600")

        largeur_label = QLabel("Largeur de la poutre (mm):")
        self.entry_largeur = QLineEdit(self)
        self.entry_largeur.setText("250")

        # Organisation horizontale des labels et des champs de saisie
        input_layout1 = QHBoxLayout()
        input_layout1.addWidget(fck_label)
        input_layout1.addWidget(self.entry_f_ck)

        input_layout2 = QHBoxLayout()
        input_layout2.addWidget(charge_label)
        input_layout2.addWidget(self.entry_charge)

        input_layout3 = QHBoxLayout()
        input_layout3.addWidget(portee_label)
        input_layout3.addWidget(self.entry_portee)

        input_layout4 = QHBoxLayout()
        input_layout4.addWidget(cmin_label)
        input_layout4.addWidget(self.entry_c_min)

        input_layout5 = QHBoxLayout()
        input_layout5.addWidget(hauteur_label)
        input_layout5.addWidget(self.entry_hauteur)

        input_layout6 = QHBoxLayout()
        input_layout6.addWidget(largeur_label)
        input_layout6.addWidget(self.entry_largeur)

        # Ajout des entrées dans le frame
        vbox_input = QVBoxLayout()
        vbox_input.addLayout(input_layout1)
        vbox_input.addLayout(input_layout2)
        vbox_input.addLayout(input_layout3)
        vbox_input.addLayout(input_layout4)
        vbox_input.addLayout(input_layout5)
        vbox_input.addLayout(input_layout6)
        input_frame.setLayout(vbox_input)


        # Bouton pour calculer la section d'acier
        calculate_button = QPushButton("Calculer la section d'acier", self)
        calculate_button.clicked.connect(self.calculer_section)

        # Affichage des résultats
        self.result_label = QLabel("Section d'acier nécessaire : ")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setWordWrap(True)
        self.result_label.setFont(QFont('Arial', 18))

        # Mise en page principale
        main_layout = QVBoxLayout()
        main_layout.addWidget(hypothese_label)
        main_layout.addWidget(input_frame)
        main_layout.addWidget(calculate_button)
        main_layout.addWidget(self.result_label)

        self.setLayout(main_layout)

    # Fonction de calcul de la section d'acier
    def calculer_section(self):
        try:
            # Modèle du béton
            phi = 0.8  # Efficacité du béton
            delta_g = 0.4  # Point d'application de compression

            # Récupérer les entrées utilisateur
            f_ck = int(self.entry_f_ck.text())  # Résistance caractéristique du béton en MPa
            f_cd = f_ck / 1.5
            f_yk = 500  # Résistance caractéristique de l'acier en MPa
            f_yd = round(f_yk / 1.15)

            charge_lineaire = float(self.entry_charge.text())  # en kN/m
            longueur = float(self.entry_portee.text())  # en m
            c_min = int(self.entry_c_min.text())  # en mm
            c_nom = c_min + 10
            h = float(self.entry_hauteur.text())  # hauteur poutre en mm
            b = float(self.entry_largeur.text()) / 1000  # largeur poutre en m

            # Détermination judicieuse de d
            i = 0.9
            while i * h > h - c_nom - 4:
                i -= 0.05
            d = i * h / 1000  # passer de mm en m

            # Calcul du moment de flexion
            M_ed = (charge_lineaire * longueur**2) / 8  # en kN.m
            #print(f"M_ed = {M_ed}")
            u = M_ed * 1000 / (b * d**2 * f_cd * 1000000)
            #print(f"u = {u:.3f}")
            # Résolution de l'équation du 2nd degré
            a1, a2 = resolution_equation2d(phi * delta_g, -phi, u)
            if not a1 and not a2:
                self.result_label.setText(f"Sinistre : u = {u:.3f} > 0.500\n-> Changer les paramètres liés à la barre et aux dimensions")
                return
            a = min(a1, a2)
            
            Fc = phi * f_cd * b * a * d  # Force du béton en MN
            #print(f"Fc = {Fc * 1000} kN")
            Mc = round(Fc * (d-a*delta_g*d) * 1000,1) # en kN.m
            #print(f"Mc = {Mc} kN.m")
            
            # Déformation des aciers tendues
            eps_s = 3.5/1000 * (d-a*d)/ (a*d) * 1000
            # Contrainte dans les aciers tendus en MPa
            #print(f"epsilon s = {eps_s}")
            c1 = f_yd
            if eps_s < f_yd/ 200:
                c1 = 200 * eps_s
            # Calcul de l'aire d'acier nécessaire
            As1 = Fc / c1 * 10**4 # en cm²

            # Afficher les résultats
            if a < 0.07:
                self.result_label.setText(f"Sinistre : a = {a:.3f} < 0.07 \n-> Changer les paramètres de calculs")
                return
            elif a > 0.617:
                infos = f"Section trop importante de As1 : {As1:.1f} cm², choix pas économique : a = {a:.3f} > 0.617 \n"
                infos += self.calcul_As1((phi * f_cd * b * 0.617 * d *1000), M_ed, d, h)
                self.result_label.setText(infos)
                return

            infos = f"Section d'acier nécessaire tendu : {As1:.1f} cm²\n d = {d:.2f} m \n a = {a:.3f}"
            self.result_label.setText(infos)
        except ValueError:
            QMessageBox.critical(self, "Erreur", "Veuillez entrer des valeurs numériques valides.")
    
    def calcul_As1(self,Fc, M_ed,d, h, a= 0.617):
        Mc = round(Fc * (d-a*0.4*d),1) # en kN.m
        #print(f"nouveau Mc = {Mc}")
        # Détermination judicieuse de d
        i = 0.1
        while i * h < 20:
            i += 0.05
        d2 = i * h / 1000  # passer de mm en m       
        M_residuel = round(M_ed - Mc)
        #print(f"M_residuel = {M_residuel}\n")
        if M_residuel > 0.4*M_ed:
            return f"Le réglement impose que la part d'effort repris par les aciers comprimés ne dépasse par 40% de l'effort total \nM_residuel = {M_residuel} --> M_residuel / M_ed = {round(M_residuel/M_ed,2)*100}" + "\n -> acceptez que les aciers trvaillent mal \n-> redimensionnez la section" 
        Fs2 = M_residuel /(d-d2) #effort aciers comprimés en kN
        es2 = 3.5/1000 / (a*d) * (a*d - d2)
        c2 = 200 * es2 # contrainte dans les aciers comprimés en MPa
        As2 = Fs2 / c2 / 1000 * 10*4 # en cm²
        As1 = (Fs2 + Fc) / 435 / 1000 * 10**4 # en cm²
        
        return f"-> Ajout d'une section As2\n Sections d'acier nécessaire : As1 = {As1:.1f} cm² et As2 = {As2:.1f} cm²"
# Lancer l'application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ArmatureCalculator()
    window.show()
    sys.exit(app.exec_())

