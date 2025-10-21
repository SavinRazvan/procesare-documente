Procesor GeoJSON V2 – Fiber Optic Networks Manager

> Sistem de procesare a fișierelor GeoJSON pentru infrastructura de rețele de fibră optică. Include validare a datelor, identificare de duplicate și generare de rezultate standardizate pentru gestionarea informațiilor geografice.



---

🗺️ Descriere generală

Proiectul Fiber Optic Networks Manager oferă un set de instrumente pentru procesarea datelor geografice asociate elementelor din rețelele de telecomunicații.
Acest modul gestionează fișierele GeoJSON care descriu infrastructura fizică (clădiri, stâlpi, fibre, zone de acoperire etc.), aplicând reguli de validare și filtrare automată.


---

⚙️ Componentele procesorului

Sistemul include 18 procesoare dedicate, fiecare destinat unui tip specific de obiect din rețea.
Fiecare procesor rulează independent sau coordonat printr-un procesor principal.

Tip element	Descriere generală

- 🏠 Case	Clădiri rezidențiale cu cod FTTB și echipamente asociate
- 📡 Camereta	Puncte tehnice de distribuție
- 📦 Enclosure	Închideri tehnice pentru echipamente
- 🌐 Hub	Hub-uri de rețea cu informații despre localitate
- 🏘️ Localitati	Localități, comune și coduri SIRUTA
- 📶 Stalpi	Stâlpi utilitari (tip, material)
- 🏢 Zona Hub	Zone de acoperire pentru fiecare hub
- 🔧 Zone Interventie	Zone de intervenție și acoperire
- 🔌 Spliter	Splittere optice (tip, porturi)
- 📡 Zona PON	Zone Passive Optical Network
- 📶 Zona Spliter	Zone de distribuție pentru splittere
- 🌐 Fibra	Tronsoane de fibră optică
- 🏢 Scari	Accese la clădiri (FTTB)
- 📡 Zona PON RE FTTH1000	Zone PON realizate FTTH1000
- 🔍 Search Layers	Layere pentru căutare (FTTB, scări, camerete, închideri)


Scop: automatizarea procesării și validării datelor geografice din infrastructura de telecomunicații, cu rezultate centralizate și coerente.


---

🚀 Pornire rapidă

# Creare și activare mediu virtual
conda create -n proc_doc python=3.11 -y
conda activate proc_doc

# Navigare în directorul proiectului
cd /home/razvansavin/Projects/procesare-documente

# Procesare completă
python3 _process_all.py _input _output


---

📋 Funcționalități principale

18 procesoare specializate pentru modele distincte

Procesor principal pentru execuție unificată

Configurare JSON pentru modele și setări

Sistem de logging pentru monitorizare și depanare

Fără dependențe externe, bazat pe biblioteca standard Python

Rezultate centralizate într-o structură uniformă



---

📁 Structura proiectului

procesare-documente/
├── _input/                    # Fișiere GeoJSON sursă
├── _output/                   # Rezultate procesate
├── config/                    # Configurații generale
│   ├── models.json
│   └── settings.json
├── src/                       # Cod sursă principal
│   ├── core/
│   └── utils/
├── logs/                      # Fișiere log
├── _process_all.py            # Procesor principal
├── _[model].py                # Procesoare dedicate (18 fișiere)
├── doc_input_headers.md       # Descriere câmpuri de intrare
├── requirements.txt           # Dependențe
├── TUTORIAL.md                # Ghid de utilizare
└── README.md                  # Acest fișier

> Pentru detalii suplimentare despre funcționare și configurare, vezi TUTORIAL.md




---

📚 Documentație

TUTORIAL.md – Ghid de utilizare și configurare

doc_input_headers.md – Descriere câmpuri de intrare

requirements.txt – Dependențe și versiuni Python



---

🔧 Cerințe de sistem

Python 3.11+

Conda pentru gestionarea mediului

Nu sunt necesare pachete externe — folosește doar biblioteca standard Python



---

🧩 Modele suportate

Layere principale (14)

camereta, enclosure, hub, localitati, stalpi,
zona_hub, zone_interventie, case, spliter,
zona_pon, zona_spliter, fibra, scari,
zona_pon_re_ftth1000

Layere de căutare (4)

fttb_search, scari_search, camereta_search, enclosure_search


---

💻 Exemple de utilizare

# Procesare modele specifice
python3 _process_all.py _input _output --models camereta case

# Procesare fără verificare duplicate
python3 _process_all.py _input _output --no-duplicates

# Rulare procesor individual
python3 _camereta.py _input _output


---

⚙️ Performanță

Fără dependențe externe

Optimizat pentru volume mari de date

Procesare în flux pentru eficiență de memorie

Scalabil pentru mii de entități



---

🧪 Dezvoltare și testare

# Testare procesor individual
python3 _camereta.py _input _output

# Testare orchestrare
python3 _process_all.py _input _output --models camereta

# Afișare opțiuni disponibile
python3 _process_all.py --help


---

📞 Suport

Pentru depanare sau întrebări:

1. Consultă TUTORIAL.md pentru ghid complet


2. Verifică doc_input_headers.md pentru câmpurile suportate


3. Analizează mesajele din consolă și fișierele log


4. Asigură-te că denumirile și formatele fișierelor sursă sunt corecte




---

Autor: Savin Ionuț Răzvan
Versiune: 2025.10.05

