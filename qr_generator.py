import qrcode
import io
import base64
from datetime import datetime
import hashlib
import os

class QRCodeGenerator:
    @staticmethod
    def generate_qr_code(data, token):
        """
        Génère un QR code avec les données et le token
        
        Returns:
            tuple: (qr_code_base64, verification_url)
        """
        # Créer l'URL de vérification
        base_url = os.environ.get('BASE_URL', 'http://10.111.144.164:5000')
        verification_url = f"{base_url}/verify/{token}"
        
        # Créer le QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(verification_url)
        qr.make(fit=True)
        
        # Générer l'image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convertir en base64 pour l'affichage
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return img_str, verification_url
    
    @staticmethod
    def generate_qr_code_bytes(data, token):
        """
        Génère un QR code et retourne les bytes PNG
        Utilisé pour insertion dans le DOCX
        
        Returns:
            bytes: Image PNG du QR Code
        """
        # Créer l'URL de vérification
        base_url = os.environ.get('BASE_URL', 'http://10.111.144.164:5000')
        verification_url = f"{base_url}/verify/{token}"
        
        # Créer le QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(verification_url)
        qr.make(fit=True)
        
        # Générer l'image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convertir en bytes
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        
        return buffered.getvalue()
    
    @staticmethod
    def generate_token(document_data):
        """Génère un token unique SHA-256 basé sur les données du document"""
        data_string = f"{document_data['document_number']}{datetime.utcnow().timestamp()}"
        return hashlib.sha256(data_string.encode()).hexdigest()
