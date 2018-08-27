def importer():
    import pandas as pd
    from bs4 import BeautifulSoup
    from urllib.request import Request, urlopen

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

        print(f"Completed Page {page_no+1}|156", end="\r")

    dframe.to_csv("Database.csv", index=False)
    return dframe


def analyser(dframe):
    # Import stuff
    import pandas as pd
    import matplotlib.pyplot as plt

    dframe["Release Date"] = pd.to_datetime(dframe["Release Date"])

    # Filter (dframe1), and average out releases on multiple platforms (dframe2)
    dframe1 = dframe.groupby(["Title","Platform",dframe["Release Date"].dt.year]).mean()
    platform_map = {"XONE": "Xbox", "X360": "Xbox", "XBOX": "Xbox",
                    "PS4": "Playstation", "PS3": "Playstation", "PS2": "Playstation", "PS": "Playstation",
                    "VITA": "Playstation", "PSP": "Playstation",
                    "Switch": "Nintendo", "WIIU": "Nintendo", "WII": "Nintendo", "3DS": "Nintendo", "DS": "Nintendo",
                    "GBA": "Nintendo", "GC": "Nintendo", "N64": "Nintendo",
                    "DC": "SEGA"}
    dframe2_construct = dframe.copy()
    dframe2_construct["Platform"] = dframe2_construct["Platform"].replace(platform_map)
    dframe2 = dframe2_construct.groupby(["Title","Platform",dframe["Release Date"].dt.year]).mean()
    dframe3 = dframe1.groupby(["Release Date","Title"]).mean()

    # Get number releases for year, total or per console
    num_year = dframe1.Metascore.groupby(["Platform","Release Date"]).count()
    num_year_comb = dframe2.Metascore.groupby(["Platform","Release Date"]).count()
    total_num_year = dframe3.groupby("Release Date").count()

    # Get average release metascore for year, total or per console
    meta_year = dframe1.Metascore.groupby(["Platform","Release Date"]).mean()
    meta_year_comb = dframe2.Metascore.groupby(["Platform","Release Date"]).mean()
    total_meta_year = dframe3.groupby("Release Date").mean()

    # Number of games released for each platform
    num_console = dframe1.groupby("Platform").count()
    num_total = len(dframe)

    # Plot things
    plt.hist(dframe["Metascore"],bins=20)
    plt.xlabel("Average Metascore (%)")
    plt.ylabel("Number of Games")

    num_year.unstack().transpose().plot()
    plt.xlabel("Release Year")
    plt.xlim(xmax=2020)
    plt.ylabel("Number of Games")
    num_year_comb.unstack().transpose().plot()
    plt.xlabel("Release Year")
    plt.xlim(xmax=2020)
    plt.ylabel("Number of Games")
    total_num_year.unstack().unstack().transpose().plot(legend=False)
    plt.xlabel("Release Year")
    plt.xlim(xmax=2020)
    plt.ylabel("Number of Games")

    meta_year.unstack().transpose().plot()
    plt.xlabel("Release Year")
    plt.xlim(xmax=2020)
    plt.ylabel("Average Metascore (%)")
    meta_year_comb.unstack().transpose().plot()
    plt.xlabel("Release Year")
    plt.xlim(xmax=2020)
    plt.ylabel("Average Metascore (%)")
    total_meta_year.unstack().unstack().transpose().plot(legend=False)
    plt.xlabel("Release Year")
    plt.xlim(xmax=2020)
    plt.ylabel("Average Metascore (%)")
