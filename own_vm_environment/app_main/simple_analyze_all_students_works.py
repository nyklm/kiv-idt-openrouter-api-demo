import time
# AI analyza ulohy pro jednoho studenta.

from pathlib import Path
import os

import basic_functions as bf
from OpenRouterAPITool import OpenRouterAPITool
from settings import *

# nacteni klice z .env souboru - musi byt instalovan dotenv
import dotenv
dotenv.load_dotenv()
# nactu spravny klic
key_location = os.environ.get("OPENROUTER_API_KEY_VAR_NAME", "not_set")
OPENROUTER_API_KEY = os.environ.get(key_location, None)


#########################################################

# ziskam seznam adresaru jednotlivych studentu
students_dirs = bf.get_dirs_with_students_code(MAIN_OUTPUT_DIR_PATH)
students_count = len(students_dirs)

# necham uzivatele potvrdit, ze chce analyzovat prace pro vsechny studenty
print(f"\n!!! Nalezeno {students_count} studentu.\n!!!Chcete analyzovat prace pro vsechny studenty? (y/n)")
answer = input().lower().strip()
if answer != "y":
    print("Analyza zrusena.")
    exit()

# pokud je vic jak 5 praci a placeny model, tak se zeptam znovu
if students_count > 5 or not OPENROUTER_API_IS_THIS_MODEL_FREE:
    print(f"\n!!! Nalezeno {students_count} studentu a pouzivany model je PLACENY.\n!!!Opravdu chcete pokracovat? (y/n)")
    answer = input().lower().strip()
    if answer != "y":
        print("Analyza zrusena.")
        exit()

# projdu studenty a provedu analyzu pro kazdeho z nich
counter = 0
for student_dir in students_dirs:
    counter += 1
    print("\n"+"-"*8 + f"[{counter}/{students_count}]" + "-"*8)
    print(f"Analyzuji ulohu pro studenta: {student_dir}")

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
    # pauza
    time.sleep(0.5)

print("Done.")





