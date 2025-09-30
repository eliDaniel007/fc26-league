#!/usr/bin/env python3
"""
Script de démarrage pour la production sur Render.com
"""
import os
from app import app

if __name__ == '__main__':
    # Configuration pour la production
    with app.app_context():
        from app import db
        db.create_all()
        print("⚽ FC 26 League - Production Ready!")
    
    # Port dynamique pour Render
    port = int(os.environ.get('PORT', 8000))
    app.run(
        debug=False,
        host='0.0.0.0', 
        port=port
    )
