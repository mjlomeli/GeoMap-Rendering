from pathlib import Path
import csv

top = Path(Path.cwd())
backups = Path(Path.cwd()) / Path('Backups')
backups_csv = backups / Path('data.csv')
data = top / Path('data.sqlite')
file = top / Path('data.csv')

class organized:
    def __init__(self):
        self.__backups()
        self.__headers()
        self.__data()
        self.__csv()

    def __backups(self):
        if not backups.exists():
            backups.mkdir()

    def __data(self):
        if not data.exists():
            data.touch()
    def __csv(self):
        if not file.exists():
            file.touch()
            with open(backups_csv, 'r') as f:
                reader = csv.DictReader(f)
                headers = reader.fieldnames
                data = list(reader)
                with open(file, 'w', newline='') as w:
                    writer = csv.DictWriter(w, headers)
                    writer.writeheader()
                    for row in data:
                        writer.writerow(row)


    def __headers(self):
        headers = backups / Path('headers.csv')
        if not headers.exists():
            headers.touch()
