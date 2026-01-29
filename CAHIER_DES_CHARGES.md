# 📋 CAHIER DES CHARGES COMPLET
## Application de Gestion des Analyses Microbiologiques d'Eau

---

## 🎯 SPÉCIFICATIONS EXACTES

### 1. FORMAT DU DOCUMENT FINAL (.docx)

#### 📄 Structure du Document

```
┌─────────────────────────────────────────────────────────┐
│ EN-TÊTE (Header)                                         │
│ ┌──────────────────────────┐  ┌───────────────────┐    │
│ │ Logo + Titre (à gauche)  │  │  QR Code (droite) │    │
│ │ (image1.jpeg)            │  │                    │    │
│ └──────────────────────────┘  └───────────────────┘    │
├─────────────────────────────────────────────────────────┤
│ CORPS DU DOCUMENT                                        │
│                                                          │
│ RESULTATS D'ANALYSE MICROBIOLOGIQUE D'EAU               │
│                                                          │
│ Analyse n° : 001/2026                                   │
│ Date de prélèvement : 11/01/2026        Lieu : [SAISI]  │
│ Date de réception : 13/01/2026                          │
│ Identité du préleveur : [SAISI]                         │
│ Identité du demandeur : [SAISI]                         │
│                                                          │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ TABLEAU DES PARAMÈTRES                              │ │
│ ├───────────┬──────────┬──────────┬──────────┬───────┤ │
│ │PARAMETRES │Tempéra-  │Technique │RESULTATS │NORMES │ │
│ │           │ture et   │et milieu │UFC/100ml │OMS    │ │
│ │           │temps     │culture   │          │       │ │
│ ├───────────┼──────────┼──────────┼──────────┼───────┤ │
│ │Coliformes │37°C 24h  │Filtration│  [X]     │0/100ml│ │
│ │totaux     │          │membrane  │          │       │ │
│ ├───────────┼──────────┼──────────┼──────────┼───────┤ │
│ │Coliformes │44°C 24h  │Filtration│  [X]     │0/100ml│ │
│ │fécaux     │          │membrane  │          │       │ │
│ ├───────────┼──────────┼──────────┼──────────┼───────┤ │
│ │Strepto-   │24h       │Filtration│  [X]     │0/100ml│ │
│ │coques     │          │membrane  │          │       │ │
│ │fécaux     │          │          │          │       │ │
│ └───────────┴──────────┴──────────┴──────────┴───────┘ │
│                                                          │
│ Conclusion : [CONTENU DE L'ÉDITEUR]                     │
│                                                          │
│ NB : [CONTENU DE L'ÉDITEUR]                             │
│                                                          │
│ [TITRE SIGNATAIRE - Ex: Le Chef du Laboratoire]         │
│                                                          │
│                                                          │
│ [NOM DU SIGNATAIRE]                                      │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

#### ⚠️ IMPORTANT - Ce qui NE doit PAS être dans un tableau :
- ❌ Analyse n°
- ❌ Date de prélèvement / Lieu
- ❌ Date de réception  
- ❌ Identité du préleveur
- ❌ Identité du demandeur

Ces informations doivent être en **texte simple** (paragraphes).

#### ✅ Ce qui DOIT être dans le tableau :
- En-tête : PARAMETRES | Température et temps | Technique | RESULTATS | NORMES
- Ligne 1 : Coliformes totaux
- Ligne 2 : Coliformes fécaux  
- Ligne 3 : Streptocoques fécaux

---

### 2. NUMÉROTATION UNIQUE

#### Format : `XXX/YYYY`
- XXX = Numéro séquentiel sur 3 chiffres (001, 002, ...)
- YYYY = Année en cours (2026)

#### Logique Auto-Incrémentée :
```python
def generer_numero():
    annee_actuelle = datetime.now().year
    
    # Récupérer ou créer le compteur pour cette année
    counter = DocumentCounter.query.filter_by(year=annee_actuelle).first()
    if not counter:
        counter = DocumentCounter(year=annee_actuelle, counter=0)
        db.session.add(counter)
    
    # Incrémenter
    counter.counter += 1
    db.session.commit()
    
    # Format: 001/2026, 002/2026, etc.
    return f"{counter.counter:03d}/{annee_actuelle}"
```

#### ✅ Garanties :
- Pas de doublon possible
- Réinitialisation automatique chaque année
- 001/2026, 002/2026, ..., 999/2026
- 001/2027, 002/2027 (nouvelle année)

---

### 3. INTERFACE WEB

#### Page 1 : Formulaire de Création

```
┌─────────────────────────────────────────────────────────┐
│ 🧪 NOUVELLE ANALYSE MICROBIOLOGIQUE                      │
├─────────────────────────────────────────────────────────┤
│                                                          │
│ Numéro (auto) : [001/2026] (lecture seule, auto-généré)│
│                                                          │
│ 📅 DATES ET LIEU                                        │
│ Date de prélèvement : [____] *                          │
│ Lieu : [________________] * (saisi manuellement)        │
│ Date de réception : [____] *                            │
│                                                          │
│ 👥 IDENTITÉS                                            │
│ Préleveur : [________________] *                        │
│ Demandeur : [________________] *                        │
│                                                          │
│ 🔬 RÉSULTATS D'ANALYSE (plusieurs échantillons)        │
│                                                          │
│ Échantillon 1:                                          │
│   Coliformes totaux (UFC/100ml) : [____]               │
│   Coliformes fécaux (UFC/100ml) : [____]               │
│   Streptocoques fécaux (UFC/100ml) : [____]            │
│   [+ Ajouter un échantillon]                            │
│                                                          │
│ 📝 CONCLUSION                                           │
│ ┌────────────────────────────────────────────────────┐ │
│ │ [Éditeur Quill]                                     │ │
│ │ Ex: Eau non conforme aux normes bactériologiques.  │ │
│ └────────────────────────────────────────────────────┘ │
│                                                          │
│ 📝 NOTE (NB)                                            │
│ ┌────────────────────────────────────────────────────┐ │
│ │ [Éditeur Quill]                                     │ │
│ │ Ex: Ouvrage à désinfecter.                          │ │
│ └────────────────────────────────────────────────────┘ │
│                                                          │
│ ✍️ SIGNATURE                                            │
│ Titre : [Le Chef du Laboratoire] *                     │
│ Nom : [Dr Ibrahim OUEDRAOGO] *                         │
│                                                          │
│ [Générer le Document & QR Code]  [Annuler]             │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

#### Page 2 : Liste des Documents

```
┌─────────────────────────────────────────────────────────┐
│ 📚 TOUS LES DOCUMENTS                                    │
├─────────────────────────────────────────────────────────┤
│                                                          │
│ 🔍 Recherche : [____________] [Rechercher par n°]       │
│                                                          │
│ ┌────────────────────────────────────────────────────┐ │
│ │ Document │ Date       │ Préleveur  │ Actions      │ │
│ ├──────────┼────────────┼────────────┼──────────────┤ │
│ │ 003/2026 │ 28/01/2026 │ SOCREGE    │ 👁️ 📥 🗑️    │ │
│ │ 002/2026 │ 27/01/2026 │ CLIENT X   │ 👁️ 📥 🗑️    │ │
│ │ 001/2026 │ 26/01/2026 │ SOCIÉTÉ Y  │ 👁️ 📥 🗑️    │ │
│ └────────────────────────────────────────────────────┘ │
│                                                          │
│ Actions :                                                │
│ 👁️ = Voir (modal avec détails)                          │
│ 📥 = Télécharger DOCX                                    │
│ 🗑️ = Supprimer (avec confirmation)                      │
│                                                          │
│ ❌ PAS de modification possible (sécurité)               │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

#### Page 3 : Vue Détails (Modal)

```
┌─────────────────────────────────────────────────────────┐
│ 📄 DÉTAILS DU DOCUMENT 001/2026                 [✖️]     │
├─────────────────────────────────────────────────────────┤
│                                                          │
│ Numéro : 001/2026                                       │
│ Date de prélèvement : 11/01/2026                        │
│ Lieu : BK01 / 11-01-26                                  │
│ Date de réception : 13/01/2026                          │
│ Préleveur : SOCREGE / PROJET BATIE GOLD                 │
│ Demandeur : SOCREGE / PROJET BATIE GOLD                 │
│                                                          │
│ Résultats :                                              │
│ - Échantillon 1: CT=34, CF=0, SF=0                      │
│                                                          │
│ Conclusion : Eau non conforme...                        │
│ NB : Ouvrage à désinfecter.                             │
│                                                          │
│ Signataire : Dr Ibrahim OUEDRAOGO                       │
│ Titre : Le Chef du Laboratoire                          │
│                                                          │
│ Créé le : 28/01/2026 à 14:30                            │
│                                                          │
│ [Télécharger DOCX]  [Fermer]                            │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

### 4. FONCTIONNALITÉS TECHNIQUES

#### A. Génération du Document DOCX

```python
def generer_docx(document_data):
    """
    Génère le document selon le format exact
    """
    from docx import Document
    from docx.shared import Inches, Pt
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    
    doc = Document()
    
    # 1. EN-TÊTE avec logo à gauche et QR à droite
    header = doc.sections[0].header
    header_table = header.add_table(1, 2, width=Inches(7))
    
    # Cellule gauche : Logo + Titre
    left_cell = header_table.rows[0].cells[0]
    left_para = left_cell.paragraphs[0]
    left_run = left_para.add_run()
    left_run.add_picture('image1.jpeg', width=Inches(2.5))
    
    # Cellule droite : QR Code
    right_cell = header_table.rows[0].cells[1]
    right_para = right_cell.paragraphs[0]
    right_para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    qr_run = right_para.add_run()
    qr_run.add_picture(qr_image_path, width=Inches(1.2))
    
    # 2. TITRE PRINCIPAL
    titre = doc.add_heading('RESULTATS D\'ANALYSE MICROBIOLOGIQUE D\'EAU', 0)
    titre.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # 3. INFORMATIONS (HORS TABLEAU)
    doc.add_paragraph(f"Analyse n° : {document_data['numero']}")
    doc.add_paragraph(
        f"Date de prélèvement : {document_data['date_prelevement']}"
        f"\t\t\tLieu : {document_data['lieu']}"
    )
    doc.add_paragraph(f"Date de réception : {document_data['date_reception']}")
    doc.add_paragraph(f"Identité du préleveur : {document_data['preleveur']}")
    doc.add_paragraph(f"Identité du demandeur : {document_data['demandeur']}")
    
    # 4. TABLEAU DES PARAMÈTRES
    for resultats in document_data['resultats']:
        table = doc.add_table(rows=4, cols=5)
        table.style = 'Light Grid Accent 1'
        
        # En-tête
        headers = ['PARAMETRES', 'Température\net temps', 
                   'Technique et milieu', 'RESULTATS\nUFC/100 ml', 
                   'NORMES OMS']
        for i, header in enumerate(headers):
            table.rows[0].cells[i].text = header
        
        # Ligne 1: Coliformes totaux
        row1 = table.rows[1].cells
        row1[0].text = '° Recherche et dénombrement\ndes Coliformes totaux'
        row1[1].text = '37°C 24h'
        row1[2].text = 'Filtration sur membrane\nChromocult agar Coliformes'
        row1[3].text = str(resultats['coliformes_totaux'])
        row1[4].text = '0/100 ml'
        
        # Ligne 2: Coliformes fécaux
        # ... (même structure)
        
        # Ligne 3: Streptocoques fécaux
        # ... (même structure)
    
    # 5. CONCLUSION
    doc.add_paragraph(f"Conclusion : {document_data['conclusion']}")
    
    # 6. NOTE
    doc.add_paragraph(f"NB : {document_data['note']}")
    
    # 7. SIGNATURE
    doc.add_paragraph(document_data['titre_signataire'])
    doc.add_paragraph()  # Espace pour signature manuscrite
    doc.add_paragraph(document_data['nom_signataire'])
    
    # PAS DE PIED DE PAGE avec URL de vérification
    
    return doc
```

#### B. Recherche par Numéro

```python
@app.route('/api/search', methods=['GET'])
def search_document():
    numero = request.args.get('numero')
    
    document = Document.query.filter_by(
        document_number=numero,
        is_active=True
    ).first()
    
    if document:
        return jsonify(document.to_dict())
    else:
        return jsonify({'error': 'Document non trouvé'}), 404
```

#### C. Suppression (sans Modification)

```python
@app.route('/api/delete/<document_id>', methods=['DELETE'])
def delete_document(document_id):
    document = Document.query.get_or_404(document_id)
    
    # Soft delete (marquer comme inactif)
    document.is_active = False
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Document supprimé'})

# PAS DE ROUTE /api/update - MODIFICATION INTERDITE
```

---

### 5. SÉCURITÉ ET RÈGLES MÉTIER

#### ✅ Autorisé :
- Créer un nouveau document
- Voir la liste complète
- Voir les détails d'un document
- Télécharger le DOCX
- Supprimer un document (soft delete)
- Rechercher par numéro

#### ❌ Interdit :
- Modifier un document existant
- Changer le numéro
- Restaurer un document supprimé (dans l'interface)

#### 🔒 Règles de Validation :
```python
# Tous les champs obligatoires
required_fields = [
    'date_prelevement',
    'lieu',
    'date_reception',
    'identite_preleveur',
    'identite_demandeur',
    'resultats' (au moins 1),
    'conclusion',
    'titre_signataire',
    'nom_signataire'
]

# Note (NB) : optionnel
# Numéro : auto-généré, jamais saisi manuellement
```

---

### 6. BASE DE DONNÉES

#### Table : `documents`
```sql
CREATE TABLE documents (
    id VARCHAR(36) PRIMARY KEY,
    document_number VARCHAR(100) UNIQUE NOT NULL,  -- 001/2026
    date_prelevement DATETIME NOT NULL,
    lieu VARCHAR(200) NOT NULL,
    date_reception DATETIME NOT NULL,
    identite_preleveur VARCHAR(200),
    identite_demandeur VARCHAR(200),
    resultats_json TEXT,  -- JSON: [{ct:34, cf:0, sf:0}, ...]
    conclusion TEXT,
    note TEXT,
    nom_signataire VARCHAR(200),
    titre_signataire VARCHAR(200),
    verification_token VARCHAR(64) UNIQUE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);
```

#### Table : `document_counter`
```sql
CREATE TABLE document_counter (
    year INTEGER PRIMARY KEY,
    counter INTEGER DEFAULT 0
);
```

---

### 7. FICHIERS À CRÉER

```
water_final/
├── app.py                      # Application Flask
├── models.py                   # Modèles (Document, DocumentCounter)
├── database.py                 # Configuration DB
├── qr_generator.py             # Génération QR Code
├── docx_generator.py           # ✨ NOUVEAU: Génération DOCX format exact
├── requirements.txt            # Dépendances
├── init_db.py                  # Initialisation DB
│
├── static/
│   └── images/
│       ├── image1.jpeg         # Logo en-tête (extrait)
│       ├── image2.jpeg         # (si nécessaire)
│       └── image3.jpeg         # (si nécessaire)
│
└── templates/
    ├── index.html              # Formulaire de création
    ├── liste.html              # Liste des documents
    └── verification.html       # Page vérification QR
```

---

### 8. PRIORITÉS D'IMPLÉMENTATION

#### Phase 1 : Base (Essentiel)
1. ✅ Modèles avec auto-incrémentation
2. ✅ Formulaire de création
3. ✅ Génération DOCX format exact
4. ✅ QR Code en en-tête

#### Phase 2 : Liste et Recherche
5. ✅ Page liste des documents
6. ✅ Recherche par numéro
7. ✅ Modal détails
8. ✅ Téléchargement DOCX

#### Phase 3 : Gestion
9. ✅ Suppression (soft delete)
10. ✅ Confirmation suppression
11. ✅ Blocage modification

---

### 9. DIFFÉRENCES CLÉS vs Version Précédente

| Aspect | Avant | Maintenant |
|--------|-------|------------|
| **Infos analyse** | Dans tableau | Hors tableau (paragraphes) |
| **Numérotation** | Manuelle | Auto: 001/2026, 002/2026... |
| **Lieu** | Non géré | Champ séparé obligatoire |
| **Tableau** | Paramètres variés | Fixe: 3 lignes bactério |
| **Pied de page** | URL vérification | Vide (pas d'URL) |
| **Modification** | Autorisée | ❌ Interdite |
| **Liste docs** | Absente | ✅ Page complète |
| **Recherche** | Absente | ✅ Par numéro |
| **Signature** | Simple | Titre + Nom |

---

### 10. TESTS À EFFECTUER

#### ✅ Checklist de Validation

**Création :**
- [ ] Numéro s'incrémente automatiquement
- [ ] Pas de doublon possible
- [ ] Tous les champs obligatoires validés
- [ ] Plusieurs échantillons gérés

**Document DOCX :**
- [ ] Logo en haut à gauche
- [ ] QR Code en haut à droite
- [ ] Infos HORS tableau (paragraphes)
- [ ] Tableau avec 3 lignes exactes
- [ ] Conclusion de l'éditeur
- [ ] NB de l'éditeur
- [ ] Signature (titre + nom)
- [ ] PAS d'URL en pied de page

**Liste :**
- [ ] Tous les documents affichés
- [ ] Tri par numéro décroissant
- [ ] Recherche fonctionne
- [ ] Vue détails s'ouvre
- [ ] Téléchargement DOCX
- [ ] Suppression avec confirmation
- [ ] Pas de bouton "Modifier"

**Vérification QR :**
- [ ] Scan QR ouvre la page
- [ ] Informations affichées
- [ ] Document invalide détecté

---

## 🚀 COMMANDES DE DÉMARRAGE

```bash
# Installation
pip install -r requirements.txt

# Initialisation
python init_db.py

# Lancement
python app.py

# Ouvrir
http://localhost:5000
```

---

## 📝 NOTES IMPORTANTES

1. **Image1.jpeg** = Logo principal en-tête
2. **Numéro auto** = JAMAIS saisi par l'utilisateur
3. **Lieu** = Toujours saisi manuellement (pas auto)
4. **Tableau** = Toujours 3 lignes identiques (structure fixe)
5. **Modification** = INTERDITE (sécurité documents officiels)
6. **Pied de page** = VIDE (pas d'URL de vérification)

---

*Cahier des charges créé le 28 janvier 2026*  
*Version : 3.0 - Analyses Microbiologiques*
