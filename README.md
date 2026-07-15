<div align="center">

#  TrocLivre

### Plateforme web communautaire d'échange, de don et de vente de livres

Projet universitaire réalisé individuellement dans le cadre de la Licence 2 Informatique.

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-black?logo=flask)
![SQLite](https://img.shields.io/badge/SQLite-blue?logo=sqlite)
![HTML5](https://img.shields.io/badge/HTML5-orange?logo=html5)
![CSS3](https://img.shields.io/badge/CSS3-blue?logo=css3)
![JavaScript](https://img.shields.io/badge/JavaScript-yellow?logo=javascript)

</div>

---

# Présentation

TrocLivre est une application web développée individuellement ayant pour objectif de favoriser la réutilisation des livres grâce à une plateforme communautaire de partage.

Les utilisateurs peuvent publier des ouvrages à vendre, à donner ou à prêter, consulter les annonces disponibles, gérer leurs livres, échanger avec les autres membres via une messagerie intégrée et suivre leurs différentes transactions.

Ce projet m'a permis de développer une application web complète en réalisant l'ensemble des couches de l'application : conception de la base de données, développement Backend, création des interfaces Frontend et intégration des fonctionnalités métiers.

---

# Fonctionnalités principales

| Fonctionnalité | Description |
|----------------|-------------|
| Authentification | Création de compte et connexion sécurisée |
| Bibliothèque | Consultation de l'ensemble des livres disponibles |
| Gestion des livres | Publication, modification et suppression d'annonces |
| Vente et don | Mise en vente ou don d'un ouvrage |
| Favoris | Sauvegarde des livres favoris |
| Messagerie | Communication entre utilisateurs |
| Profil | Consultation et modification des informations personnelles |
| Transactions | Historique des échanges réalisés |

---

# Technologies utilisées

| Catégorie | Technologies |
|-----------|--------------|
| Backend | Python • Flask |
| Frontend | HTML5 • CSS3 • JavaScript |
| Base de données | SQLite |
| Moteur de templates | Jinja2 |
| Outils | Git • GitHub |

---

# Architecture technique

```text
                     Utilisateur
                          │
                          ▼
              HTML • CSS • JavaScript
                          │
                          ▼
                 Flask (Python Backend)
                          │
                          ▼
                       SQLite
```

---

# Aperçu de l'application

## Accueil

### Accueil (visiteur)

Interface d'accueil présentant la plateforme et permettant d'accéder aux livres disponibles.

![](images/home-guest.png)

---

### Connexion

Authentification d'un utilisateur existant.

![](images/login.png)

---

### Inscription

Création d'un nouveau compte utilisateur.

![](images/register.png)

---

### Accueil (utilisateur connecté)

Accueil personnalisé après authentification.

![](images/home-user.png)

---

## Gestion des livres

### Choix d'une annonce

Sélection du type d'annonce : don ou vente.

![](images/book-options.png)

---

### Ajouter un livre à vendre

Création d'une annonce de vente.

![](images/add-book-sell.png)

---

### Ajouter un livre à donner

Publication d'un livre en don.

![](images/add-book-donate.png)

---

### Bibliothèque

Consultation des livres proposés par la communauté.

![](images/library.png)

---

### Mes livres

Gestion des ouvrages publiés.

![](images/my-books.png)

---

### Favoris

Consultation des livres enregistrés en favoris.

![](images/favorites.png)

---

## Profil utilisateur

Gestion des informations personnelles et accès à l'historique.

![](images/profile.png)

---

## Messagerie

### Liste des conversations

Visualisation des échanges avec les autres utilisateurs.

![](images/messages.png)

---

### Discussion

Messagerie permettant de communiquer directement avec un utilisateur.

![](images/conversation.png)

---

# Structure du projet

```text
TrocLivre
│
├── static/
│   ├── css/
│   ├── images/
│   └── js/
│
├── templates/
│
├── app.py
├── create_db.py
├── data_model.py
└── README.md
```

---

# Installation

```bash
git clone https://github.com/Lyna-NAILI14/TrocLivre.git

cd TrocLivre

pip install flask

python app.py
```

L'application est ensuite accessible à l'adresse :

```text
http://127.0.0.1:5000
```

---

# Compétences développées

Au travers de ce projet, j'ai développé les compétences suivantes :

- Développement Backend avec Flask
- Conception d'une base de données SQLite
- Développement d'interfaces web avec HTML, CSS et JavaScript
- Gestion de l'authentification utilisateur
- Manipulation des données avec Python
- Organisation d'un projet web complet
- Utilisation de Git et GitHub

---

# À propos

Ce projet a été réalisé dans le cadre de ma deuxième année de Licence Informatique.

Le code source est disponible à des fins de démonstration de mes compétences et d'illustration de mon parcours académique.
