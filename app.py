"""
Application Flask - Gestion des Analyses Microbiologiques d'Eau
"""

from flask import Flask, request, jsonify, render_template, send_file
from datetime import datetime
import json
import os
from models import db, Document, DocumentCounter
from qr_generator import QRCodeGenerator
from docx_generator import DocxGenerator

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///water_data.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///instance/water_lab.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialiser la base de données
db.init_app(app)

# =============================================================================
# ROUTES - PAGES
# =============================================================================

@app.route('/')
def index():
    """Page de création d'un nouveau document"""
    # Générer le prochain numéro (pour affichage uniquement)
    prochain_numero = generer_numero_document(preview=True)
    return render_template('index.html', prochain_numero=prochain_numero)

@app.route('/liste')
def liste_documents():
    """Page de liste de tous les documents"""
    return render_template('liste.html')
    
@app.route('/details')
def details_document():
    """Page de détails d'un document"""
    return render_template('details.html')

@app.route('/verify/<token>')
def verify_document(token):
    """Page de vérification via QR Code"""
    document = Document.query.filter_by(
        verification_token=token,
        is_active=True
    ).first()
    
    if document:
        return render_template('verification.html', document=document.to_dict())
    else:
        return render_template('verification.html', error='Document non trouvé ou invalide')

# =============================================================================
# API - CRÉATION
# =============================================================================

@app.route('/api/generate-document', methods=['POST'])
def generate_document():
    """
    Crée un nouveau document avec QR Code
    """
    try:
        data = request.get_json()
        
        # Validation des champs obligatoires
        required_fields = [
            'date_prelevement', 'lieu', 'date_reception',
            'identite_preleveur', 'identite_demandeur',
            'resultats', 'conclusion', 'titre_signataire', 'nom_signataire'
        ]
        
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'Champ obligatoire manquant: {field}'
                }), 400
        
        # Générer le numéro unique
        numero = generer_numero_document()
        
        # Générer le token de vérification
        token_data = {'document_number': numero}
        verification_token = QRCodeGenerator.generate_token(token_data)
        
        # Générer le QR Code
        qr_code_base64, verification_url = QRCodeGenerator.generate_qr_code(
            token_data,
            verification_token
        )
        
        # Convertir les dates
        date_prelevement = datetime.strptime(data['date_prelevement'], '%Y-%m-%d')
        date_reception = datetime.strptime(data['date_reception'], '%Y-%m-%d')
        
        # Créer le document
        document = Document(
            document_number=numero,
            date_prelevement=date_prelevement,
            lieu=data['lieu'],
            date_reception=date_reception,
            identite_preleveur=data['identite_preleveur'],
            identite_demandeur=data['identite_demandeur'],
            resultats_json=json.dumps(data['resultats']),
            conclusion=data['conclusion'],
            note=data.get('note', ''),
            nom_signataire=data['nom_signataire'],
            titre_signataire=data['titre_signataire'],
            verification_token=verification_token
        )
        
        db.session.add(document)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'document_id': document.id,
            'document_number': numero,
            'verification_token': verification_token,
            'qr_code': qr_code_base64,
            'verification_url': verification_url
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/generate-docx', methods=['POST'])
def generate_docx():
    """
    Génère le fichier DOCX pour un document
    """
    try:
        data = request.get_json()
        document_id = data.get('document_id')
        
        # Récupérer le document
        document = Document.query.get(document_id)
        if not document:
            return jsonify({'error': 'Document non trouvé'}), 404
        
        # Générer le QR Code en bytes
        qr_image_bytes = QRCodeGenerator.generate_qr_code_bytes(
            {'document_number': document.document_number},
            document.verification_token
        )
        
        # Générer le DOCX
        docx_file = DocxGenerator.generer_document(
            document.to_dict(),
            qr_image_bytes
        )
        
        # Nom du fichier
        filename = f"Analyse_{document.document_number.replace('/', '_')}.docx"
        
        return send_file(
            docx_file,
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# =============================================================================
# API - LISTE ET RECHERCHE
# =============================================================================

@app.route('/api/documents', methods=['GET'])
def get_documents():
    """
    Récupère la liste de tous les documents actifs
    """
    documents = Document.query.filter_by(is_active=True).order_by(
        Document.document_number.desc()
    ).all()
    
    return jsonify({
        'success': True,
        'documents': [doc.to_dict() for doc in documents]
    })

@app.route('/api/search', methods=['GET'])
def search_document():
    """
    Recherche un document par son numéro
    """
    numero = request.args.get('numero')
    
    if not numero:
        return jsonify({'error': 'Numéro requis'}), 400
    
    document = Document.query.filter_by(
        document_number=numero,
        is_active=True
    ).first()
    
    if document:
        return jsonify({
            'success': True,
            'document': document.to_dict()
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Document non trouvé'
        }), 404

@app.route('/api/document/<document_id>', methods=['GET'])
def get_document(document_id):
    """
    Récupère les détails d'un document
    """
    document = Document.query.get(document_id)
    
    if document and document.is_active:
        return jsonify({
            'success': True,
            'document': document.to_dict()
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Document non trouvé'
        }), 404

# =============================================================================
# API - SUPPRESSION (PAS DE MODIFICATION)
# =============================================================================

@app.route('/api/delete/<document_id>', methods=['DELETE'])
def delete_document(document_id):
    """
    Supprime un document (soft delete)
    IMPORTANT: Pas de route pour modification - interdite
    """
    document = Document.query.get(document_id)
    
    if not document:
        return jsonify({'error': 'Document non trouvé'}), 404
    
    # Soft delete
    document.is_active = False
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': f'Document {document.document_number} supprimé'
    })

# =============================================================================
# API - VÉRIFICATION
# =============================================================================

@app.route('/api/verify/<token>', methods=['GET'])
def verify_token(token):
    """
    API de vérification du token (pour mobile apps)
    """
    document = Document.query.filter_by(
        verification_token=token,
        is_active=True
    ).first()
    
    if document:
        return jsonify({
            'success': True,
            'valid': True,
            'document': document.to_dict()
        })
    else:
        return jsonify({
            'success': True,
            'valid': False,
            'message': 'Document non trouvé ou invalide'
        })

# =============================================================================
# FONCTIONS UTILITAIRES
# =============================================================================

def generer_numero_document(preview=False):
    """
    Génère un numéro unique auto-incrémenté
    Format: 001/2026, 002/2026, etc.
    
    Args:
        preview: Si True, ne modifie pas le compteur (pour affichage)
    
    Returns:
        str: Numéro au format XXX/YYYY
    """
    annee_actuelle = datetime.now().year
    
    # Récupérer ou créer le compteur pour cette année
    counter = DocumentCounter.query.filter_by(year=annee_actuelle).first()
    
    if not counter:
        counter = DocumentCounter(year=annee_actuelle, counter=0)
        db.session.add(counter)
        db.session.flush()
    
    if preview:
        # Mode preview: retourner le prochain numéro sans incrémenter
        prochain = counter.counter + 1
        return f"{prochain:03d}/{annee_actuelle}"
    else:
        # Mode réel: incrémenter et sauvegarder
        counter.counter += 1
        db.session.commit()
        return f"{counter.counter:03d}/{annee_actuelle}"

# =============================================================================
# LANCEMENT
# =============================================================================

if __name__ == '__main__':
    # Créer le dossier instance si nécessaire
    os.makedirs('instance', exist_ok=True)
    
    # Créer les tables si nécessaire
    with app.app_context():
        db.create_all()
    
    # Lancer l'application
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
