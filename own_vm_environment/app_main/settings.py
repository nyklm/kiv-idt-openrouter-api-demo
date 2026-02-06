
from pathlib import Path

# vstupni soubor a povolene pripony extrahovanych souboru
MAIN_ARCHIVE_NAME = "prace.zip"
ALLOWED_EXTENSIONS = [".cs", ".zip", ".rar", ".7z", ".7za"]
# nazev souboru s kompletnim kodem studenta pro AI
OUTPUT_FILE_NAME = "complete_code.txt"

# hlavni adresare pro vstup a vystup
MAIN_INPUT_DIR_PATH = "input_dir"
MAIN_OUTPUT_DIR_PATH = "output_dir"
MAIN_TMP_DIR_PATH = "tmp_dir"
# pokud neexistuji, tak je vytvorim
Path(MAIN_INPUT_DIR_PATH).mkdir(parents=True, exist_ok=True)
Path(MAIN_OUTPUT_DIR_PATH).mkdir(parents=True, exist_ok=True)
Path(MAIN_TMP_DIR_PATH).mkdir(parents=True, exist_ok=True)

# zakladni nastaveni pro OpenRouter API
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
# volba modelu
OPENROUTER_API_AI_MODEL = "google/gemini-2.5-flash:free"  # tento uz je bohuzel placeny

# nastaveni cest k souborum s prompty apod.
msg_path_prefix = "meta/"
MSG_SUPERVISOR_FILE_PATH = msg_path_prefix +"global/supervisor_prompt.md"
MSG_BASIC_MISTAKES_FILE_PATH = msg_path_prefix +"global/caste_chyby.md"
MSG_TASK_DESCRIPTION_FILE_PATH = msg_path_prefix +"tasks/01/textove_zadani.md"
MSG_TASK_CODE_FILE_PATH = msg_path_prefix +"tasks/01/kod_zadani.md"
MSG_TASK_MISTAKES_FILE_PATH = msg_path_prefix +"tasks/01/caste_chyby.md"
