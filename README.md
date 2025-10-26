# Procesor GeoJSON V2 - Fiber Optic Networks Manager

> Sistem profesional de procesare documente pentru fișiere GeoJSON cu validare comprehensivă a datelor, detectare duplicat și generare rezultate centralizate pentru infrastructura de rețele de telecomunicații.

## 🎯 Proiectul Fiber Optic Networks Manager

Acest sistem face parte din proiectul **Fiber Optic Networks Manager** - o soluție completă pentru managementul infrastructurii de rețele de fibră optică. Sistemul procesează datele geografice ale elementelor de rețea pentru a oferi o vizibilitate completă asupra infrastructurii de telecomunicații.

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

## 🔧 Ce Sunt Aceste Procesoare?

Acest sistem conține **18 procesoare specializate** pentru procesarea automată a fișierelor GeoJSON din infrastructura de rețele de telecomunicații. Fiecare procesor gestionează un tip specific de elemente tehnice din rețelele de fibră optică:

## Main Layers (14 procesoare)

**Case**: Procesează poligoane GeoJSON reprezentând clădiri rezidențiale cu infrastructură FTTB. Standardizează și curăță datele, elimină intrările neconforme (COD_FTTB invalid, câmpuri goale). Detectare duplicate bazată pe COD_FTTB + DENUMIRE_ART + NR_ART. Generează fișiere individuale procesate și fișier centralizat, plus manifest.json cu prioritizare fișiere (BARLAD, VASLUI). Extrage: COD_FTTB, LOCALITATE, TIP_ART, DENUMIRE_ART, NR_ART, STARE_RETEA, ZONA_RETEA, TIP_ECHIPAMENT, OBSERVATII.

**Camereta**: Procesează cabine tehnice de distribuție cu identificatori unici și observații. Standardizează și curăță datele, elimină intrările cu câmpuri obligatorii goale. Detectare duplicate bazată pe LOCALITATE + ID_TABELA + geometrie. Extrage: LOCALITATE, ID_TABELA, OBSERVATII_1, OBSERVATII_2, MI_PRINX.

**Enclosure**: Procesează închideri tehnice pentru echipamente cu identificatori și observații. Standardizează și curăță datele, elimină intrările cu ENCLOSURE_ID invalid sau câmpuri goale. Detectare duplicate bazată pe ENCLOSURE_ID + LOCALITATE + geometrie. Extrage: LOCALITATE, ENCLOSURE_ID, OBSERVATII.

**Hub**: Procesează hub-uri de rețea cu specificații tehnice complete. Standardizează și curăță datele, elimină intrările cu câmpuri obligatorii goale sau invalide. Detectare duplicate bazată pe NUME + LOCALITATE + geometrie. Extrage: NUME, LOCALITATE, ADRESA, COD_FTTB, OLT, COMBINER, SURSA_48V, AC, MOTIVE_NEFUNCT_HUB, FIBRE.

**Localitati**: Procesează localități cu statistici de acoperire și informații administrative. Standardizează și curăță datele, elimină intrările cu nume sau comună goale. Detectare duplicate bazată pe nume + comuna + geometrie. Extrage: nume, comuna, nr_case, id_city_voice, MI_PRINX, SIRUTA, obs, PROIECTANT.

**Stalpi**: Procesează stâlpi utilitari cu specificații tehnice și proprietate. Standardizează și curăță datele, elimină intrările cu câmpuri obligatorii goale. Detectare duplicate bazată pe COD_FTTB + LOCALITATE + geometrie. Extrage: LOCALITATE, FOLOSIT_RDS, MATERIAL_CONSTRUCTIV, TIP_STALP.

**Zona Hub**: Procesează zone de acoperire hub cu statistici detaliate. Standardizează și curăță datele, elimină intrările cu nume gol sau statistici invalide. Detectare duplicate bazată pe nume + geometrie. Extrage: nume, nr_case, nr_case_acoperire, nr_case_active, nr_scari, nr_apt.

**Zone Interventie**: Procesează zone de intervenție cu echipe și responsabilități. Standardizează și curăță datele, elimină intrările cu LOCALITATE sau ZONA goale. Detectare duplicate bazată pe LOCALITATE + ZONA + geometrie. Extrage: LOCALITATE, ZONA, ECHIPA, TIP_ECHIPA.

**Spliter**: Procesează puncte GeoJSON reprezentând splitere optice cu specificații tehnice. Standardizează și curăță datele, elimină intrările cu TIP_SPLITER invalid sau câmpuri goale. Detectare duplicate bazată pe TIP_SPLITER + geometrie. Extrage: TIP_SPLITER, NR_SPLITERE, NR_IESIRI, AMPLASARE, TIP_RETEA.

**Zona PON**: Procesează zone Passive Optical Network cu identificatori și observații. Standardizează și curăță datele, elimină intrările cu PON invalid sau câmpuri obligatorii goale. Detectare duplicate bazată pe PON + geometrie. Extrage: PON, OBSERVATII, MI_PRINX, NR_ABONATI.

**Zona Spliter**: Procesează zone de distribuție pentru splitere cu identificatori de zonă. Standardizează și curăță datele, elimină intrările cu ID_ZONA invalid sau gol. Detectare duplicate bazată pe ID_ZONA + geometrie. Extrage: ID_ZONA, PON.

**Fibra**: Procesează fibre optice cu specificații tehnice și măsurători. Standardizează și curăță datele, elimină intrările cu NR_FIRE invalid sau măsurători negative. Detectare duplicate bazată pe FIBRA_ID + LOCALITATE + geometrie. Extrage: NR_FIRE, LUNGIME_HARTA, LUNGIME_TEREN, AMPLASARE, LOCALITATE.

**Scari**: Procesează poligoane GeoJSON reprezentând scări de bloc cu infrastructură FTTB completă. Standardizează și curăță datele, elimină intrările neconforme (COD_FTTB invalid, câmpuri goale). Detectare duplicate bazată pe COD_FTTB + LOCALITATE. Extrage: COD_FTTB, TIP_ART, DENUMIRE_ART, NR_ART, DENUMIRE_BLOC, NR_SCARA, TIP_RETEA, ZONA_RETEA, OBSERVATII, ZONA_RETEA_FTTH1000, ZONA_RETEA_FTTH_V2, LOCALITATE.

**Zona PON RE FTTH1000**: Procesează zone PON Realizate cu tehnologia FTTH1000 și informații despre abonați. Standardizează și curăță datele, elimină intrările cu PON sau OLT invalid. Detectare duplicate bazată pe PON + geometrie. Extrage: PON, OLT, HOTLINK, NR_ABONATI, TIP_PROIECT.

## Search Layers (4 procesoare)

**FTTB Search**: Sistem de căutare pentru combinații COD_FTTB + LOCALITATE cu categorizare automată (Case, Scari, Other) pe baza TIP_ART și numele fișierului. Standardizează și curăță datele, elimină intrările cu COD_FTTB invalid sau LOCALITATE goală. Detectare duplicate bazată pe COD_FTTB + LOCALITATE. Extrage: COD_FTTB, LOCALITATE.

**Scari Search**: Sistem de căutare pentru date scări cu set complet de câmpuri și validare strictă. Standardizează și curăță datele, elimină intrările cu COD_FTTB invalid sau câmpuri obligatorii goale (TIP_ART, DENUMIRE_ART, NR_ART, DENUMIRE_BLOC, NR_SCARA, LOCALITATE). Detectare duplicate bazată pe COD_FTTB + LOCALITATE. Extrage: COD_FTTB, TIP_ART, DENUMIRE_ART, NR_ART, DENUMIRE_BLOC, NR_SCARA, LOCALITATE.

**Camereta Search**: Sistem de căutare pentru camerete cu LOCALITATE și ID_TABELA. Standardizează și curăță datele, elimină intrările cu LOCALITATE, ID_TABELA sau câmpuri obligatorii goale (TIP_CAMERETA, DIGI_ID). Detectare duplicate bazată pe LOCALITATE + ID_TABELA + geometrie. Extrage: LOCALITATE, ID_TABELA.

**Enclosure Search**: Sistem de căutare pentru închideri cu ENCLOSURE_ID și LOCALITATE. Standardizează și curăță datele, elimină intrările cu ENCLOSURE_ID sau LOCALITATE goale. Detectare duplicate bazată pe ENCLOSURE_ID + LOCALITATE + geometrie. Extrage: ENCLOSURE_ID, LOCALITATE.

> **Scopul**: Automatizarea procesării datelor geografice pentru infrastructura de rețele de fibră optică, cu standardizare și curățare automată a datelor, validare comprehensivă, detectare duplicat și generare rezultate standardizate pentru managementul rețelelor de telecomunicații.

## 🚀 Pornire Rapidă

```bash
# Configurare mediu
conda create -n .proc_doc python=3.11 -y
conda activate .proc_doc

# Navigare la proiect
cd /home/razvansavin/Projects/procesare-documente

# Procesare toate modelele
python3 _process_all.py _input _output
```

## 📋 Funcționalități

- **18 Procesori Specializați**: Gestionează tipuri specifice de modele cu validări și detectare duplicate personalizate
- **Standardizare și Curățare Date**: Elimină intrările neconforme, validează câmpuri obligatorii și standardizează formatul datelor
- **Procesor Principal**: Orchestrează toți procesorii specializați prin subprocess-uri, agregă statistici și raportează progres
- **Configurare prin JSON**: Definiții de modele bazate pe fișiere JSON cu validări și mapări de câmpuri
- **Logging Profesional**: Gestionare comprehensivă a erorilor și monitorizare cu performanță
- **Fără Dependențe Externe**: Doar biblioteca standard Python
- **Rezultate Centralizate**: Date procesate unificate cu manifest.json pentru fiecare tip de model

## 📁 Structura Proiectului

```
procesare-documente/
├── _input/                    # Fișiere GeoJSON sursă
├── _output/                   # Fișiere rezultat procesare
├── config/                    # Fișiere de configurare
│   ├── models.json           # Configurația modelelor (18 modele)
│   └── settings.json         # Setările de procesare
├── src/                       # Motor de procesare principal
│   ├── core/                  # Componente principale
│   └── utils/                 # Utilitare sistem
├── logs/                      # Fișiere log sistem
├── _process_all.py            # Procesor principal
├── _[model].py               # Procesori specializați (18 fișiere)
├── doc_input_headers.md      # Documentație câmpuri
├── requirements.txt           # Dependențe sistem
├── TUTORIAL.md               # Ghid complet utilizator
└── README.md                 # Acest fișier
```

Structura fișierelor rezultate:
> **Pentru o prezentare detaliată a arhitecturii, vezi [TUTORIAL.md](TUTORIAL.md)**

## 📚 Documentație

- **[TUTORIAL.md](TUTORIAL.md)** - Ghid complet utilizator cu instrucțiuni de configurare
- **[doc_input_headers.md](doc_input_headers.md)** - Specificații câmpuri și referință tehnică
- **[requirements.txt](requirements.txt)** - Informații despre dependențe

## 🔧 Cerințe

- **Python**: 3.11+
- **Conda**: Pentru gestionarea mediului
- **Fără Pachete Externe**: Folosește doar biblioteca standard Python

## 📊 Modele Suportate

### Main Layers (14 procesoare)
- `case` - Clădiri rezidențiale cu infrastructură FTTB (poligoane)
- `camereta` - Cabine tehnice de distribuție cu identificatori unici
- `enclosure` - Închideri tehnice pentru echipamente
- `hub` - Hub-uri de rețea cu specificații tehnice complete
- `localitati` - Localități cu statistici de acoperire și informații administrative
- `stalpi` - Stâlpi utilitari cu specificații tehnice și proprietate
- `zona_hub` - Zone de acoperire hub cu statistici detaliate
- `zone_interventie` - Zone de intervenție cu echipe și responsabilități
- `spliter` - Splitere optice cu specificații tehnice (puncte)
- `zona_pon` - Zone Passive Optical Network cu identificatori
- `zona_spliter` - Zone de distribuție pentru splitere
- `fibra` - Fibre optice cu specificații tehnice și măsurători
- `scari` - Scări de bloc cu infrastructură FTTB completă (poligoane)
- `zona_pon_re_ftth1000` - Zone PON Realizate cu tehnologia FTTH1000

### Search Layers (4 procesoare)
- `fttb_search` - Sistem de căutare pentru combinații COD_FTTB + LOCALITATE
- `scari_search` - Sistem de căutare pentru date scări cu set complet de câmpuri
- `camereta_search` - Sistem de căutare pentru camerete cu LOCALITATE și ID_TABELA
- `enclosure_search` - Sistem de căutare pentru închideri cu ENCLOSURE_ID și LOCALITATE

## 🎯 Exemple de Utilizare

```bash
# Procesare modele specifice
python3 _process_all.py _input _output --models camereta case

# Procesare fără detectare duplicat
python3 _process_all.py _input _output --no-duplicates

# Procesor specializat
python3 _camereta.py _input _output
```

## 📈 Performance

- **Lightweight**: Fără dependențe externe
- **Fast**: Optimizat pentru seturi mari de date  
- **Memory Efficient**: Procesare în flux
- **Scalable**: Gestionează mii de entități

## 🛠️ Dezvoltare

```bash
# Testare procesor specializat
python3 _camereta.py _input _output

# Testare procesor principal
python3 _process_all.py _input _output --models camereta

# Verificare ajutor
python3 _process_all.py --help
```

## 📞 Support

Pentru probleme sau întrebări:

1. Verifică [TUTORIAL.md](TUTORIAL.md) pentru instrucțiuni de utilizare și configurare
2. Revizuiește [doc_input_headers.md](doc_input_headers.md) pentru specificații câmpuri  
3. Verifică rezultatele consolei pentru mesaje de eroare
4. Verifică formatele fișierelor sursă și denumirile

---

**Autor**: Savin Ionut Razvan  
**Versiune**: 2.1  
**Data**: 26.10.2025