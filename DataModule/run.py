import pandas as pd
import geopandas as gpd
import numpy as np
import subprocess
from pathlib import Path

# File paths
root = Path(__file__).parent.parent
database = root / "Data" / "SK.txt"
matrixExport = root / "Data" / "matrixExport.txt"
compModule = root / "ComputationModule" / "build" / "bin" / "compModule.exe"
out = root / "Out" / "out.txt"

# Load Database
dataFull = pd.read_csv(database, delimiter='\t', header=None)
dataFull.columns = ['geonameid', 'name', 'asciiname', 'alternatenames', 'latitude',
              'longitude', 'feature_class', 'feature_code', 'country_code', 'cc2',
              'admin1_code', 'admin2_code', 'admin3_code', 'admin4_code', 'population',
              'elevation', 'dem', 'timezone', 'modification_date']

# Filter out to Žilina, remove 0 population
dataZa = dataFull[dataFull['admin1_code'] == 8.0]
datapop = dataZa[dataZa['population'] != 0.0]
# Remove duplicates and districts
datapop = datapop[~datapop['name'].str.startswith("Okres")]
datapop = datapop.loc[datapop.groupby('name')['population'].idxmax()]
# Remove Žilina region
datapop = datapop[datapop['name'] != "Zilina"]
datapop.reset_index(drop=True, inplace=True)
weights = datapop[['population']].to_numpy()
coords = datapop[['latitude', 'longitude']]

# Find maximum population
maxpop = 0
for i in range(0, weights.shape[0]):
    if weights[i][0] > maxpop:
        maxpop = weights[i][0]

# Convert to GeoDataFrame and set CRS
gdf = gpd.GeoDataFrame(
    coords,
    geometry=gpd.points_from_xy(coords['longitude'], coords['latitude'])
)
gdf.set_crs(epsg=4326, inplace=True)
gdf_utm = gdf.to_crs(epsg=32634)

# Calculate weighted distance matrix
distances = []
for _, row in gdf_utm.iterrows():
    distances.append(gdf_utm['geometry'].distance(row['geometry']) / 1000)
matrixA = pd.DataFrame.from_records(distances).to_numpy()
weightedMatrix = matrixA * weights

# Export matrix to text file
with open(matrixExport, "w") as f:
    f.write(str(weightedMatrix.shape[0]) + "\t" + str(weightedMatrix.shape[1]) + "\n")
    np.savetxt(f, weightedMatrix, delimiter="\t", fmt="%.6f")


p = input("How many centers do you want to place? ")

# Execute computation module
res = subprocess.run(
    [str(compModule), str(matrixExport), str(p)],
    capture_output=True, text=True
)

# Capture output
lines = res.stdout.strip().splitlines()
maxmin = list(map(int, lines[0].split()))
maxmax = list(map(int, lines[1].split()))

# Interpret and print results to console and file
with open(out, "w", encoding="utf-8") as f:
    print("MaxMin ", p, "\n", end="", sep="")
    f.write("MaxMin" + str(p) + "\n")
    for i in maxmin:
        print(datapop.iloc[i]['name'], end="", sep="")
        f.write(datapop.iloc[i]['name'])
        if maxmin.index(i) != 0 and (maxmin.index(i) + 1) % 5 == 0:
            print()
            f.write("\n")
        if maxmin.index(i) != len(maxmin) - 1:
            print(", ", end="", sep="")
            f.write(", ")
    print()
    f.write("\n")

    print("MaxMax ", p, "\n", end="", sep="")
    f.write("MaxMax" + str(p) + "\n")
    for i in maxmax:
        print(datapop.iloc[i]['name'], end="", sep="")
        f.write(datapop.iloc[i]['name'])
        if maxmax.index(i) != 0 and (maxmax.index(i) + 1) % 5 == 0:
            print()
            f.write("\n")
        if maxmax.index(i) != len(maxmax) - 1:
            print(", ", end="", sep="")
            f.write(", ")
    print()
    f.write("\n")

# Maxmax debatched
maxmax_debatch = list()
original_weights = weights.copy()
original_matrixA = matrixA.copy()
for i in range(int(p)):
    res = subprocess.run(
        [str(compModule), str(matrixExport), str(1)],
        capture_output=True, text=True
    )

    lines = res.stdout.strip().splitlines()
    maxmax_debatch.append(list(map(int, lines[1].split()))[0])

    weights[maxmax_debatch[i]][0] = maxpop
    for j in range(matrixA.shape[0]):
        matrixA[j][maxmax_debatch[i]] = 0

    # Recalculate matrix
    weightedMatrix = matrixA * weights

    with open(matrixExport, "w") as f:
        f.write(str(weightedMatrix.shape[0]) + "\t" + str(weightedMatrix.shape[1]) + "\n")
        np.savetxt(f, weightedMatrix, delimiter="\t", fmt="%.6f")

# Restore original matrix and reexport
weights = original_weights.copy()
matrixA = original_matrixA.copy()
weightedMatrix = matrixA * weights

with open(matrixExport, "w") as f:
    f.write(str(weightedMatrix.shape[0]) + "\t" + str(weightedMatrix.shape[1]) + "\n")
    np.savetxt(f, weightedMatrix, delimiter="\t", fmt="%.6f")

# DACPM debatched
maxmin_debatch = list()
for i in range(int(p)):
    res = subprocess.run(
        [str(compModule), str(matrixExport), str(1)],
        capture_output=True, text=True
    )

    lines = res.stdout.strip().splitlines()
    maxmin_debatch.append(list(map(int, lines[0].split()))[0])
    # Set weight of chosen node to maximum and set distances from it to 0
    weights[maxmin_debatch[i]][0] = maxpop
    for j in range(matrixA.shape[0]):
        matrixA[j][maxmin_debatch[i]] = 0


    # Recalculate matrix
    weightedMatrix = matrixA * weights

    with open(matrixExport, "w") as f:
        f.write(str(weightedMatrix.shape[0]) + "\t" + str(weightedMatrix.shape[1]) + "\n")
        np.savetxt(f, weightedMatrix, delimiter="\t", fmt="%.6f")

with open(out, "a", encoding="utf-8") as f:
    print("MaxMin Declustered ", p, "\n", end="", sep="")
    f.write("MaxMin Declustered" + str(p) + "\n")
    for i in maxmin_debatch:
        print(datapop.iloc[i]['name'], end="", sep="")
        f.write(datapop.iloc[i]['name'])
        if maxmin_debatch.index(i) != 0 and (maxmin_debatch.index(i) + 1) % 5 == 0:
            print()
            f.write("\n")
        if maxmin_debatch.index(i) != len(maxmin_debatch) - 1:
            print(", ", end="", sep="")
            f.write(", ")
    print()
    f.write("\n")

    print("MaxMax Declustered ", p, "\n", end="", sep="")
    f.write("MaxMax Declustered" + str(p) + "\n")
    for i in maxmax_debatch:
        print(datapop.iloc[i]['name'], end="", sep="")
        f.write(datapop.iloc[i]['name'])
        if maxmax_debatch.index(i) != 0 and (maxmax_debatch.index(i) + 1) % 5 == 0:
            print()
            f.write("\n")
        if maxmax_debatch.index(i) != len(maxmax_debatch) - 1:
            print(", ", end="", sep="")
            f.write(", ")
    print()
    f.write("\n")

# Restore original matrix
weights = original_weights.copy()
matrixA = original_matrixA.copy()
weightedMatrix = matrixA * weights

with open(matrixExport, "w") as f:
    f.write(str(weightedMatrix.shape[0]) + "\t" + str(weightedMatrix.shape[1]) + "\n")
    np.savetxt(f, weightedMatrix, delimiter="\t", fmt="%.6f")