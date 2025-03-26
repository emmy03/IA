import sys
import random
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QSpinBox, QGridLayout
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# Liste des villes
continents = [
    "Paris", "Berlin", "Madrid", "Rome", "Londres", "Amsterdam", "Vienne", "Lisbonne", "Stockholm", "Oslo", "Bruxelles", "Athènes", "Copenhague", "Varsovie", "Budapest", "Prague", "Helsinki", "Dublin", "Zagreb", "Belgrade", "Bucarest", "Sarajevo", "Washington, D.C.", "New York", "Toronto", "Mexico", "Montréal", "Los Angeles", "Vancouver", "Chicago", "San Francisco", "Miami", "Boston", "Houston", "Calgary", "Ottawa", "Dallas", "Philadelphie", "Kingston", "Guatemala", "Buenos Aires", "São Paulo", "Rio de Janeiro", "Lima", "Bogotá", "Santiago", "Caracas", "Quito", "La Paz", "Montevideo", "Asunción", "Georgetown", "Brasília", "Medellín", "Cali", "São Salvador", "Tokyo", "Pékin", "New Delhi", "Séoul", "Bangkok", "Kuala Lumpur", "Hanoï", "Singapour", "Jakarta", "Manille", "Dhaka", "Islamabad", "Karachi", "Lahore", "Tachkent", "Le Caire", "Lagos", "Kinshasa", "Nairobi", "Johannesburg", "Alger", "Addis-Abeba", "Le Cap", "Abidjan", "Dakar", "Accra", "Casablanca", "Tunis", "Luanda", "Kigali", "Douala", "Harare", "Dar es Salaam", "Ouagadougou"
    ]

# A OPTIMISER !!! PEUT-ETRE AVEC DES THREADS
class algo_genetique:
    def __init__(self, villes, population_size=90, generations=500, mutation_rate=0.01):
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



class VoyageurDeCommerceUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Optimisation du Voyageur de Commerce")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        # Bloc 1 : Texte descriptif du projet
        objectif_label = QLabel(
            "L'Objectif de l'IA :\n"
            "Le projet du Voyageur de commerce utilise des algorithmes génétiques pour résoudre le problème d'optimisation du parcours entre plusieurs villes.\n"
            "L'algorithme simule l'évolution naturelle en générant une population de solutions, puis sélectionne, croise et mute ces solutions pour améliorer progressivement le parcours.\n"
            "Le but est de minimiser la distance totale parcourue.\n"
            "L'interface permet de choisir les villes à visiter et d'afficher le chemin optimal trouvé."
        )
        layout.addWidget(objectif_label)

        # Sélection du nombre de villes
        grid_layout = QGridLayout()
        self.n_label = QLabel("Nombre de villes :")
        self.n_input = QSpinBox()
        self.n_input.setRange(3, len(continents))  # Minimum 3 villes
        self.n_input.setValue(10)  # Valeur par défaut

        grid_layout.addWidget(self.n_label, 0, 0)
        grid_layout.addWidget(self.n_input, 0, 1)
        layout.addLayout(grid_layout)

        # Bouton pour générer et afficher les villes
        self.btn_generer = QPushButton("Générer les villes")
        self.btn_generer.clicked.connect(self.generer_villes)
        layout.addWidget(self.btn_generer)

        # Bouton pour exécuter l'algorithme génétique
        self.btn_optimiser = QPushButton("Optimiser le chemin")
        self.btn_optimiser.clicked.connect(self.optimiser_chemin)
        layout.addWidget(self.btn_optimiser)

        # Graphique Matplotlib
        self.figure, self.ax = plt.subplots(figsize=(5, 5))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.setLayout(layout)

    def generer_villes(self):
        N = self.n_input.value()
        max_x = max_y = N * 10  # Ajustement dynamique de la taille de l'espace

        # Sélection aléatoire des villes sans doublons
        villes_choisies = random.sample(continents, N)

        # Génération aléatoire des villes
        self.villes = {ville: (random.randint(0, max_x), random.randint(0, max_y)) for ville in villes_choisies}

        # Affichage du graphe
        self.ax.clear()
        x, y = zip(*self.villes.values())
        self.ax.scatter(x, y, c='blue', marker='o', label="Villes")

        for ville, (xi, yi) in self.villes.items():
            self.ax.text(xi + 2, yi + 2, ville, fontsize=8, color="black")

        self.ax.set_xlim(0, max_x + 10)
        self.ax.set_ylim(0, max_y + 10)
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.set_title(f"Génération de {N} villes aléatoires")
        self.ax.legend()

        self.canvas.draw()  # Mettre à jour le graphique dans l'interface

    def optimiser_chemin(self):
        algo = algo_genetique(self.villes)
        best_chemin, best_distance = algo.run()

        # Affichage du chemin optimal
        self.ax.clear()
        x, y = zip(*self.villes.values())
        self.ax.scatter(x, y, c='blue', marker='o', label="Villes")

        for i in range(len(best_chemin) - 1):
            ville_actuelle = self.villes[best_chemin[i]]
            ville_suivante = self.villes[best_chemin[i + 1]]
            self.ax.plot([ville_actuelle[0], ville_suivante[0]], [ville_actuelle[1], ville_suivante[1]], 'r--')

        # Ajouter la ligne pour revenir à la première ville
        ville_actuelle = self.villes[best_chemin[-1]]
        ville_suivante = self.villes[best_chemin[0]]
        self.ax.plot([ville_actuelle[0], ville_suivante[0]], [ville_actuelle[1], ville_suivante[1]], 'r--')

        # Ajouter les noms des villes
        for ville, (xi, yi) in self.villes.items():
            self.ax.text(xi + 2, yi + 2, ville, fontsize=8, color="black")

        self.ax.set_xlim(0, max(x) + 10)
        self.ax.set_ylim(0, max(y) + 10)
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.set_title(f"Chemin optimal trouvé : Distance = {best_distance:.2f}")

        self.canvas.draw()  # Mettre à jour le graphique dans l'interface

    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VoyageurDeCommerceUI()
    window.show()
    sys.exit(app.exec())