from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import random

def get_game_details(game_id):
    time.sleep(random.uniform(0.2, 1.0))
    return {"id": game_id, "name": f"game {game_id}"}

def get_all_games(max_workers = 5):
    # Step 1: You have a list of game IDs (fake wishlist)
    # These represent the items you want to process (e.g., games to fetch)
    game_ids = [1,2,3,4,5,6,7,8]

    print(f"fetching {len(game_ids)} games using {max_workers} threads...")

    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Step 2: Each one gets passed to a thread through executor.submit()
        # This schedules the get_game_details() function to run for each ID
        # Step 3: Threads run get_game_details() concurrently (simulating API calls)
        # Each thread works independently to "fetch" game data
        future_to_id = {executor.submit(get_game_details, gid): gid for gid in game_ids}

        # Step 4: As each thread finishes, as_completed() yields its result
        # So we handle results as soon as a thread completes, not in order of submission
        for index, future in enumerate(as_completed(future_to_id), 1):
            game = future.result()
            # Step 5: Results are collected and printed in the order they finish
            # (This means fast threads print first, slow ones later)
            results.append(game)
            print(f"[{index}/{len(game_ids)}] done fetching {game['name']}")

    print(f"\n finished fetching {len(results)} games")
    return results

if __name__ == "__main__":
    games = get_all_games()
    print(games)