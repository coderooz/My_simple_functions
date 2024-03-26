import sqlite3, csv, json
import pandas as pd
from functions.DataHandlers import valreplace, equalizer_dict
from functions.FileHandler import getExtention, read, fileExists, write, write_csv
from collections.abc import KeysView, ValuesView
import mysql.connector as myqC
from datetime import datetime

class SqliteHandler():
    """
        The `DbSqliteHandler` class simplifies interactions with SQLite3 databases in Python, offering a dynamic and efficient approach. It is designed to accelerate the development of database-related projects using Python's SQLite3 module.

        Features:
            - Insert Data (insert)
            - Fetch Data (fetch)
            - Display Data (displayData)
            - Execute Custom SQL (execute)
            - Get Table Names (getTb)
            - Check Index Existence (checkIndex)
            - Add Index (addIndex)
            - Close Database Connection

        Initialization:
        ---------------
        To use `DbSqliteHandler`, create an instance by providing the database name (`dbname`) and an optional path to the database directory (`dbPath`). If no path is specified, the database will be created in the current working directory.

        Example:
        ```python
        db_handler = SqliteHandler("my_database.db", "path/to/database/directory")
        ```

        Insert Data (insert):
        ---------------------
        Insert data into a specified table using the `insert` method. Provide the table name (`table`), column names (`columns`), and a list of values to be inserted (`values`).

        Example:
        ```python
        db_handler.insert("my_table", "column1, column2", (value1, value2))
        ```

        Fetch Data (fetch):
        -------------------
        Retrieve data from a table with the `fetch` method. Specify the table name (`table`) and optionally, specific columns to retrieve (`columns`). You can also provide a custom SQL query for advanced retrieval.

        Example:
        ```python
        data = db_handler.fetch("my_table", "column1, column2", "column1 = 'some_value'")
        ```

        Execute Custom SQL (execute):
        -----------------------------
        Execute custom SQL queries using the `execute` method. Provide the SQL code as the `data` parameter. Use `multi=True` for executing multiple statements within a single call.

        Example:
        ```python
        db_handler.execute("CREATE TABLE new_table (column1 TEXT, column2 INTEGER);", multi=True)
        ```

        Database Management:
        --------------------
        `DbSqliteHandler` provides various methods for managing tables and indexes, including creating, renaming, cleaning, or deleting tables.

        Example (Creating a Table):
        ```python
        db_handler.createTb("new_table", ["column1 TEXT", "column2 INTEGER"])
        ```

        Closing the Connection:
        -----------------------
        To close all connections and end the session, call the `close_connection` method.

        Example:
        ```python
        db_handler.close_connection()
        ```

        `DbSqliteHandler` offers a flexible and efficient way to interact with SQLite3 databases in Python, simplifying database-related tasks and enhancing the productivity of your projects.
    """
  
    def __init__(self, dbname, dbPath:str='.', json_import:bool=False, default_timeout:int=5000):
        """
            Initializes the DbSqliteHandler instance.

            Parameters:
                - `dbname` (str): The name of the database.
                - `dbPath` (str, optional): The path to the database directory. Default is None.
        """
        self.db_init = None
        self.db_conn = None
        self.dbName = dbname
        self.dbPath = dbPath
        self.dbFullPath = self.dbPath+'/'+self.dbName
        ext = getExtention(self.dbFullPath)

        if json_import and ext == 'json':
            self.load_dbJson(self.dbFullPath, True)
        elif ext == 'db':
            self.db_init = sqlite3.connect(self.dbFullPath)    
            self.db_conn = self.db_init.cursor()
        else: 
            raise TypeError('File type error! only excepts json file containing dbcreating data or the db path.')
   
        self.DbtimeOut(default_timeout)

    def execute(self, query, data:list=[], multi: bool = False, auto_commit=True):
        """
            execute()
            ---------
            
            Executes SQLite-related code.

            Parameters:
                - `query` (str): The SQL code to execute.
                - `data` (list): Takes the list of values. Default is [].
                - `multi` (bool): True if executing multiple statements. Default is False.
                - `auto_commit` (bool): True to commit changes automatically after execution. Default is True.

            Returns:
                sqlite3.Cursor: The result of the executed query.

            If Error/Or exceptions:
                Prints out exceptions and rolls back the transaction if auto_commit is True.
            
        """
        try:
            if multi==True and data!=[]:
                result = self.db_conn.executemany(query, data)
            else:
                result = self.db_conn.execute(query)
            if auto_commit:
                self.db_init.commit()
            return result
        except sqlite3.Error as e:
            print("SQLite error:", e)
            if auto_commit: self.db_init.rollback()
        return None

    # --- Data handleing --- #

    
    def insert(self, table:str, columns, values, createTb:bool=False):
        """
            Inserts data into the specified table.

            Parameters:
                - `table` (str): The name of the table to insert data into.
                - `columns` (str, list, KeysView): Comma-separated column names.
                - `values` (list): List of values to be inserted.
                - `createTb` (bool): This will create a table in the db if not available. Default is `False`.

            Returns:
                sqlite3.Cursor: The result of the executed query.
        """
        if createTb==True and self.getTb(table_name=table) == False: self.createTb(tbName=table, columns=columns, primary_key='id')
        k=False
        if isinstance(columns, (KeysView, list, tuple, ValuesView)):
            keys = ['INDEX','KEY','SELECT','INSERT','UPDATE','DELETE','FROM','WHERE','JOIN','INNER','LEFT','RIGHT','GROUP BY','ORDER BY','AS','COUNT','SUM','MAX','MIN','AVG','DISTINCT','AND','OR','NOT','BETWEEN','LIKE','IN','NULL','TRUE','FALSE','TOP','LIMIT','OFFSET']
            for k in keys:
                columns = valreplace(columns, k, '_'+k.upper(), 1) # type: ignore
                columns = valreplace(columns, k.lower(), '_'+k.lower(), 1) # type: ignore
            columns = ','.join(columns)

        if isinstance(values, (KeysView, list, tuple, ValuesView)):
            value = []
            for val in values:
                if isinstance(val, (KeysView, list, tuple, ValuesView)):
                    value.append(str(tuple(val)))
                
                elif isinstance(val, str):
                    value = str(tuple(values))
                    return self.execute(f'INSERT INTO {table} ({columns}) VALUES {value};')
            value = ','.join(value)
            k = self.execute(f'INSERT INTO {table} ({columns}) VALUES {value} ;')
        elif isinstance(values, str):
            # print(values)
            k = self.execute(f'INSERT INTO {table} ({columns}) VALUES ({values});')
        else: raise ValueError('Invalid input format! Please provide a valid set of values.')
        return k
    
    def json_insert(self, table_name:str, data, createTb:bool=False, ifExist:str=''):
        '''
            JSON_INSERT()
            -------------

            This method is used to insert data into the table using json format data.
            Parameters:
                - `table_name` (str):This parametere of the method tales the name of the table in which the data is to inserted.
                - `data` (list|dict): This parameter takes the data either in dict format or a list containing dicts if multiple entries are to add.
                - `createTb` (bool): ..
                - `ifExist` (list): A list of fields that should exist before inserting the record. If any field does not 
                - return None
        '''
              
        table_column = self.getColumnNames(table_name)
                    
        if isinstance(data, dict):
            col, query = [], []
            for k,i in data.items():
                if k in table_column and isinstance(i, (str, float, int)):
                    col.append(k)
                    query.append(i)   
        elif isinstance(data, list) and len(data) > 0:
            data = equalizer_dict(data)
            col = data[0].keys()
            query = [list(i.values()) for i in data]
        else:raise ValueError('The data type passed is invald. The data paramerter takes a dict or a list of dict.')
        
        col = list(col)
        if ifExist!='':
            check_data = self.fetch_unique(table_name, ifExist)
            check_data = {ifExist: check_data} if isinstance(check_data, list) else check_data
            for k,v in check_data.items():
                col_idx = col.index(k)
                query = [val for val in query if val[col_idx] not in v]
        
        return self.insert(table_name, col, query, createTb)       

    def update(self, table:str, updatedata, condition:str=''):
        """
            update()
            --------

            This method is to update data in the table 

            Parameter:
                - `table`: This parameter takes the name of the table.
                - `updatedata`: This parameter takes the data that is to updated.           
                    - `"ColumnName='data1' AND ColumnName2='data2'"  OR  {'ColumnName':'data1', 'ColumnName2':'data2'}
                    `
                - `condition`: This parameter is set where the data is to be updated.
                    - `id='5'`
                    Default is ''. If left empty, then the update will happen all over the column which is specified.
            
            Return:
                - `bool`: This method returns a boolean. True is success or False for failed opeeration.s

            Usage Example:
            ```
                # assumning cl is the class like.
                updatedata = "user_email='alex123@gmail.com'"
                condition = "name='Alex'"
                cl.update('tableName', updatedata, condition)
            ```
        """
        condition = f'WHERE {condition}' if condition!='' else ''
        if isinstance(updatedata, dict):
            updatedata = ', '.join(["{}='{}'".format(k,v) for k,v in updatedata.items()])
        t = self.execute(f'UPDATE {table} SET {updatedata} {condition};')
        if t : return True
        return False

    def fetch(self, table:str, columns:str='*', query='', limit:int=0, Offset:int=0, fetchAll:bool=True,assc:str='', desc:str='', detailed:bool=True):
        """
            fetch()
            -------

            Fetches data from the specified table based on the query.

            Parameters:
                - `table` (str): The name of the table to fetch data from.
                - `query` (str|list|dict|optional): The SQL query/Search parameter that is to be executed.
                - `columns` (str): The columns that needs to be fetched.
                - `limit` (int, optioanl): This parameter is to set the number of columns to fetch.
                - `offset` (int, optional): The parameter if speciied will get the columns from the limit number pf columns to the number specifed in this parameter. eg: from column 5 to 23. This parameter will only be in effect of the limit parameter is use.
                - `fetchAll` (bool, optional): The columns that needs to be fetched.
                - `desc` (str, True, optional): The columns that are to be fetched in descending order.

            Returns:
                sqlite3.Row or list of sqlite3.Row: The fetched data.

            Usage Example:
                ```
                # assumning cl is the class like.
                columns =  "column1, column2"
                query = "column1 = 'some_value'"
                desc = "column2"
                data = cl.fetch("my_table", columns, query, True, desc)
            ```
        """
        
        if self.getTb(table) == False: 
            raise ValueError(f'The table({table}) is not present in the database.')
    
        if isinstance(query, str) and query!='':
            query = f' WHERE {query}'
        elif isinstance(query, list)and len(query) > 0:
            query = ' WHERE ' + ' AND '.join(query)
        elif isinstance(query, dict)and len(query.keys()) > 0:
            query = ' WHERE ' + ' AND '.join([f"{k}='{v}'" for k,v in query.items() if v!=None or v!='']) 
            
        order = ''
        if desc != '' or assc != '':
            order = ' ORDER BY '
            col = self.getColumnNames(table)
            if desc != '' :
                order += ' DESC' if desc==True else f'{desc} DESC' if desc in col else ''
            if assc != '' :
                order += ' ASC' if desc==True else f'{desc} ASC' if assc in col else ''
            
        if limit > 0:
            Offset = f' OFFSET {Offset}' if 0 < Offset < limit else ''
            limit = f' LIMIT {str(limit)}' + Offset
        else:
            limit = ''
            
        ret = self.execute(f'SELECT {columns} FROM {table}{query}{order}{limit};')
        try:
            if ret is not None:
                
                if detailed==False:
                    if fetchAll: return ret.fetchall()
                    else: return ret.fetchone()
                else:
                    col = [column[0] for column in ret.description] if ret.description else []
                    if fetchAll: return [dict(zip(col, row)) for row in ret.fetchall()]
                    elif ret.fetchone() is not None:  return dict(zip(col, ret.fetchone()))
            else: return []
        except Exception as e:
            print(e)
            return []

    def getTbData(self, table_name:str,columns:str='*',query:str='', limit:int=0, offset:int=0, fetchAll:bool=True, desc:str=''):
        """
            Retrieves data from the specified table and returns it in a pandas DataFrame format.

            Parameters:
                - `table_name` (str): The name of the table to fetch data from.
                - `columns` (str, optional): The columns to retrieve. Default is '*'.
                - `query` (str, optional): The SQL query or condition for data retrieval. Default is an empty string.
                - `limit` (int, optional): This parameter takes the number of columns that are to be fetched.
                - `offset` (int, optional): The parameter if speciied will get the columns from the limit number pf columns to the number specifed in this parameter. eg: from column 5 to 23. This parameter will only be in effect of the limit parameter is use.
                - `fetchAll` (bool, optional): True to fetch all rows, False to fetch only the first row. Default is True.
                - `desc` (str, optional): This parameter, if specified will get the data from the table in descending order by the name of the column mentioned.
            Returns:
                pd.DataFrame: A DataFrame containing the fetched data.

            Example:
                ```python
                data_frame = db_handler.getTbData("my_table", "column1, column2", "column1 = 'some_value'")
                ```

            Note:
                This method is similar to the fetch function, but it returns the data in a pandas DataFrame format.
            """
        if self.getCount(table_name) > 0:
            data = self.fetch(table_name,columns, query, limit, offset, fetchAll, desc)
            return pd.DataFrame(data, index=None)
        else:
            print(f'The table(`{table_name}`) is empty with no data.') 
            return False

    ### Table work/ altering related method. ###

    def fetch_unique(self, table:str, column:str):
        """
            fetch_unique()
            --------------
            This method fetches the unique values of a column.

            Parameter:
            - table str: Takes the name of the table.
            - column str: takes the name of the columns whose unique data is to fetched.
        """
        column = column.split(',')
        columnList = self.getColumnNames(table)
        if len(column) > 1:
            return {k: self.fetch_unique(table, k) for k in column if k in columnList}
        elif len(column) == 1:
            column = column[0]
            data = self.fetch(table, f'DISTINCT {column}')
            data = [i[column] for i in data] if len(data) > 0 else []
            return data

    def load_dbJson(self, data=None, fileName:bool=False)->None:
        """
            This method will create the database with all its tables table and values(if provided).
        """
        if fileName and fileExists(data):
            self.load_dbJson(read(data, decode_json=True))
        elif isinstance(data, (str, dict)) and fileName==False:
            data = json.dumps(data) if isinstance(data, str) else data
            self.dbName = data['db_name']
            self.db_init = sqlite3.connect(self.dbPath+'/'+self.dbName)    
            self.db_conn = self.db_init.cursor()
            for table in data['tables']:
                print(table['table_name'])
                self.createTb(table['table_name'], table['column_names'])
                if table['data'] != []:
                    self.insert(table['table_name'], table['column_names'], table['data'])
                if table['indexs'] != []:
                    [self.addIndex(idx['index_name'], idx['cols']) for idx in table['indexs']]
        else:
            raise ValueError('Check the value given passed as arguments.')

    def export_data(self, catg:str='json', tableName:str=''):
        if catg=='json':
            data = {'db_name': self.dbName,'tables':[],'created_on': str(datetime.now().strftime('%d-%m-%Y %H:%M:%S %p'))}
            for tb in self.getTb():
                k=self.get_info(tb)
                if k['rows'] > 0:
                    k['data'] = self.fetch(tb, detailed=False)
                data['tables'].append(k)
            write(f'{self.dbPath}/{self.dbName.replace('.','_')}.json', data, emptyPervious=True)
        elif catg=='xls':
            pass
            # write(f'{self.dbPath}/{self.dbName.replace('.','_')}.csv', data, emptyPervious=True)
        elif catg == 'csv':
            pass
        else: raise ValueError('The type of file given is not accepted.')
    
    def getCount(self, table_name:str,  columns:str='*', query:str='')->int:
        """
            getCount:
            =========

            This mehtod is to count the number of the row present in the table according the the query.

            Args:
                - `table_name` (str): Takes the name of the table.
                - `columns` (str)   : Takes the name of the column that is to be counted.
                - `query` (str)     : Takes the search query by which the table is to be counted. 

            Return:
                int : Returns the number of rows present n tahe tble according to the query. 
        """
        to = f'COUNT({columns})'
        col = self.fetch(table_name, to, query, detailed=False)
        if col != []:
            try:
                return int(col[0][0])
            except:
                return col
        return False

    def alterTb(self, tbName:str, queryType:str, modify):
        """This method is to alter tables data.

        Args:
            tbName (str): parameter takes the name of the table.
            queryType (str): This parameter takes the data in string format is to specify where to alter.
            modify (list): This parameter takes the data in list format is to specify what to alter with.

        Returns:
            _type_: _description_
        """
        if isinstance(modify, list):
            modify = str(','.join(modify))
        query =f'ALTER TABLE {tbName} {queryType.upper()} {modify};'
        return self.execute(query)

    def csv_insert(self, table_name:str, csv_file_path:str):
        """
            Creates a table (if it doesn't exist) and adds data from a CSV file.

            Parameters:
                table_name (str): The name of the table to be created or used.
                csv_file_path (str): The path to the CSV file containing data to be inserted into the table.

            Returns:
                bool: True if the operation is successful, False otherwise.
        """
        try:
            if not self.getTb(table_name):
                with open(csv_file_path, 'r') as csvfile:
                    csv_reader = csv.reader(csvfile)
                    headers = next(csv_reader)
                    column_types = ['TEXT' for _ in headers]
                    columns = [f"{header} {column_type}" for header, column_type in zip(headers, column_types)]
                    self.createTb(table_name, columns)

            with open(csv_file_path, 'r') as csvfile:
                csv_reader = csv.DictReader(csvfile)
                csv_data = [row for row in csv_reader]
            json_data = json.dumps(csv_data, indent=2)
            return self.json_insert(table_name, json_data)
        except Exception as e:
            print(f"Error: {e}")
            return False

    def get_excel(self, tbName:str='',  columns:str='*', query:str='', fetchAll:bool=True, desc:str='', fileName:str='', filePath:str='.'):
        """
           This method get the specified table and saves the data in the file
        
            Args:
                tbName (str): _description_
                columns (str, optional): _description_. Defaults to '*'.
                query (str, optional): _description_. Defaults to ''.
                fetchAll (bool, optional): _description_. Defaults to True.
                desc (str, optional): _description_. Defaults to ''.
                fileName (str, optional): _description_. Defaults to ''.
                filePath (str, optional): _description_. Defaults to './'.

            Returns:
                file: Returns a saved file.
        """
        try:
            data = self.getTbData(tbName,columns,query,fetchAll, desc)
            fileName = fileName if fileName!=None else f'{tbName}.csv'
            fileName = f'{filePath}/{fileName}'
            data.to_csv(fileName, index=False)
            return 1

        except Exception as e:
            print(e)
            return 0

    def beginTransaction(self):
        """Begin a transaction."""
        self.db_init.isolation_level = None
        self.execute("BEGIN TRANSACTION;")

    def commitTransaction(self):
        """Commit the current transaction."""
        self.execute("COMMIT;")
        self.db_init.isolation_level = ''

    def rollbackTransaction(self):
        """Roll back the current transaction."""
        self.execute("ROLLBACK;")
        self.db_init.isolation_level = ''  # Auto-commit mode is turned on

    def getColumnNames(self, table_name):
        """
            Fetches the column names of a specified table.

            Parameters:
                table_name (str): The name of the table.

            Returns:
                list: A list of column names.
        """
        query = f"PRAGMA table_info({table_name});"
        result = self.execute(query)
        columns = [row[1] for row in result.fetchall()]
        return columns

    def get_info(self, table_name:str=''):
        """
            Retrieve information about a specific table in an SQLite database.

            Parameters:
                table_name (str): The name of the table to retrieve information about.

            Returns:
                dict or None: A dictionary containing table information, or None if an error occurs or the table does not exist.

            The returned dictionary contains the following keys:
            - table_name: The name of the table or the entire Database. Default is ''. This means that it will give the info of the intire table
            - table_description: A description of the table (if available).
            - column_names: A list of column names in the table.
            - column_types: A list of column data types corresponding to the column names.
        """
        try:
            if table_name == '':
                return {i: self.get_info(i) for i in self.getTb()}
            else:
                columns_info = self.execute(f"PRAGMA table_info({table_name})").fetchall()
                if not columns_info:  return None
                column_names = [info[1] for info in columns_info]
                column_types = [info[2] for info in columns_info]
                keyType = ['', 'PRIMARY KEY','SECONDARY KEY']
                keys = [keyType[int(info[5])] for info in columns_info]
                return {'table_name': table_name,'column_names':[' '.join(k).strip() for k in zip(column_names, column_types, keys)],'rows': self.getCount(table_name), 'indexs':self.getIndexes(table_name)}
        except sqlite3.Error as e:
            print(f"Error: {e}")
            return None

    def getTb(self, table_name:str=None):
        '''
            getTb()
            -------

            This method is to get the list of all the tables present in the database.
            Additional: This method also has the function to check if the table exists or not.
            
            Parameter:
                - `table_name` (str): This parameter takes the name of the table to look for.
            
            Return:
                - If the table_name parameter is given the either it will be returned bool true or else false. If the table_name is not added then a list of tables will be returned.
        '''
        result = self.execute("SELECT name FROM sqlite_master WHERE type='table';")
        data = [row[0] for row in result.fetchall()]
        if table_name == None:return data
        elif table_name != None and table_name in data: return True
        else: return False

    def DbtimeOut(self, timeout:int=0):
        if timeout == 0:
            timeout = self.default_timeout
        else:
            self.default_timeout=timeout

        self.execute(f'PRAGMA busy_timeout = {timeout};')

    def getIndex(self, tbName:str, idxName:str):
        """Check if the index exists in the table."""
        result = self.execute(f"PRAGMA index_info({idxName});")
        return len(result.fetchall()) > 0

    def getIndexes(self, tbName:str=''):
        """
            getIndexes()
            ------------

            This methods gets the list of indexes.

            Parameeter:
                - `tbName`: Takes the name of the table.
        """
        '''This method is to get the list of the indexes related in the table.'''
        if tbName:
            query = f"PRAGMA index_list({tbName});"
        else:
            query = "PRAGMA index_list;"
        result = self.execute(query)
        return [row[1] for row in result.fetchall()]

    def addIndex(self, table:str, indexName:str, coloumns:str):
        '''This method adds an INDEX in the table presented using the provided coloumns.'''
        return self.execute(f'CREATE INDEX {indexName} ON {table} ({coloumns});')

    def delIndex(self, tbname:str, idxName:str):
        '''This method is to delete an exiting index realted to a table.'''
        return self.execute(f'DROP INDEX {idxName} ON {tbname};')

    def createTb(self, tbName: str, columns, primary_key: str = '', addUnique:str='', indexCol:str='', indexName:str=''):
        """Creates a table in the database.

        Parameters:
            tbName (str): The name of the table to be created.
            columns (List[str]): A list of column names and their data types.
            primary_key (str, optional): The primary key for the table. Default is 'id'.

        Returns:
            bool: True if the operation is successful, False otherwise.
        """
        try:
            keys = ['INDEX','SELECT','INSERT','UPDATE','DELETE','FROM','WHERE','JOIN','INNER','LEFT','RIGHT','GROUP BY','ORDER BY','AS','COUNT','SUM','MAX','MIN','AVG','DISTINCT','AND','OR','NOT','BETWEEN','LIKE','IN','NULL','TRUE','FALSE','TOP','LIMIT','OFFSET']
        
            for k in keys:
                columns = valreplace(columns, k, '_'+k.upper(), 1)
                columns = valreplace(columns, k.lower(), '_'+k.lower(), 1)
                

            if primary_key != '':
                primary_key = primary_key if primary_key not in keys else f'_{primary_key}'
                columns = [f"{primary_key} INTEGER PRIMARY KEY AUTOINCREMENT"] + columns
            
            if addUnique!='':
                columns.append(f"UNIQUE({addUnique})")

            query = f"CREATE TABLE IF NOT EXISTS {tbName} ({', '.join(columns)});"
            self.execute(query)
            
            if indexCol!='':
                indexName = f'{tbName}_idx' if indexName=='' else indexName
                self.addIndex(tbName, indexName, indexCol)
            
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def renameTb(self, tableName1:str, tableName2:str):
        """ This method is to be used to rename the tables provided in the parameter tabeName1 with the value provided in the parameter tableName2."""
        return self.alterTb(tableName1,'RENAME TO', tableName2)
    
    def cleanTb(self, tableName:str, query:str=''):
        """This method is to be used to clean the provided tables clean of any data in it."""
        query = f'WHERE {query}' if query!='' else ''
        self.execute(f'DELETE FROM {tableName}{query};')
        if query == '':
            self.execute(f"DELETE FROM sqlite_sequence WHERE name='{tableName}'")
        else: 
            self.update('sqlite_sequence', {'seq': self.getCount(tableName)}, f"name='{tableName}'")

    def addUniqueColumns(self, table:str, name:str, uniques) -> None:
        """
            This method will set unique value to the columns such that if user want to enter a value which already exists then it will reject.
        """
        if isinstance(uniques, (list, KeysView, ValuesView)):
            uniques = ','.join(uniques)
        self.alterTb(table, 'ADD CONSTRAINT', f'{name} UNIQUE({uniques})')

    def delUnique(self, table_name:str, name:str)->None:
        """
            This method delete the unique charectersitics of the table column constrain with the provideed name.
        """
        self.alterTb(table_name, 'DROP', f'CONSTRAINT {name}')

    def delTb(self, tableName:str):
        """This method is for the use of deleting tables if it exists."""
        for i in self.getIndexes(tableName):
            self.delIndex(tableName, i)
        return self.execute(f'DROP TABLE IF EXISTS {tableName};')

    def addColumn(self, table_name:str, new_column_name, data_type:str, adjacent_column_name:str, column_param:str='', after=True):
        """
            Adds a new column to the specified table before or after a specific column.

            Parameters:
                table_name (str): The name of the table to add the column to.
                new_column_name (list, str, optional): The name of the new column.
                data_type (str): The data type for the new column (e.g., "INTEGER", "TEXT", "REAL").
                adjacent_column_name (str): The name of the column before or after which the new column should be added.
                after (bool, optional): True to add the new column after the specified column, False to add it before. Default is True.

            Returns:
                sqlite3.Cursor: The result of the executed query.
        """
        temp_table_name = f"temp_{table_name}"   
        try:
            info = self.get_info(table_name)
            columns = info['column_names']
            col_index = [i for i, x in enumerate(self.getColumnNames(table_name)) if adjacent_column_name == x][0]
            if after: 
                col_index+= 1
            if isinstance(new_column_name, list):
                for i in new_column_name:
                    columns.insert(col_index, f"{i} {data_type} {column_param}")     
                    col_index += 1
            elif isinstance(new_column_name, str):
                columns.insert(col_index, f"{new_column_name} {data_type} {column_param}")        
        
            self.createTb(temp_table_name, columns)
            if info['rows'] > 0 :
                data = self.fetch(table_name)
                if isinstance(new_column_name, list):
                    for nm in new_column_name:
                        data[0][nm]= ''
                elif isinstance(new_column_name, str):
                    data[0][new_column_name]= ''
                self.json_insert(temp_table_name, equalizer_dict(data))
            self.delTb(table_name)
            self.renameTb(temp_table_name, table_name)
            return True
        except Exception as e:
            self.delTb(temp_table_name)
            return False

    def renameColumn(self, table_name:str, old_column_name:str, new_column_name:str):
        """
        Renames a column in the specified table.

        Parameters:
            table_name (str): The name of the table.
            old_column_name (str): The current name of the column to be renamed.
            new_column_name (str): The new name for the column.

        Returns:
            bool: True if the operation is successful, False otherwise.
        """
        try:
            columns = self.getColumnNames(table_name)

            if old_column_name not in columns:
                print(f"Error: Column '{old_column_name}' not found in table '{table_name}'.")
                return False

            if new_column_name in columns:
                print(f"Error: Column '{new_column_name}' already exists in table '{table_name}'.")
                return False

            
            index = columns.index(old_column_name)
            columns[index] = new_column_name

            temp_table_name = f"temp_{table_name}"
            self.createTb(temp_table_name, columns)
            data =  valreplace(self.fetch(table_name), old_column_name, new_column_name, True)
            self.json_insert(temp_table_name,)
            self.delTb(table_name)
            self.renameTb(temp_table_name, table_name)

            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def modifyColumn(self, table_name:str, column_name:str, new_column_name:str='', data_type:str='', column_param:str=''):
        """
        Modifies a column in the specified table.

        Parameters:
            table_name (str): The name of the table.
            column_name (str): The name of the column to be modified.
            new_column_name (str, optional): The new name for the column. Defaults to ''.
            data_type (str, optional): The new data type for the column. Defaults to ''.
            column_param (str, optional): Additional column parameters. Defaults to ''.

        Returns:
            bool: True if the operation is successful, False otherwise.
        """
        try:
            columns_info = self.execute(f"PRAGMA table_info({table_name})").fetchall()
            column_names = [info[1] for info in columns_info]

            if column_name not in column_names:
                print(f"Error: Column '{column_name}' not found in table '{table_name}'.")
                return False

            if new_column_name == '' and data_type == '' and column_param == '':
                print("Error: No modifications provided.")
                return False

            temp_table_name = f"temp_{table_name}"
            original_columns = self.getColumnNames(table_name)

            modified_column = f"{new_column_name} {data_type} {column_param}" if new_column_name else column_name
            modified_columns = [modified_column if col == column_name else col for col in original_columns]

            self.createTb(temp_table_name, modified_columns)
            self.json_insert(temp_table_name, self.fetch(table_name))
            self.delTb(table_name)
            self.renameTb(temp_table_name, table_name)

            print(f"Column '{column_name}' in table '{table_name}' modified successfully.")
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def modifyColumns(self, table_name:str, modifications:dict):
        """
        Modifies multiple columns in the specified table.

        Parameters:
            table_name (str): The name of the table.
            modifications (dict): A dictionary where keys are column names and values are dictionaries
                                 containing modification options (new_column_name, data_type, column_param).

        Usage:
            ```
            modifications = {
                'column1': {'new_column_name': 'new_column1', 'data_type': 'TEXT'},
                'column2': {'data_type': 'INTEGER', 'column_param': 'NOT NULL'}
            }
            db_handler.modifyColumns('your_table_name', modifications)
            ```
            
        Returns:
            bool: True if the operation is successful, False otherwise.
        """
        try:
            for column_name, options in modifications.items():
                success = self.modifyColumn(table_name, column_name, **options)
                if not success:
                    return False
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
        
    def removeColumn(self, table_name:str, column_name:str):
        """
            Removes a column from the specified table.

            Parameters:
                table_name (str): The name of the table to remove the column from.
                column_name (str): The name of the column to remove.

            Returns:
                sqlite3.Cursor: The result of the executed query.
        """
        return self.execute(f"ALTER TABLE {table_name} DROP COLUMN {column_name};")

    def close_connection(self, mesg=None):
        """This method for to close  all the connections made to the db and aslomend the session."""
        self.db_init.close()
        if mesg!=None:
            print(mesg)

class MySqlHandler():

    def __init__(self, host:str, user:str, password:str, dataBase:str=""):
        try:
            self.dbConn = myqC.connect(host=host, user=user, passwd=password)
            self.cursor = self.dbConn.cursor()
        except myqC.Error as err:
            if err.errno == myqC.errorcode.ER_ACCESS_DENIED_ERROR:
                return 'Error Password!'
            else: return err.errno

    
    def createTb(self, tableName, columns, Engine:str='InnoDb', tableComment:str=''):
        """
        """
        if self.getTables(tableName): raise ValueError(f'This table [{tableName}] already exist!')
        column = ','.join(columns)

        query = f"CREATE TABLE `{tableName}` ({column}) ENGINE = \'{Engine}'"
        if tableComment != '':
            query += f" COMMENT = '{tableComment}'"
        
        query+= ';'
        self.cursor.execute(query)

    def getTables(self, table:str=''):
        """
            The method is to get the list of tables form the database. 
        """
        self.cursor.execute("SHOW TABLES")
        tbList = [i[0] for i in self.cursor.fetchall()]
        if table!='': return table in tbList
        return tbList 

    def addIndex(self, tableName:str, index_name:str, columns:list):
        """
            This method is to add index to the tables.
        """
        
        columns = ','.join(columns)
        query = f'`{index_name}` ({columns})'
        self.alterTb(tableName, 'ADD UNIQUE', query)

    def alterTb(self, tableName:str, catg:str, query:str):
        """
            This method is to used to alter tables in the database. 
        """
        self.cursor.execute(f"ALTER TABLE `{tableName}` {catg} {query};")

    def cleanTb(self, tableName:str):
        """
            This method is to clean the table i.e. it will delete all the data from the table.
        """
        if self.getTables(tableName):
            self.cursor.execute(f'TRUNCATE TABLE `{tableName}`;')
        
    def delTb(self, tableName:str):
        """This method is to delete the specified table."""
        if self.getTables(tableName):
            self.cursor.execute(f'DROP TABLE `{tableName}`;')
        
    def connect_db(self, dataBase:str, create_db:bool=True):
        """
            The task of this mathod is to create new databases in the server.
        """
        if self.getDbList(dataBase)==False and create_db:
            self.createDb(dataBase)
        self.dbConn.database = dataBase
    
    def createDb(self, dataBase:str):
        """
            This method is to crreate a new dataBase.
        """ 
        try:
            if self.getDbList(dataBase) == True: ValueError('database already exists.')
            return self.execute(f'CREATE DATABASE {dataBase}')
        except Exception as e: return e  

    def getDbList(self, present:str=''):
        """
            This method gets the list of databases present in the server.

        """ 
        self.execute("SHOW DATABASES")
        dbList = [i[0] for i in self.cursor.fetchall()]
        if present != '': return present in dbList
        return dbList

    def execute(self, query:str):
        """
            This method is to execute the mysql queries.
        """
        try:
            return self.cursor.execute(query)
        except: 
            pass
    
    def delDb(self, dataBase:str):
        """
            This method is to delete dataBases.
        """
        if self.getDbList(dataBase):
            self.execute(f'DROP DATABASE {dataBase}')
        else:
            raise ValueError('Database does not exist!')

    def close_connection(self):
        """
            This method is to close the connection.
        """
        self.cursor.close()
        self.dbConn.close()