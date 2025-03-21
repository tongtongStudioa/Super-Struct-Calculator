# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 14:19:07 2024

@author: axel
"""
import tkinter as tk
import math

class Canva(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Beam characteristics calculator")

        # Créer un canevas pour dessiner
        self.canvas = tk.Canvas(self, bg="white", width=900, height=650)
        self.canvas.pack()

        # Créer un label pour afficher la longueur de la ligne
        self.length_label = tk.Label(self, text="Length: 0")
        self.length_label.pack()
        self.length_entry = tk.Entry(self,text="Length: 0")
        self.length_entry.pack()
        
        # Initialiser les variables pour les coordonnées de la forme
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        self.is_drawing = False

        # Liaison des événements de la souris
        self.canvas.bind("<Button-1>", self.toggle_draw)
        self.canvas.bind("<Motion>", self.draw_shape)
        self.canvas.bind("<Double-Button-1>", self.end_shape)
        
        # Liaison de l'événement clavier pour arrêter le dessin
        self.bind("<Escape>", self.end_shape)
        
    def draw_axes(self):
        # Axe X
        self.canvas.create_line(50, 200, 550, 200, fill="black", width=2, arrow=tk.LAST)
        # Axe Y
        self.canvas.create_line(300, 350, 300, 50, fill="black", width=2, arrow=tk.LAST)

    def draw_guides(self):
        # Guides horizontaux
        for y in range(100, 401, 50):
            self.canvas.create_line(50, y, 550, y, fill="lightgray", dash=(2, 2))
        # Guides verticaux
        for x in range(100, 601, 50):
            self.canvas.create_line(x, 50, x, 350, fill="lightgray", dash=(2, 2))

    def toggle_draw(self, event):
        if self.is_drawing:
            #Terminer la ligne
            self.canvas.create_line(self.start_x, self.start_y, self.end_x, self.end_y)
            # Continuer dans une autre direction
            self.start_x = self.end_x
            self.start_y = self.end_y

            self.draw_shape(event)
        else:
            # Commencer à dessiner si pas en train de dessiner
            self.start_shape(event)
            self.is_drawing = True
            
    def start_shape(self, event):
        # Enregistrer les coordonnées de début de la forme
        self.start_x = event.x
        self.start_y = event.y

    def draw_shape(self, event):
        if self.is_drawing:
            # Dessiner une ligne lors du déplacement de la souris
            self.end_x = event.x
            self.end_y = event.y
            self.canvas.delete("temp_shape") # pour "temporary_state"
    
            # Calculer les coordonnées de l'angle droit
            if abs(self.end_x - self.start_x) > abs(self.end_y - self.start_y):
                self.end_y = self.start_y
            else:
                self.end_x = self.start_x
    
            # Dessiner la ligne avec angle droit
            self.canvas.create_line(self.start_x, self.start_y, self.end_x, self.end_y, tags="temp_shape")
            self.is_drawing = True
            
            # Mettre à jour la longueur de la ligne
            self.update_line_length()

    def update_line_length(self):
        length = math.sqrt((self.end_x - self.start_x)**2 + (self.end_y - self.start_y)**2)
        x_mid = (self.end_x + self.start_x)/2 + 10
        y_mid = (self.end_y + self.start_y)/2 + 10
        self.length_label.place(x=x_mid, y=y_mid)
        self.length_label.config(text=f"Length: {length:.2f}")
    
        
    def end_shape(self, event):
        # Effacer le brouillon
        self.canvas.delete("temp_shape")
        
        #Modification de l'état
        self.is_drawing = False
        

if __name__ == "__main__":
    app = Canva()
    app.mainloop()
    
    
    
    



