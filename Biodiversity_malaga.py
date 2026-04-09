## 1. Librerías
import pandas as pd
from pygbif import occurrences as occ
import os
## 2. Descarga de datos desde GBIF
os.makedirs("C:/Users/minec/Desktop/malaga-biodiversity/data/raw", exist_ok = True)

print("Download da GBIF")

results = occ.search(taxonKey = 6, country = 'ES', stateProvince = 'Andalucia', hasCoordinate =True, hasGeospatialIssue = False, limit = 1000)

records = results['results']
df = pd.DataFrame(records)

print(f"Records descargados: {len(df)}")
print(f"Colonne dispinibili {len(df.columns)}")
print(df[['species', 'decimalLatitude', 'decimalLongitude', 'elevation']].head(10))

## 3. Limpieza y filtrado de columna
#Creamos dicionario y manteneos columas utiles
cols = ['species', 'decimalLatitude', 'decimalLongitude', 
        'elevation', 'year', 'stateProvince', 'municipality']
df_clean = df[cols].copy()
#Renombamos valore dicionarios por comodidad
df_clean.columns = ['species', 'lat', 'lon', 'elevation', 'year', 'province', 'municipality']

#Buscamos dentro Malaga con coordenadas
df_malaga = df_clean[(df_clean['lat'].between(36.0, 37.5)) & (df_clean['lon'].between(-5.5, -3.5))].copy()

#Quitamos lineas si especies
df_malaga = df_malaga.dropna(subset=['species'])

#Y salvamos en file csv
df_malaga.to_csv('C:/Users/minec/Desktop/malaga-biodiversity/data/raw/malaga_plantas.csv', index= False)

print(f"Record total Andalucía: {len(df_clean)}")
print(f"Record filtrados Málaga: {len(df_malaga)}")
print(f"Especies unicas: {df_malaga['species'].nunique()}")
print(f"Record con elevacióne: {df_malaga['elevation'].notna().sum()}")

#Tenemos solo 38 record con elevación, por eso vamos a descargar más datos de Malága
all_records=[] #creamos lista para datos

#Descargamos más datos de Malága
for offset in range(0, 3000, 300):
    batch = occ.search(taxonKey=6,
        hasCoordinate=True,
        hasGeospatialIssue=False,
        decimalLatitude='36.0,37.5',
        decimalLongitude='-5.5,-3.5',
        limit=300,
        offset=offset
    )
    records_batch = batch['results']
    if not records_batch:
        break
    all_records.extend(records_batch)
    print(f"Scaricati finora: {len(all_records)}")
df2 = pd.DataFrame(all_records)
print(f"\nTotale record: {len(df2)}")
print(f"Colonne: {len(df2.columns)}")

#Repetimos limpieza de lineas sin especias
cols = ['species', 'decimalLatitude', 'decimalLongitude',
        'year', 'family', 'stateProvince', 'locality', 'iucnRedListCategory']

df_malaga2 = df2[cols].copy()
df_malaga2.columns = ['species', 'lat', 'lon', 'year', 'family', 'province', 'locality', 'iucn']

df_malaga2 = df_malaga2.dropna(subset=['species'])
df_malaga2 = df_malaga2[df_malaga2['species'].str.strip() != '']

df_malaga2.to_csv('C:/Users/minec/Desktop/malaga-biodiversity/data/raw/malaga_plantas.csv', index=False)

print(f"Record totali: {len(df_malaga2)}")
print(f"Specie uniche: {df_malaga2['species'].nunique()}")
print(f"Famiglie uniche: {df_malaga2['family'].nunique()}")
print(f"\nSpecie più comuni:")
print(df_malaga2['species'].value_counts().head(10))
print(f"\nFamiglie più comuni:")
print(df_malaga2['family'].value_counts().head(10))

## 4. Creamos Grafica de representación numero de especies
import matplotlib.pyplot as plt
import os

os.makedirs('../results/figures', exist_ok=True)

top_families = df_malaga2['family'].value_counts().head(10)

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(top_families.index[::-1], top_families.values[::-1],
               color='seagreen', edgecolor='white')
ax.set_xlabel('Número de registros', fontsize=12)
ax.set_title('Top 10 Familias Botánicas — Provincia de Málaga\nFuente: GBIF 2024', fontsize=13)

for bar, val in zip(bars, top_families.values[::-1]):
    ax.text(bar.get_width() + 2, bar.get_y() + bar.get_height()/2,
            str(val), va='center', fontsize=10)

plt.tight_layout()
plt.savefig('../results/figures/top_families.png', dpi=150, bbox_inches='tight')
plt.show()
print("Salvato!")
