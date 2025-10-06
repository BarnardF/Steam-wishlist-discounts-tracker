from services.steam_service import SteamService
from config import Config

steam = SteamService(Config.STEAM_ID)

print("Fetching all games...")
games = steam.get_all_games()

discounts = [game['discount_percent'] for game in games]
print(f"All discount percents: {discounts}")
print(f"Unique discount percents: {set(discounts)}")


print(f"\nTotal games: {len(games)}")

# Test filtering
bins = [(0,0), (1,10), (11,20), (21,30), (31,40), (41,50), (51,60), (61,70), (71,80), (81,100)]

for min_d, max_d in bins:
    filtered = steam.filter_by_discount_range(games, min_d, max_d)
    if min_d == max_d:
        print(f"Games with {min_d}% discount: {len(filtered)}")
    else:
        print(f"Games with {min_d}-{max_d}% discount: {len(filtered)}")

