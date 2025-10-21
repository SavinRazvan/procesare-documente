# Procesor GeoJSON V2 - Fiber Optic Networks Manager

> Sistem profesional de procesare documente pentru fișiere GeoJSON cu validare comprehensivă a datelor, detectare duplicat și generare rezultate centralizate pentru infrastructura de rețele de telecomunicații.

## 🎯 Proiectul Fiber Optic Networks Manager

Acest sistem face parte din proiectul **Fiber Optic Networks Manager** - o soluție completă pentru managementul infrastructurii de rețele de fibră optică. Sistemul procesează datele geografice ale elementelor de rețea pentru a oferi o vizibilitate completă asupra infrastructurii de telecomunicații.

## 🔧 Ce Sunt Aceste Procesoare?

Acest sistem conține **18 procesoare specializate** pentru procesarea automată a fișierelor GeoJSON din infrastructura de rețele de telecomunicații. Fiecare procesor gestionează un tip specific de elemente tehnice din rețelele de fibră optică:

- **🏠 Case**: Clădiri rezidențiale cu cod FTTB și echipamente de acces
- **📡 Camereta**: Cabine tehnice de distribuție cu observații și ID tabelă
- **📦 Enclosure**: Închideri tehnice pentru echipamente cu ID și observații
- **🌐 Hub**: Hub-uri de rețea cu nume și localitate pentru distribuție
- **🏘️ Localitati**: Localități cu nume, comună și cod SIRUTA
- **📶 Stalpi**: Stâlpi utilitari pentru suportul cablurilor cu material și tip
- **🏢 Zona Hub**: Zone de acoperire hub cu statistici case și apartamente
- **🔧 Zone Interventie**: Zone de intervenție cu localitate și zonă de acoperire
- **🔌 Spliter**: Divizoare de semnal (splitere) cu tip și număr de porturi
- **📡 Zona PON**: Zone Passive Optical Network cu identificatori
- **📶 Zona Spliter**: Zone de distribuție cu ID zonă pentru splitere
- **🌐 Fibra**: Fibre optice cu număr fire și localitate pentru conectivitate
- **🏢 Scari**: Scări cu cod FTTB și articole pentru acces la clădiri
- **📡 Zona PON RE FTTH1000**: Zone PON Realizate FTTH1000 pentru acces la 1Gbps
- **🔍 Search Layers**: Sisteme de căutare FTTB, scări, camerete, închideri pentru identificare

> **Scopul**: Automatizarea procesării datelor geografice pentru infrastructura de rețele de fibră optică, cu validare automată, detectare duplicat și generare rezultate standardizate pentru managementul rețelelor de telecomunicații.

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

- **18 Procesori Specializați**: Gestionează tipuri specifice de modele
- **Procesor Principal**: Orchestrează toți procesorii specializați  
- **Configurare prin JSON**: Definiții de modele bazate pe fișiere JSON
- **Logging Profesional**: Gestionare comprehensivă a erorilor și monitorizare
- **Fără Dependențe Externe**: Doar biblioteca standard Python
- **Rezultate Centralizate**: Date procesate unificate

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

> **Pentru o prezentare detaliată a arhitecturii, vezi [TUTORIAL.md](TUTORIAL.md)**

## 📚 Documentație

- **[TUTORIAL.md](TUTORIAL.md)** - Ghid complet utilizator cu instrucțiuni de configurare
- **[doc_input_headers.md](doc_input_headers.md)** - Specificații câmpuri și referință tehnică
- **[requirements.txt](requirements.txt)** - Informații despre dependențe

## 🔧 Cerințe

- **Python**: 3.11+
- **Conda**: Pentru gestionarea mediului
- **Fără Dependențe Externe**: Folosește doar biblioteca standard Python

## 📊 Modele Suportate

### Main Layers (14)
- `camereta`, `enclosure`, `hub`, `localitati`, `stalpi`
- `zona_hub`, `zone_interventie`, `case`, `spliter`  
- `zona_pon`, `zona_spliter`, `fibra`, `scari`
- `zona_pon_re_ftth1000`

### Search Layers (4)
- `fttb_search`, `scari_search`, `camereta_search`, `enclosure_search`

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
**Versiune**: 2025.10.05