#!/usr/bin/env bash
# Skrypt uruchamiający książkę kucharską w trybie 100% offline
# Wystarczy dwukrotnie kliknąć ten plik na macOS, aby otworzyć aplikację!

cd "$(dirname "$0")"

PORT=8080
# Wykrywanie adresu IP w sieci lokalnej (Wi-Fi)
IP=$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || echo "")

echo "=========================================================="
echo "   📖 RODZINNY PRZEPIŚNIK - SKARBNICA DOMOWYCH SMAKÓW"
echo "   Tryb 100% OFFLINE (bez dostępu do Internetu)"
echo "=========================================================="
echo ""
echo " Serwer lokalny został pomyślnie uruchomiony:"
echo "   💻 Na tym komputerze:             http://localhost:$PORT"
if [ -n "$IP" ]; then
echo "   📱 Na telefonie (Android / iPhone): http://$IP:$PORT"
echo "      (telefon musi być w tej samej sieci Wi-Fi)"
fi
echo ""
echo " 💡 Jak zainstalować na telefonie z Androidem:"
echo "   1. Otwórz w Google Chrome adres: http://${IP:-localhost}:$PORT"
echo "   2. Kliknij 'Zainstaluj aplikację' lub w menu Chrome (3 kropki)"
echo "      wybierz 'Zainstaluj aplikację' / 'Dodaj do ekranu głównego'."
echo "   3. Aplikacja zainstaluje się jak natywna z własną ikoną na pulpicie,"
echo "      działa na pełnym ekranie i zachowuje wszystkie dane offline!"
echo ""
echo " Aby zakończyć działanie serwera, zamknij to okno lub wciśnij Ctrl+C."
echo "=========================================================="
echo ""

# Otwórz przeglądarkę domyślną na Macu
sleep 1 && open "http://localhost:$PORT" &

# Uruchom lekki serwer HTTP wbudowany w Pythona
python3 -m http.server $PORT
