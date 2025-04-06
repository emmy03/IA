# Gestion de l'environnement d'exécution
import sys
# Génération de donnée aléatoire 
import random
# Gestion application Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QSpinBox, QGridLayout, QTextEdit
# Gestion graphique 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# Gestion carte géographique
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import time

#---===PROJET RESOUDRE LE PROBLÈME TSP AVEC L'ALGORITHME GÉNÉTIQUE===---
# NOM : BOUGHRARA        Prénom : Soumaiya n°:20210765
# NOM : MARIE-JOSEPH     Prénom : Emmy     n°:20213708

# Liste des villes et de leurs coordonnées réelles
villes_coordonnées = {
    "Paris" : (48.862725,2.287592),"Rome" : (41.8933203,12.4829321),"Vienne" : (48.2083537,16.3725042),"Lisbonne" : (38.7077507,-9.1365919),"Stockholm" : (59.3251172,18.0710935),"Athènes" : (37.9755648,23.7348324), "Prague":(50.0874654,14.4212535), "Helsinki":(60.1674881,24.9427473), "Dublin":(53.3493795,-6.2605593), "Belgrade":(44.8178131,20.4568974), "Bucarest":(44.4361414,26.1027202), "Washington, D.C.":(38.8950368,-77.0365427), "Mexico":(19.4326296,-99.1331785), "Montréal":(45.5031824,-73.5698065), "Los Angeles":(34.0536909,-118.242766), "Vancouver":(49.2608724,-123.113952), "San Francisco":(37.7792588,-122.4193286), "Miami":(25.7741728,-80.19362), 
    "Boston":(42.3554334,-71.060511), "Houston":(29.7589382,-95.3676974), "Dallas":(32.7762719,-96.7968559), "Kingston":(17.9712148,-76.7928128), "Guatemala":(15.5855545,-90.345759), "Buenos Aires":(-34.6083696,-58.4440583), "Rio de Janeiro":(-22.9110137,-43.2093727), "Lima": (-12.0621065,-77.0365256), "Santiago":(9.8694792,-83.7980749), "Quito":(-0.2201641,-78.5123274), "La Paz":(-16.4955455,-68.1336229), "Asunción":(-25.2800459,-57.6343814), "Georgetown":(6.8137426,-58.1624465), "Brasília":(-15.7939869,-47.8828), "Medellín":(6.2697324,-75.6025597),"Cali":(3.4519988,-76.5325259), "São Salvador":(13.6989939,-89.1914249), "Tokyo":(35.6768601,139.7638947), "Pékin":(40.190632,116.412144), 
    "New Delhi":(28.6430858,77.2192671), "Séoul":(37.5666791,126.9782914), "Bangkok":(13.7524938,100.4935089), "Kuala Lumpur":(3.1526589,101.7022205), "Hanoï":(21.0283334,105.854041), "Singapour":(1.357107,103.8194992), "Jakarta":(-6.1754049,106.827168), "Manille":(14.5904492,120.9803621), "Dhaka":(23.7643863,90.3890144), "Islamabad":(33.6938118,73.0651511), "Karachi":(24.8546842,67.0207055), "Lahore":(31.5656822,74.3141829), "Tachkent":(41.3123363,69.2787079), "Le Caire":(30.0443879,31.2357257), "Lagos":(6.4550575,3.3941795), "Kinshasa":(-4.3196982,15.3424196), "Nairobi":(-1.2832533,36.8172449), "Johannesburg":(-26.205,28.049722), "Alger":(36.7729333,3.0588445), "Rabat":(34.0218454,-6.8408929), "Le Cap":(-33.9288301,18.4172197), 
    "Dakar":(14.693425,-17.447938), "Luanda":(-8.8272699,13.2439512), "Douala":(4.0429389,9.7062018), "Harare":(-17.8567035,31.0601584), "Dar es Salaam":(-6.8160837,39.2803583), "Ouagadougou":(12.3681873,-1.5270944), "Sydney":(-33.8698439,151.2082848), "Saint-Pétersbourg":(59.9606739,30.1586551), "Nuuk":(64.1766835,-51.7359356), "Vladivostok":(43.1150678,131.8855768), "Port Hedland":(-20.3111814,118.5801181),"Arequipa":(-16.3988667,-71.5369607)
}

# ---=== L'ALGORITHME GÉNÉTIQUE DU PROJET ===---

class algo_genetique:
    def __init__(self, villes, population_size=90, generations=500, mutation_rate=0.1):
        # Initialisation des paramètres de l'algorithme génétique
        self.villes = villes  # Dictionnaire contenant les villes et leurs coordonnées
        self.population_size = population_size  # Taille de la population initiale
        self.generations = generations  # Nombre de générations
        self.mutation_rate = mutation_rate  # Taux de mutation
        self.population = self.generate_initial_population()  # Génération initiale de la population

    def generate_initial_population(self):
        # Générer une population initiale aléatoire
        population = []
        for _ in range(self.population_size):
            chemin = list(self.villes.keys())  # Liste des villes
            random.shuffle(chemin)  # Mélanger aléatoirement les villes pour créer un chemin
            population.append(chemin)  # Ajouter le chemin à la population
        return population

    def calculate_distance(self, chemin):
        # Calculer la distance totale d'un chemin donné
        distance = 0
        for i in range(len(chemin) - 1):
            ville_actuelle = self.villes[chemin[i]]  # Coordonnées de la ville actuelle
            ville_suivante = self.villes[chemin[i + 1]]  # Coordonnées de la ville suivante
            # Calcul de la distance entre deux villes consécutives
            dx = ville_actuelle[0] - ville_suivante[0]
            dy = ville_actuelle[1] - ville_suivante[1]
            distance += (dx ** 2 + dy ** 2) ** 0.5  # Distance euclidienne : racine carrée de (dx^2 + dy^2)

        # Ajouter la distance pour revenir à la première ville
        ville_actuelle = self.villes[chemin[-1]]
        ville_suivante = self.villes[chemin[0]]
        dx = ville_actuelle[0] - ville_suivante[0]
        dy = ville_actuelle[1] - ville_suivante[1]
        distance += (dx ** 2 + dy ** 2) ** 0.5
        return distance

    def selection_tournoi(self, population, k=2):
        # Sélection par tournoi : choisir le meilleur parmi k individus aléatoires
        tournoi = random.sample(population, k)  # Sélection aléatoire de k individus
        tournoi.sort(key=lambda chemin: self.calculate_distance(chemin))  # Trier par distance croissante
        return tournoi[0]  # Retourner le chemin avec la plus petite distance

    def crossover_pmx(self, parent1, parent2):
        # Croisement PMX (Partially Mapped Crossover)
        size = len(parent1)  # Taille des parents (nombre de villes dans le chemin)
        
        # Sélection de deux points de croisement aléatoires
        point1, point2 = sorted(random.sample(range(size), 2))  # Exemple : [2, 5]
        
        # Initialisation de l'enfant avec des valeurs nulles (None)
        child = [None] * size

        # Etape 1 : Copier le segment du premier parent dans l'enfant
        # Exemple : Si parent1 = [A, B, C, D, E, F] et point1=2, point2=5
        # Alors segment copié = [C, D, E]
        child[point1:point2] = parent1[point1:point2]

        # Etape 2 : Compléter les positions restantes avec les valeurs du second parent
        for i in range(size):
            if child[i] is None:  # Si la position est vide
                value = parent2[i]  # Prendre la valeur correspondante du second parent
                
                # Résolution des conflits : Si la valeur existe déjà dans l'enfant
                while value in child:
                    # Trouver une valeur non utilisée en suivant le mapping des parents
                    value = parent2[parent1.index(value)]
                
                # Ajouter la valeur résolue à l'enfant
                child[i] = value

        # Retourner l'enfant, qui est une nouvelle solution valide
        return child

    def mutation_swap(self, chemin):
        # Mutation par échange : échanger deux villes aléatoires
        for i in range(len(chemin)):
            if random.random() < self.mutation_rate:  # Probabilité de mutation
                j = random.randint(0, len(chemin) - 1)  # Sélection d'une autre position aléatoire
                chemin[i], chemin[j] = chemin[j], chemin[i]  # Echanger les positions
        return chemin

    def run(self):
        # Exécution de l'algorithme génétique

        for generation in range(self.generations):
            new_population = []  # Nouvelle population pour la génération suivante

            # Elitisme : conserver les meilleurs individus
            self.population.sort(key=lambda chemin: self.calculate_distance(chemin))  # Trier par distance
            elite_size = int(0.1 * self.population_size)  # 10% de la population est conservée
            new_population.extend(self.population[:elite_size])  # Ajouter les meilleurs chemins à la nouvelle population

            # Générer le reste de la population par croisement et mutation
            while len(new_population) < self.population_size:
                parent1 = self.selection_tournoi(self.population)  # Sélection du premier parent
                parent2 = self.selection_tournoi(self.population)  # Sélection du second parent
                child = self.crossover_pmx(parent1, parent2)  # Croisement des parents
                child = self.mutation_swap(child)  # Mutation de l'enfant
        
                new_population.append(child)  # Ajouter l'enfant à la nouvelle population

            self.population = new_population  # Mettre à jour la population

            # Afficher la distance du meilleur chemin à chaque génération
            best_chemin = min(self.population, key=self.calculate_distance)
            best_distance = self.calculate_distance(best_chemin)
            print(f"Génération {generation + 1}: Distance = {best_distance:.2f}")

        # Retourner le meilleur chemin trouvé
        self.population.sort(key=lambda chemin: self.calculate_distance(chemin))  # Trier la population finale
        best_chemin = self.population[0]  # Meilleur chemin
        best_distance = self.calculate_distance(best_chemin)  # Distance du meilleur chemin
        return best_chemin, best_distance

# ---=== INTERFACE DU PROJET ===---

def dessiner_fond_equirectangulaire(ax):
    # Dessin de la carte du monde simplifié avec Cartopy (Ajouter un fond basique, couleur frontiere des pays, terre, ocean, lacs)
    ax.set_global()  
    ax.add_feature(cfeature.LAND, facecolor='green')  
    ax.add_feature(cfeature.OCEAN, facecolor='lightblue')  
    ax.add_feature(cfeature.LAKES, facecolor='lightblue') 
    
    # Ajout des grilles et labels
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')


class InterfaceUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Optimisation du Voyageur de Commerce")
        self.setGeometry(100, 100, 1200, 700)
        
        layout = QVBoxLayout()

        # 1er bloc: Descriptif
        layout.addWidget(QLabel(
            "L'Objectif de l'IA :\n"
            "Ce projet résout le problème du voyageur de commerce en utilisant un algorithme génétique.\n"
            "Il vise à optimiser l'ordre de visite des villes pour minimiser la distance totale parcourue."
        ))

        #2eme bloc : Sélection du nombre de villes
        grid_layout = QGridLayout()
        self.n_label = QLabel("Nombre de villes :")
        self.n_input = QSpinBox()
        self.n_input.setRange(3, len(villes_coordonnées))
        self.n_input.setValue(10)

        grid_layout.addWidget(self.n_label, 0, 0)
        grid_layout.addWidget(self.n_input, 0, 1)
        layout.addLayout(grid_layout)

        # 3eme bloc :  Boutons
        self.btn_generer = QPushButton("Générer les villes")
        self.btn_generer.clicked.connect(self.generer_villes)
        layout.addWidget(self.btn_generer)

        self.btn_optimiser = QPushButton("Optimiser le chemin")
        self.btn_optimiser.clicked.connect(self.optimiser_chemin)
        layout.addWidget(self.btn_optimiser)


        # 4 eme bloc : Zone Matplotlib
        self.figure, self.ax = plt.subplots(figsize=(9, 5), subplot_kw={'projection': ccrs.PlateCarree()})
        self.canvas = FigureCanvas(self.figure)
        dessiner_fond_equirectangulaire(self.ax)
        self.ax.set_title("Carte du monde - Aucune ville sélectionnée")
        self.canvas.draw()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        #5eme bloc 
        self.result_label = QLabel("Résultat du parcours optimal :")
        layout.addWidget(self.result_label)
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        layout.addWidget(self.result_text)
        self.setLayout(layout)


    def generer_villes(self):
        N = self.n_input.value()
        self.villes_choisies = random.sample(list(villes_coordonnées.keys()), N)

        self.ax.clear()
        dessiner_fond_equirectangulaire(self.ax)

        self.villes = {ville: villes_coordonnées[ville] for ville in self.villes_choisies}

        # Dessiner les villes sur la carte
        for ville, (lat, lon) in self.villes.items():
            self.ax.scatter(lon, lat, color='red', s=50, transform=ccrs.PlateCarree())
            self.ax.text(lon + 2, lat + 2, ville, fontsize=8, color='black', transform=ccrs.PlateCarree())

        self.ax.set_title(f"Carte du monde avec {N} villes générées")
        self.canvas.draw()

    def optimiser_chemin(self):
        # Assurez-vous que les villes sont définies
        if not hasattr(self, 'villes'):
           return
 
        # Appliquer l'algorithme génétique pour optimiser le chemin et calculer son temps d'execution 
        temps = 0
        start = time.perf_counter()
        algo = algo_genetique(self.villes)  
        best_chemin, best_distance = algo.run()  
        end = time.perf_counter()
        temps += end - start
    

        # Effacer le graphique précédent pour redessiner
        self.ax.clear()

        # Utilisation de Cartopy pour afficher la carte
        dessiner_fond_equirectangulaire(self.ax)

        # Extraire les coordonnées des villes
        x, y = zip(*self.villes.values())

        #appeler ligne 
        self.ligne(best_chemin)

        # Dessiner le chemin optimal
        for i in range(len(best_chemin) - 1):
            ville_actuelle = self.villes[best_chemin[i]]
            ville_suivante = self.villes[best_chemin[i + 1]]
            self.ax.plot([ville_actuelle[1], ville_suivante[1]], [ville_actuelle[0], ville_suivante[0]], 'r--')  

        # Ajouter la ligne pour revenir à la première ville (circuit fermé)
        ville_actuelle = self.villes[best_chemin[-1]]
        ville_suivante = self.villes[best_chemin[0]]
        self.ax.plot([ville_actuelle[1], ville_suivante[1]], [ville_actuelle[0], ville_suivante[0]], 'r--')

        # Ajouter les noms des villes (style)
        for ville, (lat, lon) in self.villes.items():
            self.ax.text(lon + 2, lat + 2, ville, fontsize=8, color="black", transform=ccrs.PlateCarree())

        # Mise à jour du titre avec la distance optimale
        self.ax.set_title(f"Chemin optimal trouvé en {temps:.2f} s : Distance = {best_distance:.2f} km")

        # Mettre à jour le graphique dans l'interface
        self.canvas.draw()

    def ligne(self, best_chemin):
        
        chemin_optimisé = " → ".join(best_chemin) + " → Retour au point de départ"

        self.result_text.setText(chemin_optimisé)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InterfaceUI()
    window.show()
    sys.exit(app.exec())
