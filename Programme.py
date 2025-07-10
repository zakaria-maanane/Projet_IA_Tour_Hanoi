import pygame
import sys
import time
import math

# Initialisation de Pygame
pygame.init()

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

# Paramètres du jeu
NOMBRE_DISQUES = 4
HAUTEUR_TOUR = 300
LARGEUR_BASE = 200
HAUTEUR_DISQUE = 20
ESPACEMENT_TOURS = 300

class Disque:
    def __init__(self, taille, couleur):
        self.taille = taille
        self.couleur = couleur
        self.x = 0
        self.y = 0
        self.en_mouvement = False
        self.x_cible = 0
        self.y_cible = 0
        self.vitesse = 5

class Tour:
    def __init__(self, x, nom):
        self.x = x
        self.nom = nom
        self.disques = []
        self.y_base = HAUTEUR - 100
    
    def ajouter_disque(self, disque):
        self.disques.append(disque)
        self.positionner_disques()
    
    def retirer_disque(self):
        if self.disques:
            disque = self.disques.pop()
            self.positionner_disques()
            return disque
        return None
    
    def positionner_disques(self):
        for i, disque in enumerate(self.disques):
            disque.x = self.x
            disque.y = self.y_base - (i + 1) * HAUTEUR_DISQUE
    
    def peut_recevoir_disque(self, disque):
        if not self.disques:
            return True
        return disque.taille < self.disques[-1].taille
    
    def dessiner(self, ecran):
        # Dessiner le pilier
        pygame.draw.rect(ecran, MARRON, 
                        (self.x - 10, self.y_base - HAUTEUR_TOUR, 20, HAUTEUR_TOUR))
        
        # Dessiner la base
        pygame.draw.rect(ecran, GRIS,
                        (self.x - LARGEUR_BASE//2, self.y_base, LARGEUR_BASE, 20))
        
        # Dessiner les disques
        for disque in self.disques:
            largeur_disque = 40 + disque.taille * 20
            pygame.draw.rect(ecran, disque.couleur,
                           (disque.x - largeur_disque//2, disque.y, 
                            largeur_disque, HAUTEUR_DISQUE))
            # Bordure
            pygame.draw.rect(ecran, NOIR,
                           (disque.x - largeur_disque//2, disque.y, 
                            largeur_disque, HAUTEUR_DISQUE), 2)

class ToursDeHanoi:
    def __init__(self, nombre_disques):
        self.nombre_disques = nombre_disques
        self.tours = [
            Tour(200, "A"),
            Tour(500, "B"), 
            Tour(800, "C")
        ]
        
        # Couleurs pour les disques
        couleurs = [ROUGE, VERT, BLEU, JAUNE, ORANGE, VIOLET, CYAN, ROSE]
        
        # Initialiser les disques sur la première tour
        for i in range(nombre_disques):
            taille = nombre_disques - i
            couleur = couleurs[i % len(couleurs)]
            disque = Disque(taille, couleur)
            self.tours[0].ajouter_disque(disque)
        
        self.mouvements = []
        self.index_mouvement = 0
        self.mouvement_en_cours = False
        self.disque_en_mouvement = None
        self.resolu = False
        self.nombre_mouvements = 0
        
    def resoudre_recursif(self, n, source, destination, auxiliaire):
        """Algorithme récursif pour résoudre les Tours de Hanoï"""
        if n == 1:
            # Cas de base : déplacer un seul disque
            self.mouvements.append((source, destination))
        else:
            # Déplacer n-1 disques vers la tour auxiliaire
            self.resoudre_recursif(n-1, source, auxiliaire, destination)
            
            # Déplacer le disque le plus grand vers la destination
            self.mouvements.append((source, destination))
            
            # Déplacer les n-1 disques de la tour auxiliaire vers la destination
            self.resoudre_recursif(n-1, auxiliaire, destination, source)
    
    def lancer_resolution(self):
        """Lance la résolution automatique"""
        self.mouvements = []
        self.resoudre_recursif(self.nombre_disques, 0, 2, 1)
        self.index_mouvement = 0
        self.mouvement_en_cours = False
        self.nombre_mouvements = 0
    
    def executer_mouvement_suivant(self):
        """Exécute le mouvement suivant de la solution"""
        if self.index_mouvement < len(self.mouvements) and not self.mouvement_en_cours:
            source, destination = self.mouvements[self.index_mouvement]
            
            # Prendre le disque de la tour source
            disque = self.tours[source].retirer_disque()
            if disque:
                self.disque_en_mouvement = disque
                self.mouvement_en_cours = True
                self.tour_destination = destination
                self.nombre_mouvements += 1
                
                # Définir la position cible
                disque.x_cible = self.tours[destination].x
                disque.y_cible = (self.tours[destination].y_base - 
                                 (len(self.tours[destination].disques) + 1) * HAUTEUR_DISQUE)
    
    def mettre_a_jour_mouvement(self):
        """Met à jour l'animation du mouvement en cours"""
        if self.mouvement_en_cours and self.disque_en_mouvement:
            disque = self.disque_en_mouvement
            
            # Déplacement horizontal
            if abs(disque.x - disque.x_cible) > disque.vitesse:
                if disque.x < disque.x_cible:
                    disque.x += disque.vitesse
                else:
                    disque.x -= disque.vitesse
            else:
                disque.x = disque.x_cible
            
            # Déplacement vertical
            if abs(disque.y - disque.y_cible) > disque.vitesse:
                if disque.y < disque.y_cible:
                    disque.y += disque.vitesse
                else:
                    disque.y -= disque.vitesse
            else:
                disque.y = disque.y_cible
            
            # Vérifier si le mouvement est terminé
            if disque.x == disque.x_cible and disque.y == disque.y_cible:
                self.tours[self.tour_destination].ajouter_disque(disque)
                self.mouvement_en_cours = False
                self.disque_en_mouvement = None
                self.index_mouvement += 1
                
                # Vérifier si le puzzle est résolu
                if len(self.tours[2].disques) == self.nombre_disques:
                    self.resolu = True
    
    def dessiner(self, ecran):
        # Dessiner les tours
        for tour in self.tours:
            tour.dessiner(ecran)
        
        # Dessiner le disque en mouvement
        if self.disque_en_mouvement:
            disque = self.disque_en_mouvement
            largeur_disque = 40 + disque.taille * 20
            pygame.draw.rect(ecran, disque.couleur,
                           (disque.x - largeur_disque//2, disque.y, 
                            largeur_disque, HAUTEUR_DISQUE))
            pygame.draw.rect(ecran, NOIR,
                           (disque.x - largeur_disque//2, disque.y, 
                            largeur_disque, HAUTEUR_DISQUE), 2)
        
        # Dessiner les labels des tours
        font = pygame.font.Font(None, 48)
        for i, tour in enumerate(self.tours):
            label = font.render(f"Tour {chr(65+i)}", True, BLANC)
            label_rect = label.get_rect(center=(tour.x, HAUTEUR - 50))
            ecran.blit(label, label_rect)

class Jeu:
    def __init__(self):
        self.ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
        pygame.display.set_caption("Tours de Hanoï - IA Récursive")
        self.horloge = pygame.time.Clock()
        self.police = pygame.font.Font(None, 48)
        self.police_petite = pygame.font.Font(None, 32)
        self.etat = "menu"  # menu, jeu, fin
        self.hanoi = None
        self.temps_derniere_action = 0
        self.vitesse_resolution = 1000  # millisecondes entre chaque mouvement
        
    def afficher_menu(self):
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
            f"• Nombre de disques : {NOMBRE_DISQUES}",
            f"• Nombre minimum de mouvements : {2**NOMBRE_DISQUES - 1}"
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
        
    def afficher_jeu(self):
        self.ecran.fill(NOIR)
        
        # Dessiner le jeu
        self.hanoi.dessiner(self.ecran)
        
        # Afficher les statistiques
        mouvements_text = f"Mouvements : {self.hanoi.nombre_mouvements}"
        mouvements_optimal = f"Optimal : {2**NOMBRE_DISQUES - 1}"
        progres = f"Progression : {self.hanoi.index_mouvement}/{len(self.hanoi.mouvements)}"
        
        texte_mouv = self.police_petite.render(mouvements_text, True, BLANC)
        texte_opt = self.police_petite.render(mouvements_optimal, True, GRIS)
        texte_prog = self.police_petite.render(progres, True, JAUNE)
        
        self.ecran.blit(texte_mouv, (20, 20))
        self.ecran.blit(texte_opt, (20, 50))
        self.ecran.blit(texte_prog, (20, 80))
        
        # Afficher le statut
        if self.hanoi.resolu:
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
        
    def afficher_fin(self):
        self.ecran.fill(NOIR)
        
        # Message de fin
        fin = self.police.render("PUZZLE RÉSOLU !", True, VERT)
        fin_rect = fin.get_rect(center=(LARGEUR//2, HAUTEUR//2 - 100))
        self.ecran.blit(fin, fin_rect)
        
        # Statistiques finales
        stats = [
            f"Nombre de disques : {NOMBRE_DISQUES}",
            f"Mouvements effectués : {self.hanoi.nombre_mouvements}",
            f"Mouvements optimaux : {2**NOMBRE_DISQUES - 1}",
            f"Efficacité : {'Parfait!' if self.hanoi.nombre_mouvements == 2**NOMBRE_DISQUES - 1 else 'Acceptable'}"
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
        
    def gerer_evenements(self):
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
        if self.etat == "jeu" and self.hanoi:
            # Mettre à jour l'animation
            self.hanoi.mettre_a_jour_mouvement()
            
            # Exécuter le mouvement suivant si nécessaire
            temps_actuel = pygame.time.get_ticks()
            if (temps_actuel - self.temps_derniere_action > self.vitesse_resolution and 
                not self.hanoi.mouvement_en_cours and not self.hanoi.resolu):
                self.hanoi.executer_mouvement_suivant()
                self.temps_derniere_action = temps_actuel
    
    def executer(self):
        en_cours = True
        
        while en_cours:
            en_cours = self.gerer_evenements()
            self.mettre_a_jour()
            
            # Affichage selon l'état
            if self.etat == "menu":
                self.afficher_menu()
            elif self.etat == "jeu":
                self.afficher_jeu()
            elif self.etat == "fin":
                self.afficher_fin()
            
            pygame.display.flip()
            self.horloge.tick(FPS)
        
        pygame.quit()
        sys.exit()

# Lancement du jeu
if __name__ == "__main__":
    jeu = Jeu()
    jeu.executer()