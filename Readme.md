# Personal EveryDay Usage Functions

## Project Author Details: 
- <b>Name</b>: <em>Ranit Saha</em>
- <b>Code Name</b>: <em>Codezees</em>
- <b>Guthub Profile</b>: <em>https://github.com/Codezees</em>


## Contents:

1. [Project Info](#project_info)
2. [Project Files](#project_files)
3. [Files Description](#project_file_description)

## <a id='project_info'>Project Info</a>
<p>This is just a personal project where I make classes and fuctions that will help me do certain task more effectiely rather that re-codig them again and again.</p>

## <a id='project_files'>Project Files</a>
<b><em>Project Files are:-</em></b>
- [AsyncHandler](#asyncHandler_file)
- [DataHandler](#dataHandler_file)
- [DbSqliteHandler](#dbsqlithandler_file)
- [Filehandler](#fileHandler_file)
- [HtmlScraper](#htmlScraper_file)
- [Requester](#requester_file)

## <a id='project_file_description'>Files Description</a>
<b><em>File Descriptions</em></b>

### <a  href = '' id='asyncHandler_file'>AsyncHandler</a>
<p>The file <b>AsyncHandler</b> encases a class called <code>AsyncHandler()</code>. This class is used to do task asuncronuslly.</p>

### <a  href = '' id='dataHandler_file'>DataHandler</a>
<p>The file <b>DataHandler</b> encases a class called <code>DataHandler()</code>. This class is used to menial tasks that usually require rewriting of a lot of code. 

This class is used for handleling data related tasks
</p>

<b><em>Functions of the class:-</em></b>
- <code>timestamp</code>: Returns the date and time in the specified format.
        
```
data = timestamp(given_time, format= "%Y-%m-%d %H:%M:%S", time_zone=None, normalize:str='sec')
print(data)
#output:  
```

### <a  href = '' id='dbsqlithandler_file'>DbSqliteHandler</a>
<p>The file <b>DbSqliteHandler</b> encases a class called <code>DbSqliteHandler</code>. This class is used creating and managing SQLITE3 databases.

- <b>Initializaton of database</b>:
When initalizing the database, on emust provide the desired database name. If the database existes, the class will just connect it else if the the database doesnot exist, then the database will be created and connectionn will be established.
    ````
    import DbSqliteHandler
    dbConn = DbSqliteHandler('db_name.db')
    ````
- <b><code>create()</code></b>: 
If the database is created newly, then the database will require a table to function properly, or else the db will just remain as file in the system.
So to create a table we need to use the class method called <code>createTb()</code>.
    - Parameter:
    - Usage:
    ```
    tb_name = 'table_1'
    columns = ['col1', 'col2']
    ## or you can specify the datatype like this.
    columns = ['col1 TEXT', 'col2 INT']
    dbConn.createTb(tb_name, columns)
    ```
    The method also comes with the feature of adding data along side creating the table raher than writing a special code for it and also comes with the feature to ```primary key``` while creating the table.

    ```
    col = ['col1', 'col2']
    data = ['data1', 'data2']
    dbConn.createTb(tbName, columns=col, insertData=data, addId=False, idKey='id')
    ```
- <b><code>insert</code></b>:
    - Parameter:
    - Usage:
    ```
    
    ```
- <b><code>json_insert</code></b>:
    - Parameter:
    - Usage:
    ```
    
    ```
- <b><code>fetch</code></b>:
    - Parameter:
    - Usage:
    ```
    
    ```
- <b><code>getCount</code></b>: This method counts the number of rows in the specified table. This method also allows or count with special queries like `col1='tofu'`. 
    - Parameter:
        - `table_name` : Takes the name of table.
        - `query` : Takes the search query. Default is `''` meaning, there is no search parameter and will count all the rows in the table.   
    - Returns: `int` 
    - Usage:
    ```
    query = "col1='tofu'"
    num = dbconn.getCount(table_name, query)
    print(num) ##prints out the number of row with col1 value as tofu.
    ```
- <b><code>update</code></b>:
    - Parameter:
    - Usage:
    ```
    
    ```
- <b><code>delTb</code></b>:
    - Parameter:
    - Usage:
    ```
    
    ```
- <b><code>renameTb</code></b>:
    - Parameter:
    - Usage:
    ```
    
    ```
- <b><code>getTb</code></b>:
    - Parameter:
    - Usage:
    ```
    
    ```
- <b><code>getTbData</code></b>:
    - Parameter:
    - Usage:
    ```
    
    ```
- <b><code>execute</code></b>:
    - Parameter:
    - Usage:
    ```
    
    ```
- <b><code>alterTb</code></b>:
    - Parameter:
    - Usage:
    ```
    
    ```
- <b><code>getColumnNames</code></b>:
    - Parameter:
    - Usage:
    ```
    
    ```
- <b><code>get_table_info</code></b>:
    - Parameter:
    - Usage:
    ```
    
    ```
- <b><code>modifyColumns</code></b>:
    - Parameter:
    - Usage:
    ```
    
    ```
- <b><code>checkIndex</code></b>:
    - Parameter:
    - Usage:
    ```
    
    ```
- <b><code>getIndexes</code></b>:
    - Parameter:
    - Usage:
    ```
    
    ```
- <b><code>addIndex</code></b>:
    - Parameter:
    - Usage:
    ```
    
    ```
- <b><code>delIndex</code></b>:
    - Parameter:
    - Usage:
    ```
    
    ```
- <b><code>cleanTb</code></b>:
    - Parameter:
    - Usage:
    ```
    
    ```
- <b><code>addColumn</code></b>:
    - Parameter:
    - Usage:
    ```
    
    ```
- <b><code>renameColumn</code></b>:
    - Parameter:
    - Usage:
    ```
    
    ```
- <b><code>removeColumn</code></b>: Removes a column from the specified table.
    - Parameter:
    - Usage:
    ```
    
    ```
- <b><code>close_connection</code></b>:This method for to close  all the connections made to the db and also end the session.



### <a href='' id='fileHandler_file'>Filehandler</a>
<p>The file <b>Filehandler</b> encases a class called <code>Filehandler</code>. This class is used for writing & reading file related tasks. 

- <b>Initialization</b>: The initiallization is a simple process. To use it , just add `FileHandler.func_name()` and it will work. <em>Examples are below.</em>
- <b>Class methods</b>: The class method are as follows:
    - <b>`getFiles()`</b>: Gets the list for files and folder in the specified folder.
        - <b>Parameter</b>: 
            - `file_path`: Takes the path of the folder that needs to be looked into.
            - `catg` : This parameter takes either 1 or 2, where 1 means to only look for files whereas 2 means to lik for directories. Default is 0. Which means both.
        - <b>Return</b>: `list`
        - <b>Usage</b>:
        ```
        folder_path = './test_folder' #folder present in the current directory.
        fi = getFiles(folder_path) # for both files and folder.
        print(fi) #output: [file1.txt, dir1, ....] 
        ```
    - <b>`get_only_filename()`</b>:
    - <b>`getFileCatg()`</b>:
    - <b>`splitFileName()`</b>:
    - <b>`getExtention()`</b>:
    - <b>`read()`</b>:
    - <b>`write()`</b>: This function is to write files and add contents to it.
        - <b>Parameter</b>:
            - `file_name` : The name of the file.
            - `data`: The data to be written to the file.
            - `separator`: Optional separator to append after the data.
        - <b>Usage</b>:
        ```
            data = 'This is Hello World File.' #file contents
            fileName = 'test.txt' # the file name
            FileHandler.write()
        ``` 
    - <b>`write_over()`</b>:
         - <b>Parameter</b>:
            - `file_name` : The name of the file.
            - `data`: The data to be written to the file.
            - `separator`: Optional separator to append after the data.
        - <b>Usage</b>:
        ```
            data = 'This is Hello World File.' #file contents
            fileName = 'test.txt' # the file name
            FileHandler.write()
        ```
    - <b>`read_csv()`</b>:
         - <b>Parameter</b>:
            - `file_name` : The name of the file.
            - `data`: The data to be written to the file.
            - `separator`: Optional separator to append after the data.
        - <b>Usage</b>:
        ```
            data = 'This is Hello World File.' #file contents
            fileName = 'test.txt' # the file name
            FileHandler.write()
        ```
    - <b>`write_csv()`</b>:
         - <b>Parameter</b>:
            - `file_name` : The name of the file.
            - `data`: The data to be written to the file.
            - `separator`: Optional separator to append after the data.
        - <b>Usage</b>:
        ```
            data = 'This is Hello World File.' #file contents
            fileName = 'test.txt' # the file name
            FileHandler.write()
        ```
    - <b>`read_excel()`</b>:
         - <b>Parameter</b>:
            - `file_name` : The name of the file.
            - `data`: The data to be written to the file.
            - `separator`: Optional separator to append after the data.
        - <b>Usage</b>:
        ```
            data = 'This is Hello World File.' #file contents
            fileName = 'test.txt' # the file name
            FileHandler.write()
        ```
    - <b>`write_excel()`</b>:
         - <b>Parameter</b>:
            - `file_name` : The name of the file.
            - `data`: The data to be written to the file.
            - `separator`: Optional separator to append after the data.
        - <b>Usage</b>:
        ```
            data = 'This is Hello World File.' #file contents
            fileName = 'test.txt' # the file name
            FileHandler.write()
        ```
    - <b>`read_pdf()`</b>: This function reads and returns the text values of the pdf.
            - <b>Parameter</b>:
                - `file_name` : The name of the file.
            - <b>Usage</b>:
            ```
                fileName = 'test.pdf' # the file name
                FileHandler.read_pdf()
            ```


### <a href='' id='htmlScraper_file'>HtmlScraper</a>
<p>The file <b>HtmlScraper</b> encases a class called <code>HtmlScraper</code>. This class is used to scraping HTML webpages with the help of <code>Requester</code> class along with beautifulSoup. 

### <a href='' id='requester_file'>Requester</a>
<p>The file <b>Requester</b> encases a class called <code>Requester</code>. This class is used to request related tasks.


##





