# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 10:40:41 2024

@author: La famille tong
"""

import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt

# Fonction de calcul des moments et flèches
def calcul_poutre():
    try:
        # Récupérer les entrées utilisateur
        longueur = float(entry_longueur.get())
        positions_appuis = list(map(float, entry_appuis.get().split(',')))
        charge_type = charge_var.get()
        
        if charge_type == 'Répartie':
            charge_uniforme = float(entry_charge.get())
        elif charge_type == 'Ponctuelles':
            positions_charges = list(map(float, entry_charge_positions.get().split(',')))
            valeurs_charges = list(map(float, entry_charge_valeurs.get().split(',')))

        E = float(entry_E.get())  # Module d'Young
        I = float(entry_I.get())  # Moment d'inertie

        # Calcul simplifié des moments et flèches en fonction du type de charge
        # (peut être adapté pour inclure une analyse plus poussée)
        
        moment_A = -(charge_uniforme * longueur**2) / 8  # Exemple pour charge répartie
        moment_B = (charge_uniforme * longueur**2) / 16  # Pour appuis au milieu
        moment_C = -(charge_uniforme * longueur**2) / 8

        reaction_A = (5 * charge_uniforme * longueur) / 16
        reaction_B = (charge_uniforme * longueur) / 8
        reaction_C = (5 * charge_uniforme * longueur) / 16

        fleche_max = (5 * charge_uniforme * longueur**4) / (384 * E * I)

        # Afficher les résultats
        result_moments.config(text=f"Moments: A={moment_A:.2f} kNm, B={moment_B:.2f} kNm, C={moment_C:.2f} kNm")
        result_fleche.config(text=f"Flèche maximale: {fleche_max:.2f} mm")

        # Tracer les diagrammes et les schémas
        tracer_diagrammes(longueur, positions_appuis, charge_type, E, I, charge_uniforme, positions_charges, valeurs_charges)

    except ValueError:
        messagebox.showerror("Erreur", "Veuillez entrer des valeurs numériques valides.")

# Fonction pour tracer les diagrammes de moments, flèches, et les schémas
def tracer_diagrammes(longueur, positions_appuis, charge_type, E, I, charge_uniforme=None, positions_charges=None, valeurs_charges=None):
    x = np.linspace(0, longueur, 100)
    
    # Moment de flexion approximé
    moment = -(charge_uniforme * x**2) / 8  # Exemple avec charge répartie

    # Flèche approximée
    fleche = -(charge_uniforme * x**4) / (384 * E * I)  # Exemple simplifié

    plt.figure(figsize=(12, 6))

    # Schéma structurel (poutre avec appuis variables)
    plt.subplot(2, 2, 1)
    plt.plot([0, longueur], [0, 0], 'k-', lw=4, label="Poutre")
    for appui in positions_appuis:
        plt.scatter([appui], [0], color='blue', zorder=5, label=f"Appui à {appui:.2f} m")
    plt.title("Schéma structurel")
    plt.xlabel("Longueur de la poutre (m)")
    plt.ylabel("Poutre")
    plt.xlim(-0.1, longueur + 0.1)
    plt.ylim(-0.1, 0.1)
    plt.grid(True)
    plt.legend()

    # Schéma de charge
    plt.subplot(2, 2, 2)
    if charge_type == 'Répartie':
        plt.fill_between([0, longueur], 0, charge_uniforme, color='red', alpha=0.3, label=f"Charge répartie: {charge_uniforme} kN/m")
    elif charge_type == 'Ponctuelles':
        for pos, charge in zip(positions_charges, valeurs_charges):
            plt.scatter([pos], [charge], color='red', label=f"Charge ponctuelle: {charge:.2f} kN à {pos:.2f} m")
    plt.title("Schéma de charge")
    plt.xlabel("Longueur de la poutre (m)")
    plt.ylabel("Charge (kN)")
    plt.grid(True)
    plt.legend()

    # Diagramme de moment
    plt.subplot(2, 2, 3)
    plt.plot(x, moment, label="Moment de flexion (kNm)", color='blue')
    plt.title("Diagramme de moment")
    plt.xlabel("Longueur de la poutre (m)")
    plt.ylabel("Moment (kNm)")
    plt.grid(True)
    plt.legend()

    # Diagramme de flèche
    plt.subplot(2, 2, 4)
    plt.plot(x, fleche, label="Flèche (mm)", color='orange')
    plt.title("Diagramme de flèche")
    plt.xlabel("Longueur de la poutre (m)")
    plt.ylabel("Flèche (mm)")
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()

# Interface graphique avec Tkinter
app = tk.Tk()
app.title("Calcul des Moments, Flèches et Schémas pour Poutre Hyperstatique")
app.geometry("500x450")

# Champs de saisie
tk.Label(app, text="Longueur de la poutre (m):").pack()
entry_longueur = tk.Entry(app)
entry_longueur.pack()

tk.Label(app, text="Positions des appuis (en m, séparés par des virgules):").pack()
entry_appuis = tk.Entry(app)
entry_appuis.pack()

# Option pour choisir le type de charge
charge_var = tk.StringVar(value='Répartie')
tk.Radiobutton(app, text="Charge uniformément répartie", variable=charge_var, value='Répartie').pack()
tk.Radiobutton(app, text="Charges ponctuelles", variable=charge_var, value='Ponctuelles').pack()

# Charge répartie
tk.Label(app, text="Charge répartie (kN/m):").pack()
entry_charge = tk.Entry(app)
entry_charge.pack()

# Charges ponctuelles
tk.Label(app, text="Positions des charges ponctuelles (en m, séparés par des virgules):").pack()
entry_charge_positions = tk.Entry(app)
entry_charge_positions.pack()

tk.Label(app, text="Valeurs des charges ponctuelles (en kN, séparés par des virgules):").pack()
entry_charge_valeurs = tk.Entry(app)
entry_charge_valeurs.pack()

tk.Label(app, text="Module d'Young (E en MPa):").pack()
entry_E = tk.Entry(app)
entry_E.pack()

tk.Label(app, text="Moment d'inertie (I en mm^4):").pack()
entry_I = tk.Entry(app)
entry_I.pack()

# Bouton de calcul
calculate_button = tk.Button(app, text="Calculer", command=calcul_poutre)
calculate_button.pack()

# Affichage des résultats
result_moments = tk.Label(app, text="Moments: ")
result_moments.pack()

result_fleche = tk.Label(app, text="Flèche maximale: ")
result_fleche.pack()

# Lancement de l'application
app.mainloop()
