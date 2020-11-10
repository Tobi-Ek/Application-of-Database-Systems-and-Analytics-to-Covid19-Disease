from sqlalchemy import create_engine
import psycopg2
import pandas as pd
from  psycopg2.extensions import connection as DB_CON
def get_dbCon():
        try:
            conn=psycopg2.connect(host='localhost',port=5432,database="postgres",user='postgres',password="RamP")
            return conn
        except Exception as e:
            print('Db connection occurred-',e)
            
 
def select_count(table_name,conn:DB_CON):
    query="SELECT count(*) FROM "+table_name+" "
    cur=conn.cursor()
    cur.execute(query)
    query_results=cur.fetchall()
    print(query_results)
    conn.close()

def select_res(table_name,conn:DB_CON):
    query="SELECT * FROM "+table_name+" "
    cur=conn.cursor()
    cur.execute(query)
    query_results=cur.fetchall()
    print(query_results)
    conn.close()
    return query_results
def exec_query(query:str,conn:DB_CON):
    cur=conn.cursor()
    cur.execute(query)
    query_results=cur.fetchall()
    print("query run successfull")
    conn.close()
    return query_results

def select_res_dataframe(query:str):
    try:
        engine = create_engine('postgresql://postgres:RamP@localhost:5432/postgres')
        df = pd.read_sql_query(query,con=engine)
        engine.dispose()
        print("Query run successful")
        return df
    except (Exception, psycopg2.DatabaseError) as error :
            print ("Error while inserting PostgreSQL table", error)
    finally:
            #closing database connection.
            engine.dispose()
            print("PostgreSQL connection is closed")

    
    

def create_table(table_name:str,column_detail_nameList:list,conn:psycopg2.extensions.connection):
    try:
        cursor=conn.cursor()
        create_table_query= "CREATE TABLE "+table_name+" (";
        cnt=0
        for col_detail in column_detail_nameList:
            if cnt==0:
                create_table_query+= " "+ col_detail
                cnt=1
            else:
                create_table_query+= " ,"+ col_detail
        create_table_query+=" );"
        cursor.execute(create_table_query)
        conn.commit()
        print(table_name,"-Table created successfully in PostgreSQL ")

    except (Exception, psycopg2.DatabaseError) as error :
            print ("Error while creating PostgreSQL table", error)
    finally:
            #closing database connection.
        if(conn):
            cursor.close()
            conn.close()
            print("PostgreSQL connection is closed")

def insert_csv_table(df:pd.DataFrame,table_name:str,db_cols:list):
    try:
        engine = create_engine('postgresql://postgres:RamP@localhost:5432/postgres')
        
        (df.rename(columns=dict(zip(df.columns,db_cols)))
             .to_sql(name=table_name,con=engine,if_exists="append",index=False,index_label=None,schema='public'))
        print('Data insert succecssfull into the ',table_name )
    except (Exception, psycopg2.DatabaseError) as error :
            print ("Error while inserting PostgreSQL table", error)
    finally:
            #closing database connection.
            engine.dispose()
            print("PostgreSQL connection is closed")
def insert_df_into_csv(df:pd.DataFrame,filepath:str,Index=False,sep=","):
    try:
        df.to_csv(filepath,index=Index)
        df_new=pd.read_csv(filepath)
        print("Data inserted successfull to the csv file:",filepath)
        return df_new
    except IOError as e:
        print("Error occur during of data into csv file:",e)
    
     


  
 # COVID19_open_line_list_file_cleaned
#table_name='covid19_wuhan_relation'
#column_name=['ID numeric PRIMARY KEY','city VARCHAR (100)','province VARCHAR (100)','country VARCHAR (100)',
 #           'wuhan_0_not_wuhan_1 numeric','latitude numeric','longitude numeric','geo_resolution TEXT',
  #          'date_confirmation VARCHAR(50)','source  TEXT','admin2 TEXT','admin1 TEXT',
   #         'country_new VARCHAR(100)','admin_id VARCHAR(300)']

#create_table(table_name,column_name,get_dbCon())
'''

'''
#db_column=['country','total_confirmed','total_death','total_recovered']
#insert_csv_table(df_country,table_name,db_column)'''

