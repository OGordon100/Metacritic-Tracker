# Import stuff
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import matplotlib.pyplot as plt
import Importer

#dframe = Importer()

dframe = pd.read_csv("Database.csv")
dframe["Release Date"] = pd.to_datetime(dframe["Release Date"])

# Filter (dframe1), and average out releases on multiple platforms (dframe2)
dframe1 = dframe.groupby(["Title","Platform",dframe["Release Date"].dt.year]).mean()
dframe2 = dframe1.groupby(["Release Date","Title"]).mean()

# Get number releases for year, total or per console
num_year = dframe1.groupby(["Platform","Release Date"]).count()
total_num_year = dframe2.groupby("Release Date").count()

# Get average release metascore for year, total or per console
meta_year = dframe1.groupby(["Platform","Release Date"]).mean()
total_meta_year = dframe2.groupby("Release Date").mean()

# Number of games released for each platform
num_console = dframe1.groupby("Platform").count()
num_total = len(dframe)

# Distribution of all metascores
plt.hist(dframe["Metascore"],bins=20)
