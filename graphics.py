# graphics.py - Affichage graphique avec Pygame

import pygame

# Constantes
LARGEUR = 1000
HAUTEUR = 700
FPS = 60

# Couleurs
NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
ROUGE = (255, 0, 0)
VERT = (0, 255, 0)
BLEU = (0, 0, 255)
JAUNE = (255, 255, 0)
GRIS = (128, 128, 128)
ORANGE = (255, 165, 0)
MARRON = (139, 69, 19)
VIOLET = (128, 0, 128)
CYAN = (0, 255, 255)
ROSE = (255, 192, 203)

# Paramètres graphiques
HAUTEUR_TOUR = 300
LARGEUR_BASE = 200
HAUTEUR_DISQUE = 20

class GraphicsManager:
    def __init__(self):
        pygame.init()
        self.ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
        pygame.display.set_caption("Tours de Hanoï - IA Récursive")
        self.horloge = pygame.time.Clock()
        self.police = pygame.font.Font(None, 48)
        self.police_petite = pygame.font.Font(None, 32)
        
    def dessiner_tour(self, tour):
        """Dessine une tour avec ses disques"""
        # Dessiner le pilier
        pygame.draw.rect(self.ecran, MARRON, 
                        (tour.x - 10, tour.y_base - HAUTEUR_TOUR, 20, HAUTEUR_TOUR))
        
        # Dessiner la base
        pygame.draw.rect(self.ecran, GRIS,
                        (tour.x - LARGEUR_BASE//2, tour.y_base, LARGEUR_BASE, 20))
        
        # Dessiner les disques
        for disque in tour.disques:
            largeur_disque = 40 + disque.taille * 20
            pygame.draw.rect(self.ecran, disque.couleur,
                           (disque.x - largeur_disque//2, disque.y, 
                            largeur_disque, HAUTEUR_DISQUE))
            # Bordure
            pygame.draw.rect(self.ecran, NOIR,
                           (disque.x - largeur_disque//2, disque.y, 
                            largeur_disque, HAUTEUR_DISQUE), 2)
    
    def dessiner_disque_volant(self, disque):
        """Dessine un disque en mouvement"""
        if disque:
            largeur_disque = 40 + disque.taille * 20
            pygame.draw.rect(self.ecran, disque.couleur,
                           (disque.x - largeur_disque//2, disque.y, 
                            largeur_disque, HAUTEUR_DISQUE))
            pygame.draw.rect(self.ecran, NOIR,
                           (disque.x - largeur_disque//2, disque.y, 
                            largeur_disque, HAUTEUR_DISQUE), 2)
    
    def dessiner_labels_tours(self, tours):
        """Dessine les labels des tours"""
        for i, tour in enumerate(tours):
            label = self.police.render(f"Tour {chr(65+i)}", True, BLANC)
            label_rect = label.get_rect(center=(tour.x, HAUTEUR - 50))
            self.ecran.blit(label, label_rect)
    
    def afficher_menu(self, nombre_disques):
        """Affiche le menu principal"""
        self.ecran.fill(NOIR)
        
        # Titre
        titre = self.police.render("TOURS DE HANOÏ", True, BLANC)
        titre_rect = titre.get_rect(center=(LARGEUR//2, HAUTEUR//2 - 150))
        self.ecran.blit(titre, titre_rect)
        
        # Sous-titre
        sous_titre = self.police_petite.render("L'IA va résoudre automatiquement le puzzle", True, GRIS)
        sous_titre_rect = sous_titre.get_rect(center=(LARGEUR//2, HAUTEUR//2 - 100))
        self.ecran.blit(sous_titre, sous_titre_rect)
        
        # Explication
        explication = [
            "Règles du jeu :",
            "• Déplacer tous les disques de la tour A vers la tour C",
            "• Un seul disque à la fois",
            "• Un disque plus grand ne peut pas être sur un plus petit",
            f"• Nombre de disques : {nombre_disques}",
            f"• Nombre minimum de mouvements : {2**nombre_disques - 1}"
        ]
        
        for i, ligne in enumerate(explication):
            texte = self.police_petite.render(ligne, True, BLANC)
            texte_rect = texte.get_rect(center=(LARGEUR//2, HAUTEUR//2 - 50 + i*30))
            self.ecran.blit(texte, texte_rect)
        
        # Instructions
        instruction = self.police_petite.render("Appuyez sur ESPACE pour commencer", True, VERT)
        instruction_rect = instruction.get_rect(center=(LARGEUR//2, HAUTEUR//2 + 120))
        self.ecran.blit(instruction, instruction_rect)
        
        # Quitter
        quitter = self.police_petite.render("Appuyez sur ECHAP pour quitter", True, ROUGE)
        quitter_rect = quitter.get_rect(center=(LARGEUR//2, HAUTEUR//2 + 160))
        self.ecran.blit(quitter, quitter_rect)
        
    def afficher_jeu(self, hanoi):
        """Affiche le jeu en cours"""
        self.ecran.fill(NOIR)
        
        # Dessiner les tours
        for tour in hanoi.tours:
            self.dessiner_tour(tour)
        
        # Dessiner le disque en mouvement
        self.dessiner_disque_volant(hanoi.disque_en_mouvement)
        
        # Dessiner les labels des tours
        self.dessiner_labels_tours(hanoi.tours)
        
        # Afficher les statistiques
        mouvements_text = f"Mouvements : {hanoi.nombre_mouvements}"
        mouvements_optimal = f"Optimal : {2**hanoi.nombre_disques - 1}"
        progres = f"Progression : {hanoi.index_mouvement}/{len(hanoi.mouvements)}"
        
        texte_mouv = self.police_petite.render(mouvements_text, True, BLANC)
        texte_opt = self.police_petite.render(mouvements_optimal, True, GRIS)
        texte_prog = self.police_petite.render(progres, True, JAUNE)
        
        self.ecran.blit(texte_mouv, (20, 20))
        self.ecran.blit(texte_opt, (20, 50))
        self.ecran.blit(texte_prog, (20, 80))
        
        # Afficher le statut
        if hanoi.resolu:
            statut = "RÉSOLU ! Appuyez sur ESPACE pour continuer"
            couleur = VERT
        else:
            statut = "Résolution en cours par l'IA récursive..."
            couleur = JAUNE
        
        texte_statut = self.police_petite.render(statut, True, couleur)
        statut_rect = texte_statut.get_rect(center=(LARGEUR//2, 30))
        self.ecran.blit(texte_statut, statut_rect)
        
        # Afficher les contrôles
        controles = ["+ : Accélérer", "- : Ralentir", "R : Recommencer"]
        for i, controle in enumerate(controles):
            texte = self.police_petite.render(controle, True, GRIS)
            self.ecran.blit(texte, (LARGEUR - 200, 20 + i*30))
        
    def afficher_fin(self, hanoi):
        """Affiche l'écran de fin"""
        self.ecran.fill(NOIR)
        
        # Message de fin
        fin = self.police.render("PUZZLE RÉSOLU !", True, VERT)
        fin_rect = fin.get_rect(center=(LARGEUR//2, HAUTEUR//2 - 100))
        self.ecran.blit(fin, fin_rect)
        
        # Statistiques finales
        stats = [
            f"Nombre de disques : {hanoi.nombre_disques}",
            f"Mouvements effectués : {hanoi.nombre_mouvements}",
            f"Mouvements optimaux : {2**hanoi.nombre_disques - 1}",
            f"Efficacité : {'Parfait!' if hanoi.nombre_mouvements == 2**hanoi.nombre_disques - 1 else 'Acceptable'}"
        ]
        
        for i, stat in enumerate(stats):
            texte = self.police_petite.render(stat, True, BLANC)
            texte_rect = texte.get_rect(center=(LARGEUR//2, HAUTEUR//2 - 20 + i*40))
            self.ecran.blit(texte, texte_rect)
        
        # Instructions
        instruction = self.police_petite.render("Appuyez sur ESPACE pour recommencer", True, VERT)
        instruction_rect = instruction.get_rect(center=(LARGEUR//2, HAUTEUR//2 + 120))
        self.ecran.blit(instruction, instruction_rect)
        
        quitter = self.police_petite.render("Appuyez sur ECHAP pour quitter", True, ROUGE)
        quitter_rect = quitter.get_rect(center=(LARGEUR//2, HAUTEUR//2 + 160))
        self.ecran.blit(quitter, quitter_rect)
    
    def mettre_a_jour_affichage(self):
        """Met à jour l'affichage"""
        pygame.display.flip()
        self.horloge.tick(FPS)
    
    def fermer(self):
        """Ferme Pygame"""
        pygame.quit()