#!/usr/bin/env python3
"""
Script de sauvegarde automatique pour FC 26 League
Crée des copies de sauvegarde de la base de données avec horodatage
"""

import os
import shutil
import sqlite3
from datetime import datetime
import json

def create_backup():
    """Crée une sauvegarde complète de la base de données"""
    
    # Chemins
    db_path = "instance/fifa25.db"
    backup_dir = "backups"
    
    # Créer le dossier de sauvegarde s'il n'existe pas
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        print(f"📁 Dossier de sauvegarde créé : {backup_dir}")
    
    # Vérifier que la base de données existe
    if not os.path.exists(db_path):
        print("❌ Base de données non trouvée !")
        return False
    
    # Nom du fichier de sauvegarde avec timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"fifa25_backup_{timestamp}.db"
    backup_path = os.path.join(backup_dir, backup_filename)
    
    try:
        # Copier la base de données
        shutil.copy2(db_path, backup_path)
        
        # Obtenir la taille du fichier
        size_mb = os.path.getsize(backup_path) / (1024 * 1024)
        
        print(f"✅ Sauvegarde créée avec succès !")
        print(f"📁 Fichier : {backup_path}")
        print(f"📊 Taille : {size_mb:.2f} MB")
        print(f"🕐 Date : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        
        # Créer un rapport de sauvegarde
        create_backup_report(backup_path, timestamp)
        
        # Nettoyer les anciennes sauvegardes (garder les 10 plus récentes)
        cleanup_old_backups(backup_dir)
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde : {str(e)}")
        return False

def create_backup_report(backup_path, timestamp):
    """Crée un rapport détaillé de la sauvegarde"""
    
    report = {
        "timestamp": timestamp,
        "date": datetime.now().isoformat(),
        "backup_file": backup_path,
        "file_size_mb": round(os.path.getsize(backup_path) / (1024 * 1024), 2),
        "statistics": {}
    }
    
    try:
        # Connexion à la base sauvegardée pour obtenir des stats
        conn = sqlite3.connect(backup_path)
        cursor = conn.cursor()
        
        # Statistiques des tables
        tables = ['player', 'season', 'match', 'weekly_standings']
        for table in tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                report['statistics'][table] = count
            except:
                report['statistics'][table] = 0
        
        conn.close()
        
        # Sauvegarder le rapport
        report_path = backup_path.replace('.db', '_report.json')
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"📋 Rapport créé : {os.path.basename(report_path)}")
        
    except Exception as e:
        print(f"⚠️ Impossible de créer le rapport : {str(e)}")

def cleanup_old_backups(backup_dir, keep_count=10):
    """Supprime les anciennes sauvegardes, ne garde que les plus récentes"""
    
    try:
        # Lister tous les fichiers de sauvegarde
        backup_files = []
        for filename in os.listdir(backup_dir):
            if filename.startswith("fifa25_backup_") and filename.endswith(".db"):
                filepath = os.path.join(backup_dir, filename)
                backup_files.append((filepath, os.path.getctime(filepath)))
        
        # Trier par date de création (plus récent en premier)
        backup_files.sort(key=lambda x: x[1], reverse=True)
        
        # Supprimer les anciens fichiers
        deleted_count = 0
        for i, (filepath, _) in enumerate(backup_files):
            if i >= keep_count:  # Garder seulement les 'keep_count' plus récents
                try:
                    os.remove(filepath)
                    # Supprimer aussi le rapport associé s'il existe
                    report_path = filepath.replace('.db', '_report.json')
                    if os.path.exists(report_path):
                        os.remove(report_path)
                    deleted_count += 1
                except:
                    pass
        
        if deleted_count > 0:
            print(f"🧹 {deleted_count} anciennes sauvegardes supprimées")
        
    except Exception as e:
        print(f"⚠️ Erreur lors du nettoyage : {str(e)}")

def list_backups():
    """Liste toutes les sauvegardes disponibles"""
    
    backup_dir = "backups"
    
    if not os.path.exists(backup_dir):
        print("📁 Aucun dossier de sauvegarde trouvé")
        return
    
    # Lister les sauvegardes
    backup_files = []
    for filename in os.listdir(backup_dir):
        if filename.startswith("fifa25_backup_") and filename.endswith(".db"):
            filepath = os.path.join(backup_dir, filename)
            size_mb = os.path.getsize(filepath) / (1024 * 1024)
            date_created = datetime.fromtimestamp(os.path.getctime(filepath))
            backup_files.append((filename, size_mb, date_created))
    
    if not backup_files:
        print("📁 Aucune sauvegarde trouvée")
        return
    
    # Trier par date (plus récent en premier)
    backup_files.sort(key=lambda x: x[2], reverse=True)
    
    print(f"📋 {len(backup_files)} sauvegarde(s) trouvée(s) :")
    print("=" * 60)
    
    for filename, size_mb, date_created in backup_files:
        print(f"📁 {filename}")
        print(f"   📊 Taille: {size_mb:.2f} MB")
        print(f"   🕐 Date: {date_created.strftime('%d/%m/%Y %H:%M:%S')}")
        print("-" * 40)

def restore_backup(backup_filename):
    """Restaure une sauvegarde spécifique"""
    
    backup_path = os.path.join("backups", backup_filename)
    db_path = "instance/fifa25.db"
    
    if not os.path.exists(backup_path):
        print(f"❌ Sauvegarde non trouvée : {backup_filename}")
        return False
    
    try:
        # Faire une sauvegarde de la base actuelle avant restauration
        if os.path.exists(db_path):
            current_backup = f"fifa25_before_restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            shutil.copy2(db_path, os.path.join("backups", current_backup))
            print(f"💾 Base actuelle sauvegardée : {current_backup}")
        
        # Restaurer la sauvegarde
        shutil.copy2(backup_path, db_path)
        
        print(f"✅ Restauration réussie !")
        print(f"📁 {backup_filename} → fifa25.db")
        print("🔄 Redémarrez l'application pour voir les changements")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la restauration : {str(e)}")
        return False

if __name__ == "__main__":
    print("⚽ FC 26 League - Gestionnaire de Sauvegarde")
    print("=" * 50)
    
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "backup":
            create_backup()
        elif command == "list":
            list_backups()
        elif command == "restore" and len(sys.argv) > 2:
            restore_backup(sys.argv[2])
        else:
            print("Usage:")
            print("  python backup_db.py backup          - Créer une sauvegarde")
            print("  python backup_db.py list            - Lister les sauvegardes")
            print("  python backup_db.py restore <file>  - Restaurer une sauvegarde")
    else:
        # Mode interactif
        print("Que voulez-vous faire ?")
        print("1. Créer une sauvegarde")
        print("2. Lister les sauvegardes")
        print("3. Restaurer une sauvegarde")
        print("4. Quitter")
        
        choice = input("\nVotre choix (1-4): ")
        
        if choice == "1":
            create_backup()
        elif choice == "2":
            list_backups()
        elif choice == "3":
            list_backups()
            if input("\nEntrez le nom du fichier à restaurer (ou 'q' pour annuler): ").lower() != 'q':
                backup_name = input("Nom du fichier: ")
                restore_backup(backup_name)
        else:
            print("👋 Au revoir !")
