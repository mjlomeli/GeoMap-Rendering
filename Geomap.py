import csv
from pathlib import Path
import sqlite3 as sq
from collections import OrderedDict
import pandas as pd
import numpy as np

conn = sq.connect('data.sqlite')
curr = conn.cursor()
GEO_CSV = Path(Path.cwd()) / Path('geomap.csv')
GEO_SQL = Path(Path.cwd()) / Path('data.sqlite')
GEO_DICT = Path(Path.cwd()) / Path('geomap.txt')
FILES = Path(Path.cwd()) / Path('Files')
GEO_HEADERS = FILES / Path('GEO_Headers.txt')

class geomap:
    def __init__(self):
        self.df = pd.read_csv(GEO_CSV)
        print(df)
        self.headers = self.__getHeaders()
        self.createTable()


    def __insert(self, arr):
        curr.execute(self.__getInsert(), tuple(arr))
        conn.commit()

    def __createTable(self):
    	try:
    		cmd = "SELECT * FROM Map LIMIT 5;"
    		rec = curr.execute(cmd).fetchall()
    	except:
    		curr.execute("DROP TABLE IF EXISTS Map")
    		curr.execute(self.__getTable())
    		self.__make_data()

    def __setHeaders(self):
    	with open(GEO_HEADERS, 'r') as f:
    		reader = csv.DictReader(f)
    		headers = reader.fieldnames
    		with open(GEO_HEADERS, 'w', newline='') as w:
    			writer = csv.DictWriter(w, headers)
    			writer.writeheader()

    def __getHeaders(self):
    	with open(GEO_HEADERS, 'r') as f:
    		reader = csv.DictReader(f)
    		headers = reader.fieldnames
    		if headers == None or len(headers) == 0:
    			self.__setHeaders()
    			self.__getHeaders()
    		else:
    			return reader.fieldnames

    def __getTable(self):
    	s = """
		CREATE TABLE Map(
        	{} TEXT PRIMARY KEY,
        	{} INTEGER,
        	{} INTEGER,
        	{} TEXT,
        	{} DATE,
        	{} INTEGER,
        	{} INTEGER,
        	{} INTEGER,
        	{} Real
		);
    	""".format(*tuple(self.headers))
    	return s

    def __getInsert(self):
    	s = """
		INSERT INTO Map(
		{}, {}, {},
		{}, {}, {},
		{}, {}, {})
		Values(?, ?, ?, ?, ?, ?, ?, ?, ?);
    	""".format(*tuple(self.headers))
    	return s

    def __make_data(self):
    	with open(GEO_CSV, 'r') as f:
    		reader = csv.DictReader(f)
    		headers = reader.fieldnames
    		data = list(reader)
    		for my_dict in data:
    			values = []
    			values.append(self.__fillnan(my_dict[self.headers[0]]))
    			values.append(int(self.__fillzero(my_dict[self.headers[1]])))
    			values.append(int(self.__fillzero(my_dict[self.headers[2]])))
    			values.append(self.__fillnan(my_dict[self.headers[3]]))
    			values.append(self.__fillnan(my_dict[self.headers[4]]))
    			values.append(int(self.__fillzero(my_dict[self.headers[5]])))
    			values.append(int(self.__fillzero(my_dict[self.headers[6]])))
    			values.append(int(self.__fillzero(my_dict[self.headers[7]])))
    			values.append(float(self.__fillzero(my_dict[self.headers[8]])))
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

    def __getitem__(self, comp):
        """
        Overloaded the Computer class to use brackets. To use it place brand, series, model into the brackets.
        For example:
            comp = Computer()
            comp['Apple', 'Mac Book Pro', '00000002', 'Price'] -> '1000.00'
            comp['Apple', 'Mac Book Pro', '00000002'] -> OrderedDict([('Brand', 'Apple'), ... ('Cost', '1000.00')])
            comp['Apple'] -> List of OrderedDict containing all and only 'Apple' products
            comp['Brand'] -> OrderedDict([('Apple', 7), ('Microsoft', 8), ('Dell', 9)])

        comp: string, string, string, 3-tuple of brand, series, modelNo
        return: Dictionary, the information of that particular information.
        """
        cmd = "SELECT {} FROM Map"
        if len(comp) == 3 and isinstance(comp, tuple):
            brand, series, modelNo = comp
            with open(INVENTORY, 'r') as f:
                reader = csv.DictReader(f)
                data = list(reader)
                for my_dict in data:
                    if my_dict['Brand'] == brand and my_dict['Series'] == series and my_dict['Model No'] == self.__model(modelNo):
                        return my_dict
        elif len(comp) == 4 and isinstance(comp, tuple):
            brand, series, modelNo, field = comp
            with open(INVENTORY, 'r') as f:
                reader = csv.DictReader(f)
                data = list(reader)
                for my_dict in data:
                    if my_dict['Brand'] == brand and my_dict['Series'] == series and my_dict['Model No'] == self.__model(modelNo):
                        return my_dict[field]
        elif isinstance(comp, str):
            if not comp in self.FIELD_NAMES:
                field = comp
                with open(INVENTORY, 'r') as f:
                    reader = csv.DictReader(f)
                    data = list(reader)
                    l = []
                    for my_dict in data:
                        for key in my_dict:
                            if my_dict[key] == field:
                                l.append(my_dict)
                    return l
            else:
                field = comp
                with open(INVENTORY, 'r') as f:
                    reader = csv.DictReader(f)
                    data = list(reader)
                    l = OrderedDict()
                    for my_dict in data:
                        for key in my_dict:
                            if key == field:
                                if not my_dict[key] in l:
                                    l[my_dict[key]] = 1
                                else:
                                    l[my_dict[key]] += 1
                    return l

    def __setitem__(self, key, comp):
        """
        Overloaded the Finance class to assign with brackets. To use it place brand, series, model into the brackets, then
        assign the variables necessary: Brand,Series,Model No,Inventory,Graphics Card,Processor,Operating System,Network Card,
        Motherboard,Hard Drive,Ram,Monitor,Price,Cost
        For example:
            comp = Computer()

            comp['Apple', 'Mac Book Pro', '00000001'] = 'Apple','Mac Book Pro','00000001','2','NVIDIA','Intel Core',
            'Windows','801.11ac','GiGabit Motherboard','1 TB','8 GB','20 in', '1200.00', '1000.00'

            print(comp['Apple', 'Mac Book Pro', '00000001']) ->
            OrderedDict([('Brand', 'Apple'), ('Series', 'Mac Book Pro'), ... ,('Monitor', '20 in'), ('Price', '1200.00'),
            ('Cost', '1000.00')])

        key: 3-strings, 3-tuple of brand, series, modelNo
        comp: 14-strings, 14-tuple of Brand,Series,Model No,Inventory,Graphics Card,Processor,Operating System,Network Card,
        Motherboard,Hard Drive,Ram,Monitor,Price,Cost
        """
        with open(INVENTORY, 'r', newline='') as f:
            reader = csv.DictReader(f)
            data = list(reader)
            headers = reader.fieldnames

            if isinstance(key, tuple) and len(key) == 3 and isinstance(comp, tuple) and len(comp) == len(self.FIELD_NAMES):
                b, s, m = key
                brand,series,modelNo,inventory,graphics,processor,os,network,motherboard,drive,ram,monitor,price,cost = comp
                found = False

                f = open(INVENTORY, 'w', newline='')
                writer = csv.DictWriter(f, headers)
                writer.writeheader()
                for row in data:
                    if row['Brand'] == b and row['Series'] == s and row['Model No'] == self.__model(m):
                        row['Brand'] = brand
                        row['Series'] = series
                        row['Model No'] = self.__model(modelNo)
                        row['Inventory'] += str(int(row['Inventory']) + int(inventory))
                        row['Graphics Card'] = graphics
                        row['Processor'] = processor
                        row['Operating System'] = os
                        row['Network Card'] = network
                        row['Motherboard'] = motherboard
                        row['Hard Drive'] = drive
                        row['Ram'] = ram
                        row['Monitor'] = monitor
                        row['Price'] = price
                        row['Cost'] = cost
                        found = True
                    writer.writerow(row)
                if not found:
                    writer.writerow(OrderedDict([('Brand', brand), ('Series', series),\
                    ('Model No', self.__model(modelNo)), ('Inventory', inventory), ('Graphics Card', graphics),\
                    ('Processor', processor), ('Operating System', os), ('Network Card', network),\
                    ('Motherboard', motherboard), ('Hard Drive', drive), ('Ram', ram), \
                    ('Monitor', monitor), ('Price', price), ('Cost', cost)]))

                f.close()
            elif isinstance(comp, dict) and len(comp) == len(self.FIELD_NAMES) and isinstance(key, tuple) and len(key) == 3:
                b, s, m = key
                found = False
                f = open(INVENTORY, 'w', newline='')
                writer = csv.DictWriter(f, headers)
                writer.writeheader()
                for my_dict in data:
                    if my_dict['Brand'] == b and my_dict['Series'] == s and my_dict['Model No'] == m:
                        found = True
                        comp['Inventory'] = str(int(comp['Inventory']) + int(my_dict['Inventory']))
                        my_dict = comp
                        writer.writerow(my_dict)
                    else:
                        writer.writerow(my_dict)
                if not found:
                    writer.writerow(comp)
                f.close()


    def __delitem__(self, comp):
        """
        Deletes an item of the INVENTORY file, ie:

        a = Computer()
        del a['Apple', 'Mac Book Pro', '00000001']
        del a['Apple']
        del a['Mac Book Pro']

        sale: 3-strings, of 3 tuple of brand, series, modelNo
        """

        if len(comp) == 3 and isinstance(comp, tuple):
            brand, series, modelNo = comp
            found = False
            with open(INVENTORY, 'r', newline='') as f:
                reader = csv.DictReader(f)
                data = list(reader)
                headers = reader.fieldnames

            f = open(INVENTORY, 'w', newline='')
            writer = csv.DictWriter(f, headers)
            writer.writeheader()
            for row in data:
                if row['Brand'] == brand and row['Series'] == series and row['Model No'] == self.__model(modelNo):
                    found = True
                else:
                    writer.writerow(row)
            if not found:
                print(f"ERROR: del[{brand}{series}{self.__model(modelNo)} wasn't found.]")

            f.close()
        elif isinstance(comp, str) and comp not in self.FIELD_NAMES:
            field = comp
            found = False
            with open(INVENTORY, 'r', newline='') as f:
                reader = csv.DictReader(f)
                data = list(reader)
                headers = reader.fieldnames

            f = open(INVENTORY, 'w', newline='')
            writer = csv.DictWriter(f, headers)
            writer.writeheader()
            i = 0
            d = data.copy()
            while i < len(d):
                skip = False
                j = 0
                key = list(d[i].keys())
                while not skip and j < len(key):
                    if d[i][key[j]] == comp:
                        found = True
                        skip = True
                        d.remove(d[i])
                    j += 1
                if not skip:
                    writer.writerow(d[i]) #must be out at a certain iteration
                i += 1
            if not found:
                print(f"ERROR: del[{comp}] wasn't found.]")

            f.close()

    def __iter__(self):
        with open(INVENTORY, 'r') as f:
            reader = csv.DictReader(f)
            data = list(reader)
            for my_dict in data:
                yield my_dict

    def __len__(self):
        """
        return: int, the number of rows in the INVENTORY
        """
        with open(INVENTORY, 'r') as f:
            reader = csv.DictReader(f)
            header = reader.fieldnames
            data = list(reader)
            return len(data)

    def __str__(self):
        s = ""
        with open(INVENTORY, 'r') as f:
            reader = csv.DictReader(f)
            data = list(reader)
            for my_dict in data:
                f = ""
                for key in my_dict:
                    f += my_dict[key] + ","
                s += f.rstrip(',') + '\n'
        return s