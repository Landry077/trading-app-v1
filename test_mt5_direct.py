import MetaTrader5 as mt5

PATH = r"C:\Program Files\MetaTrader 5\terminal64.exe"
LOGIN = 435316401
PASSWORD = "MotDePasse"
SERVER = "Exness-MT5Trial9"

print("Initialize direct...")
ok = mt5.initialize(
    path=PATH,
    login=LOGIN,
    password=PASSWORD,
    server=SERVER,
    timeout=60000
)

print("init:", ok)
print("last_error:", mt5.last_error())

if ok:
    print("version:", mt5.version())
    print("account_info:", mt5.account_info())

    symbols = mt5.symbols_get("*EURUSD*")
    print("symbols:")
    if symbols:
        for s in symbols:
            print("-", s.name)
    else:
        print("Aucun symbole trouvé")

    mt5.shutdown()