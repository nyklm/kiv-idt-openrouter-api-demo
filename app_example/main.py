import os
from pathlib import Path
import requests
import json

# zvoleny model v OpenRouter
# SELECTED_MODEL = "google/gemini-2.0-flash-exp:free"   # tento uz je bohuzel placeny = jine jmeno
SELECTED_MODEL = "google/gemma-3-27b-it:free"  # msg_v2


# nacteni klice z .env souboru - musi byt instalovan dotenv
import dotenv
dotenv.load_dotenv()
# nactu spravny klic
key_location = os.environ.get("OPENROUTER_API_KEY_VAR_NAME", "not_set")
OPEN_ROUTER_API_KEY = os.environ.get(key_location, "")


#########################################################################
# file loading functions

def read_file(file_path):
    """Load a file and return its content as a string."""
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        return f.read()

def write_file(file_path, content):
    """Write content to a file."""
    with open(file_path, 'w', encoding='utf-8-sig') as f:
        f.write(content)

# TODO - funkce z kodu Jakuba Sida
def load_students_code():
    """Load all files from students folder and combine them into a single string."""
    students_dir = Path("students")
    combined_text = ""
    
    # Get all Python files in the students directory and sort them
    student_files = sorted(students_dir.glob("*.py"))
    
    for i, file_path in enumerate(student_files, start=1):
        # Add student header
        combined_text += f"Student_{i:02d}:\n\n"
        
        # Read and add the file content
        with open(file_path, 'r', encoding='utf-8') as f:
            combined_text += f.read()
        
        # Add spacing between students (except after the last one)
        if i < len(student_files):
            combined_text += "\n\n"
    
    return combined_text


def create_api_messages_v1(system_prompt, student_solution, task_description="", task_code=""):
    """
    Create the message structure for the OpenRouter API.
    :param system_prompt (str): The system prompt to guide the model's behavior.
    :param student_solution (str): The student's submitted solution code.
    :param task_description (str, optional): The description of the task. (def.="")
    :param task_code (str, optional): The initial code provided for the task. (def.="")
    """
    messages = []
    # system prompt je vzdy
    tmpLen = len(system_prompt)
    print("System prompt length:", tmpLen, "cca", tmpLen / 4, "tokens.")
    messages.append({
                # nastaveni modelu, jak se ma chovat (system prompt).
                # normativni pravidlo - ma nejvyssi prioritu.
                # jak ma hodnotit, jakym zpusobem ma odpovidat a format odpovedi.
                # je vhodne mit jeden system prompt !!
                "role": "system",
                "content": system_prompt
            })
    # zadani tasks
    if task_description:
        tmpLen = len(task_description)
        print("Task description prompt length:", tmpLen, "cca", tmpLen / 4, "tokens.")
        messages.append({
                    # zadani je prvni "user" prompt !!
                    "role": "user",
                    "content": f"ZADÁNÍ ÚLOHY:\n{task_description}"
                })
    # vychozi kod
    if task_code:
        tmpLen = len(task_code)
        print("Source code length:", tmpLen, "cca", tmpLen / 4, "tokens.")
        messages.append({
                    # vychozi kod ze zadani je druhy "user" prompt !!
                    "role": "user",
                    "content": f"VÝCHOZÍ KÓD (student jej měl k dispozici):\n```csharp\n\n{task_code}\n```"
                })
    # odevzdane reseni studenta
    tmpLen = len(student_solution)
    print("Student solution length:", tmpLen, "cca", tmpLen / 2, "tokens.") # kod spotrebuje vic tokenu
    messages.append({
                # reseni je dalsi "user" prompt !!
                "role": "user",
                "content": f"ODEVZDANÉ ŘEŠENÍ STUDENTA:\n```csharp\n\n{student_solution}\n```"
            })
    return messages

def create_api_messages_v2(system_prompt, student_solution, task_description="", task_code="", print_info=False):
    '''
    Vytvori strukturu zpravy pro OpenRouter API.
    :param system_prompt (str): Systemovy prompt pro usmerneni chovani modelu.
    :param student_solution (str): Odevzdane reseni studenta (kod).
    :param task_description (str, optional): Popis ulohy. (def.="")
    :param task_code (str, optional): Vychozi kod pro ulohu. (def.="")
    '''
    # messages pro OpenRouter API
    messages = []
    # system prompt je vzdy
    messages.append({
        # nastaveni modelu, jak se ma chovat (system prompt).
        # normativni pravidlo - ma nejvyssi prioritu.
        # jak ma hodnotit, jakym zpusobem ma odpovidat a format odpovedi.
        # je vhodne mit jeden system prompt !!
        "role": "system",
        "content": [{
                "type": "text",
                "text": system_prompt
            }]
    })
    # zadani tasks
    if task_description:
        messages.append({
            # zadani je prvni "user" prompt !!
            "role": "user",
            "content": [{
                    "type": "text",
                    "text": f"ZADÁNÍ ÚLOHY:\n{task_description}"
                }]
        })
    # vychozi kod
    if task_code:
        messages.append({
            # vychozi kod ze zadani je druhy "user" prompt !!
            "role": "user",
            "content": [{
                    "type": "text",
                    "text": f"VÝCHOZÍ KÓD (student jej měl k dispozici):\n```csharp\n\n{task_code}\n```"
                }]
        })
    # odevzdane reseni studenta
    messages.append({
        # reseni je dalsi "user" prompt !!
        "role": "user",
        "content": [{
                "type": "text",
                "text": f"ODEVZDANÉ ŘEŠENÍ STUDENTA:\n```csharp\n\n{student_solution}\n```"
            }]
    })

    if print_info:
        tmpLen = len(system_prompt)
        print("System prompt length:", tmpLen, "cca", tmpLen / 4, "tokens.")
        tmpLen = len(task_description)
        print("Task description prompt length:", tmpLen, "cca", tmpLen / 4, "tokens.")
        tmpLen = len(task_code)
        print("Source code length:", tmpLen, "cca", tmpLen / 4, "tokens.")
        # pozor, kod spotrebuje vic tokenu
        tmpLen = len(student_solution)
        print("Student solution length:", tmpLen, "cca", tmpLen / 2, "tokens.")

    return messages

def analyze_with_openrouter(messages):
    """Send the students code and mistakes to OpenRouter API with Gemini 2.5 Flash."""
    
    # Get API key from environment variable
    api_key = OPEN_ROUTER_API_KEY 
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY environment variable not set")
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # minimalni data pro API
    # payload = {
    #     "model": "google/gemini-2.0-flash-exp:free",
    #     "messages": [
    #         {
    #             "role": "user",
    #             "content": prompt
    #         }
    #     ]
    # }

    # struktura dat pro hodnoceni uloh
    payload = {
        "model": SELECTED_MODEL,
        "messages": messages
    }
    
    # Send the request to OpenRouter API
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    
    result = response.json()
    result_content = result['choices'][0]['message']['content']

    tmpLen = len(result_content)
    print("Result length:", tmpLen, "cca", tmpLen / 4, "tokens.")

    # print usage info
    print(result["usage"])

    return result_content


def main():
    print("Loading system prompt...")
    supervisor = read_file("../meta/global/supervisor_prompt.md")
    mistakes = read_file("../meta/global/caste_chyby.md")
    system_prompt = supervisor + "\n\n" + mistakes
    
    print("Loading task prompt...")
    task_descriptions = read_file("../meta/tasks/01/textove_zadani.md")
    task_code = read_file("../meta/tasks/01/kod_zadani.md")

    print(task_descriptions)
    
    print("Loading students' code...")
    # TODO .....
    students_code = read_file("../ukázky/Romova.cs")  # mela 5 bodu
    # students_code = read_file("students/Vlach.cs")   # mel 2.5 bodu

    print("Creating API message...")
    # messages = create_api_messages_v1(system_prompt, students_code, task_descriptions, task_code)
    messages = create_api_messages_v2(system_prompt, students_code, task_descriptions, task_code)
    # print(message)

    with open("tmp_messages_for_api.json", "w", encoding="utf-8-sig") as f:
        json.dump(messages, f, ensure_ascii=False, indent=4, sort_keys=False)



    print("Analyzing with via OpenRouter...")
    analysis = analyze_with_openrouter(messages)
    # print(analysis)

    # Save results to file
    output_file = "tmp_analysis_results.md"
    write_file(output_file, analysis)

    print(f"Results saved to: {output_file}")


if __name__ == "__main__":
    main()
