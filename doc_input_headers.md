# Input Data Headers - Documentation

This document provides an accurate representation of the current field configurations and output headers for each processor model, based on the actual `config/models.json` configuration and current system behavior.

**Last Updated:** 2025.10.05  
**Author:** Savin Ionut Razvan  
**Version:** 2.0

## Table of Contents

### A) Main Layers (Individual Processors)
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

### B) Search Layers (Search Processors)
1. [FTTB Search](#fttb-search)
2. [Enclosure Search](#enclosure-search)
3. [Camereta Search](#camereta-search)
4. [Scari Search](#scari-search)

---

## A) Main Layers

### Case
**Processor:** `_case.py`  
**Source Files:** Files containing `CASE_` in filename  
**Output:** Individual files + Centralized file

#### **Current Output Headers (After Processing):**
- `COD_FTTB` - FTTB Code (required, pattern: ^[A-Z0-9_-]+$)
- `LOCALITATE` - Locality (optional, 2-100 chars)
- `TIP_ART` - Article Type (optional, max 50 chars)
- `DENUMIRE_ART` - Article Name (required, 2-100 chars)
- `NR_ART` - Article Number (required, max 50 chars)
- `STARE_RETEA` - Network Status (required, max 50 chars)
- `ZONA_RETEA` - Network Zone (required, max 50 chars)
- `TIP_ECHIPAMENT` - Equipment Type (required, max 50 chars)
- `OBSERVATII` - Observations (optional, max 500 chars)

**Output Files:**
- Individual files: `_output/case/CASE_*.geojson` (compact format)
- Centralized file: `_output/case_centralized.geojson`
- Manifest: `_output/case/manifest.json`

### Camereta
**Processor:** `_camereta.py`  
**Source Files:** Files containing `CAMERETA_` in filename  
**Output:** Centralized file only

#### **Current Output Headers (After Processing):**
- `LOCALITATE` - Locality (required, 2-100 chars)
- `ID_TABELA` - Table ID (required, pattern: ^[A-Z0-9_-]+$)
- `OBSERVATII_1` - Observations 1 (required, max 500 chars)
- `OBSERVATII_2` - Observations 2 (required, max 500 chars)
- `MI_PRINX` - MapInfo index (optional, max 50 chars)

**Output Files:**
- Centralized file: `_output/camereta_centralized.geojson`

### Enclosure
**Processor:** `_enclosure.py`  
**Source Files:** Files containing `ENCLOSURE_` in filename  
**Output:** Centralized file only

#### **Current Output Headers (After Processing):**
- `LOCALITATE` - Locality (required, 2-100 chars)
- `ENCLOSURE_ID` - Enclosure ID (required, pattern: ^[A-Z0-9_-]+$)
- `OBSERVATII` - Observations (required, max 500 chars)

**Output Files:**
- Centralized file: `_output/enclosure_centralized.geojson`

### Fibra
**Processor:** `_fibra.py`  
**Source Files:** Files containing `FO_` in filename  
**Output:** Centralized file only

#### **Current Output Headers (After Processing):**
- `NR_FIRE` - Number of fibers (required, integer, min 1)
- `LUNGIME_HARTA` - Map length (required, number, min 0)
- `LUNGIME_TEREN` - Terrain length (required, number, min 0)
- `AMPLASARE` - Placement (required, max 100 chars)
- `LOCALITATE` - Locality (required, 2-100 chars)

**Output Files:**
- Centralized file: `_output/fibra_centralized.geojson`

### Hub
**Processor:** `_hub.py`  
**Source Files:** Files containing `HUB_` in filename  
**Output:** Centralized file only

#### **Current Output Headers (After Processing):**
- `NUME` - Name (required, 2-100 chars)
- `LOCALITATE` - Locality (required, 2-100 chars)
- `ADRESA` - Address (required, 2-200 chars)
- `COD_FTTB` - FTTB Code (required, pattern: ^[A-Z0-9_-]+$)
- `OLT` - OLT (required, max 50 chars)
- `COMBINER` - Combiner (required, max 50 chars)
- `SURSA_48V` - 48V Source (required, max 50 chars)
- `AC` - AC (required, max 50 chars)
- `MOTIVE_NEFUNCT_HUB` - Hub Malfunction Reasons (required, max 200 chars)
- `FIBRE` - Fibers (required, max 50 chars)

**Output Files:**
- Centralized file: `_output/hub_centralized.geojson`

### Localitati
**Processor:** `_localitati.py`  
**Source Files:** Files containing `LOCALITATI_` in filename  
**Output:** Centralized file only

#### **Current Output Headers (After Processing):**
- `NUME` - Name (required, 2-100 chars)
- `COMUNA` - Commune (required, 2-100 chars)
- `NR_CASE` - Number of houses (required, max 50 chars)
- `ID_CITY_VOICE` - City voice ID (required, max 50 chars)
- `MI_PRINX` - MapInfo index (required, max 50 chars)
- `SIRUTA` - SIRUTA code (required, max 100 chars)
- `OBS` - Observations (required, max 500 chars)
- `PROIECTANT` - Designer (required, max 100 chars)

**Output Files:**
- Centralized file: `_output/localitati_centralized.geojson`

### Scari
**Processor:** `_scari.py`  
**Source Files:** Files containing `SCARI_` in filename  
**Output:** Centralized file only

#### **Current Output Headers (After Processing):**
- `COD_FTTB` - FTTB Code (required, pattern: ^[A-Z0-9_-]+$)
- `TIP_ART` - Article Type (required, max 50 chars)
- `DENUMIRE_ART` - Article Name (required, 2-100 chars)
- `NR_ART` - Article Number (required, max 50 chars)
- `DENUMIRE_BLOC` - Block Name (required, max 100 chars)
- `NR_SCARA` - Stair Number (required, max 50 chars)
- `TIP_RETEA` - Network Type (optional, max 50 chars)
- `ZONA_RETEA` - Network Zone (optional, max 50 chars)
- `OBSERVATII` - Observations (optional, max 500 chars)
- `ZONA_RETEA_FTTH1000` - FTTH1000 Network Zone (optional, max 50 chars)
- `ZONA_RETEA_FTTH_V2` - FTTH V2 Network Zone (optional, max 50 chars)
- `LOCALITATE` - Locality (optional, 2-100 chars)

**Output Files:**
- Centralized file: `_output/scari_centralized.geojson`

### Spliter
**Processor:** `_spliter.py`  
**Source Files:** Files containing `SPLITER_` in filename  
**Output:** Centralized file only

#### **Current Output Headers (After Processing):**
- `TIP_SPLITER` - Splitter Type (required, max 50 chars)

**Output Files:**
- Centralized file: `_output/spliter_centralized.geojson`

### Stalpi
**Processor:** `_stalpi.py`  
**Source Files:** Files containing `STALPI_` in filename  
**Output:** Centralized file only

#### **Current Output Headers (After Processing):**
- `LOCALITATE` - Locality (required, 2-100 chars)
- `FOLOSIT_RDS` - RDS Usage (required, max 50 chars)
- `MATERIAL_CONSTRUCTIV` - Construction Material (required, max 50 chars)
- `TIP_STALP` - Pole Type (required, max 50 chars)

**Output Files:**
- Centralized file: `_output/stalpi_centralized.geojson`

### Zona Hub
**Processor:** `_zona_hub.py`  
**Source Files:** Files containing `ZONA_ACOPERIRE_HUB_` in filename  
**Output:** Centralized file only

#### **Current Output Headers (After Processing):**
- `NUME` - Name (required, 2-100 chars)
- `NR_CASE` - Number of houses (required, max 50 chars)
- `NR_CASE_ACOPERIRE` - Number of houses covered (required, max 50 chars)
- `NR_CASE_ACTIVE` - Number of active houses (required, max 50 chars)
- `NR_SCARI` - Number of stairs (required, max 50 chars)
- `NR_APT` - Number of apartments (required, max 50 chars)

**Output Files:**
- Centralized file: `_output/zona_hub_centralized.geojson`

### Zona Interventie
**Processor:** `_zone_interventie.py`  
**Source Files:** Files containing `ZONA_` or `ZONE_` in filename  
**Output:** Centralized file only

#### **Current Output Headers (After Processing):**
- `LOCALITATE` - Locality (required, 2-100 chars)
- `ZONA` - Zone (required, max 50 chars)
- `ECHIPA` - Team (required, max 50 chars)
- `TIP_ECHIPA` - Team type (required, max 50 chars)

**Output Files:**
- Centralized file: `_output/zone_interventie_centralized.geojson`

### Zona Pon
**Processor:** `_zona_pon.py`  
**Source Files:** Files containing `ZONA_PON_REALIZAT_` in filename  
**Output:** Centralized file only

#### **Current Output Headers (After Processing):**
- `PON` - PON identifier (required, pattern: ^PON-[A-Z0-9_-]+$)
- `OBSERVATII` - Observations (required, max 500 chars)

**Output Files:**
- Centralized file: `_output/zona_pon_centralized.geojson`

### Zona Pon RE FTTH1000
**Processor:** `_zona_pon_re_ftth1000.py`  
**Source Files:** Files containing `ZONA_PON_RE_FTTH1000_` in filename  
**Output:** Centralized file only

#### **Current Output Headers (After Processing):**
- `PON` - PON identifier (required, pattern: ^PON-[A-Z0-9_-]+$)
- `OLT` - OLT identifier (required, pattern: ^OLT-[A-Z0-9_-]+$)
- `HOTLINK` - HotLink (optional, max 50 chars)

**Output Files:**
- Centralized file: `_output/zona_pon_re_ftth1000_centralized.geojson`

### Zona Spliter
**Processor:** `_zona_spliter.py`  
**Source Files:** Files containing `ZONA_SPLITER_REALIZAT_` in filename  
**Output:** Centralized file only

#### **Current Output Headers (After Processing):**
- `ID_ZONA` - Zone ID (required, max 50 chars)

**Output Files:**
- Centralized file: `_output/zona_spliter_centralized.geojson`

---

## B) Search Layers

### FTTB Search
**Processor:** `_fttb_search.py`  
**Source Files:** Files processed by FTTB search processor  
**Output:** Centralized file only

#### **Current Output Headers (After Processing):**
- `COD_FTTB` - FTTB Code (required, pattern: ^[A-Z0-9_-]+$)
- `LOCALITATE` - Locality (required, 2-100 chars)

**Output Files:**
- Centralized file: `_output/fttb_search.geojson`

### Enclosure Search
**Processor:** `_enclosure_search.py`  
**Source Files:** Files processed by enclosure search processor  
**Output:** Centralized file only

#### **Current Output Headers (After Processing):**
- `ENCLOSURE_ID` - Enclosure ID (required, pattern: ^[A-Z0-9_-]+$)
- `LOCALITATE` - Locality (required, 2-100 chars)

**Output Files:**
- Centralized file: `_output/enclosure_search.geojson`

### Camereta Search
**Processor:** `_camereta_search.py`  
**Source Files:** Files processed by camereta search processor  
**Output:** Centralized file only

#### **Current Output Headers (After Processing):**
- `LOCALITATE` - Locality (required, 2-100 chars)
- `ID_TABELA` - Table ID (required, pattern: ^[A-Z0-9_-]+$)

**Output Files:**
- Centralized file: `_output/camereta_search.geojson`

### Scari Search
**Processor:** `_scari_search.py`  
**Source Files:** Files processed by scari search processor  
**Output:** Centralized file only

#### **Current Output Headers (After Processing):**
- `COD_FTTB` - FTTB Code (required, pattern: ^[A-Z0-9_-]+$)
- `TIP_ART` - Article Type (required, max 50 chars)
- `DENUMIRE_ART` - Article Name (required, 2-100 chars)
- `NR_ART` - Article Number (required, max 50 chars)
- `DENUMIRE_BLOC` - Block Name (required, max 100 chars)
- `NR_SCARA` - Stair Number (required, max 50 chars)
- `LOCALITATE` - Locality (required, 2-100 chars)

**Output Files:**
- Centralized file: `_output/scari_search.geojson`

---

## Current System Features

### Processing Features
- **Multi-encoding Detection**: UTF-8, ISO-8859-1, Windows-1252, CP1252
- **Uppercase Header Processing**: All field names converted to uppercase for consistency
- **Duplicate Detection**: Based on key fields and geometry
- **Compact Format**: Single-line JSON for efficient storage
- **Centralized Output**: Most processors create only centralized files
- **Individual Files**: Only Case processor creates individual files + manifest.json
- **Filename Filtering**: Processors only process files with specific name patterns
- **Empty Properties Filtering**: Features with empty required fields are skipped
- **Model-specific Required Fields**: Each model has its own set of required fields for filtering

### File Processing Patterns
- **Case**: `CASE_*` → Individual files + Centralized
- **Camereta**: `CAMERETA_*` → Centralized only
- **Enclosure**: `ENCLOSURE_*` → Centralized only
- **Fibra**: `FO_*` → Centralized only
- **Hub**: `HUB_*` → Centralized only
- **Localitati**: `LOCALITATI_*` → Centralized only
- **Scari**: `SCARI_*` → Centralized only
- **Spliter**: `SPLITER_*` → Centralized only
- **Stalpi**: `STALPI_*` → Centralized only
- **Zona Hub**: `ZONA_ACOPERIRE_HUB_*` → Centralized only
- **Zona Interventie**: `ZONA_*` or `ZONE_*` → Centralized only
- **Zona Pon**: `ZONA_PON_REALIZAT_*` → Centralized only
- **Zona Pon RE FTTH1000**: `ZONA_PON_RE_FTTH1000_*` → Centralized only
- **Zona Spliter**: `ZONA_SPLITER_REALIZAT_*` → Centralized only

### Field Count Summary
**Main Layers - Extracted Fields:**
- **Case**: 9 fields (1 required, 8 optional)
- **Camereta**: 5 fields (4 required, 1 optional)
- **Enclosure**: 3 fields (3 required)
- **Fibra**: 5 fields (5 required)
- **Hub**: 10 fields (10 required)
- **Localitati**: 8 fields (8 required)
- **Scari**: 12 fields (6 required, 6 optional)
- **Spliter**: 1 field (1 required)
- **Stalpi**: 4 fields (4 required)
- **Zona Hub**: 6 fields (6 required)
- **Zona Interventie**: 4 fields (4 required)
- **Zona Pon**: 2 fields (2 required)
- **Zona Pon RE FTTH1000**: 3 fields (2 required, 1 optional)
- **Zona Spliter**: 1 field (1 required)

**Search Layers - Extracted Fields:**
- **FTTB Search**: 2 fields (2 required)
- **Enclosure Search**: 2 fields (2 required)
- **Camereta Search**: 2 fields (2 required)
- **Scari Search**: 7 fields (7 required)

### Output File Structure
- **Individual Files**: Only Case processor creates individual files in `_output/case/` folder
- **Centralized Files**: All processors create centralized files in `_output/` folder
- **Manifest Files**: Only Case processor creates `manifest.json` with file listings
- **Compact Format**: All output files use compact JSON format for efficiency
- **Professional Headers**: All files include proper GeoJSON headers and metadata
