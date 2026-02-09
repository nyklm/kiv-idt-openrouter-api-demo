
# Sbaleni archivu archivu se studentskymi ulohami do ZIP.

from pathlib import Path
import os
from sys import prefix

import basic_functions as bf
from OwnArchiveExtractorTool import OwnArchiveExtractorTool
from settings import *


#########################################################

# nechci balit celou strukturu, jako byla na vstupu, ale jen adresare s kodem studentu

# ziskam seznam adresaru jednotlivych studentu
students_dirs = bf.get_dirs_with_students_code(MAIN_OUTPUT_DIR_PATH)
if not students_dirs:
    print("Nenalezen zadny adresar se studentskym kodem.")
    exit(1)

# z prvniho adresare ziskam jeho rodice
first_student_dir = Path(students_dirs[0]).resolve()
parent_dir = first_student_dir.parent

# zabalim do ZIP
output_zip_path = os.path.join(MAIN_OUTPUT_DIR_PATH, OUTPUT_ZIP_NAME)
OwnArchiveExtractorTool.compress_directory_to_zip(parent_dir, output_zip_path)

print(f"Komprimovany adresar: {parent_dir}\nVytvoreny ZIP: {output_zip_path}")

