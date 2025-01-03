import flickrapi
import pandas as pd
import os
from dotenv import load_dotenv

print()
print("----------------====<<<<< Flickr Analyzer >>>>>====----------------")
print("------------- Photos List based on the Interest Rate --------------")
load_dotenv()
API_KEY = os.getenv('FLICKR_API_KEY')
API_SECRET = os.getenv('FLICKR_API_SECRET')
USER_ID = os.getenv('TARGET_USER_ID')

if not API_KEY or not API_SECRET:
    print("Error: API_KEY or API_SECRET is missing. Please check your .env file.")
    exit(1)

if not USER_ID:
    print("Error: USER_ID is missing. Please check your .env file.")
    exit(1)

flickr = flickrapi.FlickrAPI(API_KEY, API_SECRET, format='parsed-json')

def validate_api_keys():
    try:
        flickr.test.echo()
    except flickrapi.exceptions.FlickrError as e:
        print("Error: Invalid API Key or Secret.")
        print(f"Details: {e}")
        exit(1)

def validate_user_id(user_id):
    try:
        flickr.people.getInfo(user_id=user_id)
    except flickrapi.exceptions.FlickrError as e:
        print("Error: Invalid User ID.")
        print(f"Details: {e}")
        exit(1)

validate_api_keys()
validate_user_id(USER_ID)

def get_photos_info(user_id):
    photos_data = []
    page = 1
    while True:
        photos = flickr.photos.search(user_id=user_id, per_page=100, page=page)
        if 'photos' not in photos or 'photo' not in photos['photos']:
            break

        for photo in photos['photos']['photo']:
            photo_id = photo['id']

            details = flickr.photos.getInfo(photo_id=photo_id)
            views = int(details['photo']['views'])

            all_faves = flickr.photos.getFavorites(photo_id=photo_id, per_page=1)
            faves = int(all_faves['photo']['total'])

            if faves > 0:
                interest_rate = round(views / faves, 1)

                photos_data.append({
                    'Photo ID': photo_id,
                    'Title': details['photo']['title']['_content'],
                    'Views': views,
                    'Favorites': faves,
                    'Interest Rate': interest_rate
                })

        if page >= photos['photos']['pages']:
            break
        page += 1

    return photos_data

print('\nGetting photos information...')
photos_data = get_photos_info(USER_ID)

df = pd.DataFrame(photos_data)
df.sort_values(by='Interest Rate', ascending=True, inplace=True)

print('Photos List based on the Interest Rate:\n')
print(df)

df.to_csv('flickr_photos_analysis.csv', index=False)
print("\nData also saved to 'flickr_photos_analysis.csv'")
