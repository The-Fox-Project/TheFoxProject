import pathlib
import csv

def create_fox_dir():
    pathlib.Path.home().joinpath('.fox').mkdir(parents=True, exist_ok=True)

def download_exploitdb_csv():
    import requests
    url = "https://gitlab.com/exploit-database/exploitdb/-/raw/main/files_exploits.csv?ref_type=heads"
    response = requests.get(url)
    if response.status_code == 200:
        with open(pathlib.Path.home().joinpath('.fox/files_exploits.csv'), 'w') as f:
            f.write(response.text)


def load_exploitdb_csv():
    with open(pathlib.Path.home().joinpath('.fox/files_exploits.csv'), 'r') as f:
        return list(csv.DictReader(f))