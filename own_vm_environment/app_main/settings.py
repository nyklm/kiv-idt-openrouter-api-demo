
from pathlib import Path


# zakladni nastaveni pro OpenRouter API
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
# volba modelu
# OPENROUTER_API_AI_MODEL = "google/gemini-2.0-flash-exp:free" # msg-V1 # tento uz je bohuzel placeny
# OPENROUTER_API_AI_MODEL = "meta-llama/llama-3.3-70b-instruct:free" # msg-V1
# OPENROUTER_API_AI_MODEL = "meta-llama/llama-3.2-3b-instruct:free" # msg-V1
OPENROUTER_API_IS_THIS_MODEL_FREE = True

print("POZOR: PLACENY MODEL !!!")
# OPENROUTER_API_AI_MODEL = "google/gemini-2.5-flash-lite" # msg-V2 # cena $0.10/0.40
OPENROUTER_API_AI_MODEL = "google/gemini-2.0-flash-001" # msg-V2 # cena $0.10/0.40
# OPENROUTER_API_AI_MODEL = "openai/gpt-4o-mini" # msg-V2 # cena $0.15/0.60
OPENROUTER_API_IS_THIS_MODEL_FREE = False


##################################################

# vstupni soubor a povolene pripony extrahovanych souboru
MAIN_ARCHIVE_NAME = "prace.zip"
ALLOWED_EXTENSIONS = [".cs", ".zip", ".rar", ".7z", ".7za"]

# nazev souboru s kompletnim kodem studenta pro AI
COMPLETE_STUDENT_CODE_FILE_NAME = "complete_code.txt"
# cast nazvu souboru se zpravami do/od API
OUTPUT_MESSAGE_FOR_API_JSON_FILE_NAME_PART = "tmp_messages_for_api"
OUTPUT_RESPONSE_FROM_API_JSON_FILE_NAME_PART = "tmp_response_from_api"
# cast nazvu souboru s vysledky AI analyzy
OUTPUT_ANALYSIS_RESULTS_FILE_NAME_PART = "analysis_results"
# nazev souboru s vystupnim ZIP archivem
OUTPUT_ZIP_NAME = "prace_output.zip"

# hlavni adresare pro vstup a vystup
MAIN_INPUT_DIR_PATH = "input_dir"
MAIN_OUTPUT_DIR_PATH = "output_dir"
MAIN_TMP_DIR_PATH = "tmp_dir"
# pokud neexistuji, tak je vytvorim
Path(MAIN_INPUT_DIR_PATH).mkdir(parents=True, exist_ok=True)
Path(MAIN_OUTPUT_DIR_PATH).mkdir(parents=True, exist_ok=True)
Path(MAIN_TMP_DIR_PATH).mkdir(parents=True, exist_ok=True)

# nastaveni cest k souborum s prompty apod.
msg_path_prefix = "../../"
MSG_SUPERVISOR_FILE_PATH = msg_path_prefix + "meta/global/supervisor_prompt.md"
MSG_BASIC_MISTAKES_FILE_PATH = msg_path_prefix + "meta/global/caste_chyby.md"
MSG_TASK_DESCRIPTION_FILE_PATH = msg_path_prefix + "meta/tasks/01/textove_zadani.md"
MSG_TASK_CODE_FILE_PATH = msg_path_prefix + "meta/tasks/01/kod_zadani.md"
MSG_TASK_MISTAKES_FILE_PATH = msg_path_prefix + "meta/tasks/01/caste_chyby.md"

