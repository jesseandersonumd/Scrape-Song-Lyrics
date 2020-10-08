import requests
import bs4
import pandas as pd
import re
import os

df = pd.read_csv("songs_assigned_to_rchatte2.csv")

def clean(data, column):  
    cleaned_list = []
    for x in data[column]:
        x = re.sub("[-'.&+]", '', x)
        x = '-'.join(x.split())
        cleaned_list.append(x.lower())
    return cleaned_list

performers = clean(df,'Performer')
lyrics = clean(df,'Song')
songs_and_performers = list(zip(performers,lyrics,[re.sub("[-'.&?)(+/\"]", '', songid) for songid in df['SongID']]))
url_list = []

for x,y,z in songs_and_performers:
    url = f'http://www.songlyrics.com/{x}/{y}-lyrics/'
    url_list.append(url)
    
songs_and_performers = list(zip(performers,lyrics,[re.sub("[-'.&?)(+/\"]", '', songid) for songid in df['SongID']],url_list))

for w, x, y, z in songs_and_performers:
    chosen_url = z
    title = y
    result = requests.get(chosen_url)
    soup = bs4.BeautifulSoup(result.text,'lxml')
    
    with open(f'{title}.txt','w') as songs:
        try:
            for line in soup.select('#songLyricsDiv')[0].get_text().split('\n'):
                songs.write(line + '\n')
        except:
            songs.write("Song lyrics do not exist");
            print(title)
            continue;
