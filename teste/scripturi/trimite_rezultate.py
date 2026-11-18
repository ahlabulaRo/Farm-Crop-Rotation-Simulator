#!/usr/bin/env python3
"""
Script pentru trimiterea rezultatelor testelor la server (GitHub Actions)

Trimite punctajul la server doar daca ruleaza in GitHub Actions.
"""

import sys
import json
import os

# Schimbă directorul de lucru la rădăcina proiectului
os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def citeste_key():
    """Citeste cheia unica din fisierul key.txt (opțional)."""
    try:
        with open('teste/scripturi/key.txt', 'r') as f:
            key = f.readline().strip()
            return key if key else None
    except FileNotFoundError:
        return None


def verifica_rulare_github():
    """Verifica daca scriptul ruleaza in GitHub Actions."""
    # GitHub Actions seteaza variabila CI si GITHUB_ACTIONS
    if os.getenv('GITHUB_ACTIONS') != 'true':
        return False, None
    
    # Obtine informatii GitHub (toate sunt publice, nu necesita secrets)
    github_info = {
        'repository': os.getenv('GITHUB_REPOSITORY'),
        'commit_sha': os.getenv('GITHUB_SHA'),
        'run_id': os.getenv('GITHUB_RUN_ID'),
        'actor': os.getenv('GITHUB_ACTOR'),  # Username-ul care a facut push
        'ref': os.getenv('GITHUB_REF')  # Branch
    }
    
    return True, github_info


def trimite_la_server(key, teste_trecute, teste_totale, punctaj, scoruri_teste, github_info, server_ip):
    """Trimite rezultatele la server prin POST."""
    import requests
    import hashlib
    
    SHARED_SECRET = "tema2_poo_2025_secret_key"
    
    # Calculează scor total bani
    scor_total_bani = sum(scoruri_teste)
    
    # Construieste payload-ul
    payload = {
        'github_username': github_info.get('actor', 'unknown'),  # Identificator unic
        'key': key,  # Cheia unică pentru editare nickname
        'teste_trecute': teste_trecute,
        'teste_totale': teste_totale,
        'punctaj': punctaj,
        'scoruri_teste': scoruri_teste,  # Lista cu scorurile pentru fiecare test
        'scor_total_bani': scor_total_bani,  # Suma totală de bani
        'repository': github_info.get('repository', 'unknown'),
        'commit_sha': github_info.get('commit_sha', 'unknown'),
        'run_id': github_info.get('run_id', 'unknown'),
        'actor': github_info.get('actor', 'unknown'),
        'ref': github_info.get('ref', 'unknown')
    }
    
    # Generează semnătură pentru validare
    # Hash: (key sau github_username) + commit_sha + shared_secret
    signature_base = key if key else github_info.get('actor', 'unknown')
    signature_data = f"{signature_base}:{github_info.get('commit_sha', '')}:{SHARED_SECRET}"
    signature = hashlib.sha256(signature_data.encode()).hexdigest()
    
    # Headers cu semnătură
    headers = {
        'Content-Type': 'application/json',
        'X-GitHub-Signature': signature,
        'X-GitHub-Event': 'classroom_test'
    }
    
    try:
        # Adaugă https:// daca nu exista
        if not server_ip.startswith('http'):
            url = f"https://{server_ip}/submit_score"
        else:
            url = f"{server_ip}/submit_score"
        
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            nickname = result.get('nickname', 'Unknown')
            print(f"\n✓ Rezultate trimise cu succes la server!")
            print(f"🎯 Nickname-ul tău: {nickname}")
            print(f"   Vezi clasamentul pe: https://{server_ip}")
            return True
        else:
            print(f"\n✗ Eroare la trimitere: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Detalii: {error_data.get('error', 'Unknown error')}")
            except:
                pass
            return False
    except requests.exceptions.RequestException as e:
        print(f"\n✗ Eroare de conexiune la server: {e}")
        return False


def main():
    if len(sys.argv) < 4:
        print("Utilizare: python3 teste/scripturi/trimite_rezultate.py <teste_trecute> <teste_totale> <server_ip>")
        sys.exit(1)
    
    teste_trecute = int(sys.argv[1])
    teste_totale = int(sys.argv[2])
    server_ip = sys.argv[3]
    
    punctaj = teste_trecute * 0.5
    
    # Citește scorurile testelor din fișier
    scoruri_teste = []
    try:
        with open('.test_results.txt', 'r') as f:
            lines = f.readlines()
            if len(lines) >= 2:
                scoruri_str = lines[1].strip().split()
                scoruri_teste = [int(s) for s in scoruri_str]
    except:
        # Dacă nu poate citi scorurile, trimite listă goală
        scoruri_teste = []
    
    # Citeste cheia unica (opțional - pentru editare nickname)
    key = citeste_key()
    if not key:
        print("ℹ️  Nu există cheie în teste/scripturi/key.txt - nickname-ul va fi auto-generat")
        print("   Pentru a edita nickname-ul, generează o cheie cu: bash teste/scripturi/genereaza_key.sh")
    
    # Verifica daca ruleaza in GitHub Actions
    este_github, github_info = verifica_rulare_github()
    
    if not este_github:
        print("\nℹ️  Rulare locala detectata - rezultatele NU vor fi trimise la server.")
        print(f"   (Pentru trimitere, ruleaza in GitHub Actions cu push la repository)")
        sys.exit(0)
    
    # Trimite rezultatele
    scor_total_bani = sum(scoruri_teste)
    print(f"\n📤 Trimit rezultate")
    print(f"   Teste trecute: {teste_trecute}/{teste_totale}")
    print(f"   Punctaj: {punctaj}p")
    print(f"   Scor total bani: {scor_total_bani:,} RON")
    print(f"   Repository: {github_info.get('repository', 'N/A')}")
    
    succes = trimite_la_server(key, teste_trecute, teste_totale, punctaj, scoruri_teste, github_info, server_ip)
    
    sys.exit(0 if succes else 1)


if __name__ == '__main__':
    main()

