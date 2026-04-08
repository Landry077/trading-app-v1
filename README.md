<<<<<<< HEAD
# Trading App V3

Cette version 3 est pensée pour tourner **facilement sur ton ordinateur**.

## Ce que cette V3 apporte

- listes déroulantes **symboles** et **timeframes**
- **mise à jour partielle** des sections, sans recharger toute la page
- mode **demo** prêt à lancer immédiatement
- mode **live MT5** pour récupérer les vraies bougies depuis MetaTrader 5
- base de données SQL via **SQLite** par défaut
- possibilité d'aller vers MySQL plus tard en changeant seulement `DB_URL`

## 1. Installation

Dans VSCode ou un terminal :

```bash
python -m venv .venv
```

### Windows
```bash
.venv\Scripts\activate
```

### macOS / Linux
```bash
source .venv/bin/activate
```

Installe ensuite les dépendances :

```bash
pip install -r requirements.txt
```

## 2. Configurer le projet

Copie `.env.example` vers `.env`

### Windows
```bash
copy .env.example .env
```

### macOS / Linux
```bash
cp .env.example .env
```

## 3. Lancer l'application

```bash
uvicorn app.main:app --reload
```

Ouvre ensuite :

- API `http://127.0.0.1:8000`
- Interface `http://127.0.0.1:8000/ui`

## 4. Mode demo

Par défaut, l'app fonctionne en **demo**.

Cela veut dire que :
- la base SQLite est créée automatiquement
- des données de démonstration sont générées
- tu peux tester l'interface tout de suite

## 5. Mode live MT5

Dans `.env`, mets :

```env
APP_MODE=live
MT5_ENABLED=true
```

Si nécessaire, renseigne aussi :

```env
MT5_LOGIN=123456
MT5_PASSWORD=ton_mot_de_passe
MT5_SERVER=Nom-Du-Serveur
MT5_PATH=C:\Program Files\MetaTrader 5\terminal64.exe
```

Ensuite redémarre l'API.

### Important
Le mode live nécessite :
- MetaTrader 5 installé
- MT5 ouvert ou accessible
- les symboles visibles dans le terminal
- suffisamment d'historique chargé

## 6. Endpoints utiles

- `GET /api/symbols`
- `GET /api/timeframes`
- `GET /api/high-low?symbol=EURUSD&timeframe=M15&limit=4`
- `GET /api/latest-bar?symbol=EURUSD&timeframe=M15`
- `GET /api/daily-high-low?symbol=EURUSD&timeframe=M15`
- `GET /api/sync-logs`
- `POST /api/sync`
- `GET /api/health`

## 7. Actualisation partielle

L'interface ne recharge pas toute la page.

Elle met à jour séparément :
- les cartes
- le tableau High / Low
- la dernière bougie
- les logs

C'est donc un comportement fluide de type app, sans React.

## 8. Passer vers MySQL plus tard

Tu peux remplacer dans `.env` :

```env
DB_URL=sqlite:///./trading_app.db
```

par une URL SQLAlchemy compatible MySQL, par exemple :

```env
DB_URL=mysql+pymysql://root:motdepasse@127.0.0.1:3306/trading_app
```

et installer le driver adapté.

## 9. Si MT5 ne fonctionne pas

Lance d'abord en mode demo pour vérifier que :
- l'API tourne
- l'interface tourne
- les interactions fonctionnent

Puis active le mode live MT5.

## 10. Remarque honnête

Je peux préparer toute la structure et le code, mais je ne peux pas vérifier MT5 sur ton ordinateur depuis ici.
En revanche, cette archive est pensée pour te permettre de tester rapidement :
- d'abord le front et le backend
- puis la connexion MT5
=======
# trading-app-v1
>>>>>>> 2e6fa02b5543b697c227189b666efa53031f703a
