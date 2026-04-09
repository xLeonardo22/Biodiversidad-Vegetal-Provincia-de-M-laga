# Biodiversidad Vegetal — Provincia de Málaga
Author: Leonardo Di Crisci Salvati

Después de practicar con el proyecto del desierto de Atacama, he intentado
un estudio similar pero con datos de la 
provincia de Málaga.

En este caso usé la API de GBIF para descargar directamente desde 
Python registros reales de ocurrencias de plantas en la provincia. 
Fue un paso más respecto al proyecto anterior porque aquí los datos 
no estaban listos — tuve que descargarlos, filtrarlos y limpiarlos 
yo mismo.

## ¿Qué hace el proyecto?

- Descarga registros reales de plantas en Málaga usando la API de GBIF
- Filtra y limpia los datos para quedarse con los registros útiles
- Analiza qué familias botánicas están más representadas en la provincia

## Resultado principal

Con 2974 registros y 499 especies únicas en 105 familias botánicas, 
los datos confirman la alta biodiversidad vegetal de Málaga.

**Orchidaceae** es la familia más representada, lo que refleja la 
conocida riqueza de orquídeas silvestres de la zona, especialmente 
del género *Ophrys*.

## Datos

Descargados directamente desde GBIF via pygbif:  
https://www.gbif.org

## Tecnologías

- Python 3.11
- pandas — manipulación de datos
- pygbif — acceso a la API de GBIF
- matplotlib — visualización

## Estructura

```
malaga-biodiversity/
├── data/raw/
│   └── malaga_plantas.csv
├── notebooks/
│   └── 01_analysis.ipynb
└── results/figures/
    └── top_familias_botanicas.png
```
