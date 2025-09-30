# 🚀 Guide de Déploiement - FC 26 League

## 📱 **Accès Mobile/Réseau Local**

### Votre IP Actuelle
- **IP WiFi** : `192.168.2.39`
- **URL Mobile** : `http://192.168.2.39:8000`

### Comment Accéder depuis votre Téléphone
1. **Connectez votre téléphone au même WiFi** que votre PC
2. **Ouvrez le navigateur** sur votre téléphone
3. **Tapez l'URL** : `http://192.168.2.39:8000`
4. **Profitez de votre FC 26 League** en mobile ! 📱⚽

## 🌐 **Déploiement sur GitHub**

### Étapes pour GitHub
```bash
# 1. Créer un repository sur GitHub.com
# 2. Ajouter le remote
git remote add origin https://github.com/[VOTRE_USERNAME]/fc26-league.git

# 3. Pousser le code
git branch -M main
git push -u origin main
```

### Déploiement Gratuit sur Render.com
1. **Créez un compte** sur [render.com](https://render.com)
2. **Connectez votre GitHub**
3. **Créez un Web Service** depuis votre repo
4. **Configuration** :
   - **Build Command** : `pip install -r requirements.txt`
   - **Start Command** : `python app.py`
   - **Port** : `8000`

## ☁️ **Alternatives de Déploiement Gratuit**

### 1. Railway.app
```bash
# Installation
npm install -g @railway/cli

# Déploiement
railway login
railway init
railway up
```

### 2. Heroku (avec Procfile)
Créer `Procfile` :
```
web: python app.py
```

### 3. PythonAnywhere
- Upload votre code
- Configuration WSGI
- Accès via [username].pythonanywhere.com

## 📱 **Optimisations Mobile Déjà Incluses**

✅ **Interface Responsive**
- Grilles adaptatives
- Boutons tactiles optimisés
- Navigation mobile simplifiée

✅ **Performance Mobile**
- CSS optimisé pour mobile
- Animations fluides
- Chargement rapide

✅ **UX Mobile**
- Saisie de scores facilitée
- Menus déroulants adaptés
- Affichage compact des classements

## 🔧 **Configuration Réseau**

### Pare-feu Windows
Si l'accès mobile ne fonctionne pas :
```cmd
# Autoriser le port 8000
netsh advfirewall firewall add rule name="FC26 League" dir=in action=allow protocol=TCP localport=8000
```

### Test de Connectivité
```bash
# Depuis un autre appareil sur le réseau
ping 192.168.2.39
telnet 192.168.2.39 8000
```

## 📊 **Monitoring**

### Logs en Temps Réel
```bash
# Voir les connexions
netstat -an | findstr :8000

# Processus Python
tasklist | findstr python
```

### Accès Concurrent
L'application supporte plusieurs utilisateurs simultanés :
- ✅ Consultation des classements
- ✅ Saisie de scores (attention aux conflits)
- ✅ Navigation dans l'historique

## 🎯 **URLs d'Accès**

### Local (PC)
- `http://localhost:8000`
- `http://127.0.0.1:8000`

### Réseau Local
- `http://192.168.2.39:8000` (WiFi)
- Depuis n'importe quel appareil sur le même réseau

### Une fois déployé en ligne
- `https://[votre-app].render.com`
- `https://[votre-app].railway.app`
- `https://[username].pythonanywhere.com`

## 🔒 **Sécurité**

### Recommandations
- ✅ Base de données exclue du Git (.gitignore)
- ✅ Pas de données sensibles exposées
- ✅ Accès réseau local seulement
- ⚠️ Pour déploiement public : ajouter authentification

### Sauvegarde avant Déploiement
```bash
python backup_db.py backup
```

---

**🎮 Votre FC 26 League est maintenant accessible partout ! 🏆**
