import time
import random
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager
except ImportError:
    print("Błąd: Brakuje wymaganych bibliotek. Zainstaluj je za pomocą:")
    print("pip install selenium webdriver-manager")
    exit(1)

# KONFIGURACJA
# Wpisz tutaj adresy URL stron, gdy już zostaną opublikowane w internecie,
# lub podaj ścieżki do plików lokalnych (np. "file:///C:/Users/.../index.html")
# jeśli chcesz testować lokalnie. Uwaga: GA może nie zliczać ruchu z "file://",
# dlatego najlepiej używać prawdziwych adresów URL (np. GitHub Pages, Vercel).
URLS = [
    "https://sportpulse-cms.vercel.app/index.html",
    "https://sportpulse-cms.vercel.app/article1.html",
    "https://sportpulse-cms.vercel.app/article2.html"
]

# Ile wizyt chcemy zasymulować
NUMBER_OF_VISITS = 10

def setup_driver():
    chrome_options = Options()
    # Opcja "headless" uruchamia przeglądarkę w tle, bez okna
    # Jeśli chcesz widzieć co się dzieje, zakomentuj poniższą linię:
    # chrome_options.add_argument("--headless")
    
    # Opcje pomagające oszukać GA, by nie traktowało tego jako bota
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def simulate_traffic():
    print(f"Rozpoczynam symulację ruchu. Liczba zaplanowanych wizyt: {NUMBER_OF_VISITS}")
    
    driver = setup_driver()
    
    try:
        for i in range(1, NUMBER_OF_VISITS + 1):
            url = random.choice(URLS)
            print(f"Wizyta #{i}: Wchodzę na -> {url}")
            driver.get(url)
            
            # Symulowanie "czytania" artykułu przez losowy czas (5 - 15 sekund)
            read_time = random.uniform(5, 15)
            print(f"   -> Użytkownik czyta stronę przez {read_time:.1f} sekund...")
            time.sleep(read_time)
            
            # Losowa przerwa między kolejnymi odwiedzinami, żeby wyglądało naturalniej
            wait_time = random.uniform(2, 5)
            print(f"   -> Przerwa {wait_time:.1f} sekund przed kolejnym wejściem.\n")
            time.sleep(wait_time)
            
    except Exception as e:
        print(f"Wystąpił błąd podczas symulacji: {e}")
    finally:
        driver.quit()
        print("Symulacja zakończona.")

if __name__ == "__main__":
    if "twojadomena.pl" in URLS[0]:
        print("UWAGA: Przed uruchomieniem skryptu, musisz zamienić 'twojadomena.pl' na swój prawdziwy adres strony w pliku traffic_simulator.py!")
        print("Jeśli testujesz lokalnie za pomocą rozszerzenia np. Live Server, wpisz tutaj odpowiednie lokalne adresy (np. http://127.0.0.1:5500/index.html).")
    else:
        simulate_traffic()
