# Documentație Câmpuri Date Sursă

Acest document oferă o reprezentare precisă a configurațiilor curente de câmpuri și anteturi de ieșire pentru fiecare model de procesor, bazată pe configurația actuală `config/models.json` și comportamentul curent al sistemului.

**Ultima Actualizare:** 26.10.2025  
**Autor:** Savin Ionut Razvan  
**Versiune:** 2.1

## 📁 Structura de Input

Aplicația așteaptă următoarea structură de date pentru procesare:

```
📦_input
 ┣ 📂Case_map
 ┃ ┣ 📜CASE_1_DECEMBRIE.geojson
 ┃ ┣ 📜CASE_ALBESTI.geojson
 ┃ ┣ 📜CASE_BARLAD.geojson
 ┃ ┣ 📜CASE_VASLUI.geojson
 ┃ ┗ 📜... (fișiere CASE_*.geojson)
 ┣ 📂layere_map
 ┃ ┣ 📂Scari
 ┃ ┃ ┣ 📜SCARI_BARLAD.geojson
 ┃ ┃ ┣ 📜SCARI_HUSI.geojson
 ┃ ┃ ┗ 📜... (fișiere SCARI_*.geojson)
 ┃ ┣ 📂Spliter_Realizat
 ┃ ┃ ┣ 📜SPLITER_REALIZAT_BARLAD.geojson
 ┃ ┃ ┣ 📜SPLITER_REALIZAT_VASLUI.geojson
 ┃ ┃ ┗ 📜... (fișiere SPLITER_REALIZAT_*.geojson)
 ┃ ┣ 📂Unified_layer
 ┃ ┃ ┣ 📜CAMERETA_REALIZAT_VS.geojson
 ┃ ┃ ┣ 📜ENCLOSURE_REALIZAT_VS.geojson
 ┃ ┃ ┣ 📜HUB_VS.geojson
 ┃ ┃ ┣ 📜LOCALITATI_VS.geojson
 ┃ ┃ ┣ 📜STALPI_VS.geojson
 ┃ ┃ ┗ 📜... (fișiere unified)
 ┃ ┣ 📂Zona_Pon
 ┃ ┃ ┣ 📜ZONA_PON_REALIZAT_BARLAD.geojson
 ┃ ┃ ┣ 📜ZONA_PON_REALIZAT_VASLUI.geojson
 ┃ ┃ ┗ 📜... (fișiere ZONA_PON_REALIZAT_*.geojson)
 ┃ ┣ 📂Zona_Pon_FTTH
 ┃ ┃ ┣ 📜ZONA_PON_RE_FTTH1000_BARLAD.geojson
 ┃ ┃ ┣ 📜ZONA_PON_RE_FTTH1000_HUSI.geojson
 ┃ ┃ ┗ 📜... (fișiere ZONA_PON_RE_FTTH1000_*.geojson)
 ┃ ┗ 📂Zona_Spliter
 ┃ ┃ ┣ 📜ZONA_SPLITER_REALIZAT_BARLAD.geojson
 ┃ ┃ ┣ 📜ZONA_SPLITER_REALIZAT_VASLUI.geojson
 ┃ ┃ ┗ 📜... (fișiere ZONA_SPLITER_REALIZAT_*.geojson)
 ┗ 📜Log_*.txt (fișiere de log opționale)
```

## 📤 Structura de Output

Aplicația generează următoarea structură de date procesate:

```
📦data
 ┣ 📂case
 ┃ ┣ 📜CASE_1_DECEMBRIE.geojson
 ┃ ┣ 📜CASE_ALBESTI.geojson
 ┃ ┣ 📜CASE_BARLAD.geojson
 ┃ ┣ 📜CASE_VASLUI.geojson
 ┃ ┣ 📜... (fișiere procesate individual)
 ┃ ┣ 📜case_centralized.geojson
 ┃ ┗ 📜manifest.json
 ┣ 📜camereta_centralized.geojson
 ┣ 📜camereta_search.geojson
 ┣ 📜enclosure_centralized.geojson
 ┣ 📜enclosure_search.geojson
 ┣ 📜fibra_centralized.geojson
 ┣ 📜fttb_search.geojson
 ┣ 📜hub_centralized.geojson
 ┣ 📜localitati_centralized.geojson
 ┣ 📜scari_centralized.geojson
 ┣ 📜scari_search.geojson
 ┣ 📜spliter_centralized.geojson
 ┣ 📜stalpi_centralized.geojson
 ┣ 📜zona_hub_centralized.geojson
 ┣ 📜zona_pon_centralized.geojson
 ┣ 📜zona_pon_re_ftth1000_centralized.geojson
 ┣ 📜zona_spliter_centralized.geojson
 ┗ 📜zone_interventie_centralized.geojson
```

## Cuprins

### A) Straturi Principale (14 Procesoare Specializați)
1. [Case](#case) - Clădiri rezidențiale cu infrastructură FTTB
2. [Camereta](#camereta) - Cabine tehnice de distribuție cu identificatori unici
3. [Enclosure](#enclosure) - Închideri tehnice pentru echipamente
4. [Fibra](#fibra) - Fibre optice cu specificații tehnice și măsurători
5. [Hub](#hub) - Hub-uri de rețea cu specificații tehnice complete
6. [Localitati](#localitati) - Localități cu statistici de acoperire și informații administrative
7. [Scari](#scari) - Scări de bloc cu infrastructură FTTB completă
8. [Spliter](#spliter) - Splitere optice cu specificații tehnice
9. [Stalpi](#stalpi) - Stâlpi utilitari cu specificații tehnice și proprietate
10. [Zona Hub](#zona-hub) - Zone de acoperire hub cu statistici detaliate
11. [Zona Interventie](#zona-interventie) - Zone de intervenție cu echipe și responsabilități
12. [Zona Pon](#zona-pon) - Zone Passive Optical Network cu identificatori
13. [Zona Pon RE FTTH1000](#zona-pon-re-ftth1000) - Zone PON Realizate cu tehnologia FTTH1000
14. [Zona Spliter](#zona-spliter) - Zone de distribuție pentru splitere

### B) Straturi de Căutare (4 Procesoare de Căutare)
1. [FTTB Search](#fttb-search) - Sistem de căutare pentru combinații COD_FTTB + LOCALITATE cu categorizare automată
2. [Enclosure Search](#enclosure-search) - Sistem de căutare pentru închideri cu ENCLOSURE_ID și LOCALITATE
3. [Camereta Search](#camereta-search) - Sistem de căutare pentru camerete cu LOCALITATE și ID_TABELA
4. [Scari Search](#scari-search) - Sistem de căutare pentru date scări cu set complet de câmpuri și validare strictă

---

## A) Straturi Principale

### Case
**Procesor:** `_case.py`  
**Fișiere Sursă:** Fișiere care conțin `CASE_` în nume  
**Rezultat:** Fișiere individuale + Fișier centralizat + Manifest

**Descriere:** Procesează poligoane GeoJSON reprezentând clădiri rezidențiale cu infrastructură FTTB. Standardizează și curăță datele, elimină intrările neconforme (COD_FTTB invalid, câmpuri goale). Detectare duplicate bazată pe COD_FTTB + DENUMIRE_ART + NR_ART. Generează fișiere individuale procesate și fișier centralizat, plus manifest.json cu prioritizare fișiere (BARLAD, VASLUI).

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
- Manifest: `_output/case/manifest.json` (cu prioritizare BARLAD, VASLUI)

### Camereta
**Procesor:** `_camereta.py`  
**Fișiere Sursă:** Fișiere care conțin `CAMERETA_` în nume  
**Rezultat:** Doar fișier centralizat

**Descriere:** Procesează cabine tehnice de distribuție cu identificatori unici și observații. Standardizează și curăță datele, elimină intrările cu câmpuri obligatorii goale (ID_TABELA, LOCALITATE, OBSERVATII_1, OBSERVATII_2). Detectare duplicate bazată pe LOCALITATE + ID_TABELA + geometrie.

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

**Descriere:** Procesează închideri tehnice pentru echipamente cu identificatori unici și observații. Standardizează și curăță datele, elimină intrările cu câmpuri obligatorii goale (ENCLOSURE_ID, LOCALITATE, OBSERVATII). Detectare duplicate bazată pe ENCLOSURE_ID + LOCALITATE + geometrie.

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

**Descriere:** Procesează fibre optice cu specificații tehnice și măsurători complete. Standardizează și curăță datele, elimină intrările cu câmpuri obligatorii goale (NR_FIRE, LUNGIME_HARTA, LUNGIME_ESTIMATA, TIP_CABLU, LUNGIME_TEREN, LUNGIME_OPTICA, AMPLASARE, LOCALITATE). Detectare duplicate bazată pe LOCALITATE + AMPLASARE + geometrie.

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

**Descriere:** Procesează hub-uri de rețea cu specificații tehnice complete și informații de infrastructură. Standardizează și curăță datele, elimină intrările cu câmpuri obligatorii goale (NUME, LOCALITATE, ADRESA, COD_FTTB, OLT, COMBINER, SURSA_48V, AC, MOTIVE_NEFUNCT_HUB, FIBRE). Detectare duplicate bazată pe COD_FTTB + LOCALITATE + geometrie.

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

**Descriere:** Procesează localități cu statistici de acoperire și informații administrative complete. Standardizează și curăță datele, elimină intrările cu câmpuri obligatorii goale (NUME, COMUNA, NR_CASE, TIP_RETEA_CASE, HUB, NR_PONI, TIP_PONI, IMPLEMENTARE_RETEA, STATIE_CATV, HP_TOTAL, SIRUTA, OBS, PROIECTANT). Detectare duplicate bazată pe NUME + COMUNA + geometrie.

#### **Anteturi Rezultat Curent (După Procesare):**
- `nume` - Nume (obligatoriu, 2-100 caractere)
- `comuna` - Comună (obligatoriu, 2-100 caractere)
- `nr_case` - Număr Case (obligatoriu, max 50 caractere)
- `id_city_voice` - ID City Voice (obligatoriu, max 50 caractere)
- `MI_PRINX` - Index MapInfo (obligatoriu, max 50 caractere)
- `SIRUTA` - Cod SIRUTA (obligatoriu, max 100 caractere)
- `obs` - Observații (obligatoriu, max 500 caractere)
- `PROIECTANT` - Proiectant (obligatoriu, max 100 caractere)

**Fișiere Rezultat:**
- Fișier centralizat: `_output/localitati_centralized.geojson`

### Scari
**Procesor:** `_scari.py`  
**Fișiere Sursă:** Fișiere care conțin `SCARI_` în nume  
**Rezultat:** Doar fișier centralizat

**Descriere:** Procesează scări de bloc cu infrastructură FTTB completă și informații detaliate. Standardizează și curăță datele, elimină intrările cu câmpuri obligatorii goale (COD_FTTB, TIP_ART, DENUMIRE_ART, NR_ART, DENUMIRE_BLOC, NR_SCARA). Detectare duplicate bazată pe COD_FTTB + DENUMIRE_ART + NR_ART + geometrie.

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

**Descriere:** Procesează splitere optice cu specificații tehnice și numărul de splitere. Standardizează și curăță datele, elimină intrările cu câmpuri obligatorii goale (TIP_SPLITER). Detectare duplicate bazată pe TIP_SPLITER + geometrie.

#### **Anteturi Rezultat Curent (După Procesare):**
- `TIP_SPLITER` - Tip Splitter (obligatoriu, max 50 caractere)
- `NR_SPLITERE` - Număr Splitere (opțional, max 50 caractere)

**Fișiere Rezultat:**
- Fișier centralizat: `_output/spliter_centralized.geojson`

### Stalpi
**Procesor:** `_stalpi.py`  
**Fișiere Sursă:** Fișiere care conțin `STALPI_` în nume  
**Rezultat:** Doar fișier centralizat

**Descriere:** Procesează stâlpi utilitari cu specificații tehnice și proprietate. Standardizează și curăță datele, elimină intrările cu câmpuri obligatorii goale (LOCALITATE, COD_FTTB, DENUMIRE_ART, NR_ART, FOLOSIT_RDS, MATERIAL_CONSTRUCTIV, TIP_STALP, PROPRIETAR, TABELA). Detectare duplicate bazată pe COD_FTTB + LOCALITATE + geometrie.

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

**Descriere:** Procesează zone de acoperire hub cu statistici detaliate și informații de acoperire. Standardizează și curăță datele, elimină intrările cu câmpuri obligatorii goale (NUME, NR_CASE, NR_CASE_ACOPERIRE, NR_CASE_ACTIVE, NR_SCARI, NR_APT). Detectare duplicate bazată pe NUME + geometrie.

#### **Anteturi Rezultat Curent (După Procesare):**
- `nume` - Nume (obligatoriu, 2-100 caractere)
- `nr_case` - Număr Case (obligatoriu, max 50 caractere)
- `nr_case_acoperire` - Număr Case Acoperire (obligatoriu, max 50 caractere)
- `nr_case_active` - Număr Case Active (obligatoriu, max 50 caractere)
- `nr_scari` - Număr Scări (obligatoriu, max 50 caractere)
- `nr_apt` - Număr Apartamente (obligatoriu, max 50 caractere)

**Fișiere Rezultat:**
- Fișier centralizat: `_output/zona_hub_centralized.geojson`

### Zona Interventie
**Procesor:** `_zone_interventie.py`  
**Fișiere Sursă:** Fișiere care conțin `ZONA_` sau `ZONE_` în nume  
**Rezultat:** Doar fișier centralizat

**Descriere:** Procesează zone de intervenție cu echipe și responsabilități. Standardizează și curăță datele, elimină intrările cu câmpuri obligatorii goale (JUDET, LOCALITATE, ZONA, ECHIPA, TIP_ECHIPA, MI_PRINX, DIGI_ID). Detectare duplicate bazată pe LOCALITATE + ZONA + geometrie.

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

**Descriere:** Procesează zone Passive Optical Network cu identificatori și observații. Standardizează și curăță datele, elimină intrările cu câmpuri obligatorii goale (MI_PRINX, NR_ABONATI, OBSERVATII, PON). Detectare duplicate bazată pe PON + geometrie.

#### **Anteturi Rezultat Curent (După Procesare):**
- `PON` - Identificator PON (obligatoriu, pattern: ^PON-[A-Z0-9_-]+$)
- `OBSERVATII` - Observații (obligatoriu, max 500 caractere)

**Fișiere Rezultat:**
- Fișier centralizat: `_output/zona_pon_centralized.geojson`

### Zona Pon RE FTTH1000
**Procesor:** `_zona_pon_re_ftth1000.py`  
**Fișiere Sursă:** Fișiere care conțin `ZONA_PON_RE_FTTH1000_` în nume  
**Rezultat:** Doar fișier centralizat

**Descriere:** Procesează zone PON Realizate cu tehnologia FTTH1000 și informații despre abonați. Standardizează și curăță datele, elimină intrările cu câmpuri obligatorii goale (PON, NR_ABONATI, OLT, TIP_PROIECT). Detectare duplicate bazată pe PON + OLT + geometrie.

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

**Descriere:** Procesează zone de distribuție pentru splitere cu identificatori unici. Standardizează și curăță datele, elimină intrările cu câmpuri obligatorii goale (ID_ZONA, PON). Detectare duplicate bazată pe ID_ZONA + geometrie.

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

**Descriere:** Sistem de căutare pentru combinații COD_FTTB + LOCALITATE cu categorizare automată (Case, Scari, Other) pe baza TIP_ART și numele fișierului. Standardizează și curăță datele, elimină intrările cu COD_FTTB invalid sau LOCALITATE goală. Detectare duplicate bazată pe COD_FTTB + LOCALITATE.

#### **Anteturi Rezultat Curent (După Procesare):**
- `COD_FTTB` - Cod FTTB (obligatoriu, pattern: ^[A-Z0-9_-]+$)
- `LOCALITATE` - Localitate (obligatoriu, 2-100 caractere)

**Fișiere Rezultat:**
- Fișier centralizat: `_output/fttb_search.geojson`

### Enclosure Search
**Procesor:** `_enclosure_search.py`  
**Fișiere Sursă:** Fișiere procesate de procesorul de căutare enclosure  
**Rezultat:** Doar fișier centralizat

**Descriere:** Sistem de căutare pentru închideri cu ENCLOSURE_ID și LOCALITATE. Standardizează și curăță datele, elimină intrările cu ENCLOSURE_ID sau LOCALITATE goale. Detectare duplicate bazată pe ENCLOSURE_ID + LOCALITATE + geometrie.

#### **Anteturi Rezultat Curent (După Procesare):**
- `ENCLOSURE_ID` - ID Enclosure (obligatoriu, pattern: ^[A-Z0-9_-]+$)
- `LOCALITATE` - Localitate (obligatoriu, 2-100 caractere)

**Fișiere Rezultat:**
- Fișier centralizat: `_output/enclosure_search.geojson`

### Camereta Search
**Procesor:** `_camereta_search.py`  
**Fișiere Sursă:** Fișiere procesate de procesorul de căutare camereta  
**Rezultat:** Doar fișier centralizat

**Descriere:** Sistem de căutare pentru camerete cu LOCALITATE și ID_TABELA. Standardizează și curăță datele, elimină intrările cu LOCALITATE, ID_TABELA sau câmpuri obligatorii goale (TIP_CAMERETA, DIGI_ID). Detectare duplicate bazată pe LOCALITATE + ID_TABELA + geometrie.

#### **Anteturi Rezultat Curent (După Procesare):**
- `LOCALITATE` - Localitate (obligatoriu, 2-100 caractere)
- `ID_TABELA` - ID Tabelă (obligatoriu, pattern: ^[A-Z0-9_-]+$)

**Fișiere Rezultat:**
- Fișier centralizat: `_output/camereta_search.geojson`

### Scari Search
**Procesor:** `_scari_search.py`  
**Fișiere Sursă:** Fișiere procesate de procesorul de căutare scari  
**Rezultat:** Doar fișier centralizat

**Descriere:** Sistem de căutare pentru date scări cu set complet de câmpuri și validare strictă. Standardizează și curăță datele, elimină intrările cu COD_FTTB invalid sau câmpuri obligatorii goale (TIP_ART, DENUMIRE_ART, NR_ART, DENUMIRE_BLOC, NR_SCARA, LOCALITATE). Detectare duplicate bazată pe COD_FTTB + LOCALITATE.

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
- **Standardizare și Curățare Date**: Elimină intrările neconforme, validează câmpuri obligatorii și standardizează formatul datelor
- **Detectare Multi-encoding**: UTF-8, ISO-8859-1, Windows-1252, CP1252
- **Procesare Anteturi Majuscule**: Toate numele de câmpuri convertite la majuscule pentru consistență
- **Detectare Duplicate**: Bazată pe câmpuri cheie și geometrie (configurabilă prin settings.json)
- **Format Compact**: JSON pe o singură linie pentru stocare eficientă
- **Rezultat Centralizat**: Majoritatea procesorilor creează doar fișiere centralizate
- **Fișiere Individuale**: Doar procesorul Case creează fișiere individuale + manifest.json cu prioritizare
- **Filtrare Nume Fișiere**: Procesorii procesează doar fișiere cu modele specifice de nume
- **Filtrare Proprietăți Goale**: Entitățile cu câmpuri obligatorii goale sunt omise
- **Câmpuri Obligatorii Specifice Modelului**: Fiecare model are propriul set de câmpuri obligatorii pentru filtrare
- **Validare Configurabilă**: Validări bazate pe patterns și reguli din models.json
- **Categorizare Automată**: FTTB Search categorizează automat în Case, Scari, Other
- **Logging Configurabil**: Nivel INFO, format personalizat, backup automat
- **Procesare în Batch**: Configurabilă prin batch_size și max_workers

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
- **Case**: 9 câmpuri (6 obligatorii, 3 opționale)
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
