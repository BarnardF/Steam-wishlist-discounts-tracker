import requests, json
from time import sleep
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

class SteamService:
    def __init__(self, steam_id, country_code = "ZA"):
        self.steam_id = steam_id
        self.country_code = (country_code or "ZA").upper()
        self.wishlist_url = f"https://api.steampowered.com/IWishlistService/GetWishlist/v1/?steamid={steam_id}"
        self.appdetails_url = "https://store.steampowered.com/api/appdetails?appids={}"

    def get_wishlist_ids(self):
        url = self.wishlist_url
        
        try:
            response = requests.get(url)
            data = response.json()

            app_ids = []
            for item in data['response']['items']:
                app_ids.append(item['appid'])

            return app_ids
        except requests.RequestException as e:
            print(f"Error fetching wishlist: {e}")
            return []
        
    def get_game_details(self, app_id):
        url = self.appdetails_url.format(app_id) + f"&cc={self.country_code}&l=en"
    
        try:
            response = requests.get(url, timeout=10)
            data = response.json()

            if not data or str(app_id) not in data:
                print(f"No data for app_id {app_id}")
                return None
            
            #game data
            game_data = data[str(app_id)]

            if not game_data['success']:
                return None
            
            game_info = game_data['data']

            if 'price_overview' not in game_info:
                release_info = game_info.get('release_date', {})
                if release_info.get('coming_soon', False):
                    #unreleased
                    return {
                        'app_id': app_id,
                        'name': game_info['name'],
                        'original_price': None,
                        'current_price': None,
                        'discount_percent': None,
                        'is_free': False,
                        'status': 'Unreleased'
                    }
                else:
                    #free to play
                    return {
                        'app_id': app_id,
                        'name': game_info['name'],
                        'original_price': 0.0,
                        'current_price': 0.0,
                        'discount_percent': 0,
                        'is_free': game_info.get('is_free', True),
                        'status': 'Free'
                    }
            
            #game has pricing
            price_info = game_info['price_overview']
            original = price_info['initial'] / 100
            current = price_info['final'] / 100
            discount = price_info['discount_percent']
            
            return {
                'app_id': app_id,
                'name': game_info['name'],
                'original_price': original,
                'current_price': current,
                'discount_percent': discount,
                'is_free': game_info.get('is_free', False),
                'status': 'Available'    
            }
        except requests.RequestException as e:
            print(f"Error fetching game_details for {app_id}: {e}")
            return None
        except (ValueError, TypeError) as e:
            print(f"Json pasring error for {app_id}: {e}")
            return None

    # def get_all_games(self):
    #     game_list = []
    #     failed_ids = []
    #     wishlist_ids = self.get_wishlist_ids()

    #     if not wishlist_ids:
    #         return game_list
        
    #     total = len(wishlist_ids)
    #     print(f"Fetching {total} games from steam api")

    #     for index, app_id in enumerate(wishlist_ids, 1):
    #         print(f"{index}/{total} fetching {app_id}", end='/r')

    #         game_data = self.get_game_details(app_id)

    #         if game_data:
    #             game_list.append(game_data)
    #         else:
    #             failed_ids.append(app_id)

    #         sleep(0.5)

    #     print(f"Fetched {len(game_list)} games")
    #     if failed_ids:
    #         print(f"Failed fetching {len(failed_ids)} games: {failed_ids[:5]}...")

    #     return game_list

    #     # for id in wishlist_ids:
    #     #     game_data = self.get_game_details(id)
    #     #     game_list.append(game_data)
    #     #     sleep(1)
    #     # return game_list

    def get_all_games(self, max_workers = 10):
        wishlist_ids = self.get_wishlist_ids()

        if not wishlist_ids:
            return []
        
        game_list = []
        total = len(wishlist_ids)
        print(f"Fetching {total} games, using {max_workers} threads")

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_id = {
                executor.submit(self.get_game_details, app_id): app_id #2
                for app_id in wishlist_ids #1
            }

            for index, future in enumerate(as_completed(future_to_id), 1):
                print(f"[{index}/{total}] completed", end='\r')

                game_data = future.result()
                if game_data:
                    game_list.append(game_data)

                sleep(0.05)
        
        print(f"\n successfully fetched {len(game_list)} games")
        return game_list 


    def filter_by_discount_range(self, games, min_discount = 0, max_discount = 100):
        filtered = []
        if not games:
            return filtered
        
        for game in games:
            discount = game.get('discount_percent')
            if discount is None:
                continue

            if min_discount <= discount <= max_discount:
                filtered.append(game)    
            # if min_discount <= game.get('discount_percent', 0) <= max_discount:
            #     discounted_games.append(game)  

        return filtered     
    
