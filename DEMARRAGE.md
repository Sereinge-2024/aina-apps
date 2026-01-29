# 🚀 GUIDE DE DÉMARRAGE RAPIDE

## Application de Gestion des Analyses Microbiologiques d'Eau

---

## ⚡ Installation en 4 Étapes

### 1. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 2. Initialiser la base de données
```bash
python init_db.py
```

### 3. Lancer l'application
```bash
python app.py
```

### 4. Ouvrir dans le navigateur
```
http://localhost:5000
```

---

## 📁 Structure du Projet

```
water_final/
├── app.py                      # Application Flask principale
├── models.py                   # Modèles de données
├── docx_generator.py           # Générateur DOCX format exact
├── qr_generator.py             # Générateur QR Code
├── database.py                 # Configuration DB
├── init_db.py                  # Script initialisation
├── requirements.txt            # Dépendances
│
├── static/
│   └── images/
│       └── image1.jpeg         # Logo en-tête
│
└── templates/
    ├── index.html              # Formulaire de création
    ├── liste.html              # Liste des documents
    └── verification.html       # Vérification QR
```

---

## 🎯 Fonctionnalités

### ✅ Création de Documents
- Numérotation automatique (001/2026, 002/2026...)
- Formulaire complet avec validation
- Éditeur Quill pour conclusion et note
- Support de plusieurs échantillons

### ✅ Format DOCX Exact
- Logo en haut à gauche
- QR Code en haut à droite
- Informations HORS tableau (paragraphes)
- Tableau des paramètres (3 lignes fixes)
- Conclusion + NB de l'éditeur
- Signature (titre + nom)
- PAS de pied de page

### ✅ Gestion des Documents
- Liste complète
- Recherche par numéro
- Téléchargement DOCX
- Suppression (soft delete)
- ❌ PAS de modification (sécurité)

### ✅ Vérification QR Code
- Scan du QR ouvre la page de vérification
- Affiche les informations du document
- Détecte les documents invalides

---

## 📝 Utilisation

### Créer une Nouvelle Analyse

1. Ouvrir `http://localhost:5000`
2. Le numéro est généré automatiquement (ex: 001/2026)
3. Remplir le formulaire :
   - Dates de prélèvement et réception
   - Lieu (saisi manuellement)
   - Identités préleveur/demandeur
   - Résultats d'analyse (plusieurs échantillons possibles)
   - Conclusion (éditeur)
   - Note NB (optionnel)
   - Signature (titre + nom)
4. Cliquer sur "Générer le Document & QR Code"
5. Télécharger le DOCX

### Voir la Liste des Documents

1. Cliquer sur "Liste des Documents" dans la navigation
2. Tous les documents actifs s'affichent
3. Actions disponibles :
   - 👁️ Voir (détails)
   - 📥 Télécharger DOCX
   - 🗑️ Supprimer (avec confirmation)

### Rechercher un Document

1. Sur la page "Liste"
2. Entrer le numéro (ex: 001/2026)
3. Cliquer sur "Rechercher"

### Vérifier un Document via QR Code

1. Scanner le QR Code avec un smartphone
2. La page de vérification s'ouvre
3. Les informations du document s'affichent

---

## ⚙️ Configuration

### Variables d'Environnement (optionnel)

Créer un fichier `.env` :

```bash
SECRET_KEY=votre-clé-secrète-production
DATABASE_URL=sqlite:///instance/water_lab.db
BASE_URL=https://votre-domaine.com
PORT=5000
```

### URL du QR Code

Par défaut : `http://localhost:5000`

Pour changer (production) :
```bash
export BASE_URL=https://votre-domaine.com
python app.py
```

---

## 🔍 Points Importants

### ✅ Numérotation Unique
- Format : XXX/YYYY (ex: 001/2026)
- Auto-incrémentée par année
- Aucun doublon possible
- Réinitialisation automatique chaque année

### ✅ Informations d'Analyse
**HORS tableau** (en paragraphes simples) :
- Numéro d'analyse
- Dates de prélèvement/réception
- Lieu
- Identités préleveur/demandeur

### ✅ Tableau des Paramètres
**Structure FIXE** (3 lignes) :
1. Coliformes totaux
2. Coliformes fécaux
3. Streptocoques fécaux

Colonnes :
- PARAMETRES
- Température et temps
- Technique et milieu
- RESULTATS (UFC/100ml)
- NORMES OMS

### ✅ Signature
Deux champs :
- Titre : "Le Chef du Laboratoire"
- Nom : "Dr Ibrahim OUEDRAOGO"

### ❌ Modification Interdite
- Pas de bouton "Modifier"
- Pas de route `/api/update`
- Sécurité des documents officiels

### ✅ Suppression
- Soft delete (is_active = False)
- Document reste en base
- Confirmation obligatoire

---

## 🧪 Exemple de Données de Test

```json
{
  "date_prelevement": "2026-01-11",
  "lieu": "BK01 / 11-01-26",
  "date_reception": "2026-01-13",
  "identite_preleveur": "SOCREGE / PROJET BATIE GOLD",
  "identite_demandeur": "SOCREGE / PROJET BATIE GOLD",
  "resultats": [
    {
      "coliformes_totaux": "34",
      "coliformes_fecaux": "0",
      "streptocoques_fecaux": "0"
    }
  ],
  "conclusion": "Eau non conforme aux normes bactériologiques.",
  "note": "Ouvrage à désinfecter.",
  "titre_signataire": "Le Chef du Laboratoire",
  "nom_signataire": "Dr Ibrahim OUEDRAOGO"
}
```

---

## 🐛 Dépannage

### Erreur : "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### Erreur : "database is locked"
```bash
# Arrêter toutes les instances
killall python3

# Relancer
python app.py
```

### Erreur : "No such file: image1.jpeg"
```bash
# Vérifier que les images sont dans static/images/
ls static/images/
```

### Le numéro ne s'incrémente pas
```bash
# Recréer la base
rm instance/water_lab.db
python init_db.py
```

---

## 📚 Documentation Complète

Voir `CAHIER_DES_CHARGES.md` pour :
- Spécifications détaillées
- Architecture complète
- Exemples de code
- Tests à effectuer

---

## ✅ Checklist de Validation

Après installation, vérifier :

- [ ] Application démarre sans erreur
- [ ] Page d'accueil affiche le prochain numéro
- [ ] Formulaire est complet
- [ ] Éditeurs Quill fonctionnent
- [ ] Génération de document réussit
- [ ] QR Code s'affiche
- [ ] DOCX se télécharge avec :
  - [ ] Logo en haut à gauche
  - [ ] QR Code en haut à droite
  - [ ] Infos HORS tableau
  - [ ] Tableau avec 3 lignes
  - [ ] Conclusion de l'éditeur
  - [ ] Signature complète
  - [ ] PAS de pied de page
- [ ] Page liste fonctionne
- [ ] Recherche trouve les documents
- [ ] Téléchargement fonctionne
- [ ] Suppression demande confirmation
- [ ] Scan QR ouvre la vérification

---

## 🎉 C'est Prêt !

Votre application est maintenant opérationnelle.

Pour créer votre première analyse :
```bash
python app.py
# Puis ouvrir http://localhost:5000
```

**Bonne utilisation ! 🚀**
