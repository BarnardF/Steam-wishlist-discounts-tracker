from services.steam_service import SteamService
from config import Config

steam = SteamService(Config.STEAM_ID)

print("Fetching all games...")
games = steam.get_all_games()

print(f"\nTotal games: {len(games)}")

# Test filtering
for threshold in [10, 20, 30, 40]:
    filtered = steam.filter_by_discount(games, threshold)
    print(f"Games with {threshold}%+ discount: {len(filtered)}")