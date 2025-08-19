import pandas as pd
import requests
import os
from urllib.parse import urlparse

def download_images_from_csv(file_path, max_downloads, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    df = pd.read_csv(file_path)
    count = 0
    for index, row in df.iterrows():
        if count >= max_downloads:
            break
        name = str(row.iloc[0])
        url = str(row.iloc[1])  # Annahme: URL in zweiter Spalte
        print(f"Verarbeite Eintrag: Name='{name}', URL='{url}'")
        if pd.isna(url) or not isinstance(url, str) or url.strip() == "":
            print("URL ungültig oder leer, überspringe.")
            continue
        parsed_url = urlparse(url)
        file_ext = os.path.splitext(parsed_url.path)[1]
        filename = f"{name}{file_ext}"
        filepath = os.path.join(output_dir, filename)
        try:
            response = requests.get(url, stream=True)
            print(f"HTTP-Statuscode: {response.status_code} für URL: {url}")
            if response.status_code == 200:
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                print(f"Datei heruntergeladen: {filepath}")
                count += 1
            else:
                print(f"Fehler: Datei konnte nicht geladen werden (Status {response.status_code})")
        except Exception as e:
            print(f"Fehler beim Herunterladen: {e}")

if __name__ == "__main__":
    csv_file = "/home/otmar/Downloads/itemimport_202508191150.csv"
    output_folder = "/home/otmar/Downloads/skatechneupics"
    anzahl = int(input("Wie viele Dateien sollen heruntergeladen werden? "))
    download_images_from_csv(csv_file, anzahl, output_folder)
