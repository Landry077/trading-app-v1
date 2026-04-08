import MetaTrader5 as mt5

PATH = r"C:\Program Files\MetaTrader 5\terminal64.exe"
LOGIN = 435316401
PASSWORD = "MotDePasse"
SERVER = "Exness-MT5Trial9"
SYMBOL = "EURUSDm"

ok = mt5.initialize(
    path=PATH,
    login=LOGIN,
    password=PASSWORD,
    server=SERVER,
    timeout=60000
)

print("init:", ok, mt5.last_error())

if ok:
    selected = mt5.symbol_select(SYMBOL, True)
    print("selected:", selected, mt5.last_error())

    rates = mt5.copy_rates_from_pos(SYMBOL, mt5.TIMEFRAME_M5, 0, 4)
    print("rates:", rates)

    mt5.shutdown()