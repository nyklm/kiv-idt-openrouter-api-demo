
# AI analyza ulohy pro jednoho studenta.

from pathlib import Path
import os

import basic_functions as bf
from OpenRouterAPITool import OpenRouterAPITool
from settings import *

# cesta k adresari, kde jsou ulozeny kody studentu
STUDENT_DIR_PATH = "A123P-Jmeno-PRIJMENI"
# TODO - zadat dle potreby


# nacteni klice z .env souboru - musi byt instalovan dotenv
import dotenv
dotenv.load_dotenv()
# nactu spravny klic
key_location = os.environ.get("OPENROUTER_API_KEY_VAR_NAME", "not_set")
OPENROUTER_API_KEY = os.environ.get(key_location, None)


#########################################################

# ziskam seznam adresaru jednotlivych studentu
students_dirs = bf.get_dirs_with_students_code(MAIN_OUTPUT_DIR_PATH)

# filtr pro ziskani pouze adresare daneho studenta
students_dirs = [Path(d).resolve() for d in students_dirs]
students_dirs = [d for d in students_dirs if d.name == STUDENT_DIR_PATH]

if len(students_dirs) == 0:
    print(f"Nenalezen adresar studenta: {STUDENT_DIR_PATH}")
    exit()

#########################################################

# jen jeden student
student_dir = students_dirs[0]
print(f"Analyzuji ulohu pro studenta: {student_dir.name}")

# soubor s kompletnim kodem studenta pro AI
student_code_file_path = os.path.join(student_dir, COMPLETE_STUDENT_CODE_FILE_NAME)

# provedeni jedne kompletni analyzy pro jednoho studenta, v jednom behu,
# s ulozenim mezivysledku do JSON souboru a finalni analyzy do markdown souboru.
OpenRouterAPITool.perform_one_whole_analysis(
    OPENROUTER_API_URL,
    OPENROUTER_API_KEY,
    OPENROUTER_API_AI_MODEL,
    MSG_SUPERVISOR_FILE_PATH,
    MSG_BASIC_MISTAKES_FILE_PATH,
    MSG_TASK_DESCRIPTION_FILE_PATH,
    MSG_TASK_CODE_FILE_PATH,
    MSG_TASK_MISTAKES_FILE_PATH,
    student_code_file_path,
    student_dir,
    OUTPUT_MESSAGE_FOR_API_JSON_FILE_NAME_PART,
    OUTPUT_RESPONSE_FROM_API_JSON_FILE_NAME_PART,
    OUTPUT_ANALYSIS_RESULTS_FILE_NAME_PART
)

print("Done.")





