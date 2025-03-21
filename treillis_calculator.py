# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 09:23:35 2024

@author: La famille tong
"""

import numpy as np

# Données du problème
# Coordonnées des nœuds : [(x1, y1), (x2, y2), ...]
nodes = [(0, 0), (4, 0), (2, 3), (8,0), (6,3)]

# Connectivité des barres : [(nœud1, nœud2), ...]
bars = [(0, 1), (1, 2), (0, 2), (2,3), (3,1), (3,4), (1,4)]

# Forces extérieures sur chaque nœud : [(Fx1, Fy1), (Fx2, Fy2), ...]
forces = [(0, 0), (0, -1000), (0, 0)]

# Appuis : True pour bloqué, False pour libre, dans l'ordre [Ux, Uy]
supports = [(True, True), (True, True), (True, True), (True, True), (True, True)]

# Calcul de la matrice de rigidité locale
def bar_stiffness_matrix(E, A, L, angle):
    c = np.cos(angle)
    s = np.sin(angle)
    k = (E * A / L) * np.array([
        [c*c, c*s, -c*c, -c*s],
        [c*s, s*s, -c*s, -s*s],
        [-c*c, -c*s, c*c, c*s],
        [-c*s, -s*s, c*s, s*s]
    ])
    return k

# Assemblage des matrices globales
def assemble_global_stiffness(nodes, bars, E, A):
    num_dofs = len(nodes) * 2  # Nombre de degrés de liberté
    K_global = np.zeros((num_dofs, num_dofs))

    for bar in bars:
        n1, n2 = bar
        x1, y1 = nodes[n1]
        x2, y2 = nodes[n2]
        L = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        angle = np.arctan2(y2 - y1, x2 - x1)
        
        k_local = bar_stiffness_matrix(E, A, L, angle)

        # Map local DOFs to global DOFs
        dofs = [
            2 * n1, 2 * n1 + 1,
            2 * n2, 2 * n2 + 1
        ]
        
        for i in range(4):
            for j in range(4):
                K_global[dofs[i], dofs[j]] += k_local[i, j]

    return K_global

# Réduction de la matrice pour tenir compte des appuis
def apply_supports(K, forces, supports):
    num_dofs = len(forces) * 2
    F = np.array(forces).flatten()
    fixed_dofs = []

    for i, support in enumerate(supports):
        if support[0]:
            fixed_dofs.append(2 * i)
        if support[1]:
            fixed_dofs.append(2 * i + 1)

    free_dofs = list(set(range(num_dofs)) - set(fixed_dofs))
    
    K_reduced = K[np.ix_(free_dofs, free_dofs)]
    F_reduced = F[free_dofs]

    return K_reduced, F_reduced, fixed_dofs, free_dofs

# Paramètres matériels
E = 210e9  # Module d'Young en Pa
A = 0.01   # Section en m²

# Assemblage et réduction
K_global = assemble_global_stiffness(nodes, bars, E, A)
K_reduced, F_reduced, fixed_dofs, free_dofs = apply_supports(K_global, forces, supports)

# Résolution du système réduit
U_reduced = np.linalg.solve(K_reduced, F_reduced)

# Reconstruction du vecteur complet des déplacements
U = np.zeros(len(nodes) * 2)
U[free_dofs] = U_reduced

# Calcul des réactions aux appuis
reactions = K_global @ U

# Affichage des résultats
print("Déplacements aux nœuds :", U.reshape(-1, 2))
print("Réactions aux appuis :", reactions.reshape(-1, 2))
