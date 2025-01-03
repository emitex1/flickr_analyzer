import flickrapi
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('FLICKR_API_KEY')
API_SECRET = os.getenv('FLICKR_API_SECRET')
USER_ID = os.getenv('TARGET_USER_ID')

flickr = flickrapi.FlickrAPI(API_KEY, API_SECRET, format='parsed-json')

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

photos_data = get_photos_info(USER_ID)

df = pd.DataFrame(photos_data)
df.sort_values(by='Interest Rate', ascending=True, inplace=True)

print("Photos sorted based on the Interest Rate:\n", df)

df.to_csv('flickr_photos_analysis.csv', index=False)
print("Data also saved to 'flickr_photos_analysis.csv'")
