### QRCode-wep-app

## Générateur de QR Code


# Description
Ce projet est une application web permettant de générer, gérer et scanner des QR Codes. Développée avec un backend en FastAPI (Python) et une interface frontend en HTML/CSS/JavaScript avec TailwindCSS, cette application offre une expérience utilisateur fluide et responsive, adaptée aux appareils mobiles et desktop. Elle permet de générer des QR Codes personnalisés, de les sauvegarder dans un historique local, de les générer en lot, et de scanner des QR Codes via upload d’image ou caméra.

# Fonctionnalités principales

Génération de QR Codes :

Supporte différents types de données : URL, vCard, Wi-Fi, SMS.
Options avancées : correction d’erreur, version, taille des modules, bordure, couleurs, format (PNG, SVG), style (standard ou arrondi).
Affichage du QR Code généré avec options pour le télécharger ou l’afficher en ASCII/matrice.


Génération par lot :

Génère plusieurs QR Codes à partir d’une liste d’URLs (une par ligne) et les télécharge sous forme d’un fichier ZIP.


Historique :

Stocke les QR Codes générés dans le localStorage du navigateur (jusqu’à 10 entrées).
Affiche une liste des QR Codes avec aperçu et lien de téléchargement.


Scanner de QR Codes :

Permet de scanner un QR Code via un fichier image ou directement avec la caméra de l’appareil.
Utilise la bibliothèque jsQR pour le traitement des images.


# Responsive Design :

Interface optimisée pour mobile et desktop.
Sidebar compacte sur mobile (80px) et disposition en colonne pour une meilleure ergonomie.
Options avancées masquables sur mobile pour réduire le défilement.



## Technologies utilisées

Backend :

FastAPI (Python) pour l’API REST.
Bibliothèques Python : qrcode, Pillow (pour PNG), io, zipfile.


Frontend :

HTML, CSS, JavaScript.
TailwindCSS pour le design.
jsQR pour le scan de QR Codes.
localStorage pour l’historique.

# Utilisation

Générer un QR Code :

Sélectionne le type de données (URL, vCard, etc.), remplis les champs nécessaires, et ajuste les options avancées si besoin.
Clique sur "Générer QR Code" pour voir le résultat. Télécharge ou affiche en ASCII/matrice.


Générer par lot :

Saisis une liste d’URLs (une par ligne) et clique sur "Générer par lot" pour télécharger un fichier ZIP contenant les QR Codes.


Historique :

Les QR Codes générés sont automatiquement sauvegardés dans l’historique (limité à 10 entrées). Clique sur "Historique" pour les voir et les télécharger.


Scanner :

Clique sur "Scanner", puis choisis entre "Upload de fichier" (pour une image) ou "Scan par caméra" (pour utiliser la caméra de ton appareil). Le résultat s’affiche directement.


# Prochaines étapes

Ajout d’une fonctionnalité de partage pour copier le lien d’un QR Code généré.
Personnalisation avancée : ajout d’un logo au centre des QR Codes (côté backend).
Optimisation et sécurité : mise en cache côté serveur et validation renforcée des entrées.
Les propositions de design de l’interface utilisateur sont les bienvenues pour améliorer l’esthétique et l’ergonomie de l’application.

Licence
Ce projet est sous licence GNU General Public License v3.0 (GNU GPLv3.0).
