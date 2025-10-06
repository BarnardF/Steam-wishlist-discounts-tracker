import requests
import json
from dotenv import load_dotenv
import os
from time import sleep

# Load environment variables
load_dotenv()
STEAM_ID = os.getenv('STEAM_ID')

print("=" * 60)
print("STEAM WISHLIST DISCOUNT TRACKER - API TEST")
print("=" * 60)
print(f"Steam ID: {STEAM_ID}\n")

# ==========================================
# TASK 1: Fetch Wishlist IDs
# ==========================================

def get_wishlist_ids():
    """
    Fetch list of app IDs from your wishlist
    Returns: list of integers [227300, 270880, ...]
    """
    print("📋 Fetching wishlist...")
    
    url = f"https://api.steampowered.com/IWishlistService/GetWishlist/v1/?steamid={STEAM_ID}"
    
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
    


# ==========================================
# TASK 2: Fetch Game Details
# ==========================================

def get_game_details(app_id):
    """
    Fetch pricing and discount info for a single game
    
    Args:
        app_id: Steam app ID (integer)
    
    Returns:
        Dictionary with: {
            'app_id': int,
            'name': str,
            'original_price': float,
            'current_price': float,
            'discount_percent': int,
            'is_free': bool
        }
        or None if game not found / no price data
    """
    url = f"https://store.steampowered.com/api/appdetails?appids={app_id}"
    
    try:
        response = requests.get(url)
        data = response.json()

        #game data
        game_data = data[str(app_id)]

        if not game_data['success']:
            return None
        
        game_info = game_data['data']

        if 'price_overview' not in game_info:
            return {
                'app_id': app_id,
                'name': game_info['name'],
                'original_price': 0.0,
                'current_price': 0.0,
                'discount_percent': 0,
                'is_free': game_info.get('is_free', True)
            }
        
        price_info = game_info['price_overview']
        original = price_info['initial'] / 100
        current = price_info['final'] /100
        discount = price_info['discount_percent']
        
        return {
            'app_id': app_id,
            'name': game_info['name'],
            'original_price': original,
            'current_price': current,
            'discount_percent': discount,
            'is_free': game_info.get('is_free', False)        
        }
    except requests.RequestException as e:
        print(f"Error fetching game_details: {e}")
        return {}


# ==========================================
# MAIN TEST
# ==========================================

if __name__ == "__main__":
    # Step 1: Get wishlist
    wishlist_ids = get_wishlist_ids()
    
    if not wishlist_ids:
        print("❌ Failed to fetch wishlist!")
        exit(1)
    
    print(f"✅ Found {len(wishlist_ids)} games in wishlist\n")
    
    # Step 2: Test with first 5 games
    print("🎮 Testing with first 5 games:")
    print("-" * 60)
    
    for app_id in wishlist_ids[:5]:
        print(f"\nFetching app {app_id}...")
        game = get_game_details(app_id)
        
        if game:
            print(f"  Name: {game['name']}")
            print(f"  Original: R{game['original_price']:.2f}")
            print(f"  Current: R{game['current_price']:.2f}")
            print(f"  Discount: {game['discount_percent']}%")
            
            if game['discount_percent'] > 0:
                print(f"  🔥 ON SALE!")
        else:
            print(f"  ⚠️  Could not fetch data for {app_id}")
        
        # Be nice to Steam's servers
        sleep(1)
    
    print("\n" + "=" * 60)
    print("✅ Test complete!")
    print("=" * 60)