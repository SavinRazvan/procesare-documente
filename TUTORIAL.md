# Procesor GeoJSON V2 - Ghid Complet (Actualizat)

## 📋 Prezentare Generală

Acest ghid acoperă utilizarea sistemului Procesor GeoJSON V2 pentru procesarea diferitelor tipuri de date de infrastructură de rețea. Sistemul suportă **23 tipuri diferite de modele** pentru atât straturile principale cât și operațiunile de căutare.

## 🏗️ Arhitectura Sistemului

### Componente Principale
- **Procesoare Individuale**: Procesează tipuri specifice de modele cu anteturi standardizate
- **Procesor Principal**: Orchestrează toate procesoarele individuale
- **Configurația Modelelor**: Definește regulile de detectare și maparea câmpurilor
- **Procesarea Centralizată**: Creează fișiere de ieșire unificate per tip de model

### Tipuri de Modele

#### Straturi Principale (14 modele)
- `camereta` - Cabină Tehnică
- `enclosure` - Închidere Tehnică  
- `hub` - Hub de Rețea
- `localitati` - Localități
- `stalpi` - Stâlpi Utilitari
- `zona_hub` - Zona de Acoperire Hub
- `zone_interventie` - Zona de Intervenție
- `case` - Clădire Rezidențială
- `spliter` - Divizor de Semnal
- `zona_pon` - Zona PON
- `zona_spliter` - Zona Divizor
- `fibra` - Fibră Optică
- `scari` - Scări
- `zona_pon_re_ftth1000` - Zona PON RE FTTH1000

#### Straturi de Căutare (4 modele)
- `fttb_search` - Căutare FTTB
- `scari_search` - Căutare Scări
- `camereta_search` - Căutare Cameră
- `enclosure_search` - Căutare Închidere

## 🚀 Început Rapid

### Cerințe Preliminare
- **Python**: 3.11+ (recomandat: 3.11.13)
- **Conda**: Pentru managementul mediilor
- **Sistem de Operare**: Linux (testat pe WSL2)

### Configurarea Mediului

#### 1. Creează Mediul Conda
```bash
# Creează mediul nou (dacă nu există)
conda create -n .proc_doc python=3.11 -y

# Verifică mediile disponibile
conda env list
```

#### 2. Activează Mediul
```bash
# Activează mediul conda
conda activate .proc_doc

# Verifică că mediul este activ (ar trebui să vezi * lângă .proc_doc)
conda info --envs
```

#### 3. Navighează la Proiect
```bash
# Navighează la directorul proiectului
cd /home/razvansavin/Projects/procesare-documente

# Verifică că ești în directorul corect
pwd
```

#### 4. Testează Instalarea
```bash
# Testează un procesor individual
python3 _camereta.py --help

# Testează procesorul principal
python3 _process_all.py --help
```

### Dependențe

#### ✅ Nu Sunt Necesare Pachete Externe!

Acest proiect folosește **doar module din biblioteca standard Python**:

- `json` - Procesarea JSON
- `sys` - Parametrii sistem
- `pathlib` - Căi sistem de fișiere
- `typing` - Hint-uri de tip
- `dataclasses` - Clase de date
- `datetime` - Utilitare dată/timp
- `logging` - Facilitate de logging
- `re` - Expresii regulate
- `enum` - Enumerări
- `time` - Funcții de timp
- `hashlib` - Algoritmi hash
- `argparse` - Argumente linie de comandă
- `subprocess` - Management procese

#### De ce Nu Este Necesar requirements.txt?

Deoarece toată funcționalitatea este construită folosind biblioteca standard Python, nu sunt necesare pachete externe. Acest lucru face sistemul:

- **Ușor**: Fără conflicte de pachete
- **Portabil**: Funcționează pe orice sistem Python 3.11+
- **De încredere**: Fără probleme de management al dependențelor
- **Rapid**: Fără timp de instalare a pachetelor

### Utilizare de Bază
```bash
# Procesează toate modelele deodată
python3 _process_all.py _input _output

# Procesează modele specifice
python3 _process_all.py _input _output --models camereta case spliter

# Dezactivează detectarea duplicatelor
python3 _process_all.py _input _output --no-duplicates
```

## 📁 Comenzi Procesoare Individuale

### Procesoare Strat Principal

#### 1. Procesor Camereta
```bash
# Procesează fișierele camereta
python3 _camereta.py _input _output

# Fără detectarea duplicatelor
python3 _camereta.py _input _output --no-duplicates
```
**Ieșire**: 
- **Doar fișier centralizat**: `camereta_centralized.geojson`
- **Filtrare**: Doar fișiere cu `CAMERETA_` în nume

#### 2. Procesor Case
```bash
# Procesează fișierele case (creează subdirectorul case/)
python3 _case.py _input _output
```
**Ieșire**: 
- **Fișiere individuale**: `case/CASE_*.geojson` (compact format)
- **Fișier centralizat**: `case_centralized.geojson`
- **Manifest**: `case/manifest.json`
- **Filtrare**: Doar fișiere cu `CASE_` în nume

#### 3. Procesor Enclosure
```bash
python3 _enclosure.py _input _output
```
**Ieșire**: 
- **Doar fișier centralizat**: `enclosure_centralized.geojson`
- **Filtrare**: Doar fișiere cu `ENCLOSURE_` în nume

#### 4. Procesor Hub
```bash
python3 _hub.py _input _output
```
**Ieșire**: 
- **Doar fișier centralizat**: `hub_centralized.geojson`
- **Filtrare**: Doar fișiere cu `HUB_` în nume

#### 5. Procesor Localitati
```bash
python3 _localitati.py _input _output
```
**Ieșire**: 
- **Doar fișier centralizat**: `localitati_centralized.geojson`
- **Filtrare**: Doar fișiere cu `LOCALITATI_` în nume

#### 6. Procesor Stalpi
```bash
python3 _stalpi.py _input _output
```
**Ieșire**: 
- **Doar fișier centralizat**: `stalpi_centralized.geojson`
- **Filtrare**: Doar fișiere cu `STALPI_` în nume

#### 7. Procesor Zona Hub
```bash
python3 _zona_hub.py _input _output
```
**Ieșire**: 
- **Doar fișier centralizat**: `zona_hub_centralized.geojson`
- **Filtrare**: Doar fișiere cu `ZONA_ACOPERIRE_HUB_` în nume

#### 8. Procesor Zone Interventie
```bash
python3 _zone_interventie.py _input _output
```
**Ieșire**: 
- **Doar fișier centralizat**: `zone_interventie_centralized.geojson`
- **Filtrare**: Doar fișiere cu `ZONA_` sau `ZONE_` în nume

#### 9. Procesor Spliter
```bash
python3 _spliter.py _input _output
```
**Ieșire**: 
- **Doar fișier centralizat**: `spliter_centralized.geojson`
- **Filtrare**: Doar fișiere cu `SPLITER_` în nume

#### 10. Procesor Zona PON
```bash
python3 _zona_pon.py _input _output
```
**Ieșire**: 
- **Doar fișier centralizat**: `zona_pon_centralized.geojson`
- **Filtrare**: Doar fișiere cu `ZONA_PON_REALIZAT_` în nume

#### 11. Procesor Zona Spliter
```bash
python3 _zona_spliter.py _input _output
```
**Ieșire**: 
- **Doar fișier centralizat**: `zona_spliter_centralized.geojson`
- **Filtrare**: Doar fișiere cu `ZONA_SPLITER_REALIZAT_` în nume

#### 12. Procesor Fibra
```bash
python3 _fibra.py _input _output
```
**Ieșire**: 
- **Doar fișier centralizat**: `fibra_centralized.geojson`
- **Filtrare**: Doar fișiere cu `FO_` în nume

#### 13. Procesor Scari
```bash
python3 _scari.py _input _output
```
**Ieșire**: 
- **Doar fișier centralizat**: `scari_centralized.geojson`
- **Filtrare**: Doar fișiere cu `SCARI_` în nume

#### 14. Procesor Zona PON RE FTTH1000
```bash
python3 _zona_pon_re_ftth1000.py _input _output
```
**Ieșire**: 
- **Doar fișier centralizat**: `zona_pon_re_ftth1000_centralized.geojson`
- **Filtrare**: Doar fișiere cu `ZONA_PON_RE_FTTH1000_` în nume

### Procesoare Strat de Căutare

#### 1. Procesor FTTB Search
```bash
python3 _fttb_search.py _input _output
```
**Ieșire**: 
- **Doar fișier centralizat**: `fttb_search.geojson`

#### 2. Procesor Scari Search
```bash
python3 _scari_search.py _input _output
```
**Ieșire**: 
- **Doar fișier centralizat**: `scari_search.geojson`

#### 3. Procesor Camereta Search
```bash
python3 _camereta_search.py _input _output
```
**Ieșire**: 
- **Doar fișier centralizat**: `camereta_search.geojson`

#### 4. Procesor Enclosure Search
```bash
python3 _enclosure_search.py _input _output
```
**Ieșire**: 
- **Doar fișier centralizat**: `enclosure_search.geojson`

## 🎯 Utilizarea Procesorului Principal

### Procesează Toate Modelele
```bash
# Procesează toate cele 23 tipuri de modele
python3 _process_all.py _input _output
```

### Procesează Modele Specifice
```bash
# Procesează doar straturile principale
python3 _process_all.py _input _output --models camereta case spliter hub

# Procesează doar straturile de căutare
python3 _process_all.py _input _output --models fttb_search camereta_search scari_search enclosure_search

# Procesează selecție mixtă
python3 _process_all.py _input _output --models camereta camereta_search case fttb_search
```

### Opțiuni Avansate
```bash
# Dezactivează detectarea duplicatelor
python3 _process_all.py _input _output --no-duplicates

# Procesează modele specifice fără duplicate
python3 _process_all.py _input _output --models camereta case --no-duplicates
```

## 📊 Formatul Ieșirii

### Fișiere Individuale (Doar Case)
- **Format**: GeoJSON compact (o singură linie)
- **Denumire**: `case/CASE_[nume_fisier_original].geojson`
- **Conținut**: Anteturi standardizate cu doar câmpurile extrase
- **Manifest**: `case/manifest.json` cu lista fișierelor procesate

### Fișiere Centralizate (Toate Procesoarele)
- **Format**: GeoJSON compact (o singură linie)
- **Denumire**: `[model]_centralized.geojson`
- **Conținut**: Toate features din fișierele corespunzătoare combinate
- **Sortare**: Alfabetică după LOCALITATE

### Cazuri Speciale
- **Fișiere case**: Stocate în subdirectorul `case/` cu manifest.json
- **Fișiere căutare**: Optimizate pentru operațiuni de căutare cu câmpuri minime
- **Filtrare avansată**: Toate procesoarele filtrează features cu câmpuri goale

## 🔧 Configurare

### Managementul Mediului

#### Verificarea Mediului
```bash
# Verifică mediul activ
conda info --envs
# Ar trebui să vezi * lângă .proc_doc

# Verifică versiunea Python
python3 --version
# Ar trebui să fie 3.11+

# Verifică că nu sunt necesare pachete externe
cat requirements.txt
# Arată că se folosesc doar module din biblioteca standard
```

#### Recrearea Mediului (dacă este necesar)
```bash
# Dezactivează mediul curent
conda deactivate

# Șterge mediul vechi (dacă există probleme)
conda env remove -n .proc_doc -y

# Creează mediul nou
conda create -n .proc_doc python=3.11 -y

# Activează mediul
conda activate .proc_doc
```

### Configurația Modelelor (`config/models.json`)
- Definește câmpurile necesare pentru detectarea modelelor
- Specifică câmpurile de extragere pentru ieșire
- Setează regulile de validare și maparea câmpurilor
- **23 modele configurate** cu validări specifice

### Setările (`config/settings.json`)
- Parametrii de procesare
- Configurația de logging
- Setările de performanță

### Dependențe
- **Nu sunt necesare pachete externe!**
- Sistemul folosește doar module din biblioteca standard Python
- Verifică `requirements.txt` pentru lista completă de module folosite

## 📈 Sfaturi de Performanță

### Pentru Seturi de Date Mari
```bash
# Dezactivează detectarea duplicatelor pentru procesare mai rapidă
python3 _process_all.py _input _output --no-duplicates

# Procesează modelele individual pentru o gestionare mai bună a memoriei
python3 _camereta.py _input _output
python3 _case.py _input _output
# ... etc
```

### Pentru Dezvoltare/Testare
```bash
# Procesează modele specifice pentru testare
python3 _camereta.py _input _output
python3 _camereta_search.py _input _output
```

## 🐛 Rezolvarea Problemelor

### Probleme de Mediu

#### 1. Mediul Conda Nu Este Activ
```bash
# Verifică mediile disponibile
conda env list

# Activează mediul (ar trebui să vezi * lângă .proc_doc)
conda activate .proc_doc

# Verifică că mediul este activ
echo $CONDA_DEFAULT_ENV
# Ar trebui să afișeze: .proc_doc
```

#### 2. Mediul Nu Există
```bash
# Creează mediul dacă nu există
conda create -n .proc_doc python=3.11 -y

# Activează mediul
conda activate .proc_doc
```

#### 3. Probleme cu Python
```bash
# Verifică versiunea Python
python3 --version
# Ar trebui să fie 3.11+

# Verifică că Python este din mediul conda
which python3
# Ar trebui să conțină: /home/razvansavin/miniconda3/envs/.proc_doc
```

#### 4. Probleme de Import
```bash
# Verifică că ești în directorul corect
pwd
# Ar trebui să fie: /home/razvansavin/Projects/procesare-documente

# Verifică că directorul src există
ls -la src/
```

### Probleme de Procesare

#### 1. Nu Sunt Create Fișiere de Ieșire
```bash
# Verifică dacă fișierele de intrare se potrivesc cu cerințele modelelor
# Verifică configurația modelelor în config/models.json
# Verifică ieșirea consolei pentru avertismente de detectare
```

#### 2. Conflicte de Detectare a Modelelor
```bash
# Unele fișiere pot fi detectate ca modele diferite
# Verifică ieșirea consolei pentru mesajele "detected: [model]"
# Ajustează configurația modelelor dacă este necesar
```

#### 3. Probleme de Memorie cu Fișiere Mari
```bash
# Procesează fișierele individual în loc să folosești _process_all.py
python3 _camereta.py _input _output
python3 _case.py _input _output
```

### Comenzi de Debug
```bash
# Verifică structura fișierelor
ls -la _input/
ls -la _output/

# Verifică integritatea GeoJSON
python3 -c "import json; print('JSON Valid' if json.load(open('_output/camereta_centralized.geojson')) else 'JSON Invalid')"
```

## 📋 Fluxuri de Lucru Exemplu

### Flux de Procesare Complet
```bash
# 1. Creează și activează mediul (dacă nu există)
conda create -n .proc_doc python=3.11 -y
conda activate .proc_doc

# 2. Navighează la proiect
cd /home/razvansavin/Projects/procesare-documente

# 3. Verifică instalarea
python3 _camereta.py --help

# 4. Procesează toate modelele
python3 _process_all.py _input _output

# 5. Verifică ieșirea
ls -la _output/
```

### Flux de Testare Dezvoltare
```bash
# 1. Testează procesoarele individuale
python3 _camereta.py _input _output
python3 _camereta_search.py _input _output

# 2. Verifică formatul ieșirii
head -n 5 _output/camereta_centralized.geojson

# 3. Testează procesorul principal
python3 _process_all.py _input _output --models camereta camereta_search
```

### Flux Doar Straturi de Căutare
```bash
# Procesează doar straturile de căutare
python3 _process_all.py _input _output --models fttb_search camereta_search scari_search enclosure_search
```

## 📁 Structura Fișierelor

```
procesare-documente/
├── _input/                          # Fișiere GeoJSON de intrare
├── _output/                         # Fișiere procesate de ieșire
│   ├── case/                        # Subdirectorul fișierelor case
│   │   ├── CASE_*.geojson           # Fișiere individuale case
│   │   └── manifest.json            # Manifest cu lista fișierelor
│   ├── *_centralized.geojson         # Fișiere centralizate (toate modelele)
│   └── *_search.geojson             # Fișiere de căutare
├── config/
│   ├── models.json                  # Configurația modelelor (23 modele)
│   └── settings.json                # Setările de procesare
├── src/                             # Motorul de procesare principal
├── _process_all.py                  # Procesorul master
├── _[model].py                      # Procesoare individuale (23 procesoare)
└── TUTORIAL.md                      # Acest tutorial
```

## 🎉 Indicatori de Succes

### Verificarea Mediului
```bash
# Verifică că mediul este activ
conda info --envs
# Ar trebui să vezi * lângă .proc_doc

# Verifică versiunea Python
python3 --version
# Ar trebui să fie 3.11+

# Verifică că procesorii funcționează
python3 _camereta.py --help
# Ar trebui să afișeze ajutorul procesorului
```

### Ieșirea Consolei
```
🎉 Procesarea Completă!
📊 Procesate: X/Y fișiere
🔢 Total features: XXXX
🔄 Duplicate sărite: XX
📁 Fișier centralizat: _output/[model]_centralized.geojson
```

### Verificarea Fișierelor
```bash
# Verifică dimensiunile fișierelor (ar trebui să fie rezonabile)
ls -lh _output/*.geojson

# Verifică structura JSON
python3 -c "import json; data=json.load(open('_output/camereta_centralized.geojson')); print(f'Features: {len(data[\"features\"])}')"
```

## 🔍 Caracteristici Avansate

### Filtrare Inteligentă
- **Filtrare câmpuri goale**: Toate procesoarele sar peste features cu câmpuri goale
- **Câmpuri obligatorii**: Fiecare model are câmpurile sale obligatorii
- **Detectare duplicate**: Bazată pe câmpuri cheie și geometrie
- **Validare avansată**: Pattern matching și limite de lungime

### Procesare Multi-Encoding
- **UTF-8, ISO-8859-1, Windows-1252, CP1252**: Detectare automată
- **Anteturi uppercase**: Toate câmpurile convertite la uppercase
- **Format compact**: JSON pe o singură linie pentru eficiență

### Structura de Ieșire
- **Case**: Fișiere individuale + centralizat + manifest
- **Toate celelalte**: Doar fișier centralizat
- **Sortare**: Alfabetică după LOCALITATE
- **Metadate**: Timestamp și informații de procesare

## 📞 Suport

Pentru probleme sau întrebări:
1. Verifică ieșirea consolei pentru mesaje de eroare
2. Verifică formatul și conținutul fișierelor de intrare
3. Revizuiește configurația modelelor în `config/models.json`
4. Testează mai întâi cu procesoarele individuale
5. Verifică permisiunile fișierelor și spațiul pe disc

---

**Have fun! 🚀**

**Versiune**: 2.0  
**Autor**: Savin Ionut Razvan  
**Data**: 2025.10.05
