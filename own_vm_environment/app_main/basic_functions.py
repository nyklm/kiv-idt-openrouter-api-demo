
# Zakladni funkce pro praci s archivy a ziskani kodu studentu

import os
from pathlib import Path

from OwnArchiveExtractorTool import OwnArchiveExtractorTool

def extract_main_archive(main_input_dir_path, main_archive_name, main_output_dir_path, allowed_extensions=[]):
    '''
    Extrahuje hlavni archiv s ulohami studentu do vystupniho adresare.
    :param main_input_dir_path: Vstupni adresar.
    :param main_archive_name: Nazev hlavniho archivu (ZIP).
    :param main_output_dir_path: Vystupni adresar.
    :param allowed_extensions: Povolene pripony extrahovanych souboru.
    :return:
    '''
    # cela cesta k archivu
    archive_path = os.path.join(main_input_dir_path, main_archive_name)
    extracted_path = None
    try:
        extracted_path = OwnArchiveExtractorTool.extract(archive_path, out_dir=main_output_dir_path, allowed_extensions=allowed_extensions)
        print(f"Files extracted to: {extracted_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
        # ale vyjimku presto predam dal
        raise e
    return extracted_path


def get_dirs_with_students_code(main_output_dir_path):
    '''
    Ziska seznam adresaru, ktere obsahuji ulohy studentu.
    :param main_output_dir_path: Hlavni vystupni adresar.
    :return: Seznam adresaru s kodem studentu.
    '''
    # adresare s ulohami jsou zanoreny ve 3. urovni
    dirs = []
    # prvni
    for tmp1 in os.listdir(main_output_dir_path):
        path_tmp1 = os.path.join(main_output_dir_path, tmp1)
        if not os.path.isdir(path_tmp1):
            continue
        # druha
        for tmp2 in os.listdir(path_tmp1):
            path_tmp2 = os.path.join(path_tmp1, tmp2)
            if not os.path.isdir(path_tmp2):
                continue
            # treti
            for tmp3 in os.listdir(path_tmp2):
                path_tmp3 = os.path.join(path_tmp2, tmp3)
                if not os.path.isdir(path_tmp3):
                    continue
                # ctvrta
                for tmp4 in os.listdir(path_tmp3):
                    path_tmp4 = os.path.join(path_tmp3, tmp4)
                    if os.path.isdir(path_tmp4):
                        # Toto je pozadovany adresar
                        # print("Adresar ve 4. urovni:", path_tmp4)
                        dirs.append(path_tmp4)
    return dirs

def merge_all_codes_for_one_student(student_dir, output_file_name):
    '''
    Zpracuje jeden adresar se studentovym kodem.
    Spoji vsechny .cs soubory do jednoho vystupniho souboru.
    :param student_dir: Adresar studenta.
    '''
    # soubor, do ktereho se ulozi kompletni kod studenta
    output_file_path = os.path.join(student_dir, output_file_name)
    # projdu vsechny .cs soubory v adresari a podadresarich a ulozim jejich obsahy do vystupniho souboru
    with open(output_file_path, "w", encoding="utf-8") as out_f:
        # projdu rekurzivne vsechny soubory v adresari
        for root, dirs, files in os.walk(student_dir):
            for file in files:
                if file.endswith(".cs"):
                    file_path = os.path.join(root, file)
                    # Relativni cesta od student_dir
                    rel_path = os.path.relpath(file_path, student_dir)
                    # zapis do souboru
                    out_f.write(f"############ {rel_path} ############\n")  # název souboru
                    try:
                        with open(file_path, "r", encoding="utf-8-sig", errors="ignore") as in_f:
                            content = in_f.read()
                        out_f.write(content + "\n\n")
                    except Exception as e:
                        out_f.write(f"CHYBA při čtení souboru: {e}\n\n")