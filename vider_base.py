"""
Script pour vider la base de données
Supprime tous les documents
"""

from app import app, db, Document, DocumentCounter
import os

def vider_base_donnees():
    """Vide complètement la base de données"""
    
    print("=" * 60)
    print("🗑️  VIDAGE DE LA BASE DE DONNÉES")
    print("=" * 60)
    print()
    
    # Avertissement
    print("⚠️  ATTENTION : Cette opération va supprimer TOUTES les données !")
    print("   - Tous les documents")
    print("   - Tous les compteurs")
    print()
    
    # Demander confirmation
    confirmation = input("Êtes-vous sûr de vouloir continuer ? (tapez 'OUI' pour confirmer) : ")
    
    if confirmation.upper() != 'OUI':
        print("\n❌ Opération annulée.")
        return
    
    print("\n🔄 Vidage en cours...")
    
    with app.app_context():
        try:
            # Compter les documents avant suppression
            nb_documents = Document.query.count()
            nb_compteurs = DocumentCounter.query.count()
            
            print(f"\n📊 Données actuelles :")
            print(f"   - Documents : {nb_documents}")
            print(f"   - Compteurs : {nb_compteurs}")
            
            # Supprimer tous les documents
            Document.query.delete()
            print("\n✓ Tous les documents supprimés")
            
            # Supprimer tous les compteurs
            DocumentCounter.query.delete()
            print("✓ Tous les compteurs supprimés")
            
            # Valider les changements
            db.session.commit()
            
            print("\n✅ Base de données vidée avec succès !")
            print(f"   {nb_documents} document(s) supprimé(s)")
            print(f"   {nb_compteurs} compteur(s) supprimé(s)")
            print()
            print("📝 La numérotation recommencera à 001/2026")
            
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Erreur lors du vidage : {e}")
            print("   Les données n'ont pas été modifiées.")

def afficher_statistiques():
    """Affiche les statistiques de la base de données"""
    
    print("=" * 60)
    print("📊 STATISTIQUES DE LA BASE DE DONNÉES")
    print("=" * 60)
    print()
    
    with app.app_context():
        try:
            # Compter les documents
            total_documents = Document.query.count()
            documents_actifs = Document.query.filter_by(is_active=True).count()
            documents_supprimes = Document.query.filter_by(is_active=False).count()
            
            print(f"Documents :")
            print(f"   Total : {total_documents}")
            print(f"   Actifs : {documents_actifs}")
            print(f"   Supprimés (soft delete) : {documents_supprimes}")
            
            # Afficher les derniers documents
            if total_documents > 0:
                print(f"\n📄 Derniers documents :")
                derniers = Document.query.order_by(Document.created_at.desc()).limit(5).all()
                for doc in derniers:
                    statut = "✓" if doc.is_active else "✗"
                    print(f"   {statut} {doc.document_number} - {doc.lieu} ({doc.created_at.strftime('%d/%m/%Y %H:%M')})")
            
            # Compteurs
            print(f"\nCompteurs :")
            compteurs = DocumentCounter.query.all()
            if compteurs:
                for compteur in compteurs:
                    print(f"   Année {compteur.year} : {compteur.counter} document(s)")
            else:
                print("   Aucun compteur")
            
        except Exception as e:
            print(f"❌ Erreur : {e}")

def menu_principal():
    """Menu principal du script"""
    
    while True:
        print("\n" + "=" * 60)
        print("🗄️  GESTION DE LA BASE DE DONNÉES")
        print("=" * 60)
        print()
        print("1. Afficher les statistiques")
        print("2. Vider la base de données")
        print("3. Quitter")
        print()
        
        choix = input("Votre choix (1-3) : ")
        
        if choix == '1':
            afficher_statistiques()
        elif choix == '2':
            vider_base_donnees()
        elif choix == '3':
            print("\n👋 Au revoir !")
            break
        else:
            print("\n❌ Choix invalide. Veuillez choisir 1, 2 ou 3.")

if __name__ == '__main__':
    print()
    print("╔════════════════════════════════════════════════════════════╗")
    print("║  GESTION BASE DE DONNÉES - Analyses Microbiologiques      ║")
    print("╚════════════════════════════════════════════════════════════╝")
    
    # Vérifier que la base de données existe
    db_path = 'instance/water_lab.db'
    if not os.path.exists(db_path):
        print("\n❌ ERREUR : Base de données introuvable !")
        print(f"   Chemin attendu : {db_path}")
        print("\nCréez d'abord la base avec : python init_db.py")
    else:
        menu_principal()