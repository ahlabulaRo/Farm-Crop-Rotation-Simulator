#!/usr/bin/env python3
"""
Script de verificare pentru Tema 2 - Simulare Ferma

Verifica daca fisierul de output este valid pe baza fisierului de input.
"""

import sys
import os

# Schimbă directorul de lucru la rădăcina proiectului
os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Coduri culori ANSI
VERDE = '\033[92m'
ROSU = '\033[91m'
GALBEN = '\033[93m'
RESET = '\033[0m'


class Leguma:
    def __init__(self, nume, timp_cultivare, cost, pret_vanzare):
        self.nume = nume
        self.timp_cultivare = timp_cultivare
        self.cost = cost
        self.pret_vanzare = pret_vanzare


class Patrat:
    def __init__(self):
        self.ocupat = False
        self.leguma_plantata = None
        self.zi_plantare = -1
        self.ultima_leguma_culesa = None
        self.zi_ultima_culegere = -1


class Ferma:
    def __init__(self):
        self.L = 0
        self.zile = 0
        self.bani_initiali = 0
        self.bani_curent = 0
        self.N = 0
        self.M = 0
        self.legume = {}  # dict: nume -> Leguma
        self.rotatii = {}  # dict: nume_leguma -> lista de legume dupa care poate fi plantata
        self.patrate = []  # matrice L x L
        self.erori = []


def citeste_input(nume_fisier):
    """Citeste fisierul de input si construieste starea initiala a fermei."""
    ferma = Ferma()
    
    with open(nume_fisier, 'r') as f:
        # Prima linie: L L ZILE BANI N
        linie = f.readline().strip().split()
        ferma.L = int(linie[0])
        ferma.zile = int(linie[2])
        ferma.bani_initiali = int(linie[3])
        ferma.bani_curent = ferma.bani_initiali
        ferma.N = int(linie[4])
        
        # Initializeaza matricea de patrate
        ferma.patrate = [[Patrat() for _ in range(ferma.L)] for _ in range(ferma.L)]
        
        # Citeste legumele
        for _ in range(ferma.N):
            linie = f.readline().strip().split()
            nume = linie[0]
            timp = int(linie[1])
            cost = int(linie[2])
            pret = int(linie[3])
            ferma.legume[nume] = Leguma(nume, timp, cost, pret)
        
        # Citeste rotatiile
        linie = f.readline().strip().split()  # ROTATIE M
        ferma.M = int(linie[1])
        
        for _ in range(ferma.M):
            linie = f.readline().strip().split()
            leguma = linie[0]
            dupa_leguma = linie[1]
            
            if leguma not in ferma.rotatii:
                ferma.rotatii[leguma] = []
            
            ferma.rotatii[leguma].append(dupa_leguma)
    
    return ferma


def parseaza_coordonate(coord_str):
    """Parseaza coordonatele din format 00x00 si returneaza (linie, coloana)."""
    parti = coord_str.split('x')
    linie = int(parti[0])
    coloana = int(parti[1])
    return linie, coloana


class VerificareEsuata(Exception):
    """Exceptie pentru oprirea verificarii la prima eroare."""
    def __init__(self, mesaj, numar_linie=None, continut_linie=None):
        self.mesaj = mesaj
        self.numar_linie = numar_linie
        self.continut_linie = continut_linie
        super().__init__(mesaj)


def verifica_leguma_exista(ferma, nume_leguma):
    """Verifica daca leguma exista in lista de legume definite."""
    if nume_leguma not in ferma.legume:
        raise VerificareEsuata(f"Leguma '{nume_leguma}' nu exista in lista de legume definite")
    return True


def verifica_zi_valida(ferma, zi):
    """Verifica daca ziua este in intervalul valid."""
    if zi < 1 or zi > ferma.zile:
        raise VerificareEsuata(f"Ziua {zi} este invalida (trebuie sa fie intre 1 si {ferma.zile})")
    return True


def verifica_coordonate_valide(ferma, linie, coloana):
    """Verifica daca coordonatele sunt in matricea fermei."""
    if linie < 0 or linie >= ferma.L or coloana < 0 or coloana >= ferma.L:
        raise VerificareEsuata(f"Coordonate invalide ({linie:02d}x{coloana:02d}), ferma este {ferma.L}x{ferma.L}")
    return True


def verifica_are_bani_plantare(ferma, nume_leguma):
    """Verifica daca are suficienti bani pentru a planta leguma."""
    cost = ferma.legume[nume_leguma].cost
    if ferma.bani_curent < cost:
        raise VerificareEsuata(f"Bani insuficienti pentru plantare {nume_leguma} (cost: {cost}, disponibil: {ferma.bani_curent})")
    return True


def verifica_patrat_liber(ferma, linie, coloana):
    """Verifica daca patratul este liber pentru plantare."""
    patrat = ferma.patrate[linie][coloana]
    if patrat.ocupat:
        raise VerificareEsuata(f"Patratul {linie:02d}x{coloana:02d} este deja ocupat cu {patrat.leguma_plantata}")
    return True


def verifica_poate_planta_initial(ferma, nume_leguma, linie, coloana):
    """Verifica daca leguma poate fi plantata intr-un patrat nefolosit (trebuie N/A)."""
    patrat = ferma.patrate[linie][coloana]
    
    # Daca patratul a fost folosit, nu aplicam aceasta regula
    if patrat.zi_ultima_culegere != -1:
        return True
    
    # Verifica daca leguma are N/A in rotatie
    if nume_leguma in ferma.rotatii:
        if 'N/A' in ferma.rotatii[nume_leguma]:
            return True
    
    raise VerificareEsuata(f"{nume_leguma} nu poate fi plantata in patrat nefolosit (nu are N/A in ROTATIE)")


def verifica_rotatie_culturi_identice(ferma, nume_leguma, linie, coloana, zi):
    """Verifica regula de rotatie culturi identice (nu poti planta aceeasi leguma imediat)."""
    patrat = ferma.patrate[linie][coloana]
    
    if patrat.ultima_leguma_culesa == nume_leguma:
        if zi - patrat.zi_ultima_culegere <= 2:
            raise VerificareEsuata(f"Nu poti planta {nume_leguma} in {linie:02d}x{coloana:02d} la ziua {zi} (culesa la ziua {patrat.zi_ultima_culegere}, trebuie sa astepti 3 zile)")
    
    return True


def verifica_rotatie_legume_prietenoase(ferma, nume_leguma, linie, coloana, zi):
    """Verifica daca leguma poate fi plantata dupa ultima leguma culesa."""
    patrat = ferma.patrate[linie][coloana]
    
    # Daca patratul nu a fost folosit, verificarea se face in alta functie
    if patrat.zi_ultima_culegere == -1:
        return True
    
    # Verifica daca a trecut cel putin o zi de la culegere
    if zi - patrat.zi_ultima_culegere < 1:
        raise VerificareEsuata(f"Nu a trecut cel putin o zi de la culegere in {linie:02d}x{coloana:02d}")
    
    # Verifica daca leguma poate fi plantata dupa ultima culesa
    if nume_leguma in ferma.rotatii:
        # Are N/A -> poate fi plantata dupa orice
        if 'N/A' in ferma.rotatii[nume_leguma]:
            return True
        
        # Verifica daca ultima leguma culesa e in lista de rotatii
        if patrat.ultima_leguma_culesa in ferma.rotatii[nume_leguma]:
            return True
    
    raise VerificareEsuata(f"{nume_leguma} nu poate fi plantata dupa {patrat.ultima_leguma_culesa} in {linie:02d}x{coloana:02d}")


def verifica_actiune_plantare(ferma, zi, linie, coloana, nume_leguma):
    """Verifica daca actiunea de plantare este valida."""
    # Verifica toate conditiile (ridica exceptie la prima eroare)
    verifica_leguma_exista(ferma, nume_leguma)
    verifica_coordonate_valide(ferma, linie, coloana)
    verifica_are_bani_plantare(ferma, nume_leguma)
    verifica_patrat_liber(ferma, linie, coloana)
    verifica_poate_planta_initial(ferma, nume_leguma, linie, coloana)
    verifica_rotatie_culturi_identice(ferma, nume_leguma, linie, coloana, zi)
    verifica_rotatie_legume_prietenoase(ferma, nume_leguma, linie, coloana, zi)
    
    # Executa plantarea
    patrat = ferma.patrate[linie][coloana]
    patrat.ocupat = True
    patrat.leguma_plantata = nume_leguma
    patrat.zi_plantare = zi
    ferma.bani_curent -= ferma.legume[nume_leguma].cost
    
    return True


def verifica_patrat_ocupat_culegere(ferma, linie, coloana):
    """Verifica daca patratul este ocupat pentru a putea culege."""
    patrat = ferma.patrate[linie][coloana]
    if not patrat.ocupat:
        raise VerificareEsuata(f"Nu poti culege din {linie:02d}x{coloana:02d}, patratul este gol")
    return True


def verifica_leguma_matura(ferma, linie, coloana, zi):
    """Verifica daca leguma este matura si poate fi culesa."""
    patrat = ferma.patrate[linie][coloana]
    
    leguma = ferma.legume[patrat.leguma_plantata]
    zile_trecute = zi - patrat.zi_plantare
    
    if zile_trecute < leguma.timp_cultivare:
        raise VerificareEsuata(f"{patrat.leguma_plantata} din {linie:02d}x{coloana:02d} nu este matura (plantata la zi {patrat.zi_plantare}, matura la zi {patrat.zi_plantare + leguma.timp_cultivare})")
    
    return True


def verifica_actiune_culegere(ferma, zi, linie, coloana):
    """Verifica daca actiunea de culegere este valida."""
    # Verifica toate conditiile (ridica exceptie la prima eroare)
    verifica_coordonate_valide(ferma, linie, coloana)
    verifica_patrat_ocupat_culegere(ferma, linie, coloana)
    verifica_leguma_matura(ferma, linie, coloana, zi)
    
    # Executa culegerea
    patrat = ferma.patrate[linie][coloana]
    leguma = ferma.legume[patrat.leguma_plantata]
    
    ferma.bani_curent += leguma.pret_vanzare
    patrat.ultima_leguma_culesa = patrat.leguma_plantata
    patrat.zi_ultima_culegere = zi
    patrat.ocupat = False
    patrat.leguma_plantata = None
    patrat.zi_plantare = -1
    
    return True


def verifica_suma_finala(ferma, suma_din_fisier):
    """Verifica daca suma finala calculata este corecta."""
    if ferma.bani_curent != suma_din_fisier:
        raise VerificareEsuata(f"Suma finala incorecta (calculat: {ferma.bani_curent}, in fisier: {suma_din_fisier})")
    return True


def verifica_output(fisier_input, fisier_output):
    """Functia principala de verificare a fisierului de output."""
    try:
        # Citeste input-ul
        ferma = citeste_input(fisier_input)
        
        # Citeste si proceseaza fisierul de output
        suma_finala_din_fisier = 0
        numar_linie = 0
        
        with open(fisier_output, 'r') as f:
            for linie in f:
                numar_linie += 1
                linie = linie.strip()
                if not linie:
                    continue
                
                # Verifica linia SUMA_FINALA
                if linie.startswith('SUMA_FINALA:'):
                    parti = linie.split(':')
                    suma_finala_din_fisier = int(parti[1].strip())
                    continue
                
                # Parseaza actiunea
                parti = linie.split()
                if len(parti) < 3:
                    raise VerificareEsuata(f"Linie invalida", numar_linie, linie)
                
                zi = int(parti[0])
                actiune = parti[1]
                coord_str = parti[2]
                
                try:
                    # Verifica ziua
                    verifica_zi_valida(ferma, zi)
                    
                    # Parseaza coordonatele
                    linie_coord, coloana_coord = parseaza_coordonate(coord_str)
                    
                    # Proceseaza actiunea
                    if actiune == "planteaza":
                        if len(parti) < 4:
                            raise VerificareEsuata(f"Actiune planteaza lipseste numele legumei")
                        
                        nume_leguma = parti[3]
                        verifica_actiune_plantare(ferma, zi, linie_coord, coloana_coord, nume_leguma)
                        
                    elif actiune == "culege":
                        verifica_actiune_culegere(ferma, zi, linie_coord, coloana_coord)
                        
                    else:
                        raise VerificareEsuata(f"Actiune necunoscuta: {actiune}")
                except VerificareEsuata as e:
                    # Adauga informatii despre linie la exceptie
                    raise VerificareEsuata(e.mesaj, numar_linie, linie)
        
        # Verifica suma finala
        verifica_suma_finala(ferma, suma_finala_din_fisier)
        
        # Verificare reusita
        print(f"\n{VERDE}✓ VERIFICARE REUSITA{RESET} 🎉")
        print(f"{VERDE}Fisierul este valid!{RESET}")
        print(f"Suma finala: {GALBEN}{ferma.bani_curent} RON{RESET}\n")
        return True
        
    except FileNotFoundError:
        print(f"\n{ROSU}✗ EROARE{RESET} ❌")
        print(f"{ROSU}Fisierul {fisier_output} nu a fost gasit!{RESET}\n")
        return False
    except VerificareEsuata as e:
        print(f"\n{ROSU}{'='*60}{RESET}")
        print(f"{ROSU}✗ VERIFICARE ESUATA{RESET} ❌\n")
        
        if e.numar_linie:
            print(f"{GALBEN}Linia {e.numar_linie}:{RESET}")
            print(f"  {e.continut_linie}\n")
        
        print(f"{ROSU}Eroare: {e.mesaj}{RESET}")
        print(f"{ROSU}{'='*60}{RESET}\n")
        return False
    except Exception as e:
        print(f"\n{ROSU}✗ EROARE{RESET} ❌")
        print(f"{ROSU}Eroare la procesare: {e}{RESET}\n")
        return False


def ruleaza_un_test(numar_test):
    """Ruleaza si verifica un singur test."""
    import subprocess
    
    fisier_input = f"teste/test{numar_test}.txt"
    fisier_output = f"teste/test{numar_test}.out"
    
    # Rulează programul
    try:
        subprocess.run(["./ferma", fisier_input, fisier_output], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print(f"{ROSU}✗ Eroare la rularea programului{RESET}")
        return False
    except FileNotFoundError:
        print(f"{ROSU}✗ Programul ./ferma nu a fost gasit! Ruleaza 'make' intai.{RESET}")
        return False
    
    # Verifică output-ul
    return verifica_output(fisier_input, fisier_output)


def citeste_limite_minime():
    """Citeste limitele minime de bani pentru fiecare test."""
    limite = []
    try:
        with open('teste/limite_minime.txt', 'r') as f:
            for linie in f:
                linie = linie.strip()
                if linie:
                    limite.append(int(linie))
        return limite
    except FileNotFoundError:
        # Daca nu exista fisierul, nu avem limite
        return []


def ruleaza_toate_testele(mod_quiet=False):
    """Ruleaza si verifica toate cele 18 teste."""
    import subprocess
    
    # Verifică dacă programul există
    if not os.path.exists("./ferma"):
        print(f"{ROSU}✗ Programul ./ferma nu a fost gasit! Ruleaza 'make' intai.{RESET}\n")
        return False, 0, 0, []
    
    # Citește limitele minime
    limite_minime = citeste_limite_minime()
    
    if not mod_quiet:
        print(f"\n{GALBEN}{'='*70}{RESET}")
        print(f"{GALBEN}           RULARE TESTE AUTOMATE - TEMA 2 FERMA{RESET}")
        print(f"{GALBEN}{'='*70}{RESET}\n")
    
    teste_trecute = 0
    teste_esuate = 0
    scoruri_teste = []  # Lista cu scorurile pentru fiecare test
    
    for i in range(1, 19):
        fisier_input = f"teste/test{i}.txt"
        fisier_output = f"teste/test{i}.out"
        
        # Verifică dacă fișierul de test există
        if not os.path.exists(fisier_input):
            print(f"  Test {i:2d}: {GALBEN}⊘ SKIP{RESET} (fișier lipsă)")
            continue
        
        # Rulează programul
        try:
            subprocess.run(["./ferma", fisier_input, fisier_output], 
                         check=True, capture_output=True, timeout=5)
        except subprocess.TimeoutExpired:
            print(f"  Test {i:2d}: {ROSU}✗ TIMEOUT{RESET} ⏱️")
            teste_esuate += 1
            # Șterge fișierul de output
            if os.path.exists(fisier_output):
                os.remove(fisier_output)
            continue
        except subprocess.CalledProcessError:
            print(f"  Test {i:2d}: {ROSU}✗ CRASH{RESET} 💥")
            teste_esuate += 1
            # Șterge fișierul de output
            if os.path.exists(fisier_output):
                os.remove(fisier_output)
            continue
        
        # Verifică output-ul (fără afișare detaliată)
        try:
            ferma = citeste_input(fisier_input)
            suma_finala_din_fisier = 0
            
            with open(fisier_output, 'r') as f:
                for linie in f:
                    linie_text = linie.strip()
                    if not linie_text:
                        continue
                    
                    if linie_text.startswith('SUMA_FINALA:'):
                        parti = linie_text.split(':')
                        suma_finala_din_fisier = int(parti[1].strip())
                        continue
                    
                    parti = linie_text.split()
                    if len(parti) < 3:
                        raise VerificareEsuata(f"Linie invalida")
                    
                    zi = int(parti[0])
                    actiune = parti[1]
                    coord_str = parti[2]
                    
                    verifica_zi_valida(ferma, zi)
                    linie_coord, coloana_coord = parseaza_coordonate(coord_str)
                    
                    if actiune == "planteaza":
                        if len(parti) < 4:
                            raise VerificareEsuata(f"Actiune planteaza lipseste numele legumei")
                        nume_leguma = parti[3]
                        verifica_actiune_plantare(ferma, zi, linie_coord, coloana_coord, nume_leguma)
                    elif actiune == "culege":
                        verifica_actiune_culegere(ferma, zi, linie_coord, coloana_coord)
                    else:
                        raise VerificareEsuata(f"Actiune necunoscuta: {actiune}")
            
            verifica_suma_finala(ferma, suma_finala_din_fisier)
            
            # Verifică limita minimă dacă există
            if limite_minime and len(limite_minime) >= i:
                limita_minima = limite_minime[i - 1]
                if suma_finala_din_fisier < limita_minima:
                    raise VerificareEsuata(f"Suma finala {suma_finala_din_fisier} < limita minima {limita_minima}")
            
            # Test trecut - salvează scorul
            scoruri_teste.append(suma_finala_din_fisier)
            if not mod_quiet:
                limita_info = ""
                if limite_minime and len(limite_minime) >= i:
                    limita_info = f" / min {limite_minime[i - 1]}"
                print(f"  Test {i:2d}: {VERDE}✓ PASSED{RESET} ✨  ({suma_finala_din_fisier}{limita_info} RON)")
            teste_trecute += 1
            
        except VerificareEsuata as e:
            # Test eșuat - salvează 0
            scoruri_teste.append(0)
            if not mod_quiet:
                print(f"  Test {i:2d}: {ROSU}✗ FAILED{RESET} ❌  ({e.mesaj})")
            teste_esuate += 1
        except Exception as e:
            # Test eroare - salvează 0
            scoruri_teste.append(0)
            if not mod_quiet:
                print(f"  Test {i:2d}: {ROSU}✗ ERROR{RESET} ⚠️  ({str(e)[:40]}...)")
            teste_esuate += 1
        
        # Șterge fișierul de output după verificare
        if os.path.exists(fisier_output):
            os.remove(fisier_output)
    
    # Afișează rezumatul
    total = teste_trecute + teste_esuate
    procent = (teste_trecute * 100 // total) if total > 0 else 0
    scor_total_bani = sum(scoruri_teste)
    
    if not mod_quiet:
        print(f"\n{GALBEN}{'='*70}{RESET}")
        print(f"{GALBEN}                         REZUMAT TESTE{RESET}")
        print(f"{GALBEN}{'='*70}{RESET}")
        
        if teste_trecute > 0:
            print(f"{VERDE}  ✓ Trecute: {teste_trecute}/{total}{RESET}")
        if teste_esuate > 0:
            print(f"{ROSU}  ✗ Eșuate:  {teste_esuate}/{total}{RESET}")
        
        print(f"\n  Punctaj teste: {teste_trecute * 0.5:.1f}p / {total * 0.5:.1f}p ({procent}%)")
        print(f"  Scor total bani: {GALBEN}{scor_total_bani:,}{RESET} RON")
        print(f"{GALBEN}{'='*70}{RESET}\n")
    
    return teste_esuate == 0, teste_trecute, total, scoruri_teste


def main():
    if len(sys.argv) < 2:
        print("Utilizare:")
        print("  python3 teste/scripturi/verifica.py <fisier_input> <fisier_output>  - verifica un test")
        print("  python3 teste/scripturi/verifica.py all                             - ruleaza toate testele")
        print("  python3 teste/scripturi/verifica.py <numar_test>                    - ruleaza un test specific")
        print("\nExemple:")
        print("  python3 teste/scripturi/verifica.py ferma.txt ferma.out")
        print("  python3 teste/scripturi/verifica.py all")
        print("  python3 teste/scripturi/verifica.py 5")
        sys.exit(1)
    
    # Verifică dacă e un număr de test sau "all"
    if sys.argv[1] == "all":
        succes, trecute, total, scoruri = ruleaza_toate_testele()
        
        # Scrie rezultatele intr-un fisier pentru scriptul de trimitere
        with open('.test_results.txt', 'w') as f:
            f.write(f"{trecute} {total}\n")
            # Scrie scorurile pentru fiecare test
            f.write(" ".join(map(str, scoruri)) + "\n")
        
        sys.exit(0 if succes else 1)
    elif sys.argv[1].isdigit():
        numar_test = int(sys.argv[1])
        succes = ruleaza_un_test(numar_test)
        sys.exit(0 if succes else 1)
    else:
        # Mod clasic: verifica un fisier specific
        if len(sys.argv) < 3:
            print("Eroare: Lipseste fisierul de output!")
            print("Utilizare: python3 teste/scripturi/verifica.py <fisier_input> <fisier_output>")
            sys.exit(1)
        
        fisier_input = sys.argv[1]
        fisier_output = sys.argv[2]
        
        succes = verifica_output(fisier_input, fisier_output)
        
        sys.exit(0 if succes else 1)


if __name__ == '__main__':
    main()

