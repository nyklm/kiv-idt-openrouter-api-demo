
# Zadání
* doplňte třídu Plan reprezentující konkrétní rozvrh doučovacích hodin. Třída bude obsahovat jako atribut pole referencí na instance třídy PlanEvent reprezentující jednotlivé položky rozvrhu.
* doplňte konstruktor třídy Plan přebírající existující pole nabídek.
* doplňte metodu bool IsConflict() testující, zda existuje mezi kterýmikoli dvěma položkami rozvrhu konflikt (použijte metodu isInConflict třídy PlanEvent).
* doplňte metodu bool IsOK() testující, zda se v daném rozvrhu vyskytují alespoň tři doučování matematiky a alespoň dvě doučování informatiky, a zároveň všechny termíny matematiky probíhají v různých dnech a všechny termíny informatiky probíhají v různých dnech.

* doplňte načtení nabídek ze souboru. Každá nabídka je na pěti řádcích v následujícím pořadí:
  * jméno tutora,
  * doučovaný předmět,
  * den v týdnu (číslo 0-4),
  * začátek (číslo reprezentující hodinu),
  * konec (číslo reprezentující hodinu).
* doplňte metodu vytvářející všechny možné kombinace pěti nabídek. Pro každou pětici vytvořte instanci třídy Plan a otestujte, zda je vzniklý rozvrh v pořádku (IsOK) a bezkonfliktní (IsConflict). Správné a bezkonfliktní rozvrhy vypište v rozumném formátu do konzole.
* otestujte program na datech v souboru ssc.txt, který je k dispozici ke stažení na webu courseware a nakonec vypište počet nalezených správných a bezkonfliktních rozvrhů.

## Požadované funkce
* Konstruktor Plan přejímá pole eventů PlanEvent.
* isConflict() vrací true, pokud existuje mezi kterýmikoli dvěma položkami rozvrhu konflikt.
* isOK() vrací true, pokud se v daném rozvrhu vyskytují
  * alespoň tři doučování matematiky,
  * alespoň dvě doučování informatiky, 
  * a zároveň všechny termíny matematiky probíhají v různých dnech a všechny termíny informatiky probíhají v různých dnech.