# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 19:45:31 2024

@author: Axel
"""
import numpy as np

def calculate_alpha(u, phi=0.8, delta_g=0.4):
    alpha = -(-phi+np.sqrt(phi**2 - 4*phi*delta_g*u))/(phi*delta_g*2)
    alpha = 1/ (2 * delta_g) * (1 - np.sqrt(1 - 4 * delta_g/phi * u))
    return alpha

class Pivot_A:
    
    def __init__(self,u,E_ud = 0.9 * 2.5/100,E_c = 2/1000):
        self.u = u
        self.E_ud = E_ud # E_ud = 0.9 * E_uk et E_uk = 2.5/100 pour acier classe A
        self.E_c = E_c
        self.sigma_max = 466 # MPa
        self.tolerance = 0.01 # 20% de tolérance
        
    def calculate_steel_section(self):
        phi_init = 0.8
        delta_g_init = 0.4
        alpha = calculate_alpha(u,phi_init,delta_g_init)
        initial_E_c = self.E_c 
        # Calcule efficacité et position selon modele rectangulaire
        phi = (initial_E_c - 0.7/1000)/ initial_E_c 
        delta_g = phi/2
        print(f"phi = {phi:.3f}")
        print(f"delta_g = {delta_g:.3f}")
        
        i = 1
        E_c = initial_E_c
        print(f"Initial E_c = {initial_E_c*1000:.2f}")
        while (abs(calculate_alpha(u, phi, delta_g)- alpha)/alpha > self.tolerance):
            alpha = calculate_alpha(u, phi, delta_g)
            print(f"alpha {i} = {alpha:.3f}")
            #phi, delta_g = self.calculate_steel_section()
            E_c = self.E_ud * alpha / (1 - alpha)
            print(f"E_c = {E_c * 1000:.2f} (/1000)")
            if (E_c > 3.5/1000):
               print("Sinistre !")
               break
            phi = (E_c - 0.7/1000)/ E_c 
            delta_g = phi/2
            print(f"phi = {phi:.2f}")
            print(f"delta_g = {delta_g:.2f}")
            print("\n")
            i = i +1
        return alpha, phi, delta_g, E_c
    
    def change_phi_and_deltag_g(self,alpha):
        E_c = self.E_ud * alpha / (1 - alpha)
        print(f"E_c = {E_c * 1000} (/1000)")
        if (E_c > 3.5/1000):
            print("Sinistre !")
            return None
        phi = (E_c - 0.7/1000)/ E_c 
        delta_g = phi/2
        return phi, delta_g
    
b=0.3
h=0.6

d = 0.9*h
Mg = 0.025
Mq = 0.1
M_ed = 1.35 * Mg + 1.5 * Mq
print(f"M_ed = {M_ed * 1000}")
f_cd = 20
phi = 0.8
delta_g = 0.4
u = M_ed/(f_cd * b * d**2)

print(f"u = {u:.4f}")

alpha = calculate_alpha(u)
print(f"alpha init = {alpha:.3f}")
if alpha < 0.07:
    new_alpha, phi, delta_g, E_c = Pivot_A(u, E_c= 1.4/1000).calculate_steel_section()
    print(f"new alpha = {new_alpha:.3f} ({((new_alpha - alpha)/alpha * 100):.2f})")
    print(f"Hypothèses : phi = {phi:.2f}, delta_g = {delta_g:.2f} et E_c = {E_c*1000:.2f}")
    Fc = phi * f_cd * b * d * new_alpha # en MN
    As1 = Fc / 466 # 466 egal sigma max pour E_ud
    print(f"As1 = {As1 * 10000:.2f} cm²")
    print(As1 * 466.5 * d * (1-alpha) - M_ed)
if alpha > 0.714:
    print("Ajouter As2")

