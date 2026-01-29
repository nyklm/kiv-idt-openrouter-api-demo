
# Využití AI pro automatizované hodnocení kódu studentů v KIV/IDT

- AI pro KIV (Jakub Sido) - https://docs.google.com/document/d/17zUVPaYPc_7ls-EphV34u-836Lavl5enG07fOBhSTy0/edit?usp=drive_link
- Ukázka kódu (Jakub Sido) - https://github.com/JakubSido/llm-api-demo-base


- **main.py** - Aplikace pro opravu studentských úloh.
- **openrouter_key_info.py** - Poskytne informace o využití kreditu.


- **Klíč k OpenRouter API** od KIV pro KIV/IDT poskytne M.N. na požádání, 
ale pro prvotní testy stačí vytvořit vlastní klíč (pouze nesmíte nastavit limit 0) 
a používat free modely.


## Obecné postupy a doporučení

* Používat Markdown pro formátování textu promptu.
* Každý blok promptu musí začínat popisem, co je jeho obsahem (zadání úlohy, výchozí kód, odevzdané řešení).
  * **system prompt** je vhodné mít jeden:
    * nastavení modelu, jak se má chovat.
    * normativni pravidlo - ma nejvyssi prioritu.
    * jak ma hodnotit, jakym zpusobem ma odpovidat a format odpovedi.
  * **user prompt** je vícekrát dle potřeby:
    * zadání úlohy,
    * výchozí kód,
    * odevzdané řešení.
  

* Tímto způsobem by měl být formátován vstup do OpenRouter API pro hodnocení kódu studenta:
```
  {
    "role": "system",
    "content": "Jsi učitel C#. Hodnoť podle pravidel…"
  },
  {
    "role": "user",
    "content": "ZADÁNÍ ÚLOHY:\nPopis problému, požadavky, omezení…"
  },
  {
    "role": "user",
    "content": "VÝCHOZÍ KÓD (student jej měl k dispozici):\n```csharp\n...\n```"
  },
  {
    "role": "user",
    "content": "ODEVZDANÉ ŘEŠENÍ STUDENTA:\n```csharp\n...\n```"
  }
```

* System prompt by měl být jen jeden a měl by obsahovat jasná pravidla hodnocení.
  * ChatGPT dokáže tento promt zajímavě navrhnout a doplnit.
```
Jsi učitel C#.

### Pravidla hodnocení
- …

### Kritéria
- …

### Bodování
- …

### Formát odpovědi
- vrať JSON
- dodrž přesně strukturu
```


## Poznámky:
- Je vhodné se s nastavením seznámit třeba přes ChatGPT a nechat si vysvětlit následující (otázky si rozšiřte, tady jen stručně):
  - rozdíl mezi system a user promptem.
  - dát mu popis ze supervisor_prompt.md a nechat si vysvětlit, jak by měl být prompt strukturován.
  - rozdíl mezi normálním a přísným učitelem.
  - má smysl dávat do system prompt časté chyby? (zajímavé je, že ano, ale pokud špatně, tak problém)
  - 