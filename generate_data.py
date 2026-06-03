import urllib.request
import urllib.parse
import json
import time

locations_raw = [
    # SEZIONE I
    {"name": "Alba Fucens", "region": "Abruzzo", "sezione": "I"},
    {"name": "Parco Nazionale del Gran Sasso e Monti della Laga", "region": "Abruzzo", "sezione": "I", "fallback_lat": 42.4278, "fallback_lon": 13.5539},
    {"name": "Costa dei Trabocchi", "region": "Abruzzo", "sezione": "I", "search": "Costa dei Trabocchi", "fallback_lat": 42.3025, "fallback_lon": 14.4447},
    {"name": "Dolomiti lucane", "region": "Basilicata", "sezione": "I", "fallback_lat": 40.5167, "fallback_lon": 16.0667},
    {"name": "Metaponto (sito archeologico)", "region": "Basilicata", "sezione": "I"},
    {"name": "Parco nazionale del Pollino", "region": "Basilicata", "sezione": "I"},
    {"name": "Sassi di Matera", "region": "Basilicata", "sezione": "I"},
    {"name": "Gerace", "region": "Calabria", "sezione": "I"},
    {"name": "Locri Epizefiri", "region": "Calabria", "sezione": "I"},
    {"name": "Cattolica di Stilo", "region": "Calabria", "sezione": "I"},
    {"name": "Sibari", "region": "Calabria", "sezione": "I"},
    {"name": "Capo Colonna", "region": "Calabria", "sezione": "I"},
    {"name": "Le Castella", "region": "Calabria", "sezione": "I", "fallback_lat": 38.9082, "fallback_lon": 17.0229},
    {"name": "Parco nazionale della Sila", "region": "Calabria", "sezione": "I"},
    
    # ID 15 Split
    {"name": "Certosa di San Giacomo", "region": "Campania", "sezione": "I"},
    {"name": "Grotta Azzurra", "region": "Campania", "sezione": "I"},
    
    # ID 16 Split
    {"name": "Amalfi", "region": "Campania", "sezione": "I"},
    {"name": "Positano", "region": "Campania", "sezione": "I"},
    {"name": "Ravello", "region": "Campania", "sezione": "I"},
    
    {"name": "Cuma", "region": "Campania", "sezione": "I"},
    {"name": "Grotte di Pertosa", "region": "Campania", "sezione": "I"},
    {"name": "Reggia di Caserta", "region": "Campania", "sezione": "I"},
    {"name": "Scavi archeologici di Ercolano", "region": "Campania", "sezione": "I"},
    {"name": "Paestum", "region": "Campania", "sezione": "I"},
    {"name": "Scavi archeologici di Pompei", "region": "Campania", "sezione": "I"},
    {"name": "Parco nazionale del Vesuvio", "region": "Campania", "sezione": "I"},
    
    # ID 24 Cluster
    {"name": "Centro storico monumentale di Napoli", "region": "Campania", "sezione": "I", "fallback_lat": 40.8518, "fallback_lon": 14.2681, "subsections": ["Duomo di Napoli", "Cappella Sansevero", "Quartieri Spagnoli", "Napoli sotterranea", "Palazzo Reale (Napoli)"]},
    
    # ID 25 Split
    {"name": "Monumenti paleocristiani di Ravenna", "region": "Emilia-Romagna", "sezione": "I", "fallback_lat": 44.4178, "fallback_lon": 12.1993},
    {"name": "Domus dei tappeti di pietra", "region": "Emilia-Romagna", "sezione": "I"},
    
    # ID 26 Split
    {"name": "Duomo di Parma", "region": "Emilia-Romagna", "sezione": "I", "fallback_lat": 44.8033, "fallback_lon": 10.3314},
    {"name": "Battistero di Parma", "region": "Emilia-Romagna", "sezione": "I"},
    
    {"name": "Palazzo della Pilotta", "region": "Emilia-Romagna", "sezione": "I"},
    
    # ID 28 Split
    {"name": "Ferrara", "region": "Emilia-Romagna", "sezione": "I"},
    {"name": "Castello Estense", "region": "Emilia-Romagna", "sezione": "I"},
    {"name": "Parco regionale del Delta del Po dell'Emilia-Romagna", "region": "Emilia-Romagna", "sezione": "I"},
    
    # ID 29 Split
    {"name": "Duomo di Modena", "region": "Emilia-Romagna", "sezione": "I"},
    {"name": "Palazzo Ducale (Modena)", "region": "Emilia-Romagna", "sezione": "I"},
    
    # ID 30 Cluster
    {"name": "Torri di Bologna", "region": "Emilia-Romagna", "sezione": "I", "subsections": ["Torre degli Asinelli", "Torre della Garisenda"]},
    
    # ID 31 Split
    {"name": "Ponte del Diavolo (Cividale)", "region": "Friuli-Venezia Giulia", "sezione": "I", "search": "Ponte del Diavolo (Cividale del Friuli)"},
    {"name": "Tempietto longobardo", "region": "Friuli-Venezia Giulia", "sezione": "I"},
    {"name": "Complesso episcopale del patriarca Callisto", "region": "Friuli-Venezia Giulia", "sezione": "I"},
    
    # ID 32 Split
    {"name": "Aquileia", "region": "Friuli-Venezia Giulia", "sezione": "I"},
    {"name": "Museo archeologico nazionale di Aquileia", "region": "Friuli-Venezia Giulia", "sezione": "I"},
    
    {"name": "Sacrario militare di Redipuglia", "region": "Friuli-Venezia Giulia", "sezione": "I"},
    {"name": "Castello di Miramare", "region": "Friuli-Venezia Giulia", "sezione": "I"},
    {"name": "Basilica di San Giovanni in Laterano", "region": "Lazio", "sezione": "I"},
    {"name": "Cattedrale di Anagni", "region": "Lazio", "sezione": "I", "fallback_lat": 41.7431, "fallback_lon": 13.1611},
    
    # ID 37 Split
    {"name": "Circo Massimo", "region": "Lazio", "sezione": "I"},
    {"name": "Terme di Caracalla", "region": "Lazio", "sezione": "I"},
    
    {"name": "Civita di Bagnoregio", "region": "Lazio", "sezione": "I", "fallback_lat": 42.6277, "fallback_lon": 12.1136},
    {"name": "Colosseo", "region": "Lazio", "sezione": "I"},
    {"name": "Necropoli dei Monterozzi", "region": "Lazio", "sezione": "I"},
    {"name": "Necropoli della Banditaccia", "region": "Lazio", "sezione": "I"},
    {"name": "Ostia Antica", "region": "Lazio", "sezione": "I"},
    {"name": "Pantheon (Roma)", "region": "Lazio", "sezione": "I"},
    {"name": "Fori Imperiali", "region": "Lazio", "sezione": "I"},
    {"name": "Basilica di San Pietro in Vaticano", "region": "Lazio", "sezione": "I", "fallback_lat": 41.9022, "fallback_lon": 12.4539},
    
    # Empty Description Fix
    {"name": "Via Appia Antica", "region": "Lazio", "sezione": "I", "search": "Parco regionale dell'Appia antica", "fallback_lat": 41.8396, "fallback_lon": 12.5218},
    
    # ID 47 Cluster
    {"name": "Roma Barocca Monumentale", "region": "Lazio", "sezione": "I", "fallback_lat": 41.8986, "fallback_lon": 12.4769, "subsections": ["Fontana di Trevi", "Piazza Navona", "Vittoriano", "Piazza Venezia"]},
    
    {"name": "Cattedrale di San Lorenzo (Genova)", "region": "Liguria", "sezione": "I"},
    
    # ID 49 Split
    {"name": "Riomaggiore", "region": "Liguria", "sezione": "I"},
    {"name": "Manarola", "region": "Liguria", "sezione": "I"},
    {"name": "Corniglia", "region": "Liguria", "sezione": "I"},
    {"name": "Vernazza", "region": "Liguria", "sezione": "I"},
    {"name": "Monterosso al Mare", "region": "Liguria", "sezione": "I"},
    
    # ID 50 Split
    {"name": "Centro storico di Genova", "region": "Liguria", "sezione": "I"},
    {"name": "Strade Nuove e Sistema dei Palazzi dei Rolli di Genova", "region": "Liguria", "sezione": "I", "search": "Palazzi dei Rolli", "fallback_lat": 44.4116, "fallback_lon": 8.9325},
    
    # ID 51 Split
    {"name": "Piazza Vecchia (Bergamo)", "region": "Lombardia", "sezione": "I", "fallback_lat": 45.7039, "fallback_lon": 9.6625},
    {"name": "Basilica di Santa Maria Maggiore (Bergamo)", "region": "Lombardia", "sezione": "I"},
    
    {"name": "Duomo di Milano", "region": "Lombardia", "sezione": "I"},
    
    # ID 53 Split
    {"name": "Certosa di Pavia", "region": "Lombardia", "sezione": "I"},
    {"name": "Castello Visconteo (Pavia)", "region": "Lombardia", "sezione": "I"},
    
    {"name": "Castello Scaligero (Sirmione)", "region": "Lombardia", "sezione": "I"},
    
    # ID 55 Split
    {"name": "Palazzo Ducale (Mantova)", "region": "Lombardia", "sezione": "I"},
    {"name": "Sabbioneta", "region": "Lombardia", "sezione": "I"},
    
    {"name": "Teatro alla Scala", "region": "Lombardia", "sezione": "I"},
    
    # ID 57 Split
    {"name": "Museo di Santa Giulia", "region": "Lombardia", "sezione": "I", "fallback_lat": 45.5401, "fallback_lon": 10.2285},
    {"name": "Brixia", "region": "Lombardia", "sezione": "I"},
    
    # ID 58 Split
    {"name": "Lago di Como", "region": "Lombardia", "sezione": "I", "fallback_lat": 46.0000, "fallback_lon": 9.2667},
    {"name": "Lago d'Iseo", "region": "Lombardia", "sezione": "I"},
    {"name": "Franciacorta", "region": "Lombardia", "sezione": "I"},
    
    {"name": "Grotte di Frasassi", "region": "Marche", "sezione": "I"},
    {"name": "Palazzo Ducale (Urbino)", "region": "Marche", "sezione": "I"},
    {"name": "Parco nazionale dei Monti Sibillini", "region": "Marche", "sezione": "I"},
    {"name": "Piazza del Popolo (Ascoli Piceno)", "region": "Marche", "sezione": "I"},
    {"name": "Rocca di Gradara", "region": "Marche", "sezione": "I", "fallback_lat": 43.9419, "fallback_lon": 12.7719},
    {"name": "Santuario della Santa Casa", "region": "Marche", "sezione": "I", "search": "Santuario della Santa Casa di Loreto", "fallback_lat": 43.4411, "fallback_lon": 13.6094},
    {"name": "Saepinum", "region": "Molise", "sezione": "I", "sezione_both": True},
    {"name": "Mole Antonelliana", "region": "Piemonte", "sezione": "I"},
    {"name": "Parco naturale delle Alpi Marittime", "region": "Piemonte", "sezione": "I"},
    
    # ID 68 Split
    {"name": "Val di Susa", "region": "Piemonte", "sezione": "I"},
    {"name": "Anfiteatro romano di Susa", "region": "Piemonte", "sezione": "I"},
    
    {"name": "Venaria Reale", "region": "Piemonte", "sezione": "I"},
    
    # ID 70 Split
    {"name": "Langhe", "region": "Piemonte", "sezione": "I"},
    {"name": "Roero", "region": "Piemonte", "sezione": "I"},
    {"name": "Monferrato", "region": "Piemonte", "sezione": "I"},
    
    {"name": "Sacra di San Michele", "region": "Piemonte", "sezione": "I"},
    {"name": "Trulli di Alberobello", "region": "Puglia", "sezione": "I", "fallback_lat": 40.7836, "fallback_lon": 17.2372},
    
    # ID 73 Split
    {"name": "Basilica di San Nicola", "region": "Puglia", "sezione": "I"},
    {"name": "Castello normanno-svevo (Bari)", "region": "Puglia", "sezione": "I"},
    
    # ID 74 Split
    {"name": "Basilica di Santa Croce (Lecce)", "region": "Puglia", "sezione": "I"},
    {"name": "Palazzo dei Celestini (Lecce)", "region": "Puglia", "sezione": "I"},
    
    {"name": "Castel del Monte", "region": "Puglia", "sezione": "I"},
    {"name": "Castello Aragonese (Otranto)", "region": "Puglia", "sezione": "I", "fallback_lat": 40.1444, "fallback_lon": 18.4925},
    {"name": "Cattedrale di Trani", "region": "Puglia", "sezione": "I"},
    {"name": "Santuario di San Michele Arcangelo (Monte Sant'Angelo)", "region": "Puglia", "sezione": "I", "fallback_lat": 41.7075, "fallback_lon": 15.9553},
    
    # ID 80 Split
    {"name": "Tomba dei giganti di Coddu Vecchiu", "region": "Sardegna", "sezione": "I"},
    {"name": "Complesso nuragico La Prisgiona", "region": "Sardegna", "sezione": "I"},
    
    # ID 81 Split
    {"name": "Necropoli di Anghelu Ruju", "region": "Sardegna", "sezione": "I", "fallback_lat": 40.6306, "fallback_lon": 8.3267},
    {"name": "Necropoli di Montessu", "region": "Sardegna", "sezione": "I"},
    {"name": "Pranu Muttedu", "region": "Sardegna", "sezione": "I"},
    
    # ID 82 Split
    {"name": "Santuario nuragico di Santa Cristina", "region": "Sardegna", "sezione": "I"},
    {"name": "Santuario nuragico di Santa Vittoria", "region": "Sardegna", "sezione": "I"},
    
    # ID 83 Split
    {"name": "Museo civico archeologico Giovanni Marongiu", "region": "Sardegna", "sezione": "I"},
    {"name": "Giganti di monte Prama", "region": "Sardegna", "sezione": "I", "search": "Giganti di Mont'e Prama", "fallback_lat": 39.9328, "fallback_lon": 8.5283},
    
    # ID 84 Split
    {"name": "Tharros", "region": "Sardegna", "sezione": "I"},
    {"name": "Nora (Italia)", "region": "Sardegna", "sezione": "I"},
    {"name": "Monte Sirai", "region": "Sardegna", "sezione": "I"},
    
    # ID 85 Split
    {"name": "Duomo di Catania", "region": "Sicilia", "sezione": "I", "fallback_lat": 37.5025, "fallback_lon": 15.0881},
    {"name": "Fontana dell'Elefante", "region": "Sicilia", "sezione": "I"},
    
    {"name": "Modica", "region": "Sicilia", "sezione": "I"},
    {"name": "Noto", "region": "Sicilia", "sezione": "I", "fallback_lat": 36.8911, "fallback_lon": 15.0706},
    
    # ID 88 Split
    {"name": "Palermo arabo-normanna", "region": "Sicilia", "sezione": "I", "search": "Cattedrale di Palermo"},
    {"name": "Duomo di Cefalù", "region": "Sicilia", "sezione": "I"},
    {"name": "Duomo di Monreale", "region": "Sicilia", "sezione": "I"},
    
    # ID 89 Split
    {"name": "Parco archeologico della Neapolis", "region": "Sicilia", "sezione": "I"},
    {"name": "Necropoli di Pantalica", "region": "Sicilia", "sezione": "I"},
    
    {"name": "Parco dell'Etna", "region": "Sicilia", "sezione": "I"},
    {"name": "Segesta", "region": "Sicilia", "sezione": "I"},
    {"name": "Selinunte", "region": "Sicilia", "sezione": "I"},
    {"name": "Teatro antico di Taormina", "region": "Sicilia", "sezione": "I"},
    {"name": "Valle dei Templi", "region": "Sicilia", "sezione": "I"},
    {"name": "Villa del Casale", "region": "Sicilia", "sezione": "I", "fallback_lat": 37.3644, "fallback_lon": 14.3347},
    {"name": "Basilica di Santa Maria Novella", "region": "Toscana", "sezione": "I"},
    
    # ID 97 Split
    {"name": "Duomo di Firenze", "region": "Toscana", "sezione": "I", "search": "Cattedrale di Santa Maria del Fiore"},
    {"name": "Battistero di San Giovanni (Firenze)", "region": "Toscana", "sezione": "I"},
    
    {"name": "Piazza dei Miracoli", "region": "Toscana", "sezione": "I"},
    
    # ID 100 Split
    {"name": "Ponte Vecchio", "region": "Toscana", "sezione": "I"},
    {"name": "Palazzo Vecchio", "region": "Toscana", "sezione": "I"},
    
    {"name": "Torri di San Gimignano", "region": "Toscana", "sezione": "I", "search": "San Gimignano", "fallback_lat": 43.4678, "fallback_lon": 11.0431},
    {"name": "Cosa (colonia romana)", "region": "Toscana", "sezione": "I"},
    
    # ID 103 Split
    {"name": "Santuario della Verna", "region": "Toscana", "sezione": "I"},
    {"name": "Monastero di Camaldoli", "region": "Toscana", "sezione": "I"},
    
    # ID 106 Split
    {"name": "Piazza del Campo", "region": "Toscana", "sezione": "I"},
    {"name": "Duomo di Siena", "region": "Toscana", "sezione": "I"},
    
    # ID 107 Split
    {"name": "Colline del Chianti", "region": "Toscana", "sezione": "I"},
    {"name": "Pienza", "region": "Toscana", "sezione": "I"},
    {"name": "Val d'Orcia", "region": "Toscana", "sezione": "I"},
    
    {"name": "Cappelle Medicee", "region": "Toscana", "sezione": "I", "fallback_lat": 43.7747, "fallback_lon": 11.2536},
    
    # ID 109 Split
    {"name": "Dolomiti", "region": "Trentino-Alto Adige", "sezione": "I"},
    {"name": "Lago di Braies", "region": "Trentino-Alto Adige", "sezione": "I"},
    
    {"name": "Duomo di Trento", "region": "Trentino-Alto Adige", "sezione": "I"},
    
    # ID 111 Cluster
    {"name": "Assisi e le sue Basiliche", "region": "Umbria", "sezione": "I", "fallback_lat": 43.0758, "fallback_lon": 12.6094, "subsections": ["Basilica di San Francesco", "Basilica di Santa Chiara", "Basilica di Santa Maria degli Angeli"]},
    
    {"name": "Cattedrale di San Lorenzo (Perugia)", "region": "Umbria", "sezione": "I"},
    {"name": "Carsulae", "region": "Umbria", "sezione": "I"},
    {"name": "Duomo di Orvieto", "region": "Umbria", "sezione": "I"},
    {"name": "Cascata delle Marmore", "region": "Umbria", "sezione": "I"},
    {"name": "Parco nazionale del Gran Paradiso", "region": "Valle d'Aosta", "sezione": "I"},
    {"name": "Castello di Quart", "region": "Valle d'Aosta", "sezione": "I"},
    
    # ID 118 Cluster
    {"name": "Vicenza Centro", "region": "Veneto", "sezione": "I", "fallback_lat": 45.5467, "fallback_lon": 11.5475, "subsections": [
        {"name": "Duomo di Vicenza", "search": "Cattedrale di Santa Maria Annunziata"},
        {"name": "Criptoportico di Vicenza", "search": "Criptoportico romano (Vicenza)"},
        {"name": "Basilica Palladiana"}
    ]},
    
    # ID 119 Split
    {"name": "Arena di Verona", "region": "Veneto", "sezione": "I"},
    {"name": "Basilica di San Zeno", "region": "Veneto", "sezione": "I"},
    {"name": "Arche Scaligere", "region": "Veneto", "sezione": "I"},
    
    # ID 120 Cluster
    {"name": "Padova Centro", "region": "Veneto", "sezione": "I", "fallback_lat": 45.4064, "fallback_lon": 11.8767, "subsections": ["Basilica di Sant'Antonio di Padova", "Prato della Valle", "Cappella degli Scrovegni"]},
    
    # ID 121 Cluster
    {"name": "Sistema monumentale di Piazza San Marco", "region": "Veneto", "sezione": "I", "fallback_lat": 45.4336, "fallback_lon": 12.3384, "subsections": ["Basilica di San Marco", "Palazzo Ducale (Venezia)"]},
    
    # ID 122 Cluster
    {"name": "Laguna di Venezia", "region": "Veneto", "sezione": "I", "fallback_lat": 45.4371, "fallback_lon": 12.3326, "subsections": ["Canal Grande", "Murano", "Burano", "Torcello"]},
    
    {"name": "Colline del Prosecco di Conegliano e Valdobbiadene", "region": "Veneto", "sezione": "I", "fallback_lat": 45.8972, "fallback_lon": 12.0000},
    {"name": "Ville palladiane", "region": "Veneto", "sezione": "I", "fallback_lat": 45.5317, "fallback_lon": 11.5622},
    
    # SEZIONE II (Musei)
    {"name": "Museo archeologico nazionale di Reggio Calabria", "region": "Calabria", "sezione": "II", "subsections": [
        {"name": "Bronzi di Riace"}, 
        {"name": "Sezione Preistorica"}
    ]},
    {"name": "Museo archeologico nazionale di Napoli", "region": "Campania", "sezione": "II", "subsections": [
        {"name": "Collezione Farnese"}, 
        {"name": "Arte egizia"}
    ]},
    {"name": "Museo di Capodimonte", "region": "Campania", "sezione": "II", "fallback_lat": 40.8672, "fallback_lon": 14.2506, "subsections": [
        {"name": "Appartamenti reali di Capodimonte"}, 
        {"name": "Tiziano Vecellio", "specific_works": "Ritratto di Papa Paolo III, Danae, Maddalena penitente."}, 
        {"name": "Raffaello Sanzio", "specific_works": "Ritratto del cardinale Alessandro Farnese, frammenti della pala di San Nicola da Tolentino."}, 
        {"name": "Caravaggio", "specific_works": "La Flagellazione di Cristo."}
    ]},
    {"name": "Museo nazionale di Ravenna", "region": "Emilia-Romagna", "sezione": "II", "subsections": [{"name": "Codice miniato"}]},
    {"name": "Musei Vaticani", "region": "Lazio", "sezione": "II", "subsections": [
        {"name": "Cappella Sistina"}, 
        {"name": "Stanze di Raffaello"}, 
        {"name": "Galleria delle carte geografiche"}, 
        {"name": "Museo Pio-Clementino"}
    ]},
    {"name": "Galleria Borghese", "region": "Lazio", "sezione": "II", "subsections": [
        {"name": "Gian Lorenzo Bernini", "specific_works": "Apollo e Dafne, Il Ratto di Proserpina, David, Enea Anchise e Ascanio."}, 
        {"name": "Caravaggio", "specific_works": "Bacchino Malato, Giovane con canestra di frutta, Davide con la testa di Golia, Madonna dei Palafrenieri."}, 
        {"name": "Raffaello Sanzio", "specific_works": "Deposizione Baglioni, Dama col liocorno."},
        {"name": "Antonio Canova", "specific_works": "Paolina Borghese come Venere vincitrice."}
    ]},
    {"name": "Castel Sant'Angelo", "region": "Lazio", "sezione": "II", "subsections": [{"name": "Mausoleo di Adriano"}, {"name": "Passetto di Borgo"}]},
    {"name": "Galleria nazionale d'arte moderna e contemporanea", "region": "Lazio", "sezione": "II", "subsections": [{"name": "Arte contemporanea"}]},
    {"name": "Museo nazionale romano", "region": "Lazio", "sezione": "II", "fallback_lat": 41.9014, "fallback_lon": 12.4983, "subsections": [
        {"name": "Palazzo Massimo alle Terme"}, 
        {"name": "Terme di Diocleziano"}, 
        {"name": "Crypta Balbi"}, 
        {"name": "Palazzo Altemps"}
    ]},
    {"name": "Museo nazionale etrusco di Villa Giulia", "region": "Lazio", "sezione": "II"},
    {"name": "Musei Capitolini", "region": "Lazio", "sezione": "II", "subsections": [
        {"name": "Palazzo dei Conservatori"}, 
        {"name": "Palazzo Nuovo (Roma)"}, 
        {"name": "Pinacoteca Capitolina"}, 
        {"name": "Tabularium"}
    ]},
    {"name": "Palazzo Barberini", "region": "Lazio", "sezione": "II"},
    {"name": "Palazzo Reale (Genova)", "region": "Liguria", "sezione": "II"},
    {"name": "Pinacoteca di Brera", "region": "Lombardia", "sezione": "II", "subsections": [
        {"name": "Piero della Francesca", "specific_works": "Pala di Brera (Pala Montefeltro)."}, 
        {"name": "Donato Bramante", "specific_works": "Cristo alla colonna."}, 
        {"name": "Raffaello Sanzio", "specific_works": "Sposalizio della Vergine."}
    ]},
    {"name": "Cenacolo Vinciano", "region": "Lombardia", "sezione": "II", "search": "Ultima Cena (Leonardo)"},
    {"name": "Museo Egizio (Torino)", "region": "Piemonte", "sezione": "II", "fallback_lat": 45.0683, "fallback_lon": 7.6844, "subsections": [
        {"name": "Tomba di Kha e Merit"}, 
        {"name": "Tempio di Ellesija"}
    ]},
    {"name": "Musei Reali (Torino)", "region": "Piemonte", "sezione": "II", "subsections": [
        {"name": "Palazzo Reale di Torino"}, 
        {"name": "Cappella della Sacra Sindone"}, 
        {"name": "Galleria Sabauda"}
    ]},
    {"name": "Museo archeologico nazionale di Taranto", "region": "Puglia", "sezione": "II"},
    {"name": "Museo archeologico nazionale di Cagliari", "region": "Sardegna", "sezione": "II"},
    {"name": "Museo archeologico regionale Paolo Orsi", "region": "Sicilia", "sezione": "II"},
    {"name": "Gallerie degli Uffizi", "region": "Toscana", "sezione": "II", "fallback_lat": 43.7678, "fallback_lon": 11.2556, "subsections": [
        {"name": "Sandro Botticelli", "specific_works": "La Primavera, Nascita di Venere, Adorazione dei Magi."}, 
        {"name": "Leonardo da Vinci", "specific_works": "Annunciazione, Adorazione dei Magi, Battesimo di Cristo (con Verrocchio)."}, 
        {"name": "Michelangelo Buonarroti", "specific_works": "Tondo Doni."},
        {"name": "Raffaello Sanzio", "specific_works": "Madonna del Cardellino, Ritratto di Leone X."},
        {"name": "Caravaggio", "specific_works": "Scudo con testa di Medusa, Bacco, Sacrificio di Isacco."}
    ]},
    {"name": "Galleria dell'Accademia (Firenze)", "region": "Toscana", "sezione": "II", "fallback_lat": 43.7769, "fallback_lon": 11.2586, "subsections": [
        {"name": "David di Michelangelo"}, 
        {"name": "Prigioni (Michelangelo)"}
    ]},
    {"name": "Palazzo Pitti", "region": "Toscana", "sezione": "II", "subsections": [{"name": "Galleria Palatina"}]},
    {"name": "Gallerie dell'Accademia", "region": "Veneto", "sezione": "II"},

    # SEZIONE III (Siti Archeologici / Ville / Area)
    {"name": "Domus Aurea", "region": "Lazio", "sezione": "III"},
    {"name": "Villa Adriana", "region": "Lazio", "sezione": "III"},
    {"name": "Villa d'Este", "region": "Lazio", "sezione": "III", "search": "Villa d'Este (Tivoli)", "fallback_lat": 41.9633, "fallback_lon": 12.7967},
    {"name": "Villa dei Quintili", "region": "Lazio", "sezione": "III"},
    {"name": "Incisioni rupestri della Val Camonica", "region": "Lombardia", "sezione": "III"},
    {"name": "Grotte di Catullo", "region": "Lombardia", "sezione": "III"},
    {"name": "Parco archeologico di Urbs Salvia", "region": "Marche", "sezione": "III"},
    {"name": "Castello di Racconigi", "region": "Piemonte", "sezione": "III", "fallback_lat": 44.7706, "fallback_lon": 7.6742},
    {"name": "Su Nuraxi", "region": "Sardegna", "sezione": "III"},
    {"name": "Menhir di Laconi", "region": "Sardegna", "sezione": "III", "search": "Menhir", "fallback_lat": 39.8531, "fallback_lon": 9.0525},
    {"name": "Turris Libisonis", "region": "Sardegna", "sezione": "III", "fallback_lat": 40.8358, "fallback_lon": 8.3972}
]

# Unify duplicate locations between Sezione I and III
locations_dict = {}
for loc in locations_raw:
    name = loc["name"]
    norm = name.lower().strip()
    if norm in locations_dict:
        existing = locations_dict[norm]
        if existing["sezione"] != loc["sezione"]:
            existing["sezione_both"] = True
    else:
        loc["sezione_both"] = False
        locations_dict[norm] = loc

locations = list(locations_dict.values())

def fetch_wiki_info(title, retries=4):
    url = "https://it.wikipedia.org/w/api.php?action=query&prop=coordinates|pageimages|extracts&exintro&explaintext&exchars=250&redirects=1&titles=" + urllib.parse.quote(title) + "&format=json&pithumbsize=500"
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'MappaEsameBot/1.5'})
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                pages = data['query']['pages']
                page = list(pages.values())[0]
                
                lat = None
                lon = None
                if 'coordinates' in page:
                    lat = page['coordinates'][0]['lat']
                    lon = page['coordinates'][0]['lon']
                
                image = None
                if 'thumbnail' in page:
                    image = page['thumbnail']['source']
                    
                extract = page.get('extract', '')
                if 'missing' in page or len(extract.strip()) < 10:
                    extract = f"Descrizione o riassunto di Wikipedia non disponibile per {title}."
                
                return {
                    "title": page.get('title', title),
                    "lat": lat,
                    "lon": lon,
                    "image": image,
                    "extract": extract,
                    "url": "https://it.wikipedia.org/wiki/" + urllib.parse.quote(page.get('title', title).replace(' ', '_'))
                }
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait_time = 5 * (attempt + 1)
                print(f"Rate limited (429) for {title}. Waiting {wait_time}s before retry...")
                time.sleep(wait_time)
            else:
                print(f"HTTP Error {e.code} fetching {title}")
                return None
        except Exception as e:
            print(f"Error fetching {title}: {e}")
            return None
    return None

final_data = []

print("Starting to fetch Wikipedia data. This may take a moment...")
for loc in locations:
    print(f"Fetching: {loc['name']}")
    info = fetch_wiki_info(loc.get("search", loc["name"]))
    
    subsections_data = []
    if "subsections" in loc:
        for sub in loc["subsections"]:
            sub_name = sub["name"] if isinstance(sub, dict) else sub
            sub_search = sub.get("search", sub_name) if isinstance(sub, dict) else sub_name
            specific_works = sub.get("specific_works") if isinstance(sub, dict) else None
            
            print(f"  Fetching subsection: {sub_name}")
            sub_info = fetch_wiki_info(sub_search)
            if sub_info:
                extract_text = sub_info["extract"]
                if specific_works:
                    extract_text += f"\\n\\nOpere principali per l'esame in questa collezione: {specific_works}"
                    
                subsections_data.append({
                    "name": sub_name,
                    "image": sub_info["image"],
                    "extract": extract_text,
                    "url": sub_info["url"]
                })
            time.sleep(1.0)

    if info:
        lat = info['lat'] if info['lat'] else loc.get("fallback_lat")
        lon = info['lon'] if info['lon'] else loc.get("fallback_lon")
        
        if lat and lon:
            final_data.append({
                "name": loc["name"],
                "region": loc["region"],
                "sezione": loc["sezione"],
                "sezione_both": loc["sezione_both"],
                "lat": lat,
                "lon": lon,
                "image": info["image"],
                "extract": info["extract"],
                "url": info["url"],
                "subsections": subsections_data
            })
        else:
            print(f" -> MISSING COORDS per: {loc['name']}")
    time.sleep(1.0)

js_content = f"const locationsData = {json.dumps(final_data, indent=2, ensure_ascii=False)};"

with open('data.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"Successfully wrote {len(final_data)} locations to data.js")
