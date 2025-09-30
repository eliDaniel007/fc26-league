# ⚽ FC 26 League - Système NBA FIFA

Une application web de gestion de ligue FIFA avec système NBA pour 5 joueurs.

## 🏆 Fonctionnalités

- **👥 5 Joueurs fixes** : ABOUBACAR, DIOGO, LIONEL, CHERIF, ELI
- **📅 Système de semaines** : 4 matchs par joueur par semaine
- **📊 Double classement** : Hebdomadaire et cumulé depuis le début
- **⚽ Moyenne de buts** : Intégrée dans le calcul des classements
- **💾 Persistance** : Toutes les données sont sauvegardées automatiquement
- **📱 Interface responsive** : Moderne avec design glassmorphism

## 🚀 Installation Locale

### Prérequis
- Python 3.8+
- pip

### Installation
```bash
# Cloner le projet
git clone https://github.com/VOTRE-USERNAME/fc26-league.git
cd fc26-league

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
python app.py
```

### Accès
- Local: http://localhost:8000
- Réseau: http://[VOTRE-IP]:8000

## 📋 Comment jouer

1. **Gérer les joueurs** : Les 5 joueurs sont pré-configurés
2. **Générer une semaine** : Crée 10 matchs automatiquement (4 par joueur)
3. **Saisir les résultats** : Directement sur la page d'accueil
4. **Voir les classements** : Hebdomadaire et cumulé en temps réel
5. **Passer à la semaine suivante** : Une fois tous les matchs terminés

## 🎯 Système NBA

- **5 joueurs maximum** actifs simultanément
- **4 matchs par joueur** par semaine
- **Classement par points** : Victoire = 3pts, Nul = 1pt, Défaite = 0pt
- **Moyenne de buts** : Critère de départage secondaire
- **Historique complet** : Toutes les saisons sont archivées

## 💾 Sauvegarde

### Automatique
Toutes les données sont automatiquement sauvegardées dans `instance/fifa25.db`

### Manuelle
```bash
# Créer une sauvegarde
python backup_db.py backup

# Lister les sauvegardes
python backup_db.py list

# Restaurer une sauvegarde
python backup_db.py restore <fichier>
```

## 📁 Structure du Projet

```
fc26-league/
├── app.py                 # Application Flask principale
├── backup_db.py          # Script de sauvegarde
├── requirements.txt      # Dépendances Python
├── instance/            # Base de données
│   └── fifa25.db       
├── templates/           # Templates HTML
│   ├── base.html
│   ├── home.html
│   ├── manage_players.html
│   ├── standings.html
│   └── season_history.html
├── backups/            # Sauvegardes automatiques
└── DATA_PERSISTENCE.md # Documentation persistance
```

## 🛠️ Technologies

- **Backend** : Flask (Python)
- **Base de données** : SQLite
- **Frontend** : HTML5, CSS3, JavaScript
- **Design** : Glassmorphism, CSS Grid/Flexbox
- **Icons** : Font Awesome

## 🔧 Configuration

### Variables d'environnement
```bash
# Pour la production
export FLASK_ENV=production
export SECRET_KEY=votre-clé-secrète-très-sécurisée
```

### Base de données
L'application utilise SQLite par défaut. Pour PostgreSQL :
```python
# Dans app.py
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@host:port/database'
```

## 📊 Base de Données

### Tables principales
- **Player** : Joueurs de la ligue
- **Season** : Saisons avec statut actif/terminé  
- **Match** : Tous les matchs avec scores
- **WeeklyStandings** : Classements hebdomadaires archivés

## 🌐 Déploiement

### Heroku
1. Créer un compte Heroku
2. Installer Heroku CLI
3. Suivre les instructions dans `DEPLOY.md`

### Vercel/Netlify
Compatible avec les plateformes serverless (voir documentation déploiement)

### VPS/Serveur
```bash
# Avec gunicorn
pip install gunicorn
gunicorn app:app
```

## 🤝 Contributeurs

- **ABOUBACAR** - Joueur FC 26
- **DIOGO** - Joueur FC 26  
- **LIONEL** - Joueur FC 26
- **CHERIF** - Joueur FC 26
- **ELI** - Joueur FC 26

## 📝 Licence

Ce projet est sous licence MIT. Voir `LICENSE` pour plus de détails.

## 🐛 Support

Pour tout problème ou suggestion :
1. Ouvrir une issue sur GitHub
2. Consulter `DATA_PERSISTENCE.md` pour la gestion des données
3. Utiliser les outils de sauvegarde intégrés

---

**🏆 Que le meilleur gagne ! Bonne chance à tous les joueurs FC 26 ! ⚽**
