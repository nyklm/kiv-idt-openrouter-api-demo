
# Kompletni aplikace, ktera:
# 1) rozbali ZIP s ulohami studentu,
# 2) spoji kody pro kazdeho studenta do jednoho souboru,
# 3) pro kazdeho studenta provede analyzu pres OpenRouter API,
# 4) ulozi vysledky analyzy do markdown souboru do adresare studenta,
# 5) zabali vstup a vysledky opet do ZIPu.


from pathlib import Path
import os
import time

import basic_functions as bf
from OwnArchiveExtractorTool import OwnArchiveExtractorTool
from OpenRouterAPITool import OpenRouterAPITool
from settings import *


# nacteni klice z .env souboru - musi byt instalovan dotenv
import dotenv
dotenv.load_dotenv()
# nactu spravny klic
key_location = os.environ.get("OPENROUTER_API_KEY_VAR_NAME", "not_set")
OPENROUTER_API_KEY = os.environ.get(key_location, None)


def main():
    #########################################################
    # priprava dat pro analyzu (rozbaleni ZIP a spojeni kodu pro kazdeho studenta do jednoho souboru)

    # extrahuju ZIP s ulahami studentu
    bf.extract_main_archive(MAIN_INPUT_DIR_PATH, MAIN_ARCHIVE_NAME, MAIN_OUTPUT_DIR_PATH, ALLOWED_EXTENSIONS)

    # ziskam seznam adresaru jednotlivych studentu
    students_dirs = bf.get_dirs_with_students_code(MAIN_OUTPUT_DIR_PATH)
    # students_dirs = [students_dirs[1]]
    # print(students_dirs)

    # ziskam seznam adresaru jednotlivych studentu
    if not students_dirs:
        print("Nenalezen zadny adresar se studentskym kodem.")
        exit(1)

    # spojim vsechny kody jednoho studenta do jednoho souboru
    # a udelam to pro vsechny studenty
    for student_dir in students_dirs:
        print(f"Zpracovávám adresář: {student_dir}")
        bf.merge_all_codes_for_one_student(student_dir, COMPLETE_STUDENT_CODE_FILE_NAME)


    #########################################################
    # pro jistotu necham uzivatele potvrdit analyzu

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


    #########################################################
    # analyza pro kazdeho studenta pres OpenRouter API

    # projdu studenty a provedu analyzu pro kazdeho z nich
    counter = 0
    for student_dir in students_dirs:
        counter += 1
        print("\n" + "-" * 8 + f"[{counter}/{students_count}]" + "-" * 8)
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

    print("\nAnalyza dokoncena.")


    ##########################################################
    # ulozeni vysledku analyzy do ZIPu, vcetne puvodnich dat
    # nechci balit celou strukturu, jako byla na vstupu, ale jen adresare s kodem studentu

    # z prvniho adresare ziskam jeho rodice
    first_student_dir = Path(students_dirs[0]).resolve()
    parent_dir = first_student_dir.parent
    # zabalim do ZIP
    output_zip_path = os.path.join(MAIN_OUTPUT_DIR_PATH, OUTPUT_ZIP_NAME)
    OwnArchiveExtractorTool.compress_directory_to_zip(parent_dir, output_zip_path)
    print(f"Komprimovany adresar: {parent_dir}\nVytvoreny ZIP: {output_zip_path}")



if __name__ == "__main__":
    main()