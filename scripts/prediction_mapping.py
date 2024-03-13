from matplotlib import pyplot as plt
import geopandas as gpd
import pandas as pd

pred = pd.read_csv('data/prediction.csv')
agg = pred.groupby('neighborhood').agg('sum').reset_index()

agg['neighborhood'] = agg['neighborhood'].str.upper()
agg.rename(columns={'neighborhood': 'community'}, inplace=True)


import geopandas
gpdf = geopandas.read_file("data/boundaries.geojson")

community_mapping = {
    'BRONZEVILLE': 'GRAND BOULEVARD',
    'BACK OF THE YARDS': 'NEW CITY',
    'BOYSTOWN': 'LAKE VIEW',
    'ANDERSONVILLE': 'EDGEWATER',
    'BUCKTOWN': 'LOGAN SQUARE',
    'BUENA PARK': 'UPTOWN',
    'CHINATOWN': 'ARMOUR SQUARE',
    'FULTON MARKET': 'NEAR WEST SIDE',
    'FULTON RIVER DISTRICT': 'NEAR WEST SIDE',
    'GOLD COAST': 'NEAR NORTH SIDE',
    'GOOSE ISLAND': 'NEAR NORTH SIDE',
    'ILLINOIS MEDICAL DISTRICT': 'NEAR WEST SIDE',
    'STREETERVILLE': 'NEAR NORTH SIDE',
    'LAKESHORE EAST': 'LOOP',
    'LAKEVIEW': 'LAKE VIEW',
    'LINCOLN YARDS': 'LINCOLN PARK',
    'LITTLE ITALY': 'NEAR WEST SIDE',
    'LITTLE VILLAGE': 'SOUTH LAWNDALE',
    'MCCORMICK SQUARE': 'NEAR SOUTH SIDE',
    'NEAR NORTH': 'NEAR NORTH SIDE',
    'NOBLE SQUARE': 'WEST TOWN',
    'NORTH BRANCH': 'NEAR NORTH SIDE',
    "O'HARE": 'OHARE',
    'OLD IRVING PARK': 'IRVING PARK',
    'OLD TOWN': 'LINCOLN PARK',
    'PILSEN': 'LOWER WEST SIDE',
    'RAVENSWOOD': 'LINCOLN SQUARE',
    'RIVER NORTH': 'NEAR NORTH SIDE',
    'RIVER WEST': 'NEAR WEST SIDE',
    'ROSCOE VILLAGE': 'NORTH CENTER',
    'SOUTH LOOP': 'NEAR SOUTH SIDE',
    'STREETERVILLE': 'NEAR NORTH SIDE',
    'THE LOOP': 'LOOP',
    'UNIVERSITY VILLAGE': 'NEAR WEST SIDE',
    'WEST LOOP': 'NEAR WEST SIDE',
    'WEST LOOP GATE': 'NEAR WEST SIDE',
    'WICKER PARK': 'WEST TOWN',
    'WRIGLEYVILLE': 'LAKE VIEW',
    'DOWNTOWN': 'LOOP'
}

agg['community'] = agg['community'].replace(community_mapping)

communities_to_drop = ['ARCHITECTURE', 'CITYWIDE', 'DOWNTOWN', 'EVANSTON', 'OAK BROOK', 'OAK PARK', 'SKOKIE', 'SUBURBS']
agg = agg[~agg['community'].isin(communities_to_drop)]


for agg_community in agg['community']:
    if agg_community not in gpdf['community'].values:
        print(f"Community {agg_community} in agg is not present in gpdf.community")

subset = agg[['community','prediction']]
chicago = gpdf.merge(subset, on='community', how='left')
result = chicago.groupby('community')['prediction'].sum().reset_index()

final = gpdf.merge(result, on='community', how='left')
final.to_file('data/predictions_mapping.geojson', driver='GeoJSON')

final['affordable_instance_percentage'] = final['prediction'] / final['prediction'].sum()


final = final.to_crs('EPSG:3857')

fig, ax = plt.subplots(figsize=(10, 10))
ax.set_axis_off()

final.boundary.plot(ax=ax, linewidth=0.3, color='black')
plt.title("Count of Urbanize Chicago\nAffordable Housing Coverage", fontsize=16)
final.plot(column="prediction", cmap="Purples", ax=ax, legend=True)
# for x, y, label in zip(final.geometry.centroid.x, final.geometry.centroid.y, final['area_numbe']):
#     ax.annotate(str(label), xy=(x, y), xytext=(0, 0), textcoords="offset points", ha='center', va='center', color='black', fontsize=10)

plt.savefig("figures/chicago.png", dpi=450)
