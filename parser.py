import pandas as pd, json, gzip

def parse_zengm(path):
    if path.endswith(".gz"):
        with gzip.open(path, "rt", encoding="utf-8") as f:
            data = json.load(f)
    elif path.endswith(".json"):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    elif path.endswith(".csv"):
        df = pd.read_csv(path)
        return {"overview": pd.DataFrame(), "teams": pd.DataFrame(), "players": pd.DataFrame(), "stats": df}
    else:
        raise ValueError("Unsupported file type")

    overview = pd.DataFrame([{
        "League": data.get("meta", {}).get("leagueName", "Unknown"),
        "Season": data.get("season", "Unknown"),
        "Teams": len(data.get("teams", [])),
        "Players": len(data.get("players", []))
    }])

    teams = pd.json_normalize(data.get("teams", []), sep="_")
    players = pd.json_normalize(data.get("players", []), sep="_")
    stats = pd.json_normalize(data.get("playerStats", []), sep="_") if "playerStats" in data else pd.DataFrame()

    players = players[~players.astype(str).apply(lambda x: x.str.contains("Died", case=False)).any(axis=1)]

    if "born_year" in players.columns:
        players["Age"] = 2025 - players["born_year"]

    return {"overview": overview, "teams": teams, "players": players, "stats": stats}
