import sqlite3
import pandas as pd
class sqliteConnect:
    def __init__(self,dbname):
        self.conn = sqlite3.connect(dbname)
        self.cursorObj = self.conn.cursor()
    def dict_query(self,sql_query,params=None):
        try:
            if params:
                df = pd.read_sql_query(sql_query,self.conn,params=params)
            else:
                df = pd.read_sql_query(sql_query,self.conn)
        
            result_dict = df.to_dict(orient="records")
            return result_dict
        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Error executing query: {e}")
    def array_query(self,sql_query,params=None):
        try:
            if params:
                self.cursorObj.execute(sql_query,params)
            else:
                self.cursorObj.execute(sql_query)
            result_arr = self.cursorObj.fetchall()
            return result_arr
        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Error executing query: {e}")


    #sqlite新增資料
    def insert_record(self, table_name, column_data):
        try:
            cursor = self.conn.cursor()
            
            # Extract column names and values from the dictionary
            columns = ', '.join(column_data.keys())
            placeholders = ', '.join(['?'] * len(column_data))
            values = tuple(column_data.values())
            
            # Build and execute SQL statement
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            cursor.execute(query, values)
            
            # Get the ID of the last inserted row
            last_row_id = cursor.lastrowid
            
            # Commit changes
            self.conn.commit()
            
            return last_row_id
        
        except sqlite3.Error as e:
            # Rollback on error
            self.conn.rollback()
            raise Exception(f"Error occurred during data insertion: {e}")
    def update_record(self, table_name, column_data, condition_data):
        try:
            cursor = self.conn.cursor()
            
            # Build SET clause
            set_clause = ', '.join([f"{column} = ?" for column in column_data.keys()])
            set_values = list(column_data.values())
            
            # Build WHERE clause
            where_clause = ' AND '.join([f"{column} = ?" for column in condition_data.keys()])
            where_values = list(condition_data.values())
            
            # Combine all values
            all_values = set_values + where_values
            
            # Build and execute complete SQL statement
            query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
            cursor.execute(query, all_values)
            
            # Get number of affected rows
            rows_affected = cursor.rowcount
            
            # Commit changes
            self.conn.commit()
            
            return rows_affected
            
        except sqlite3.Error as e:
            # Rollback on error
            self.conn.rollback()
            raise Exception(f"Error occurred during data update: {e}")
    def delete(self,table_name,colume_name,params=None):
        try:
            if params:
                self.cursorObj.execute("delete from "+table_name+" where "+colume_name+" = ?",params)
            else:
                self.cursorObj.execute("delete from "+table_name)
        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Error occurred during data update: {e}")



















#sqlite_class = sqliteConnect('mydatabase.db')
#sqlite_class.delete("employees","name",("Dino",))
#print(sqlite_class.dict_query("Select *from employees"))
# user_data = {
#     "id":2,
#     "name":"Dino",
#     "salary":900,
#     "department":"IT",
#     "position":"System Administrator",
#     "hireDate": "2022-03-26"
# }
# update_data = {
#     "salary":950
# }
# condition = {
#     "name":"Dino"
# }












#sqlite_class.update_record("employees",update_data,condition)
#print(sqlite_class.array_query("Select *from employees where name = ?",("Dino",)))
#sqlite_class.insert_record('employees',user_data)
#print(sqlite_class.dict_query("Select *from employees"))
# con = sqlite3.connect('mydatabase.db')
# cursorObj = con.cursor()
# check_table_exist = cursorObj.execute("SELECT name FROM sqlite_master WHERE type='table';")
# if int(check_table_exist.arraysize) == 0:
#     cursorObj.execute("Create table employees (id, name, salary, department, position, hireDate)")
# df = pd.read_sql_query("select *from employees",con)
# result_dict = df.to_dict(orient='records')
# print(result_dict)
# #cursorObj.execute("INSERT INTO employees VALUES(1, 'John', 700, 'HR', 'Manager', '2017-01-04')")
# #con.commit()