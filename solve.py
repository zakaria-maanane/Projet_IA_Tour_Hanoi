#solve.py - 
# 
# Logique de résolution des Tours de Hanoï

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
        self.y_base = 600  # Position de base
    
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
        hauteur_disque = 20
        for i, disque in enumerate(self.disques):
            disque.x = self.x
            disque.y = self.y_base - (i + 1) * hauteur_disque
    
    def peut_recevoir_disque(self, disque):
        if not self.disques:
            return True
        return disque.taille < self.disques[-1].taille

class ToursDeHanoi:
    def __init__(self, nombre_disques):
        self.nombre_disques = nombre_disques
        self.tours = [
            Tour(200, "A"),
            Tour(500, "B"), 
            Tour(800, "C")
        ]
        
        # Couleurs pour les disques
        couleurs = [
            (255, 0, 0),    # ROUGE
            (0, 255, 0),    # VERT
            (0, 0, 255),    # BLEU
            (255, 255, 0),  # JAUNE
            (255, 165, 0),  # ORANGE
            (128, 0, 128),  # VIOLET
            (0, 255, 255),  # CYAN
            (255, 192, 203) # ROSE
        ]
        
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
                                 (len(self.tours[destination].disques) + 1) * 20)
    
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