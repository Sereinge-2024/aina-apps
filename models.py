from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import uuid

db = SQLAlchemy()

class Document(db.Model):
    __tablename__ = 'documents'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Numéro unique auto-incrémenté (ex: 001/2026)
    document_number = db.Column(db.String(100), unique=True, nullable=False)
    
    # Informations d'analyse (HORS tableau)
    date_prelevement = db.Column(db.DateTime, nullable=False)
    lieu = db.Column(db.String(200), nullable=False)
    date_reception = db.Column(db.DateTime, nullable=False)
    identite_preleveur = db.Column(db.String(200))
    identite_demandeur = db.Column(db.String(200))
    
    # Résultats des analyses (stockés en JSON pour plusieurs échantillons)
    # Format: [{coliformes_totaux: 34, coliformes_fecaux: 0, streptocoques: 0}, ...]
    resultats_json = db.Column(db.Text)
    
    # Conclusion et NB (contenu de l'éditeur)
    conclusion = db.Column(db.Text)
    note = db.Column(db.Text)
    
    # Signature
    nom_signataire = db.Column(db.String(200))
    titre_signataire = db.Column(db.String(200))  # Ex: "Le Chef du Laboratoire"
    
    # QR Code
    verification_token = db.Column(db.String(64), unique=True, nullable=False)
    
    # Métadonnées
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    def to_dict(self):
        import json
        return {
            'id': self.id,
            'document_number': self.document_number,
            'date_prelevement': self.date_prelevement.isoformat() if self.date_prelevement else None,
            'lieu': self.lieu,
            'date_reception': self.date_reception.isoformat() if self.date_reception else None,
            'identite_preleveur': self.identite_preleveur,
            'identite_demandeur': self.identite_demandeur,
            'resultats': json.loads(self.resultats_json) if self.resultats_json else [],
            'conclusion': self.conclusion,
            'note': self.note,
            'nom_signataire': self.nom_signataire,
            'titre_signataire': self.titre_signataire,
            'verification_token': self.verification_token,
            'created_at': self.created_at.isoformat(),
            'is_active': self.is_active
        }

class DocumentCounter(db.Model):
    """Table pour gérer le compteur auto-incrémenté par année"""
    __tablename__ = 'document_counter'
    
    year = db.Column(db.Integer, primary_key=True)
    counter = db.Column(db.Integer, default=0)
