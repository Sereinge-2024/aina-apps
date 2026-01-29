"""
Script d'initialisation de la base de données
"""

from app import app, db
import os

def init_database():
    """Initialise la base de données"""
    
    # Créer le dossier instance
    os.makedirs('instance', exist_ok=True)
    
    with app.app_context():
        # Créer toutes les tables
        db.create_all()
        print("✅ Base de données créée avec succès!")
        print("   Tables créées: documents, document_counter")
        print()
        print("Vous pouvez maintenant lancer l'application:")
        print("   python app.py")

if __name__ == '__main__':
    init_database()
