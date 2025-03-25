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
class algo_genetique():
    def generate_initial_population(villes, population_size):
        population = []
        for _ in range(population_size):
            chemin = list(villes.keys())
            random.shuffle(chemin)
            population.append(chemin)
        print(population)
        return population
    
    def calculate_distance(chemin, villes):
        distance = 0
        for i in range(len(chemin) - 1):
            ville_actuelle = villes[chemin[i]]
            ville_suivante = villes[chemin[i + 1]]
            distance += ((ville_actuelle[0] - ville_suivante[0]) ** 2 + (ville_actuelle[1] - ville_suivante[1]) ** 2) ** 0.5
            
        # Ajouter la distance pour revenir à la première ville
        ville_actuelle = villes[chemin[-1]]
        ville_suivante = villes[chemin[0]]
        distance += ((ville_actuelle[0] - ville_suivante[0]) ** 2 + (ville_actuelle[1] - ville_suivante[1]) ** 2) ** 0.5
        print(distance)
        return distance

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
        self.n_input.setRange(3, len(continents))  # Minimum 5 villes
        self.n_input.setValue(10)  # Valeur par défaut

        grid_layout.addWidget(self.n_label, 0, 0)
        grid_layout.addWidget(self.n_input, 0, 1)
        layout.addLayout(grid_layout)

        # Bouton pour générer et afficher les villes
        self.btn_generer = QPushButton("Générer les villes")
        self.btn_generer.clicked.connect(self.generer_villes)
        layout.addWidget(self.btn_generer)

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
            self.ax.text(xi + 2, yi + 2, ville, fontsize=8, color="red")

        self.ax.set_xlim(0, max_x)
        self.ax.set_ylim(0, max_y)
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.set_title(f"Génération de {N} villes aléatoires")
        self.ax.legend()

        self.canvas.draw()  # Mettre à jour le graphique dans l'interface

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VoyageurDeCommerceUI()
    window.show()
    sys.exit(app.exec())
