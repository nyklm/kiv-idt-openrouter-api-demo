
# Extrahovani archivu se studentskymi ulohami
# a spojeni jejich kodu do jednoho souboru pro kazdeho studenta.

from pathlib import Path
import os
from sys import prefix

import basic_functions as bf
from settings import *


# nacteni klice z .env souboru - musi byt instalovan dotenv
import dotenv
dotenv.load_dotenv()
# nactu spravny klic
key_location = os.environ.get("OPENROUTER_API_KEY_VAR_NAME", "not_set")
OPEN_ROUTER_API_KEY = os.environ.get(key_location, "")


#########################################################

# extrahuju ZIP s ulahami studentu
bf.extract_main_archive(MAIN_INPUT_DIR_PATH, MAIN_ARCHIVE_NAME, MAIN_OUTPUT_DIR_PATH, ALLOWED_EXTENSIONS)

# ziskam seznam adresaru jednotlivych studentu
students_dirs = bf.get_dirs_with_students_code(MAIN_OUTPUT_DIR_PATH)
# students_dirs = [students_dirs[1]]
# print(students_dirs)

# spojim vsechny kody jednoho studenta do jednoho souboru
# a udelam to pro vsechny studenty
for student_dir in students_dirs:
    print(f"Zpracovávám adresář: {student_dir}")
    bf.merge_all_codes_for_one_student(student_dir, OUTPUT_FILE_NAME)
