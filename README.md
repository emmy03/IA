# IA - Algorithme Génétique pour le TSP

Ce projet implémente un **algorithme génétique** pour résoudre le problème du voyageur de commerce (**TSP**). Il inclut une interface graphique interactive pour visualiser les résultats et optimiser le chemin.

L'objectif est de trouver le chemin le plus court reliant un ensemble de villes en utilisant des techniques comme la sélection, le croisement (PMX) et la mutation.

## Fonctionnalités
- Génération de populations aléatoires.
- Calcul des distances entre les villes (distance euclidienne).
- Sélection des individus les plus adaptés (sélection par tournoi).
- Croisement des individus (Partially Mapped Crossover - PMX).
- Mutation pour introduire de la diversité (mutation par échange).
- Visualisation graphique des résultats sur une carte mondiale avec **Cartopy**.
- Interface utilisateur interactive avec **PyQt6**.

## Prérequis
- Python 3.x
- Bibliothèques nécessaires :
  - `matplotlib`
  - `PyQt6`
  - `cartopy`

## Instructions d'utilisation
1. Installez les bibliothèques requises avec la commande suivante :
   ```bash
   pip install matplotlib PyQt6 cartopy
```
## Auteur
Projet réalisé dans le cadre de la L3 en Intelligence Artificielle avec [BOUGHRARA Soumaiya](https://github.com/Boughrara-Soumaiya).