import pandas as pd
import yaml

class Loader:
    def __init__(self, config_path="config/column_maps.yaml"):
        with open(config_path) as archivo:
            self.map_columnas = yaml.safe_load(archivo)

    def cargar(self, nombre: str) -> pd.DataFrame:
        if nombre not in self.map_columnas:
            raise ValueError(f"'{nombre}' no tiene mapa definido en columnas_map.yaml")

        df = pd.read_csv(f"data/raw/{nombre}.csv")
        mapa = self.map_columnas[nombre]
        df = df.rename(columns=mapa)
        cols = [c for c in mapa.values() if c in df.columns]
        df = df[cols].copy()
        df["origen"] = nombre
        return df

    def cargar_todos(self, nombres: list) -> pd.DataFrame:
        dfs = [self.cargar(n) for n in nombres]
        return pd.concat(dfs, ignore_index=True)