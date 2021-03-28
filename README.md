# IRRADROOM01
Systém byl vyvinut firmou [UST.cz](www.ust.cz)


# Návod k použití
_Uživatel zařízení by měl vždy postupovat podle tohoto návodu a neměl by zařízení nechávat bez dozoru nebo k němu pouštět uživatele neseznámené s touto příručkou._

## Popis zařízení
Řidící systém ozařovny IRRADROOM01 slouží pro ovládání zařízení umístěných v ozařovně [ODZ ÚJF AV ČR](http://www.ujf.cas.cz/cs/oddeleni/oddeleni-dozimetrie-zareni/). Systém se skládá z následujících komponent:

 * Řídící počítač
 * Ovládací terminál u vstupních dveří
 * Webové rozhraní pro přípravu experimentů
 * Stínící krabice s dvojicí zářičů
 * Motorový mechanizmus pro vytažení zářiče ze stínící krabice
 * Čtyřmístný display pro zobrazení vzdálenosti stolu pro vzorky
 * Senzor zavřených vstupních dveří
 * Senzor polohy zdrojů (zářičů)

Cílem celého systému je zbezpečnit a zjednodušit práci s ozařovnou a jejím vybavením. Cílem je, aby kdokoliv nemohl otevřít zářič nebo ho nechat vytáhnutý ze stínící krabice. 
Systém funguje tak, že uživatel si ve webovém prostředí přípraví program. K němu si vygeneruje pin pro jedno spuštění programu. Následně zkontroluje umístění vzorku v ozařovně, vyloučí přítomnost osob v místnosti a z terminálu u vstupních dveří spustí program, který se postupně vykoná. 


## Webové rozhraní


### Tvorba nových užívatelů. 



## Terminál

Terminál je zařízení vybavené dotykovou obrazovkou sloužící k základnímu zobrazení stavu systému a pro spouštění jednotlivých běhů programů. Terminál je umístěn u vstupních dveří do ozařovny. Tak, aby uživatel viděl, jestli vstup do místnosti je bezpečný a aby při spouštění programu mohl zkontrolovat, jestli se v místnosti nikdo nenachází. 

Na vrchní straně terminálu se vždy nachází název zařízení, který je zároveň tlačítkem pro znovu-načtení stránky. To může být řešením některých technických potíží. Během běžného provozu by nemělo být používáno. 

Za názvem zařízení je kroužek, který ukazuje stav připojení terminálu k řídícímu počítači. Prázdný kroužek zobrazuje nezinicializovaný terminál. Pokud je v kroužku křížek, tak byl terminál odpojený nebo se nedokázal přípojit k řídícímu počítačí. Kroužek s fajfkou zobrazuje připojený terminál. 

Následuje aktuální čas terminálu a v pravé časti jsou tři tlačítka, která 



### Domů
Úvodní stránka terminálu poskytuje přehled o stavu dílčích částí systému. 

![Domaci stranka terminalu](https://github.com/UniversalScientificTechnologies/IRRADROOM01/blob/IRRADROOM01A/doc/terminal_home.png)

##### Pogram
Popisuje, jestli je v zařízení spuštěný nějaký program nebo ne. V případě, že program běží, tlačítko je zelené a je tam napsán aktuální krok programu. 

##### Zářič
Ukazuje v jakém poloze je umístěn zářič. Díky tomu uživatel pozná, jestli je bezpečné do místnosti vstoupit nebo ne. 

##### Dveře
Stav vstupních dveří. Červený panel ukazuje otevřený stav. 

##### Vzdálenost stolu
Zobrazuje aktuální vzdálenost lavice se vzorky od zářiče. 


### Program
Záložka  program  slouží ke spuštění programu na základě pinu, který uživatel získá ve webovém rozhraní. V základním stavu je v této záložce zobrazená pouze klávesnice pro zadání pinu. Klávesnice je vybavena dvojicí dodatkových tlačítek. Červené tlačítko slouží ke smazání posledního znaku. Zelené tlačítko slouží pro odeslání pinu. Pokud je pin správný, otevře se náhled programu tohoto pinu. V jiném případě je zobrazena chybová hláška o nenalezeném programu. 

![terminalu](https://github.com/UniversalScientificTechnologies/IRRADROOM01/blob/IRRADROOM01A/doc/terminal_program_1.png)


V druhém kroku se vám zobrazí přehled zvolného programu. Je zde zobrazený název programu. Jeho autor a autor spuštění programu. Dále odhad času a jednotuvé kroky. 
![terminalu](https://github.com/UniversalScientificTechnologies/IRRADROOM01/blob/IRRADROOM01A/doc/terminal_program_2.png)

V pravém sloupci pak vidíte samotý průběh programu. 
![terminalu](https://github.com/UniversalScientificTechnologies/IRRADROOM01/blob/IRRADROOM01A/doc/terminal_program_3.png)

### O zařízení
V poslední záložce terminálu uživatel nalezne popis terminálu a QR kód s odkazem a tento návod. 



## Tenchniké detaily
### Řidící počítač

* Odroid C2
* Ubuntu 20.04.4 minimal ()
* ROS 2 Foxy; Debain binaries (https://index.ros.org/doc/ros2/Installation/Foxy/Linux-Install-Debians/)
  * ros-foxy-ros-base
* `sudo apt install git htop nano mc python3-colcon-common-extensions   `
* `pip3 install serial tornado pymongo  `
* Pymlab, i2c-tools (fork)
* Create ROS2 WS
* Setup enviroment
* `export ROS_DOMAIN_ID=35`
* Install `rosbridge_server` (from git; branch `ros2`)

### Schéma zařízení
![Schéma zařízení](https://github.com/UniversalScientificTechnologies/IRRADROOM01/blob/IRRADROOM01A/doc/irradroom_schema.png)

#### ROS 2
Jako základní framework je použit ROS2. Domain ID je nastaveno na 35 v `~/.bashrc`.
