# First IPP 23/24 course project. Simple parser in python 3.10

Documentation of Project Implementation for IPP 2023/2024 \
Name and surname: Kirill Shchetiniuk\
Login: xshche05

# Documentation for task #1 (parse.py)
As a task we have to implement simple **IPPcode24** (assembly like language) parser. As an input we gets data from *stdin*, analyze input code according to basic syntax rules of provided language. Parser validates header in input code (got expected header and header got before instructions), validates opcodes according to opcode lexical form and existence of this particular instruction opcode in instruction set, next we validate instruction's arguments according to the described instruction's syntax. As a last thing we transform a valid code to the XML form, provided by the task, and out doc to *stdout*. In case of errors script returns exit code according to errors described in the task. 

## Getting the data
In the beginning of each script run, script reads input using the `Reader` instance, which is defined to use *stdin* as input data stream. `Reader` also provide a method to convert input to the list of particular lines of code.
## Input data parsing
After reading of all data from input stream, script initialize a `Parser` object, which accepts a list of lines during initialization. To start parsing, script calls `parse()` method provided by `Parser` class.
### Accepted instruction set
Parsing in the beginning of the module has an initializing of `InstructionSet` object, which is provided for easy  registration/addition of acceptable instructions. `register_header()` method is defines language header, `register_opcode()` defines particular instructions with their argument syntax. In general `InstructionSet` provides an easy interface to adding new instructions and editing instructions' configuration.
### Looking for a header
Each parsing run begins with looking for a header, in case of comments before the header they are just removed. In case of something except header and comments parser raises an error with code  `21`. In case of header we change `look_for_header` flag and begin a new iteration.
### Removing comments
In case of appearing of comment in some line, script remove the comment and increase comment counter by 1 and begin a new iteration
### Parsing instructions
Instruction parsing is simply validation instruction parts and building an instruction using the `InstructionBuilder`
#### Opcode parsing
In case if after the removing comment we don't get an empty line, we continue current iteration with instruction parsing. First of all, we splits opcode form instruction arguments, next check if opcode is presented in instruction set and continue current iteration, otherwise we raises an error with code `22` in case of opcode kind string and `23` otherwise. 
#### Argument parsing
Argument parsing is simply adding an argument string to argument list of instruction builder, for later validation.
#### Argument validation
After finishing instruction building (setting instruction order an running the `build()` method of `InstructionBuilder`) we simply runs `validate()` method of `Instruction` class. This method simply looks every possible type of each argument and checks if one of this types is corresponding to expected argument type. In case none corresponding types, parser raises an exception with code `23`.
#### Instruction final
After all validations, instructions is being added to instruction flow of `Program` object.

## Data output
After parsing using the `parse()` method of `Parser` class, method returns an `Program` object. `Program` object simply serializes using property `xml_string`, which is recursively gets an XML nodes of instruction and arguments.

## Extensions
Here would be described implemented extensions such as `STATP` and `NVP`

### STATP
This extension is implemented using custom argument parser and `Program` object methods. During argument parsing form different statistic groups according to user command line arguments.

During parsing, parser affects statistics counters in program object such as comment counter. Adding an instruction to instruction flow of program also affects internal counters, which changes according to instruction that was added.

Every stat group is a fishbone for statistic out, after parsing finishing, this fishbone is filled with values and prints to the provided file.

Extension could produce more than one file at the same time, but do not allow to print different stat groups to one file.

### NVP
Full script is written according to OOP principles, most of implemented classes is also use python magic methods such as `__str__`, `__eq__` for better implementing different limitations and validity checks. Script uses different module-files, where which file contains logic for corresponding thing. The main entry point is located in `parse.py` file, and from this point all other modules are called.

For implementation was used one of the design patterns such as **Builder Pattern** which is supposed to help to build complex objects such as `Instruction` (builds by using `InstructionBuilder`) and `Prorgam` (builds by using `Parser`)


# Final results

Následující procentuální hodnocení je FINÁLNÍ hodnocení Vaší úlohy č. 1.

Projekt byl nejdříve rozbalen a následně spuštěn s řadou hodnotících testů.
Testy jsou rozděleny do několika kategorií. Podle výsledků
jednotlivých testů byla stanovena procentuální úspěšnost Vašeho skriptu
v jednotlivých kategoriích a z těchto hodnot odvozeny body.
Do StudIS se importují body zaokrouhlené na jedno desetinné místo.
Testovací příklady nebudou uveřejněny.

Hodnocení je individuálně vygenerováno pro každého studenta, doplněno o ručně vložené připomínky a následně
automaticky rozesláno na školní e-mail.

Hodnocené části (nehodnocené části jsou vynechány):
 1) Automatické testy parse.php - základní.
 2) Automatické testy parse.php - registrovaná rozšíření (uvedená ve vašem souboru rozsireni).
 3) Manuální hodnocení rozšíření NVP (komentář je uveden u komentářů k dokumentaci).
 4) Případné malusy a bonusy (pozdní odevzdání, opravy zadání, ...).
 5) Hodnocení dokumentace readme1(.pdf/.md) a štábní kultury zdrojových kódů (především komentářů). Za bodovým hodnocením dokumentace je v závorkách 30% korelace vzhledem k hodnocení z části 1).


 Ad 5) Následuje seznam zkratek, které se mohou vyskytnout v komentářích k hodnocení dokumentace a štábní kultury skriptů:
Vysvětlivky zkratek v dokumentaci:
  CH = pravopisné chyby, překlepy
  FORMAT = špatný formát vzhledu dokumentu (nedodrženy požadavky)
  SHORT = nesplňuje minimální požadavky na délku či obsah
  STRUCT = nevhodně strukturováno (např. bez nadpisů)
  MISSING = dokumentace nebyla odevzdána (nebo chybí její významná část)
  COPY = text obsahuje úryvky ze zadání nebo cizí necitované materiály
  STYLE = stylizace vět, nečitelnost, nesrozumitelnost
  NOOOP = chybí použítí objektově orientovaného paradigma, příp. funkce jen zabaleny do jedné/dvou tříd
  NOSRP = špatná/nešikovná aplikace principu jedné zodpovědnosti pro každou metodu, příp. příliš dlouhá těla metod
  BADUML = chybějící, neodpovídající nebo syntakticky chybný UML diagram tříd
  EXT = nešikovný/nesmyslný nebo zcela chybějící popis rozšiřitelnosti vašeho návrhu
  BADDP = nevhodné využití návrhového vzoru, nebo zcela špatná/chybějící implementace jinak dokumentovaného návrhového vzoru
  COMMENT = chybějící nebo nedostatečné komentáře ve zdrojovém textu
  FILO = nedostatečná filosofie návrhu (abstraktní popis struktury programu, co následuje za čím)
  JAK/HOW = technicky nedostatečný popis řešení
  CONTENT = nevhodný obsah (popis časového průběhu řešení, vyjadřování pocitů, irelevantních myšlenek a nepodložených názorů)
  SRCFORMAT = opravdu velmi špatná štábní kultura zdrojového kódu
  SPACETAB (jen pro informaci) = kombinování mezer a tabelátorů k odsazování zdrojového textu
  DECOMPOSE     = skript není vůbec/dostatečně dekomponován na funkce (příp. třídy a metody), nešikovné opakování regulárních výrazů
  AUTHOR (jen pro informaci) = ve skriptu chybí jméno (login) autora
  LANG = míchání jazyků (většinou anglické termíny v českém textu)
  HOV = hovorové nebo nevhodné slangové výrazy
  FORM = nepěkná úprava, nekonzistentní velikost a typ písma apod.
  TERM = problematická terminologie (neobvyklá, nepřesná či přímo špatná) včetně terminologie OOP v Pythonu (objekty, třídy, metody, instanční proměnné/atributy, dědičnost tříd, nikoli objektů apod.)
  IR = nedostatečně popsaná vnitřní reprezentace (např. pro paměť, sekvenci instrukcí apod.)
  PRED (jen pro informaci) = pozor na osamocené neslabičné předložky na konci řádků
  BLOK (jen pro informaci) = chybí zarovnaní do bloku místo méně pěkného zarovnání na prapor (doleva)
  KAPTXT (jen pro informaci) = mezi nadpisem a jeho podnadpisem by měl být vždy nějaký text
  MEZ (jen pro informaci) = za otevírající nebo před zavírající závorku mezera nepatří, případně další prohřešky při sazbě mezer
  ICH (jen pro informaci) = ich-forma (psaní v první osobě jednotného čísla) není většinou vhodná pro programovou dokumentaci
  SAZBA (jen pro informaci) = alespoň identifikátory proměnných a funkcí se patří sázet písmem s jednotnou šířkou písmen (např. font Courier)
  NVP, EX = smysluplné a dokumentované využití objektového paradigmatu, návrhových vzorů (rozšíření NVP), nebo výjimek
  NVPDOC = použití návrhového vzoru nebylo (dostatečně) dokumentováno/zdůvodněno
  OK = k dokumentaci byly nanejvýše nepodstatné připomínky


Osobní reklamace budou primárně v pondělí 8. 4. 2024 10:00-11:30 v C229. Je možné vést reklamaci i přes e-mail, což budu vyřizovat dle časových možností (krivka@fit.vut.cz a !!v odpovědi zachovejte i text tohoto e-mailu!!).


Vaše hodnocení části 1): 6,02 bodů
Vaše hodnocení části 2): 1,41 bodů
Vaše hodnocení části 3): 1,00 bodů
  Komentář hodnocení části 3):
Vaše hodnocení části 5): 0,90 bodů (po 50% korelaci 0,90 bodů)
  Komentář hodnocení části 5) (srážky uváděny v minibodech, 1 bod = 100 minibodů): AUTHOR, CH (-10), NVP (+100)

Pokud jste obdrželi výsledek částí 1) mimo hodnotící interval, tak
bude oříznut, tak že získáte za implementaci alespoň 0 a ne více jak maximum bodů za daný skript.

Dekomprimace archivu proběhla úspěšně.

Procentuální hodnocení jednotlivých kategorií skriptu parse.py:
Lexikální analýza (detekce chyb): 94 %
Syntaktická analýza (detekce chyb): 100 %
Zpracování instrukcí (včetně chyb): 99 %
Zpracování netriviálních programů: 87 %
Rozšíření STATP 94 %
Celkem bez rozšíření: 97 %
