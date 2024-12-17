# Leitura do arquivo

import pandas as pd

taxi = pd.read_csv('202307-divvy-tripdata.csv')
taxi.head()
taxi.shape[0]

# Primeiras impressoes (verificar tipos de dados, se há valores ausentes e duplicatas)
taxi.dtypes
taxi.drop_duplicates()
taxi.isna().sum()

# Selecionando somente as colunas que vou usar

taxi.drop(columns=['start_lat','start_lng','end_lat','end_lng'], inplace = True)

# Lidando com valores nulos para futuras análises

taxi[['start_station_name','end_station_name']] = taxi[['start_station_name','end_station_name']].fillna(value = 'Desconhecido')
taxi[['start_station_id','end_station_id']] = taxi[['start_station_id','end_station_id']].fillna(value=0)

# Transformando colunas de data em data type

taxi['started_at'] = pd.to_datetime(taxi['started_at'], errors='coerce')
taxi['ended_at'] = pd.to_datetime(taxi['ended_at'], errors='coerce')

# Transformando as estações em categoria
col = ['start_station_name','start_station_id','end_station_name','end_station_id']
taxi[col] = taxi[col].astype('category')

# Criando coluna de duração da viagem

taxi['trip_duration_seconds'] = (taxi['ended_at'] - taxi['started_at']).dt.total_seconds()
taxi = taxi[taxi['trip_duration_seconds'] > 0]
taxi['trip_duration_seconds'].describe()

# Filtrar outliers

q3 = taxi['trip_duration_seconds'].quantile(0.75)
q1 = taxi['trip_duration_seconds'].quantile(0.25)
iqr = q3 - q1
lower_bond = q1 - 1.5 * iqr
upper_bond = q3 + 1.5 * iqr

# Como o lower_bond está dando negativo e há valores muito baixo utilizarei o percentil 1
p1 = taxi['trip_duration_seconds'].quantile(0.01)

# Filtrando os dados
taxi = taxi[(taxi['trip_duration_seconds'] >= p1) & 
                 (taxi['trip_duration_seconds'] <= upper_bond)]

taxi['trip_duration_seconds'].describe()

# Analise descritiva por usuario

average_duration_members = taxi.groupby('member_casual')['trip_duration_seconds'].mean().reset_index()
print(average_duration_members)