#!/bin/bash
# Script pentru generare cheie unică (opțional - doar pentru editare nickname)

# Schimbă directorul la rădăcina proiectului
cd "$(dirname "$0")/../.."

if [ -f "teste/scripturi/key.txt" ] && [ -s "teste/scripturi/key.txt" ]; then
    echo "✓ Cheia există deja în teste/scripturi/key.txt"
    echo "🔑 Cheia ta: $(cat teste/scripturi/key.txt)"
    echo ""
    echo "Folosește această cheie pentru a edita nickname-ul pe rezultate.eu"
    exit 0
fi

# Generează cheie unică
KEY=$(python3 -c "import uuid; print(uuid.uuid4().hex)")

# Salvează în fișier
echo "$KEY" > teste/scripturi/key.txt

echo "════════════════════════════════════════════════════════════"
echo "✓ Cheie unică generată și salvată în teste/scripturi/key.txt"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "🔑 Cheia ta: $KEY"
echo ""
echo "📌 PAȘI URMĂTORI:"
echo "   1. git add teste/scripturi/key.txt"
echo "   2. git commit -m \"Add personal key\""
echo "   3. git push"
echo "   4. Accesează rezultate.eu și editează nickname-ul"
echo ""
echo "⚠️  IMPORTANT: Salvează această cheie! O vei folosi pentru"
echo "    a edita nickname-ul pe https://rezultate.eu"
echo ""
echo "════════════════════════════════════════════════════════════"
echo ""

