import urllib, json, os
from tqdm import tqdm
from dotenv import load_dotenv
from plexapi.myplex import MyPlexAccount

load_dotenv()
plexUsername = os.getenv('PLEX_USERNAME')
plexToken = os.getenv('PLEX_TOKEN')

account = MyPlexAccount(plexUsername, None, plexToken)

open("errors.txt", "w")

url = f'https://letterboxd-list-radarr.onrender.com/{os.getenv("LETTERBOXD_USERNAME")}/watchlist/'

response = urllib.request.urlopen(url)

data = json.loads(response.read())

alreadyDone = False

name = [item['title'] for item in data]
year = [item['release_year'] for item in data]
with tqdm(total=len(name)) as pbar:
    for i in range(len(name)):
# you can uncomment this when you've already done everything once: the script will only consider new additions
#        if alreadyDone:
#           pbar.update(len(name)-i)
#           break
        search_query = name[i]+" ("+year[i]+")"
        pbar.set_description(f"Processing {search_query}")
        results = account.searchDiscover(search_query,libtype="movie")
        if len(results) == 1:
            try:
                results[0].addToWatchlist()
            except Exception as e:
                with open("errors.txt", "a") as f:
                    f.write(str(e) + "\n")
        elif len(results) != 0:
            found_exact_match = False
            for result in results:
                if found_exact_match:
                    break
                if result.title.replace(" ","").lower() == name[i].replace(" ","").lower():
                    if result.year is None:
                        with open("errors.txt", "a") as f:
                            f.write(f'{result.title} has no year property!\n')
                    elif int(result.year) == int(year[i]):
                        try:
                            found_exact_match = True
                            result.addToWatchlist()
                        except Exception as e:
                            alreadyDone = True
                            with open("errors.txt", "a") as f:
                                f.write(str(e) + "\n")
                    elif int(result.year)-1 == int(year[i]):
                        try:
                            found_exact_match = True
                            with open("errors.txt", "a") as f:
                                f.write(result.title+" ("+str(result.year)+") associated with "+name[i]+" ("+str(year[i])+") \n")
                            result.addToWatchlist()
                        except Exception as e:
                            with open("errors.txt", "a") as f:
                                f.write(str(e) + "\n")
            if not found_exact_match:
                print(f"Multiple movies found for {name[i]} ({year[i]}):")
                for j, result in enumerate(results):
                    if(j>4):
                       break
                    if(len(result.directors)>0):
                        print(f"{j+1}. {result.title} ({result.year}) - {result.directors[0]}")
                    else:
                        print(f"{j+1}. {result.title} ({result.year})")
                choice = input("Enter the number of the movie to add (enter 0 to select none): ")
                if(int(choice) != 0):
                    result = results[int(choice) - 1]
                    try:
                        result.addToWatchlist()
                    except Exception as e:
                        with open("errors.txt", "a") as f:
                            f.write(str(e) + "\n")
        else:
            with open("errors.txt", "a") as f:
                f.write(f"No results found for {search_query}\n")
        pbar.update(1)
