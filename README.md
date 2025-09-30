# ⚽ FC 26 League - Système NBA FIFA

Une application web moderne pour gérer une ligue FIFA avec système NBA : 5 joueurs, 4 matchs par semaine, classements hebdomadaires et cumulés.

## 🎮 **Fonctionnalités**

- **👥 5 Joueurs Fixes** : ABOUBACAR, DIOGO, LIONEL, CHERIF, ELI
- **📅 Système de Semaines** : Chaque joueur joue 4 matchs par semaine
- **🏆 Double Classement** : Hebdomadaire + Cumulé depuis le début
- **⚽ Moyenne de Buts** : Intégrée dans le calcul des classements
- **💾 Persistance** : Base de données SQLite avec historique complet
- **📱 Interface Responsive** : Compatible mobile et desktop
- **🎨 Design Moderne** : Interface glassmorphism avec animations

## 🚀 **Installation Rapide**

### Prérequis
- Python 3.7+
- Git

### Installation
```bash
# Cloner le repository
git clone [URL_DU_REPO]
cd PROJET-FIFA

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
python app.py
```

### Accès
- **Local** : `http://localhost:8000`
- **Réseau** : `http://[VOTRE_IP]:8000`

## 📱 **Utilisation**

### Première Configuration
1. **Ajoutez vos joueurs** via "Gérer Joueurs"
2. **Générez une semaine** avec "Générer Semaine"
3. **Saisissez les scores** directement sur l'accueil
4. **Consultez les classements** en temps réel

### Navigation
- 🏠 **Accueil** : Vue d'ensemble et saisie des matchs
- 👥 **Gérer Joueurs** : Activation/désactivation des 5 joueurs
- 🏆 **Classements** : Hebdomadaires et cumulés détaillés
- 📚 **Historique** : Archive de toutes les saisons

## 🏆 **Système de Classement**

### Points
- **Victoire** : 3 points
- **Match nul** : 1 point  
- **Défaite** : 0 point

### Critères de Tri
1. **Points** (priorité 1)
2. **Moyenne de buts** (priorité 2)
3. **Différence de buts** (priorité 3)

## 💾 **Sauvegarde des Données**

### Automatique
- Toutes les données sont sauvegardées automatiquement
- Base SQLite dans `instance/fifa25.db`
- Historique complet conservé indéfiniment

### Manuelle
```bash
# Créer une sauvegarde
python backup_db.py backup

# Lister les sauvegardes
python backup_db.py list

# Restaurer une sauvegarde
python backup_db.py restore [fichier]
```

## 🌐 **Accès Réseau/Mobile**

### Configuration Réseau
L'application écoute sur `0.0.0.0:8000` permettant l'accès depuis :
- **Même réseau WiFi** : `http://[IP_DU_PC]:8000`
- **Mobile** : Connecté au même WiFi
- **Autres appareils** : Sur le même réseau local

### Trouver votre IP
```bash
# Windows
ipconfig

# Cherchez "Adresse IPv4" de votre connexion WiFi
```

## 📁 **Structure du Projet**

```
PROJET FIFA/
├── app.py                 # Application principale Flask
├── requirements.txt       # Dépendances Python
├── backup_db.py          # Script de sauvegarde
├── instance/             # Base de données (non versionné)
│   └── fifa25.db
├── templates/            # Templates HTML
│   ├── base.html
│   ├── home.html
│   ├── manage_players.html
│   ├── standings.html
│   └── season_history.html
├── backups/              # Sauvegardes (non versionné)
└── DATA_PERSISTENCE.md   # Documentation persistance
```

## 🔧 **Configuration**

### Port personnalisé
Modifiez dans `app.py` ligne 646 :
```python
app.run(debug=True, host='0.0.0.0', port=VOTRE_PORT)
```

### Joueurs personnalisés
Modifiez dans `app.py` la fonction `initialize_default_players()` :
```python
default_players = ['NOM1', 'NOM2', 'NOM3', 'NOM4', 'NOM5']
```

## 🐛 **Dépannage**

### L'application ne démarre pas
```bash
# Vérifier la syntaxe
python -c "import app; print('OK')"

# Vérifier le port
netstat -an | findstr :8000
```

### Problèmes de connexion
- Vérifiez le pare-feu Windows
- Essayez `http://127.0.0.1:8000`
- Redémarrez en mode navigation privée

### Perte de données
```bash
# Restaurer une sauvegarde
python backup_db.py list
python backup_db.py restore [fichier_backup]
```

## 📱 **Optimisation Mobile**

- Interface responsive automatique
- Boutons tactiles optimisés
- Navigation simplifiée sur petit écran
- Saisie des scores facilitée

## 🤝 **Contribution**

1. Fork le projet
2. Créez une branche (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Commit (`git commit -am 'Ajout nouvelle fonctionnalité'`)
4. Push (`git push origin feature/nouvelle-fonctionnalite`)
5. Créez une Pull Request

## 📄 **Licence**

Projet personnel - FC 26 League

## 👥 **Équipe**

- **ABOUBACAR**
- **DIOGO**
- **LIONEL**
- **CHERIF**
- **ELI**

---

**⚽ Bonne chance pour votre FC 26 League ! 🏆**
