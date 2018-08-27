# Import stuff
import pandas as pd
import functions

if (input("Update Database? [y|n]") == 'y') is True:
    # Parse metacritic for info
    data = functions.importer()
else:
    # Load metacritic info from file
    data = pd.read_csv("Database.csv")

# Analyse data
functions.analyser(data)