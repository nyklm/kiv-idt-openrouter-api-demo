import os
from pathlib import Path
from time import sleep
import requests
from requests import HTTPError
import json
from datetime import datetime



class OpenRouterAPITool:
    '''
    Nastroj pro praci s OpenRouter API.
    '''

    @staticmethod
    def read_file(file_path, not_found_rise_error=True, not_found_value=""):
        '''
        Nacte obsah souboru a pokud soubor neexistuje, vrati prazdny retezec.
        :param file_path: Cesta k souboru.
        :param not_found_rise_error: Pokud je True, vyvola vyjimku FileNotFoundError, pokud soubor neexistuje. (def.=True)
        :param not_found_value: Hodnota, ktera se vrati, pokud soubor neexistuje a not_found_rise_error je False. (def.="")
        :return: Obsah souboru jako retezec nebo prazdny retezec, pokud soubor neexistuje.
        '''
        try:
            with open(file_path, 'r', encoding='utf-8-sig') as f:
                return f.read()
        except FileNotFoundError as err:
            # pokud se soubor nepovedlo najit, mam vyvolat vyjimku nebo vratit zadanou hodnotu
            if not_found_rise_error:
                raise err
            else:
                print(f"File not found: {file_path}. Returning default value.")
                return not_found_value


    @staticmethod
    def write_file(file_path, content):
        """Write content to a file."""
        with open(file_path, 'w', encoding='utf-8-sig') as f:
            f.write(content)


    @staticmethod
    def load_basic_prompts(system_prompt_path, basic_mistakes_path, task_description_path, task_code_path, task_mistakes_path):
        '''
        Nacte zakladni prompty pro hodnoceni ulohy.
        :param system_prompt_path: Cesta k souboru se system promptem.
        :param basic_mistakes_path: Cesta k souboru s popisem zakladnich chyb.
        :param task_description_path: Cesta k souboru s popisem ulohy.
        :param task_code_path: Cesta k souboru s vychozim kodem pro ulohu.
        :param task_mistakes_path: Cesta k souboru s popisem specifickych chyb pro danou ulohu.
        :return: Nactena data jako stringy v poradi: system_prompt, task_description, task_code.
        '''
        # system prompt je povinny a pri nenacteni vyhodi vyjimku
        system_prompt = OpenRouterAPITool.read_file(system_prompt_path, True)
        basic_mistakes = OpenRouterAPITool.read_file(basic_mistakes_path, False, "")
        task_description = OpenRouterAPITool.read_file(task_description_path, False, "")
        task_code = OpenRouterAPITool.read_file(task_code_path, False, "")
        task_mistakes = OpenRouterAPITool.read_file(task_mistakes_path, False, "")
        # pokud jsou task_mistakes, tak je pripojim k basic_mistakes
        if task_mistakes:
            if basic_mistakes:
                basic_mistakes += "\n\n" + task_mistakes
            else:
                basic_mistakes = task_mistakes
        # pokud jsou basic_mistakes, tak je pripojim k system_prompt
        if basic_mistakes:
            system_prompt += "\n\n" + basic_mistakes
        # vracim jako tuple - udava poradi
        return system_prompt, task_description, task_code


    @staticmethod
    def create_api_messages_v1(system_prompt, student_solution, task_description="", task_code="", print_info=False):
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
            "content": system_prompt
        })
        # zadani tasks
        if task_description:
            messages.append({
                # zadani je prvni "user" prompt !!
                "role": "user",
                "content": f"ZADÁNÍ ÚLOHY:\n{task_description}"
            })
        # vychozi kod
        if task_code:
            messages.append({
                # vychozi kod ze zadani je druhy "user" prompt !!
                "role": "user",
                "content": f"VÝCHOZÍ KÓD (student jej měl k dispozici):\n```csharp\n\n{task_code}\n```"
            })
        # odevzdane reseni studenta
        messages.append({
            # reseni je dalsi "user" prompt !!
            "role": "user",
            "content": f"ODEVZDANÉ ŘEŠENÍ STUDENTA:\n```csharp\n\n{student_solution}\n```"
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

    @staticmethod
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


    @staticmethod
    def analyze_with_openrouter(messages, api_url, api_key, ai_model="google/gemini-2.0-flash-exp:free"):
        '''
        Odesle zpravy do OpenRouter API.
        :param messages: Jednotlive zpravy pro API.
        :param api_url: URL pro OpenRouter API.
        :param api_key: Klic pro OpenRouter API.
        :param selected_model: Zvoleny model v OpenRouter. (def.="google/gemini-2.0-flash-exp:free")
        :return: 
        '''

        if not api_key:
            raise ValueError("OpenRouter API key is not set in environment variable.")

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

        # hlavicky pozadavku
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        # struktura dat pro hodnoceni uloh
        payload = {
            "model": ai_model,
            "messages": messages
        }
        # odeslani pozadavku na OpenRouter API
        response = requests.post(api_url, json=payload, headers=headers)
        # klasicke vyvolani vyjimky pro chybne status kody (4xx a 5xx)
        # response.raise_for_status()
        # chci po svem - status 200 je OK, 4xx a 5xx jsou chyby
        if response.status_code != 200:
            # vytvorim vlastni vyjimku a vlozim do ni response a text odpovedi
            myException = HTTPError(f"OpenRouter API returned error status code: {response.status_code}, response: {response.text}")
            myException.response = response
            raise myException

        # TODO
        # OpenRouter API returned error status code: 402, response: {"error":{"message":"Provider returned error","code":402,"metadata":{"raw":"{\"error\":\"API key USD spend limit exceeded. Your account may still have USD balance, but this API key has reached its configured USD spending limit.\"}","provider_name":"Venice","is_byok":false}},"user_id":"user_38cI8OQTeKUVTmJuZYkYYaHGntW"}

        # Analyzing with via OpenRouter...
        # {'error': {'code': 402,
        #            'message': 'Provider returned error',
        #            'metadata': {'is_byok': False,
        #                         'provider_name': 'Venice',
        #                         'raw': '{"error":"API key USD spend limit exceeded. '
        #                                'Your account may still have USD balance, but '
        #                                'this API key has reached its configured USD '
        #                                'spending limit."}'}},
        #  'user_id': 'user_38cI8OQTeKUVTmJuZYkYYaHGntW'}
        # {'error': {'code': 402,
        #            'message': 'Provider returned error',
        #            'metadata': {'is_byok': False,
        #                         'provider_name': 'Venice',
        #                         'raw': '{"error":"API key USD spend limit exceeded. '
        #                                'Your account may still have USD balance, but '
        #                                'this API key has reached its configured USD '
        #                                'spending limit."}'}},
        #  'user_id': 'user_38cI8OQTeKUVTmJuZYkYYaHGntW'}
        # Traceback (most recent call last):
        #   File "OpenRouterAPITool.py", line 292, in <module>
        #     main()
        #   File "OpenRouterAPITool.py", line 287, in main
        #     write_file(output_file, analysis)
        # NameError: name 'write_file' is not defined

        # zpracovani odpovedi
        result = response.json()

        return result
    

    @staticmethod
    def process_openrouter_response(result_json):
        '''
        Zpracuje odpoved z OpenRouter API.
        :param response: Odpoved z OpenRouter API.
        :return: Zpracovana odpoved.
        '''
        # mam obsah odpovedi s textovou odpovedi
        if ("choices" in result_json and len(result_json["choices"]) > 0
                and "message" in result_json["choices"][0]
                and "content" in result_json["choices"][0]["message"]):
            # vyjmu odpoved
            result_content = result_json['choices'][0]['message']['content']
        else:
            # pokud nemam, tak vratim vystup prevedeny na JSON
            result_content = json.dumps(result_json, ensure_ascii=False, indent=4, sort_keys=False);

        return result_content

    @staticmethod
    def perform_one_whole_analysis(
            openrouter_api_url,
            openrouter_api_key,
            openrouter_api_ai_model,
            msg_supervisor_file_path,
            msg_basic_mistakes_file_path,
            msg_task_description_file_path,
            msg_task_code_file_path,
            msg_task_mistakes_file_path,
            msg_student_code_file_path,
            output_dir = "tmp_dir",
            output_message_for_api_json_file_name_part = "tmp_messages_for_api",
            output_response_from_api_json_file_name_part = "tmp_response_from_api",
            output_analysis_results_file_name_part = "analysis_results",
            encodings = "utf-8-sig"
        ):
        # ulozim si soucasny datetime pro oznaceni
        dateString = datetime.now().strftime("%Y%m%d_%H%M%S")

        # nactu zakladni prompty pro API
        system_prompt, task_description, task_code = OpenRouterAPITool.load_basic_prompts(
            msg_supervisor_file_path,
            msg_basic_mistakes_file_path,
            msg_task_description_file_path,
            msg_task_code_file_path,
            msg_task_mistakes_file_path
        )
        # nactu kod studenta
        students_code = OpenRouterAPITool.read_file(msg_student_code_file_path)  # mela 5 bodu

        # slozim zpravy pro API
        print("Creating API message...")
        # V1: nema uveden typ vstupu, vsechno je text
        # messages = OpenRouterAPITool.create_api_messages_v1(system_prompt, students_code, task_description, task_code, True)
        # V2: kazda zprava ma urcen typ vstupu "text"
        messages = OpenRouterAPITool.create_api_messages_v2(
            system_prompt, students_code, task_description, task_code, True
        )

        # pprint.pprint(messages)
        # ulozim zpravy pro API do JSON souboru (jen pro kontrolu),
        # jen pokud mam nazev
        if output_message_for_api_json_file_name_part:
            tmpName = dateString +"_"+ output_message_for_api_json_file_name_part +".json"
            tmpName = os.path.join(output_dir, tmpName)
            with open(tmpName, "w", encoding=encodings) as f:
                json.dump(messages, f, ensure_ascii=False, indent=4, sort_keys=False)

        # exit()

        # volam OpenRouter API pro analyzu
        counter = 1
        limit = 5
        while counter <= limit:
            print("Analyzing with via OpenRouter...")
            try:
                result = OpenRouterAPITool.analyze_with_openrouter(messages, openrouter_api_url, openrouter_api_key, openrouter_api_ai_model)

            except HTTPError as e:
                # pri techto chybach chci pozadavek opakovat
                # 429 - too many requests
                # 402 - payment required (prekroceny limit, ale muze byt i u free modelu)
                if e.response.status_code == 429 or e.response.status_code == 402:
                    # pokud je to chyba 429 (too many requests), tak pockam a zkusim to znovu
                    if e.response.status_code == 429:
                        print(f"Error: Too many requests (429). Retrying...")
                    elif e.response.status_code == 402:
                        print(f"Error: Payment required / quota exceeded (402). Retrying...")
                    # pockam pred dalsim pokusem
                    tmp_sleep_time = 60
                    print(f"Waiting for {tmp_sleep_time} seconds before retrying... [{counter}/{limit}] \n")
                    counter += 1
                    sleep(tmp_sleep_time)
                    continue
                # pokud je jina chyba, tak ukocim aplikaci
                else:
                    print("Error while calling OpenRouter API:")
                    print(e.response.status_code)
                    print(e)
                    return
            # pokud jsem dosel az sem, tak mam vysledek analyzy
            break

        # ulozim odpoved pro kontrolu do JSON souboru
        tmpName = dateString +"_"+ output_response_from_api_json_file_name_part +".json"
        tmpName = os.path.join(output_dir, tmpName)
        with open(tmpName, "w", encoding=encodings) as f:
            json.dump(result, f, ensure_ascii=False, indent=4, sort_keys=False)

        # zpracovani odpovedi
        analysis = OpenRouterAPITool.process_openrouter_response(result)
        # pprint.pprint(analysis)

        # doplnim do vystupu info o nastaveni analyzy
        analysis = openrouter_api_ai_model + "\n" + msg_student_code_file_path + "\n\n" + analysis

        # ulozim analyzu do markdown souboru
        # pripona je datum a cas ulozeni
        tmpName = dateString +"_"+ output_analysis_results_file_name_part +".md"
        tmpName = os.path.join(output_dir, tmpName)
        OpenRouterAPITool.write_file(tmpName, analysis)
        print(f"Analysis saved to: {tmpName}")


############################################################
# Ukazka pouziti

def main():
    import pprint

    ##############
    # nastaveni

    # zakladni nastaveni pro OpenRouter API
    OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
    # volba modelu
    # OPENROUTER_API_AI_MODEL = "google/gemini-2.0-flash-exp:free" # msg-V1 # tento uz je bohuzel placeny
    # OPENROUTER_API_AI_MODEL = "meta-llama/llama-3.3-70b-instruct:free" # msg-V1
    # OPENROUTER_API_AI_MODEL = "meta-llama/llama-3.2-3b-instruct:free" # msg-V1

    print("POZOR: PLACENY MODEL !!!")
    # OPENROUTER_API_AI_MODEL = "google/gemini-2.5-flash-lite" # msg-V2 # cena $0.10/0.40
    OPENROUTER_API_AI_MODEL = "google/gemini-2.0-flash-001" # msg-V2 # cena $0.10/0.40
    # OPENROUTER_API_AI_MODEL = "openai/gpt-4o-mini" # msg-V2 # cena $0.15/0.60

    # nacteni klice z .env souboru - musi byt instalovan dotenv
    import dotenv
    dotenv.load_dotenv()
    # nactu spravny klic
    key_location = os.environ.get("OPENROUTER_API_KEY_VAR_NAME", "not_set")
    OPENROUTER_API_KEY = os.environ.get(key_location, None)


    # nastaveni cest k souborum s prompty apod.
    msg_path_prefix = "../../"
    MSG_SUPERVISOR_FILE_PATH = msg_path_prefix + "meta/global/supervisor_prompt.md"
    MSG_BASIC_MISTAKES_FILE_PATH = msg_path_prefix + "meta/global/caste_chyby.md"
    MSG_TASK_DESCRIPTION_FILE_PATH = msg_path_prefix + "meta/tasks/01/textove_zadani.md"
    MSG_TASK_CODE_FILE_PATH = msg_path_prefix + "meta/tasks/01/kod_zadani.md"
    MSG_TASK_MISTAKES_FILE_PATH = msg_path_prefix + "meta/tasks/01/caste_chyby.md"

    # cesta k souboru studenta
    MSG_STUDENT_CODE_FILE_PATH = msg_path_prefix + "ukázky/Romova.cs"  # mela 5 bodu
    # MSG_STUDENT_CODE_FILE_PATH = msg_path_prefix + "ukázky/Vlach.cs"  # mel 2.5 bodu

    ##############
    # vykonani

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
        MSG_STUDENT_CODE_FILE_PATH,
        output_dir = "tmp_dir",
        output_message_for_api_json_file_name_part = "tmp_messages_for_api",
        output_response_from_api_json_file_name_part = "tmp_response_from_api",
        output_analysis_results_file_name_part = "analysis_results"
    )

    print("Done.")


if __name__ == "__main__":
    main()
