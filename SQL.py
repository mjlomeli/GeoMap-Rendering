import sqlite3 as sq
from pathlib import Path
import csv

conn = sq.connect('data.sqlite')
curr = conn.cursor()
CSV = Path(Path.cwd()) / Path('data.csv')

BACKUPS = Path(Path.cwd()) / Path('Backups')
HEADERS = BACKUPS / Path('headers.csv')

class sql:
    def __init__(self):
        self.headers = self.__getHeaders()
        self.__createTable()


    def __insert(self, arr):
        curr.execute(self.__getInsert(), tuple(arr))
        conn.commit()

    def __createTable(self):
    	try:
            cmd = "SELECT * FROM Data LIMIT 5;"
            rec = curr.execute(cmd).fetchall()
            if rec == None or len(rec) == 0:
                self.__make_data()
    	except:
    		curr.execute("DROP TABLE IF EXISTS Data")
    		curr.execute(self.__getTable())
    		self.__make_data()

    def __make_data(self):
    	with open(CSV, 'r') as f:
    		reader = csv.DictReader(f)
    		headers = reader.fieldnames
    		data = list(reader)
    		for my_dict in data:
    			values = []
    			values.append(int(my_dict[self.headers[0]]))

    			if my_dict[self.headers[1]] == '':
    				values.append('NaN')
    			else:
    				date_split = my_dict[self.headers[1]].split('/')
    				date = date_split[2] + date_split[1] + date_split[0]
    				values.append(date)

    			values.append(self.__fillnan(my_dict[self.headers[2]]))
    			values.append(self.__fillnan(my_dict[self.headers[3]]))
    			values.append(self.__fillnan(my_dict[self.headers[4]]))
    			values.append(self.__fillnan(my_dict[self.headers[5]]))
    			values.append(self.__fillnan(my_dict[self.headers[6]]))
    			values.append(float(self.__fillzero(my_dict[self.headers[7]])))
    			values.append(int(self.__fillzero(my_dict[self.headers[8]])))
    			values.append(self.__fillnan(my_dict[self.headers[9]]))
    			values.append(self.__fillnan(my_dict[self.headers[10]]))
    			values.append(self.__fillnan(my_dict[self.headers[11]]))
    			values.append(int(self.__fillzero(my_dict[self.headers[12]])))
    			values.append(int(self.__fillzero(my_dict[self.headers[13]])))
    			values.append(int(self.__fillzero(my_dict[self.headers[14]])))
    			values.append(float(self.__fillzero(my_dict[self.headers[15]])))
    			values.append(self.__fillnan(my_dict[self.headers[16]]))
    			values.append(self.__fillnan(my_dict[self.headers[17]]))
    			values.append(int(self.__fillzero(my_dict[self.headers[18]])))
    			values.append(int(self.__fillzero(my_dict[self.headers[19]])))
    			values.append(self.__fillnan(my_dict[self.headers[20]]))
    			values.append(int(self.__fillzero(my_dict[self.headers[21]])))
    			values.append(int(self.__fillzero(my_dict[self.headers[22]])))
    			values.append(int(self.__fillzero(my_dict[self.headers[23]])))
    			self.__insert(values)
    def __fillzero(self, entry):
    	if entry == '':
    		return 0
    	else:
    		try:
    			try:
    				a = int(entry)
    				return entry
    			except:
    				b = float(entry)
    				return entry
    		except:
    			return 0

    def __fillnan(self, entry):
    	if entry == '':
    		return 'NaN'
    	else:
    		return entry

    def __setHeaders(self):
    	with open(CSV, 'r') as f:
    		reader = csv.DictReader(f)
    		headers = reader.fieldnames
    		with open(HEADERS, 'w', newline='') as w:
    			writer = csv.DictWriter(w, headers)
    			writer.writeheader()

    def __getHeaders(self):
    	with open(HEADERS, 'r') as f:
    		reader = csv.DictReader(f)
    		headers = reader.fieldnames
    		if headers == None or len(headers) == 0:
    			self.__setHeaders()
    			self.__getHeaders()
    		else:
    			return reader.fieldnames
    def __getTable(self):
    	s = """
		CREATE TABLE Data(
        	{} INTEGER PRIMARY KEY,
        	{} DATE,
        	{} TEXT,
        	{} TEXT,
        	{} TEXT,
        	{} TEXT,
        	{} TEXT,
        	{} REAL,
        	{} INTEGER,
        	{} TEXT,
        	{} TEXT,
        	{} TEXT,
        	{} INTEGER,
        	{} INTEGER,
        	{} INTEGER,
        	{} FLOAT,
        	{} TEXT,
        	{} TEXT,
        	{} BIT,
        	{} BIT,
        	{} TEXT,
        	{} INTEGER,
        	{} INTEGER,
        	{} INTEGER
		);
    	""".format(*tuple(self.headers))
    	return s

    def __getInsert(self):
    	s = """
		INSERT INTO Data({}, {}, {}, {}, {}, {},
		{}, {}, {}, {}, {}, {},
		{}, {}, {},
		{}, {}, {}, {},
		{}, {}, {}, {}, {})
		Values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    	""".format(*tuple(self.headers))
    	return s