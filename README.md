# Procesor GeoJSON V2

> Sistem profesional de procesare documente pentru fișiere GeoJSON cu validare comprehensivă a datelor, detectare duplicat și generare rezultate centralizate.

## 🎯 Ce Sunt Aceste Procesoare?

Acest sistem conține **18 procesoare specializați** pentru procesarea automată a fișierelor GeoJSON din infrastructura de telecomunicații. Fiecare procesor gestionează un tip specific de elemente tehnice:

- **🏠 Case & Locuințe**: Procesare date despre case, apartamente și locuințe
- **📡 Infrastructură Tehnică**: Cabine tehnice, camerete, enclosures și hub-uri
- **🔌 Rețele de Comunicare**: Fibre optice, splitere, stalpi și zone de acoperire
- **📍 Localizare**: Localități, zone de intervenție și zone PON
- **🔍 Căutare Avansată**: Sisteme de căutare pentru toate tipurile de elemente

**Scopul**: Automatizarea procesării datelor geografice pentru infrastructura de telecomunicații, cu validare automată, detectare duplicat și generare rezultate standardizate.

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
├── src/                       # Motor de procesare principal
├── _process_all.py            # Procesor principal
├── _[model].py               # Procesori specializați (23 fișiere)
└── README.md                  # Acest fișier
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

### Straturi Principale (14)
- `camereta`, `enclosure`, `hub`, `localitati`, `stalpi`
- `zona_hub`, `zone_interventie`, `case`, `spliter`
- `zona_pon`, `zona_spliter`, `fibra`, `scari`
- `zona_pon_re_ftth1000`

### Straturi de Căutare (4)
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

## 📈 Performanță

- **Ușor**: Fără dependențe externe
- **Rapid**: Optimizat pentru seturi mari de date
- **Eficient la Memorie**: Procesare în flux
- **Scalabil**: Gestionează mii de entități

## 🛠️ Dezvoltare

```bash
# Testare procesor specializat
python3 _camereta.py _input _output

# Testare procesor principal
python3 _process_all.py _input _output --models camereta

# Verificare ajutor
python3 _process_all.py --help
```

## 📞 Suport

Pentru probleme sau întrebări:
1. Verifică [TUTORIAL.md](TUTORIAL.md) pentru instrucțiuni de utilizare și configurare
2. Revizuiește [doc_input_headers.md](doc_input_headers.md) pentru specificații câmpuri
3. Verifică rezultatele consolei pentru mesaje de eroare
4. Verifică formatele fișierelor sursă și denumirile

---

**Autor**: Savin Ionut Razvan  
**Versiune**: 2025.10.05  