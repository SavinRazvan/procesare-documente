# Procesor GeoJSON V2

> Sistem profesional de procesare documente pentru fișiere GeoJSON cu validare comprehensivă a datelor, detectare duplicat și generare rezultate centralizate.

## 🎯 Ce Sunt Aceste Procesoare?

Acest sistem conține **18 procesoare specializate** pentru procesarea automată a fișierelor GeoJSON din telecom infrastructure. Fiecare procesor gestionează un tip specific de elemente tehnice:

- **🏠 Case & Housing**: Procesare date despre case, apartamente și locuințe
- **📡 Technical Infrastructure**: Cabine tehnice, camerete, enclosures și hub-uri
- **🔌 Communication Networks**: Fibre optice, splitere, stalpi și zone de acoperire
- **📍 Location Services**: Localități, zone de intervenție și zone PON
- **🔍 Advanced Search**: Sisteme de căutare pentru toate tipurile de elemente

**Scopul**: Automatizarea procesării datelor geografice pentru telecom infrastructure, cu validare automată, detectare duplicat și generare rezultate standardizate.

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