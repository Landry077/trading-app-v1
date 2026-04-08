import MetaTrader5 as mt5

PATH = r"C:\Program Files\MetaTrader 5\terminal64.exe"
LOGIN = 435316401
PASSWORD = "MotDePasse"
SERVER = "Exness-MT5Trial9"

SYMBOL = "EURUSD"

print("Initialize...")
ok = mt5.initialize(path=PATH)
print("init:", ok, mt5.last_error())

if ok:
    print("Login...")
    logged = mt5.login(login=LOGIN, password=PASSWORD, server=SERVER)
    print("login:", logged, mt5.last_error())

    if logged:
        print("Version:", mt5.version())

        print("\\n--- TEST SYMBOL INFO ---")
        info = mt5.symbol_info(SYMBOL)
        print("symbol_info:", info)

        print("\\n--- TEST SYMBOL SELECT ---")
        selected = mt5.symbol_select(SYMBOL, True)
        print("symbol_select:", selected, mt5.last_error())

        print("\\n--- TEST RATES ---")
        rates = mt5.copy_rates_from_pos(SYMBOL, mt5.TIMEFRAME_M5, 0, 4)
        print("rates:", rates)

        print("\\n--- RECHERCHE DES SYMBOLES QUI CONTIENNENT EURUSD ---")
        matches = mt5.symbols_get("*EURUSD*")
        if matches:
            for s in matches:
                print(s.name)
        else:
            print("Aucun symbole trouvé")

    mt5.shutdown()