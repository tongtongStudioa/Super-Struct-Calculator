# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 20:31:18 2024

@author: La famille tong
"""

from numpy import sqrt


class Beam:
    """Classe de base pour les poutres."""

    def __init__(self, h, b_w, c_nom, fck, fyk):
        self.c_min = []
        
        # Caractéristiques de la poutre 
        self.h = h # en m
        self.b_w = b_w # en m
        self.c_nom = c_nom # en mm
        
        # Caractéristiques du béton
        self.fcd = fck / 1.5
        self.phi = 0.8
        self.delta_g = 0.4
        self.E_c = 3.5 / 1000 # 3.5 /1000 de déformation au pivot B et 2/1000 au pivot A
        # Caractéristiques de l'acier
        self.fyd = fyk / 1.15
        self.E_ud = 0.9 * 2.5/100 # E_ud = 0.9 * E_uk et E_uk = 2.5/100 pour acier classe A
        self.sigma_max = 466 # MPa Pivot A
        
        # Bouclage d, et vérification
        self.tolerance = 0.01 # 10% de tolérance
        
    def determiner_alpha(self,u,phi,delta_g):
        """Determiner la position de la fibre neutre dans la poutre"""
        alpha = 1 / (2 * delta_g) * (1 - sqrt(1 - 4 * delta_g / phi * u))
        return alpha
   
    def section_armature_longitudinale_ELU(self, M_g, M_q):
        """Calcule la section de l'armature longitudinale selon l'Eurocode 2."""
        raise NotImplementedError("Cette méthode doit être implémentée dans les classes enfants.")
        
class RectangularBeam(Beam):
    """Classe pour les poutres de section rectangulaire."""
    
    def section_armature_longitudinale_ELU(self,M_g,M_q):
        """Calcule de section de l'armature longitudinale selon l'eurocode 2 pour une poutre en flexion simple.
        Choix du pivot B en priorité, puis calcul avec pivot A si alpha < 0.07 et dimensionnement As2 si alpha > 0.617."""
        
        # 1 Détermination judicieuse de d
        i = 0.9
        while i * self.h * 1000 > self.h * 1000- self.c_nom - 4:
            i -= 0.05
        d = i * self.h # d en m
        #print(f"d = {d}")
        
        # 2 Calcul du moment de flexion Med ELU
        M_ed = 1.35 * M_g + 1.5 * M_q  # en kN.m
        #print(f"M_ed = {M_ed}")
        
        # 3 Calcul du moment intermediare
        u = M_ed * 1000 / (self.b_w * d**2 * self.fcd * 1000000) # f_cd en MPA et M_ed en kN.m
        #print(f"u = {u:.3f}")
        if u > 0.5:
            infos = f"Sinistre : u = {u:.3f} > 0.500\n-> Changer les paramètres liés à la barre et aux dimensions"
            return infos
        
        # 5 Résolution de l'équation du 2nd degré pour trouver alpha
        a = self.determiner_alpha(u, self.phi, self.delta_g)
        #print(f"alpha = {a}")
        As1 = self.calcul_As1_pivot_B(a, d)
        infos = ""
        
        if a < 0.07:
            infos = f"Sinistre au Pivot B: a = {a:.3f} < 0.07, u = {u:.3f} As1 = {As1:.1f} cm²\n-> Changer les paramètres de calculs"
            infos += self.calcul_As1_pivot_A(u, d)
            return infos
        elif a > 0.617:
            infos = f"Section trop importante de As1 : {As1:.1f} cm², choix pas économique : a = {a:.3f} > 0.617 \n"
            infos += self.calcul_As2_pivot_B(M_ed, d)
            return infos
       
        # Afficher les résultats si Pivot B ok :
        infos = f"Section d'acier nécessaire tendu ELU : {As1:.1f} cm²\n d = {d:.2f} m \n a = {a:.3f} \n u = {u:.3f}"
        return infos
    
    def calcul_As1_pivot_B(self,alpha,d):
        # Calcul de la résultante du béton
        Fc = self.phi * self.fcd * self.b_w * alpha * d  # Force du béton en MN
        #print(f"Fc = {Fc * 1000} kN")
        
        # Déformation des aciers tendues
        eps_s = self.E_c * (d-alpha *d)/ (alpha*d) * 1000
        
        # Contrainte dans les aciers tendus en MPa
        #print(f"epsilon s = {eps_s}")
        c1 = self.fyd
        if eps_s < self.fyd/ 200:
            c1 = 210 * eps_s # 210 GPa Module de Young
            
        # Calcul section d'acier nécessaire
        As1 = Fc / c1 * 10**4 # en cm²
        
        return As1
        
    def calcul_As2_pivot_B(self, M_ed,d, a= 0.617):
        Fc = self.phi * self.fcd * self.b_w * 0.617 * d *1000
        Mc = round(Fc * (d - a * self.delta_g * d),1) # en kN.m
        print(f"nouveau Mc = {Mc}")
        
        # Détermination judicieuse de d2
        i = 0.1
        while i * self.h < 20:
            i += 0.05
        d2 = i * self.h / 1000  # passer de mm en m       
        M_residuel = round(M_ed - Mc)
        print(f"M_residuel = {M_residuel}\n")
        
        if M_residuel > 0.4*M_ed:
            return f"Le réglement impose que la part d'effort repris par les aciers comprimés ne dépasse par 40% de l'effort total \nM_residuel = {M_residuel} --> M_residuel / M_ed = {round(M_residuel/M_ed,2)*100}" + "\n -> acceptez que les aciers trvaillent mal \n-> redimensionnez la section" 
        Fs2 = M_residuel /(d-d2) #effort aciers comprimés en kN
        es2 = 3.5/1000 / (a*d) * (a*d - d2)
        c2 = 200 * es2 # contrainte dans les aciers comprimés en MPa
        As2 = Fs2 / c2 / 1000 * 10*4 # en cm²
        As1 = (Fs2 + Fc) / 435 / 1000 * 10**4 # en cm²
        return f"-> Ajout d'une section As2\n Sections d'acier nécessaire --> As1 = {As1:.1f} cm² et As2 = {As2:.1f} cm²"
    
    def calcul_As1_pivot_A(self,u,d):
        phi_init = self.phi
        delta_g_init = self.delta_g
        alpha = self.determiner_alpha(u,phi_init,delta_g_init)
        initial_E_c = 2 / 1000 # max déformation béton au pivot A
        # Calcule efficacité et position selon modele rectangulaire
        phi = (initial_E_c - 0.7/1000)/ initial_E_c 
        delta_g = phi/2
        #print(f"phi = {phi:.3f}")
        #print(f"delta_g = {delta_g:.3f}")
        
        i = 1
        E_c = initial_E_c
        #print(f"Initial E_c = {initial_E_c*1000:.2f}")
        while (abs(self.determiner_alpha(u, phi, delta_g)- alpha)/alpha > self.tolerance):
            alpha = self.determiner_alpha(u, phi, delta_g)
            #print(f"alpha {i} = {alpha:.3f}")
            #phi, delta_g = self.calculate_steel_section()
            E_c = self.E_ud * alpha / (1 - alpha)
            #print(f"E_c = {E_c * 1000:.2f} (/1000)")
            if (E_c > 3.5/1000):
               print("Sinistre ! E_c > 3.5 / 1000")
               break
            phi = (E_c - 0.7/1000)/ E_c 
            delta_g = phi/2
            #print(f"phi = {phi:.2f}")
            #print(f"delta_g = {delta_g:.2f}")
            #print("\n")
            i = i +1
            
        Fc = phi * self.fcd * self.b_w * alpha * d  # Force du béton en MN
        As1 = Fc / self.sigma_max * 10**4 # Contrainte max pour modèle plat à Eud acier
        return f"\nPivot A : Section d'acier nécessaire tendu --> {As1:.1f} cm²\n d = {d:.2f} m "

class TéBeam(Beam):
    """Classe pour les poutres en T."""
    def __init__(self, h, b_w, c_nom, fck, fyk, b_f, h_f):
        super().__init__(h, b_w, c_nom, fck, fyk)
        self.b_f = b_f  # Largeur de la semelle
        self.h_f = h_f  # Hauteur de la semelle

    def section_armature_longitudinale_ELU(self, M_g, M_q):
        
        i = 0.9
        while i * self.h * 1000 > self.h * 1000 - self.c_nom - 4:
            i -= 0.05
        d = i * self.h

        M_ed = 1.35 * M_g + 1.5 * M_q
        M_t100 = self.b_f * self.h_f * self.fcd * (d - self.h_f/2)
        
        # Vérifier si la table seule suffit, alors même calcul que poutre rectangulaire
        if (M_t100 > M_ed):
            beam = RectangularBeam(self.h, self.b_w, self.c_nom, self.fck, self.fyk)
            return beam.section_armature_longitudinale_ELU(M_g, M_q)
        
        
        # 1 As1,1 section constitué des débords
        Mu1 =(self.b_f - self.b_w) * self.h_f * self.fcd * (d - self.h_f/2) # en MN.m
        As1_1 = Mu1 / self.fyd * 10**4 # en cm²
        
        # 2 As1,2 section centrale rectangulaire
        Mu2 = M_ed/1000 - Mu1 # en MN.m
        u = Mu2 / (self.b_w * d**2 * self.fcd )

        if u > 0.5:
            return f"Sinistre : u = {u:.3f} > 0.500\n-> Modifiez les dimensions ou les matériaux."

        alpha = self.determiner_alpha(u, self.phi, self.delta_g)
        As1_2 = self.calcul_As1_pivot_B(alpha, d)

        As1 = As1_1 + As1_2
        if alpha < 0.07:
            return f"Sinistre au Pivot B : alpha = {alpha:.3f} < 0.07, u = {u:.3f}, As1 = {As1:.1f} cm².\n-> Ajustez les paramètres."
        elif alpha > 0.617:
            return f"As1 trop élevé : {As1:.1f} cm². Choix économique non viable : alpha = {alpha:.3f} > 0.617."

        return f"Section d'acier nécessaire tendu : {As1:.1f} cm²\n d = {d:.2f} m\n alpha = {alpha:.3f}\n u = {u:.3f}"

    def calcul_As1_pivot_B(self, alpha, d):
        Fc = self.phi * self.fcd * self.b_w * alpha * d
        eps_s = self.E_c * (d - alpha * d) / (alpha * d) * 1000

        c1 = self.fyd if eps_s >= self.fyd / 200 else 210 * eps_s
        As1 = Fc / c1 * 10**4  # en cm²
        return As1