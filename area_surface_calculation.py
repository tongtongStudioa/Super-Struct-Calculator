# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 14:32:43 2024

@author: La famille tong
"""

import tkinter as tk

class Piece:
    def __init__(self, canvas, start_x, start_y, end_x, end_y, unit_conversion=100):
        """Initialisation d'une pièce (rectangle) avec ses coordonnées et le canvas."""
        self.canvas = canvas
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.unit_conversion = unit_conversion  # Conversion des pixels en unités (ex : 100 px = 1 m)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.end_x, self.end_y, outline="black", width=2)
        self.lengths = self.display_lengths()

    def move(self, new_x, new_y):
        """Déplacer la pièce en conservant ses dimensions initiales."""
        self.canvas.delete(self.lengths[0])
        self.canvas.delete(self.lengths[1])

        width = self.end_x - self.start_x
        height = self.end_y - self.start_y
        self.start_x = new_x
        self.start_y = new_y
        self.end_x = new_x + width
        self.end_y = new_y + height
        self.canvas.coords(self.rect, self.start_x, self.start_y, self.end_x, self.end_y)
        self.lengths = self.display_lengths()
        
    def display_lengths(self):
        """Afficher les longueurs des côtés de la pièce (en mètres ou autre unité)."""
        length_x = abs(self.end_x - self.start_x) / self.unit_conversion
        length_y = abs(self.end_y - self.start_y) / self.unit_conversion
        mid_x = (self.start_x + self.end_x) / 2
        mid_y = (self.start_y + self.end_y) / 2

        # Afficher les longueurs sur le canvas
        length1 = self.canvas.create_text(mid_x, self.start_y - 10, text=f"L = {length_x:.2f} m", fill="blue")
        length2 = self.canvas.create_text(self.end_x + 20, mid_y, text=f"H = {length_y:.2f} m", fill="blue")
        return (length1, length2)

    def delete(self):
        """Supprimer la pièce du canvas."""
        self.canvas.delete(self.rect)
        self.canvas.delete(self.lengths[0])
        self.canvas.delete(self.lengths[1])

class InfluenceSurfaceCalculator:
    """Calculateur de surface d'influence pour descentes de charges"""
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=800, height=600, bg='white')
        self.canvas.pack()

        self.start_x = None
        self.start_y = None
        self.temp_rect = None  # Rectangle temporaire pendant le dessin
        self.pieces = []   # Liste des pièces (rectangles)
        self.selected_piece = None  # Pièce actuellement sélectionnée
        self.unit_conversion = 100  # Conversion px -> mètres (1 m = 100 px)

        # Liaison des événements pour dessiner un rectangle
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.update_rectangle)
        self.canvas.bind("<ButtonRelease-1>", self.finish_rectangle)

        # Liaison des événements pour déplacer/redimensionner un rectangle
        self.canvas.bind("<Button-3>", self.select_piece)
        self.canvas.bind("<B3-Motion>", self.move_piece)

        # Bouton pour supprimer une pièce
        self.delete_button = tk.Button(root, text="Supprimer la pièce sélectionnée", command=self.delete_selected)
        self.delete_button.pack()

    def start_draw(self, event):
        """Stocker les coordonnées du premier point de clic."""
        self.start_x, self.start_y = event.x, event.y

    def update_rectangle(self, event):
        """Mettre à jour le rectangle pendant le tracé."""
        if self.temp_rect:
            self.canvas.delete(self.temp_rect)  # Effacer le rectangle temporaire précédent

        end_x, end_y = event.x, event.y

        # Dessiner le rectangle temporaire pendant le déplacement de la souris
        self.temp_rect = self.canvas.create_rectangle(self.start_x, self.start_y, end_x, end_y, outline="black", width=2)
        self.display_updated_lengths()
    def finish_rectangle(self, event):
        """Finaliser le rectangle une fois que le bouton de la souris est relâché."""
        end_x, end_y = event.x, event.y

        # Créer et ajouter une nouvelle pièce (rectangle) à la liste
        new_piece = Piece(self.canvas, self.start_x, self.start_y, end_x, end_y, self.unit_conversion)
        self.pieces.append(new_piece)

        # Supprimer le rectangle temporaire
        if self.temp_rect:
            self.canvas.delete(self.temp_rect)
            self.temp_rect = None

    def select_piece(self, event):
        """Sélectionner une pièce (clic droit) pour pouvoir la déplacer."""
        clicked_x, clicked_y = event.x, event.y
        for piece in self.pieces:
            if piece.start_x <= clicked_x <= piece.end_x and piece.start_y <= clicked_y <= piece.end_y:
                self.selected_piece = piece
                break

    def move_piece(self, event):
        """Déplacer une pièce sélectionnée (clic droit maintenu)."""
        if self.selected_piece:
            new_x = event.x
            new_y = event.y
            self.selected_piece.move(new_x, new_y)

    def delete_selected(self):
        """Supprimer la pièce actuellement sélectionnée."""
        if self.selected_piece:
            self.selected_piece.delete()
            self.pieces.remove(self.selected_piece)
            self.selected_piece = None

# Créer l'interface principale
root = tk.Tk()
root.title("Drawing App - Gestion des Pièces avec Suppression et Déplacement")

app = InfluenceSurfaceCalculator(root)

root.mainloop()



