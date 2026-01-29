"""
Script de correction pour Windows
Crée le dossier instance et initialise la base de données
"""

import os

# Créer le dossier instance
if not os.path.exists('instance'):
    os.makedirs('instance')
    print("✅ Dossier 'instance' créé")
else:
    print("✅ Dossier 'instance' existe déjà")

# Initialiser la base de données
from app import app, db

with app.app_context():
    db.create_all()
    print("✅ Base de données créée avec succès!")
    print("\nVous pouvez maintenant lancer l'application:")
    print("   python app.py")