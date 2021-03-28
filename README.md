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

Terminál slouží k základnímu zobrazení stavu systému a pro spouštění jednotlivých běhů programů. Terminál je umístěn u vstupních dveří do ozařovny. Tak, aby uživatel viděl, jestli vstup do místnosti je bezpečný a aby při spouštění programu mohl zkontrolovat, jestli se v místnosti nikdo nenachází. 


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


#### ROS 2
Jako základní framework je použit ROS2. Domain ID je nastaveno na 35 v `~/.bashrc`.
