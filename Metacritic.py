# Import stuff
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen


def importer():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3"}
    dframe = pd.DataFrame(data={"Title": [],
                                "Metascore": [],
                                "Platform": [],
                                "Release Date": []})

    # For each metacritic page
    for page_no in range(0, 156):  # 156

        # Some pages are broken??????

        # Request page
        req = Request(f"http://www.metacritic.com/browse/games/score/metascore/all/all/filtered?page={page_no}",
                      headers=headers)
        BSoup = BeautifulSoup(urlopen(req).read(), "lxml")

        # Parse page into single dataframe
        dframe_metascore = []
        dframe_date = []
        dframe_title = []
        dframe_platform = []

        for extractor in BSoup.find("div", {"class": "product_rows"}).findChildren(recursive=False):
            dframe_title.append(
                extractor.find("div", {"class": "product_item product_title"}).text.strip().splitlines()[0])
            dframe_metascore.append(int(
                extractor.find("div", {"class": "product_item product_score"}).findChildren(recursive=False)[
                    0].string))
            dframe_platform.append(
                extractor.find("div", {"class": "product_item product_title"}).text.strip().splitlines()[1].strip()[
                1:-1])
            dframe_date.append(
                pd.to_datetime(extractor.find("div", {"class": "product_item product_date"}).string.strip()))

        # Append dataframe to existing data
        dframeNew = pd.DataFrame(data={"Title": dframe_title,
                                       "Metascore": dframe_metascore,
                                       "Platform": dframe_platform,
                                       "Release Date": dframe_date})
        dframe = pd.concat([dframe, dframeNew], ignore_index=True)

        print(f"Completed Page {page_no+1}|156")

    # Find stuff out!!
    # filter multiplat releases to average    
    return dframe

#dframe = importer()
#dframe.to_csv("Database.csv", index=False)

dframe = pd.read_csv("Database.csv")



# Filter multiplat games
# dframe.drop_duplicates(['Title'])
