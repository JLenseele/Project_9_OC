<a name="readme-top"></a>
# LITReview

Application Web permettant à une communeauté d'utilisateurs de consulter ou de solliciter une critique de livres à la demande.

## Features

- Création / Connexion de compte 
- Demander des critiques de livres ou d’articles, en créant un ticket 
- Publier des critiques de livres ou d’articles
- Voir, modifier et supprimer ses propres tickets et commentaires
- Suivre les autres utilisateurs en entrant leur nom d'utilisateur
- Voir qui il suit et suivre qui il veut

## Requirements

+ [Python v3+](https://www.python.org/downloads/)

## Installation & Get Started

#### Récuperer le projet sur GitHub

    git clone https://github.com/JLenseele/Project_9_OC
    cd Project_9_OC

#### Créer l'environement virtuel

    python -m venv env
    env\Scripts\activate
    pip install -r requierments.txt
    
#### (Optionnel - rapport Flake8)  
Il est possible de générer un nouveau rapport via la commande suivante :  
Le rapport sera disponible dans ./flake-report/index.html

    flake8 --format=html --htmldir=flake-report
    
#### Lancer le serveur

    python LITReview\manage.py runserver

## Utilisation

Depuis votre navigateur, ouvrez l'URL suivant : 

    127.0.0.1:8000/ (application web)  
    
    127.0.0.1:8000/admin/ (systeme d'administration Django accessible avec le compte superuser)  
    
    
Vous pourrez ensuite vous connecter avec l'un des identifiants suivant :  
  Antoine  
	Fabrice  
	Helene  
	Julien  
	Marc  
	Noemie  
	IAmAdmin (compte superuser)  
  
Le mot de passe est identique pour tout les comptes :  

    Axr235689

## Fonctionnalités de l'application

### Page Login / Signup

La page de connexion sera le première affiché depuis 127.0.0.1:8000/  
Elle vous permet de choisir de vous connecter via un compte ci dessus, ou d'inscrire un nouvel utilisateur  

### Page flux

Une fois connecté, la page de flux s'affichera automatiquement.
Sur cette page, vous y verrez vos propres ticket et critique, ainsi que ceux créé par les utilisateurs que vous suivez.

Vous verrez également les réponses à vos ticket d'utilisateurs que vous ne suivez pas.

### Page Post

Cette page affiche l'intégralité de vos posts.  
C'est à partir de cette page que vous pourrez modifier ou supprimer vos différents post.

### Page Abonnement

Cette page affiche la liste des utilisateurs que vous suivez et qui vous suivent.  
Vous avez la possibilité de vous désabonner des utilisateurs que vous suivez.  

Un formulaire est également à disposition pour saisir le nom d'un utilisateur que vous souhaitez suivre.  

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contributors

[JLenseele](https://github.com/JLenseele)
