import MetaTrader5 as mt5

print("Initialize...")
ok = mt5.initialize()
print("init:", ok)
print("last_error:", mt5.last_error())

if ok:
    print("\nVersion:")
    print(mt5.version())

    print("\nAccount:")
    print(mt5.account_info())

    print("\nSymbols EURUSD:")
    symbols = mt5.symbols_get("*EURUSD*")
    if symbols:
        for s in symbols:
            print(s.name)
    else:
        print("Aucun")

    mt5.shutdown()