
# Aplikace pro analýzu studentských úloh

## Simple skripty
Jednotlivé kroky analýzy lze postupně spouštět pomocí jednoduchých skriptů.

- *simple_extract_archive_with_student_works.py* - extrahuje ZIP archiv s úlohami studentů do výstupní složky a pro každého studenta vytvoří jeden soubor s obsahem všech jeho .cs souborů (s programem).
- *simple_analyze_one_student_work.py* - provede AI analýzu pro jednoho studenta voláním OpenRouter API.
- *simple_analyze_all_students_works.py* - provede AI analýzu pro všechny studenty ve výstupní složce.
- *simple_compress_dir_with_student_works.py* - zkomprimuje výstupní složku s úlohami studentů a jejich analýzou do ZIP archivu.

```
# extrakce ZIPu a kodu studentu
python3 simple_extract_archive_with_student_works.py

# analyza jednoho studenta
python3 simple_analyze_one_student_work.py

# analyza vsech studentu
python3 simple_analyze_all_students_works.py

# komprese vysledku do ZIPu
python3 simple_compress_dir_with_student_works.py
```

## Kompletní skript
Kompletní aplikace, která má na vstupu prace.zip archiv s pracemi studentů z Courseware a na vystupu ZIP archiv s AI analýzou pro každého studenta.

```
python3 main.py
```

