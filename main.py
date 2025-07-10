# main.py - Script principal du jeu

import pygame
import sys
from solve import ToursDeHanoi
from graphics import GraphicsManager

# Configuration
NOMBRE_DISQUES = 4

class Jeu:
    def __init__(self):
        self.graphics = GraphicsManager()
        self.etat = "menu"  # menu, jeu, fin
        self.hanoi = None
        self.temps_derniere_action = 0
        self.vitesse_resolution = 1000  # millisecondes entre chaque mouvement
        
    def gerer_evenements(self):
        """Gère les événements du jeu"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                
                if event.key == pygame.K_SPACE:
                    if self.etat == "menu":
                        self.etat = "jeu"
                        self.hanoi = ToursDeHanoi(NOMBRE_DISQUES)
                        self.hanoi.lancer_resolution()
                        self.temps_derniere_action = pygame.time.get_ticks()
                    
                    elif self.etat == "jeu" and self.hanoi.resolu:
                        self.etat = "fin"
                    
                    elif self.etat == "fin":
                        self.etat = "jeu"
                        self.hanoi = ToursDeHanoi(NOMBRE_DISQUES)
                        self.hanoi.lancer_resolution()
                        self.temps_derniere_action = pygame.time.get_ticks()
                
                # Contrôles de vitesse
                if self.etat == "jeu":
                    if event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                        self.vitesse_resolution = max(100, self.vitesse_resolution - 200)
                    elif event.key == pygame.K_MINUS:
                        self.vitesse_resolution = min(2000, self.vitesse_resolution + 200)
                    elif event.key == pygame.K_r:
                        self.hanoi = ToursDeHanoi(NOMBRE_DISQUES)
                        self.hanoi.lancer_resolution()
                        self.temps_derniere_action = pygame.time.get_ticks()
        
        return True
    
    def mettre_a_jour(self):
        """Met à jour la logique du jeu"""
        if self.etat == "jeu" and self.hanoi:
            # Mettre à jour l'animation
            self.hanoi.mettre_a_jour_mouvement()
            
            # Exécuter le mouvement suivant si nécessaire
            temps_actuel = pygame.time.get_ticks()
            if (temps_actuel - self.temps_derniere_action > self.vitesse_resolution and 
                not self.hanoi.mouvement_en_cours and not self.hanoi.resolu):
                self.hanoi.executer_mouvement_suivant()
                self.temps_derniere_action = temps_actuel
    
    def afficher(self):
        """Affiche le jeu selon l'état actuel"""
        if self.etat == "menu":
            self.graphics.afficher_menu(NOMBRE_DISQUES)
        elif self.etat == "jeu":
            self.graphics.afficher_jeu(self.hanoi)
        elif self.etat == "fin":
            self.graphics.afficher_fin(self.hanoi)
        
        self.graphics.mettre_a_jour_affichage()
    
    def executer(self):
        """Boucle principale du jeu"""
        en_cours = True
        
        while en_cours:
            # Gestion des événements
            en_cours = self.gerer_evenements()
            
            # Mise à jour de la logique
            self.mettre_a_jour()
            
            # Affichage
            self.afficher()
        
        # Fermeture
        self.graphics.fermer()
        sys.exit()

def main():
    """Fonction principale"""
    print("Lancement du jeu Tours de Hanoï avec IA récursive...")
    print(f"Nombre de disques : {NOMBRE_DISQUES}")
    print(f"Nombre minimum de mouvements : {2**NOMBRE_DISQUES - 1}")
    
    jeu = Jeu()
    jeu.executer()

if __name__ == "__main__":
    main()