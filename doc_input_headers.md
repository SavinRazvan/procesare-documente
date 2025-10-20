# Documentație Câmpuri Date Sursă

Acest document oferă o reprezentare precisă a configurațiilor curente de câmpuri și anteturi de ieșire pentru fiecare model de procesor, bazată pe configurația actuală `config/models.json` și comportamentul curent al sistemului.

**Ultima Actualizare:** 2025.10.05  
**Autor:** Savin Ionut Razvan  
**Versiune:** 2.0

## Cuprins

### A) Straturi Principale (Procesori Specializați)
1. [Case](#case)
2. [Camereta](#camereta)
3. [Enclosure](#enclosure)
4. [Fibra](#fibra)
5. [Hub](#hub)
6. [Localitati](#localitati)
7. [Scari](#scari)
8. [Spliter](#spliter)
9. [Stalpi](#stalpi)
10. [Zona Hub](#zona-hub)
11. [Zona Interventie](#zona-interventie)
12. [Zona Pon](#zona-pon)
13. [Zona Pon RE FTTH1000](#zona-pon-re-ftth1000)
14. [Zona Spliter](#zona-spliter)

### B) Straturi de Căutare (Procesori de Căutare)
1. [FTTB Search](#fttb-search)
2. [Enclosure Search](#enclosure-search)
3. [Camereta Search](#camereta-search)
4. [Scari Search](#scari-search)

---

## A) Straturi Principale

### Case
**Procesor:** `_case.py`  
**Fișiere Sursă:** Fișiere care conțin `CASE_` în nume  
**Rezultat:** Fișiere individuale + Fișier centralizat

#### **Anteturi Rezultat Curent (După Procesare):**
- `COD_FTTB` - Cod FTTB (obligatoriu, pattern: ^[A-Z0-9_-]+$)
- `LOCALITATE` - Localitate (opțional, 2-100 caractere)
- `TIP_ART` - Tip Articol (opțional, max 50 caractere)
- `DENUMIRE_ART` - Denumire Articol (obligatoriu, 2-100 caractere)
- `NR_ART` - Număr Articol (obligatoriu, max 50 caractere)
- `STARE_RETEA` - Stare Rețea (obligatoriu, max 50 caractere)
- `ZONA_RETEA` - Zonă Rețea (obligatoriu, max 50 caractere)
- `TIP_ECHIPAMENT` - Tip Echipament (obligatoriu, max 50 caractere)
- `OBSERVATII` - Observații (opțional, max 500 caractere)

**Fișiere Rezultat:**
- Fișiere individuale: `_output/case/CASE_*.geojson` (format compact)
- Fișier centralizat: `_output/case_centralized.geojson`
- Manifest: `_output/case/manifest.json`

### Camereta
**Procesor:** `_camereta.py`  
**Fișiere Sursă:** Fișiere care conțin `CAMERETA_` în nume  
**Rezultat:** Doar fișier centralizat

#### **Anteturi Rezultat Curent (După Procesare):**
- `LOCALITATE` - Localitate (obligatoriu, 2-100 caractere)
- `ID_TABELA` - ID Tabelă (obligatoriu, pattern: ^[A-Z0-9_-]+$)
- `OBSERVATII_1` - Observații 1 (obligatoriu, max 500 caractere)
- `OBSERVATII_2` - Observații 2 (obligatoriu, max 500 caractere)
- `MI_PRINX` - Index MapInfo (opțional, max 50 caractere)

**Fișiere Rezultat:**
- Fișier centralizat: `_output/camereta_centralized.geojson`

### Enclosure
**Procesor:** `_enclosure.py`  
**Fișiere Sursă:** Fișiere care conțin `ENCLOSURE_` în nume  
**Rezultat:** Doar fișier centralizat

#### **Anteturi Rezultat Curent (După Procesare):**
- `LOCALITATE` - Localitate (obligatoriu, 2-100 caractere)
- `ENCLOSURE_ID` - ID Enclosure (obligatoriu, pattern: ^[A-Z0-9_-]+$)
- `OBSERVATII` - Observații (obligatoriu, max 500 caractere)

**Fișiere Rezultat:**
- Fișier centralizat: `_output/enclosure_centralized.geojson`

### Fibra
**Procesor:** `_fibra.py`  
**Fișiere Sursă:** Fișiere care conțin `FO_` în nume  
**Rezultat:** Doar fișier centralizat

#### **Anteturi Rezultat Curent (După Procesare):**
- `NR_FIRE` - Număr Fire (obligatoriu, întreg, min 1)
- `LUNGIME_HARTA` - Lungime Hartă (obligatoriu, număr, min 0)
- `LUNGIME_TEREN` - Lungime Teren (obligatoriu, număr, min 0)
- `AMPLASARE` - Amplasare (obligatoriu, max 100 caractere)
- `LOCALITATE` - Localitate (obligatoriu, 2-100 caractere)

**Fișiere Rezultat:**
- Fișier centralizat: `_output/fibra_centralized.geojson`

### Hub
**Procesor:** `_hub.py`  
**Fișiere Sursă:** Fișiere care conțin `HUB_` în nume  
**Rezultat:** Doar fișier centralizat

#### **Anteturi Rezultat Curent (După Procesare):**
- `NUME` - Nume (obligatoriu, 2-100 caractere)
- `LOCALITATE` - Localitate (obligatoriu, 2-100 caractere)
- `ADRESA` - Adresă (obligatoriu, 2-200 caractere)
- `COD_FTTB` - Cod FTTB (obligatoriu, pattern: ^[A-Z0-9_-]+$)
- `OLT` - OLT (obligatoriu, max 50 caractere)
- `COMBINER` - Combiner (obligatoriu, max 50 caractere)
- `SURSA_48V` - Sursă 48V (obligatoriu, max 50 caractere)
- `AC` - AC (obligatoriu, max 50 caractere)
- `MOTIVE_NEFUNCT_HUB` - Motive Nefuncționare Hub (obligatoriu, max 200 caractere)
- `FIBRE` - Fire (obligatoriu, max 50 caractere)

**Fișiere Rezultat:**
- Fișier centralizat: `_output/hub_centralized.geojson`

### Localitati
**Procesor:** `_localitati.py`  
**Fișiere Sursă:** Fișiere care conțin `LOCALITATI_` în nume  
**Rezultat:** Doar fișier centralizat

#### **Anteturi Rezultat Curent (După Procesare):**
- `NUME` - Nume (obligatoriu, 2-100 caractere)
- `COMUNA` - Comună (obligatoriu, 2-100 caractere)
- `NR_CASE` - Număr Case (obligatoriu, max 50 caractere)
- `ID_CITY_VOICE` - ID City Voice (obligatoriu, max 50 caractere)
- `MI_PRINX` - Index MapInfo (obligatoriu, max 50 caractere)
- `SIRUTA` - Cod SIRUTA (obligatoriu, max 100 caractere)
- `OBS` - Observații (obligatoriu, max 500 caractere)
- `PROIECTANT` - Proiectant (obligatoriu, max 100 caractere)

**Fișiere Rezultat:**
- Fișier centralizat: `_output/localitati_centralized.geojson`

### Scari
**Procesor:** `_scari.py`  
**Fișiere Sursă:** Fișiere care conțin `SCARI_` în nume  
**Rezultat:** Doar fișier centralizat

#### **Anteturi Rezultat Curent (După Procesare):**
- `COD_FTTB` - Cod FTTB (obligatoriu, pattern: ^[A-Z0-9_-]+$)
- `TIP_ART` - Tip Articol (obligatoriu, max 50 caractere)
- `DENUMIRE_ART` - Denumire Articol (obligatoriu, 2-100 caractere)
- `NR_ART` - Număr Articol (obligatoriu, max 50 caractere)
- `DENUMIRE_BLOC` - Denumire Bloc (obligatoriu, max 100 caractere)
- `NR_SCARA` - Număr Scară (obligatoriu, max 50 caractere)
- `TIP_RETEA` - Tip Rețea (opțional, max 50 caractere)
- `ZONA_RETEA` - Zonă Rețea (opțional, max 50 caractere)
- `OBSERVATII` - Observații (opțional, max 500 caractere)
- `ZONA_RETEA_FTTH1000` - Zonă Rețea FTTH1000 (opțional, max 50 caractere)
- `ZONA_RETEA_FTTH_V2` - Zonă Rețea FTTH V2 (opțional, max 50 caractere)
- `LOCALITATE` - Localitate (opțional, 2-100 caractere)

**Fișiere Rezultat:**
- Fișier centralizat: `_output/scari_centralized.geojson`

### Spliter
**Procesor:** `_spliter.py`  
**Fișiere Sursă:** Fișiere care conțin `SPLITER_` în nume  
**Rezultat:** Doar fișier centralizat

#### **Anteturi Rezultat Curent (După Procesare):**
- `TIP_SPLITER` - Tip Splitter (obligatoriu, max 50 caractere)
- `NR_SPLITERE` - Număr Splitere (opțional, max 50 caractere)

**Fișiere Rezultat:**
- Fișier centralizat: `_output/spliter_centralized.geojson`

### Stalpi
**Procesor:** `_stalpi.py`  
**Fișiere Sursă:** Fișiere care conțin `STALPI_` în nume  
**Rezultat:** Doar fișier centralizat

#### **Anteturi Rezultat Curent (După Procesare):**
- `LOCALITATE` - Localitate (obligatoriu, 2-100 caractere)
- `FOLOSIT_RDS` - Folosit RDS (obligatoriu, max 50 caractere)
- `MATERIAL_CONSTRUCTIV` - Material Constructiv (obligatoriu, max 50 caractere)
- `TIP_STALP` - Tip Stâlp (obligatoriu, max 50 caractere)

**Fișiere Rezultat:**
- Fișier centralizat: `_output/stalpi_centralized.geojson`

### Zona Hub
**Procesor:** `_zona_hub.py`  
**Fișiere Sursă:** Fișiere care conțin `ZONA_ACOPERIRE_HUB_` în nume  
**Rezultat:** Doar fișier centralizat

#### **Anteturi Rezultat Curent (După Procesare):**
- `NUME` - Nume (obligatoriu, 2-100 caractere)
- `NR_CASE` - Număr Case (obligatoriu, max 50 caractere)
- `NR_CASE_ACOPERIRE` - Număr Case Acoperire (obligatoriu, max 50 caractere)
- `NR_CASE_ACTIVE` - Număr Case Active (obligatoriu, max 50 caractere)
- `NR_SCARI` - Număr Scări (obligatoriu, max 50 caractere)
- `NR_APT` - Număr Apartamente (obligatoriu, max 50 caractere)

**Fișiere Rezultat:**
- Fișier centralizat: `_output/zona_hub_centralized.geojson`

### Zona Interventie
**Procesor:** `_zone_interventie.py`  
**Fișiere Sursă:** Fișiere care conțin `ZONA_` sau `ZONE_` în nume  
**Rezultat:** Doar fișier centralizat

#### **Anteturi Rezultat Curent (După Procesare):**
- `LOCALITATE` - Localitate (obligatoriu, 2-100 caractere)
- `ZONA` - Zonă (obligatoriu, max 50 caractere)
- `ECHIPA` - Echipă (obligatoriu, max 50 caractere)
- `TIP_ECHIPA` - Tip Echipă (obligatoriu, max 50 caractere)

**Fișiere Rezultat:**
- Fișier centralizat: `_output/zone_interventie_centralized.geojson`

### Zona Pon
**Procesor:** `_zona_pon.py`  
**Fișiere Sursă:** Fișiere care conțin `ZONA_PON_REALIZAT_` în nume  
**Rezultat:** Doar fișier centralizat

#### **Anteturi Rezultat Curent (După Procesare):**
- `PON` - Identificator PON (obligatoriu, pattern: ^PON-[A-Z0-9_-]+$)
- `OBSERVATII` - Observații (obligatoriu, max 500 caractere)

**Fișiere Rezultat:**
- Fișier centralizat: `_output/zona_pon_centralized.geojson`

### Zona Pon RE FTTH1000
**Procesor:** `_zona_pon_re_ftth1000.py`  
**Fișiere Sursă:** Fișiere care conțin `ZONA_PON_RE_FTTH1000_` în nume  
**Rezultat:** Doar fișier centralizat

#### **Anteturi Rezultat Curent (După Procesare):**
- `PON` - Identificator PON (obligatoriu, pattern: ^PON-[A-Z0-9_-]+$)
- `OLT` - Identificator OLT (obligatoriu, pattern: ^OLT-[A-Z0-9_-]+$)
- `HOTLINK` - HotLink (opțional, max 50 caractere)

**Fișiere Rezultat:**
- Fișier centralizat: `_output/zona_pon_re_ftth1000_centralized.geojson`

### Zona Spliter
**Procesor:** `_zona_spliter.py`  
**Fișiere Sursă:** Fișiere care conțin `ZONA_SPLITER_REALIZAT_` în nume  
**Rezultat:** Doar fișier centralizat

#### **Anteturi Rezultat Curent (După Procesare):**
- `ID_ZONA` - ID Zonă (obligatoriu, max 50 caractere)

**Fișiere Rezultat:**
- Fișier centralizat: `_output/zona_spliter_centralized.geojson`

---

## B) Straturi de Căutare

### FTTB Search
**Procesor:** `_fttb_search.py`  
**Fișiere Sursă:** Fișiere procesate de procesorul de căutare FTTB  
**Rezultat:** Doar fișier centralizat

#### **Anteturi Rezultat Curent (După Procesare):**
- `COD_FTTB` - Cod FTTB (obligatoriu, pattern: ^[A-Z0-9_-]+$)
- `LOCALITATE` - Localitate (obligatoriu, 2-100 caractere)

**Fișiere Rezultat:**
- Fișier centralizat: `_output/fttb_search.geojson`

### Enclosure Search
**Procesor:** `_enclosure_search.py`  
**Fișiere Sursă:** Fișiere procesate de procesorul de căutare enclosure  
**Rezultat:** Doar fișier centralizat

#### **Anteturi Rezultat Curent (După Procesare):**
- `ENCLOSURE_ID` - ID Enclosure (obligatoriu, pattern: ^[A-Z0-9_-]+$)
- `LOCALITATE` - Localitate (obligatoriu, 2-100 caractere)

**Fișiere Rezultat:**
- Fișier centralizat: `_output/enclosure_search.geojson`

### Camereta Search
**Procesor:** `_camereta_search.py`  
**Fișiere Sursă:** Fișiere procesate de procesorul de căutare camereta  
**Rezultat:** Doar fișier centralizat

#### **Anteturi Rezultat Curent (După Procesare):**
- `LOCALITATE` - Localitate (obligatoriu, 2-100 caractere)
- `ID_TABELA` - ID Tabelă (obligatoriu, pattern: ^[A-Z0-9_-]+$)

**Fișiere Rezultat:**
- Fișier centralizat: `_output/camereta_search.geojson`

### Scari Search
**Procesor:** `_scari_search.py`  
**Fișiere Sursă:** Fișiere procesate de procesorul de căutare scari  
**Rezultat:** Doar fișier centralizat

#### **Anteturi Rezultat Curent (După Procesare):**
- `COD_FTTB` - Cod FTTB (obligatoriu, pattern: ^[A-Z0-9_-]+$)
- `TIP_ART` - Tip Articol (obligatoriu, max 50 caractere)
- `DENUMIRE_ART` - Denumire Articol (obligatoriu, 2-100 caractere)
- `NR_ART` - Număr Articol (obligatoriu, max 50 caractere)
- `DENUMIRE_BLOC` - Denumire Bloc (obligatoriu, max 100 caractere)
- `NR_SCARA` - Număr Scară (obligatoriu, max 50 caractere)
- `LOCALITATE` - Localitate (obligatoriu, 2-100 caractere)

**Fișiere Rezultat:**
- Fișier centralizat: `_output/scari_search.geojson`

---

## Funcționalități Actuale ale Sistemului

### Funcționalități de Procesare
- **Detectare Multi-encoding**: UTF-8, ISO-8859-1, Windows-1252, CP1252
- **Procesare Anteturi Majuscule**: Toate numele de câmpuri convertite la majuscule pentru consistență
- **Detectare Duplicate**: Bazată pe câmpuri cheie și geometrie
- **Format Compact**: JSON pe o singură linie pentru stocare eficientă
- **Rezultat Centralizat**: Majoritatea procesorilor creează doar fișiere centralizate
- **Fișiere Individuale**: Doar procesorul Case creează fișiere individuale + manifest.json
- **Filtrare Nume Fișiere**: Procesorii procesează doar fișiere cu modele specifice de nume
- **Filtrare Proprietăți Goale**: Entitățile cu câmpuri obligatorii goale sunt omise
- **Câmpuri Obligatorii Specifice Modelului**: Fiecare model are propriul set de câmpuri obligatorii pentru filtrare

### Modele de Procesare Fișiere
- **Case**: `CASE_*` → Fișiere individuale + Centralizat
- **Camereta**: `CAMERETA_*` → Doar centralizat
- **Enclosure**: `ENCLOSURE_*` → Doar centralizat
- **Fibra**: `FO_*` → Doar centralizat
- **Hub**: `HUB_*` → Doar centralizat
- **Localitati**: `LOCALITATI_*` → Doar centralizat
- **Scari**: `SCARI_*` → Doar centralizat
- **Spliter**: `SPLITER_*` → Doar centralizat
- **Stalpi**: `STALPI_*` → Doar centralizat
- **Zona Hub**: `ZONA_ACOPERIRE_HUB_*` → Doar centralizat
- **Zona Interventie**: `ZONA_*` sau `ZONE_*` → Doar centralizat
- **Zona Pon**: `ZONA_PON_REALIZAT_*` → Doar centralizat
- **Zona Pon RE FTTH1000**: `ZONA_PON_RE_FTTH1000_*` → Doar centralizat
- **Zona Spliter**: `ZONA_SPLITER_REALIZAT_*` → Doar centralizat

### Rezumat Numărul de Câmpuri
**Straturi Principale - Câmpuri Extrase:**
- **Case**: 9 câmpuri (1 obligatoriu, 8 opționale)
- **Camereta**: 5 câmpuri (4 obligatorii, 1 opțional)
- **Enclosure**: 3 câmpuri (3 obligatorii)
- **Fibra**: 5 câmpuri (5 obligatorii)
- **Hub**: 10 câmpuri (10 obligatorii)
- **Localitati**: 8 câmpuri (8 obligatorii)
- **Scari**: 12 câmpuri (6 obligatorii, 6 opționale)
- **Spliter**: 2 câmpuri (1 obligatoriu, 1 opțional)
- **Stalpi**: 4 câmpuri (4 obligatorii)
- **Zona Hub**: 6 câmpuri (6 obligatorii)
- **Zona Interventie**: 4 câmpuri (4 obligatorii)
- **Zona Pon**: 2 câmpuri (2 obligatorii)
- **Zona Pon RE FTTH1000**: 3 câmpuri (2 obligatorii, 1 opțional)
- **Zona Spliter**: 1 câmp (1 obligatoriu)

**Straturi de Căutare - Câmpuri Extrase:**
- **FTTB Search**: 2 câmpuri (2 obligatorii)
- **Enclosure Search**: 2 câmpuri (2 obligatorii)
- **Camereta Search**: 2 câmpuri (2 obligatorii)
- **Scari Search**: 7 câmpuri (7 obligatorii)

### Structura Fișierelor Rezultat
- **Fișiere Individuale**: Doar procesorul Case creează fișiere individuale în folderul `_output/case/`
- **Fișiere Centralizate**: Toți procesorii creează fișiere centralizate în folderul `_output/`
- **Fișiere Manifest**: Doar procesorul Case creează `manifest.json` cu listarea fișierelor
- **Format Compact**: Toate fișierele rezultat folosesc format JSON compact pentru eficiență
- **Anteturi Profesionale**: Toate fișierele includ anteturi GeoJSON și metadate corespunzătoare
