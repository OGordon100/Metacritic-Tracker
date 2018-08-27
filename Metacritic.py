# Import stuff
import pandas as pd
import matplotlib.pyplot as plt
import Importer

# Parse metacritic for info
#dframe = Importer()

# Load metacritic info from file
dframe = pd.read_csv("Database.csv")
dframe["Release Date"] = pd.to_datetime(dframe["Release Date"])

# Filter (dframe1), and average out releases on multiple platforms (dframe2)
dframe1 = dframe.groupby(["Title","Platform",dframe["Release Date"].dt.year]).mean()
dframe2 = dframe1.groupby(["Release Date","Title"]).mean()

# Get number releases for year, total or per console
num_year = dframe1.Metascore.groupby(["Platform","Release Date"]).count()
total_num_year = dframe2.groupby("Release Date").count()

# Get average release metascore for year, total or per console
meta_year = dframe1.Metascore.groupby(["Platform","Release Date"]).mean()
total_meta_year = dframe2.groupby("Release Date").mean()

# Number of games released for each platform
num_console = dframe1.groupby("Platform").count()
num_total = len(dframe)

# Plot things
plt.figure(0)
plt.hist(dframe["Metascore"],bins=20)
plt.xlabel("Average Metascore")
plt.ylabel("Number of Games")
plt.figure(1)
num_year.unstack().transpose().plot()
plt.xlabel("Release Year")
plt.ylabel("Number of Games")
plt.figure(2)
meta_year.unstack().transpose().plot()
plt.xlabel("Release Year")
plt.ylabel("Average Metascore")
plt.figure(3)
total_num_year.unstack().unstack().transpose().plot(legend=False)
plt.xlabel("Release Year")
plt.ylabel("Number of Games")
plt.figure(4)
total_meta_year.unstack().unstack().transpose().plot(legend=False)
plt.xlabel("Release Year")
plt.ylabel("Average Metascore")
