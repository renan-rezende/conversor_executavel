import openmeteo_requests
import requests_cache
from retry_requests import retry
import pandas as pd
import os
import tkinter as tk

###################################### ----------- I.N.P.U.T.S -- D.O -- U.S.U.A.R.I.O ----------- ######################################

# Função para mostrar a tela principal
def show_main_window():
    loading_window.destroy()  # Fecha a janela de carregamento
    
    # Cria a janela principal
    global pastDays, forecastDays, root
    pastDays = None
    forecastDays = None

    root = tk.Tk()
    root.title("Selecione o intervalo de dias")

    # Rótulos e entradas para os números
    tk.Label(root, text="Dias atrás:").grid(row=0, column=0, padx=10, pady=10)
    entry1 = tk.Entry(root)
    entry1.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(root, text="Dias após hoje:").grid(row=1, column=0, padx=10, pady=10)
    entry2 = tk.Entry(root)
    entry2.grid(row=1, column=1, padx=10, pady=10)

    # Botão para processar os números
    def obter_entradas():
        global pastDays, forecastDays
        try:
            # Obtém os valores inseridos
            pastDays = int(entry1.get())
            forecastDays = int(entry2.get())
            root.destroy()  # Fecha a janela após a obtenção dos valores
        except ValueError:
            error_label.config(text="Por favor, insira números válidos!")

    submit_button = tk.Button(root, text="PRONTO", command=obter_entradas)
    submit_button.grid(row=2, column=0, columnspan=2, pady=20)

    # Rótulo para exibir mensagens de erro
    error_label = tk.Label(root, text="", fg="red")
    error_label.grid(row=3, column=0, columnspan=2)

    # Inicia o loop da interface gráfica
    root.mainloop()

# Cria a janela de carregamento
loading_window = tk.Tk()
loading_window.title("Carregando...")
loading_label = tk.Label(loading_window, text="Carregando, por favor aguarde...", font=("Arial", 14))
loading_label.pack(padx=20, pady=20)

# Configura o fechamento da janela de carregamento após 3 segundos
loading_window.after(3000, show_main_window)

# Inicia o loop da interface gráfica para a janela de carregamento
loading_window.mainloop()
###################################### ----------- A.P.I -- O.P.E.N -- M.E.T.E.O.R ----------- ######################################

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://api.open-meteo.com/v1/forecast"
params = {"latitude": -20.8058,
          "longitude": -40.6456,
          "hourly": ["temperature_2m", 
          "relative_humidity_2m", 
          "precipitation", 
          "surface_pressure", 
          "cloud_cover", 
          "wind_speed_10m", 
          "wind_direction_10m", 
          "shortwave_radiation"],
          "wind_speed_unit": "ms","timezone": "America/Sao_Paulo","past_days":{pastDays},"forecast_days":{forecastDays},"models": "best_match"}
responses = openmeteo.weather_api(url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]
print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation {response.Elevation()} m asl")
print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

# Process hourly data. The order of variables needs to be the same as requested.
hourly = response.Hourly()
hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
hourly_precipitation = hourly.Variables(2).ValuesAsNumpy()
hourly_surface_pressure = hourly.Variables(3).ValuesAsNumpy()
hourly_cloud_cover = hourly.Variables(4).ValuesAsNumpy()
hourly_wind_speed_10m = hourly.Variables(5).ValuesAsNumpy()
hourly_wind_direction_10m = hourly.Variables(6).ValuesAsNumpy()
hourly_shortwave_radiation = hourly.Variables(7).ValuesAsNumpy()

hourly_data = {"date": pd.date_range(
    start = pd.to_datetime(hourly.Time(), unit = "s", utc = True).tz_convert("America/Sao_Paulo"),
    end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True).tz_convert("America/Sao_Paulo"),
    freq = pd.Timedelta(seconds = hourly.Interval()),
    inclusive = "left"
)}
hourly_data["temperature_2m"] = hourly_temperature_2m
hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
hourly_data["precipitation"] = hourly_precipitation
hourly_data["surface_pressure"] = hourly_surface_pressure
hourly_data["cloud_cover"] = hourly_cloud_cover
hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
hourly_data["wind_direction_10m"] = hourly_wind_direction_10m
hourly_data["shortwave_radiation"] = hourly_shortwave_radiation

hourly_dataframe = pd.DataFrame(data = hourly_data)

###################################### ----------- C.O.N.V.E.R.S.O.R ----------- ######################################

def xlsx_to_sam(xlsx_file, sam_file):
    # Ler o arquivo XLSX (assumindo que as colunas são Data, Hora, Temperatura, Umidade, Pressão, etc.)
    df = pd.read_excel(xlsx_file)
    df['date'] = df['date'].astype(str)


    # Cria novas 3 colunas para de ano, Mês e Dia (separa a coluna "time" em 3)
    df['YR'] = df['date'].str.slice(2, 4)    # Últimos dois dígitos do ano
    df['MO'] = df['date'].str.slice(5, 7)    # Mês
    df['DA'] = df['date'].str.slice(8, 10)   # Dia
    df['HR'] = df['date'].str.slice(11, 13)  # Hora
    
    df = df.drop(columns=['date'])

    # Abrir o arquivo SAM para escrita
    with open(sam_file, 'w') as sam:

        sam.write("~    1 ANCHIETA               ES  -3  S20 48  W040 36    10\n")
        sam.write(f"~YR MO DA HR I    1    2       3       4       5  6  7     8     9  10   11  12    13     14     15        16   17     18   19  20      21\n")

        for index, row in df.iterrows():

            sam.write(f"{''} {row['YR']:>2} {row['MO']:>2} {int(row['DA']):>2} {int(row['HR']):>2} {'0 9999 9999':>} {row['shortwave_radiation']:>4} {'?0 9999 ?0 9999 ?0'} {row['cloud_cover']/10:>2.0f} {row['cloud_cover']/10:>2.0f} {row['temperature_2m']:>5} {'9999.'} {row['relative_humidity_2m']:>3} {int(row['surface_pressure'])} {int(row['wind_direction_10m']):>3} {row['wind_speed_10m']:>5} 99999. 999999 999999999 9999 99999. 9999 999      0\n")

# Salvar o DataFrame como arquivo Excel
hourly_dataframe['date'] = hourly_dataframe['date'].dt.tz_localize(None)
excel_file = 'arquivo.xlsx'
hourly_dataframe.to_excel(excel_file, index=False, engine='openpyxl',float_format='%.1f')


# Criar a pasta de saída, se não existir
output_folder = 'arquivos'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Definir o nome do arquivo SAM
sam_file = os.path.join(output_folder, 'dados_meteorologicos.sam')

# Chamar a função de conversão
xlsx_to_sam(excel_file, sam_file)

