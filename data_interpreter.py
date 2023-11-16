import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import sqlite3

class data_interpreter():
    table=None
    sqlite_table="test.db"
    separate_tables=["director", "cast", "country", "listed_in"]
    date_added_bounds=[]

    def __init__(self, file_name:str):
        self.table = pd.read_csv(file_name)
        print(self.table.columns)
        self.drop_tables()
        self.intialize_database()
        self.fill_database()

        self.determine_date_added_bounds()

    def build_plot_data(self, x:str, y:str, points:int, title:str, labels:list, filter:dict=None):
        query = self.build_filtered_query(x, y, filter)
        print(query)
        frequent = self.database_query(query)
        parsed_data = self.parse_frequency_data(frequent, True)
        for point in range(len(parsed_data)):
            parsed_data[point] = (parsed_data[point][0], self.fill_in_blank_year_data(parsed_data[point][1]), parsed_data[point][2])
        plot_data = self.get_graph_data(parsed_data[:points])
        self.data_grapher(plot_data[0], plot_data[1], title=title, labels=labels, ylabels=plot_data[2], legend=True)

    def fill_in_blank_year_data(self, data):
        full_data = [(data[0][i], data[1][i]) for i in range(len(data[0]))]
        for year in range(self.date_added_bounds[0], self.date_added_bounds[1] + 1):
            if not year in data[0]:
                full_data.append((year, 0))
        full_data = sorted(full_data, key=lambda x: x[0])
        return [[i[0] for i in full_data],[i[1] for i in full_data]]

    def build_filtered_query(self, x:str, y:str, filter:dict=None):
        table_name = x
        x_data = x
        if x in self.separate_tables:
            x_data = x + "NAME"
        else:
            table_name = "MOVIE"
        query = '''SELECT \"%s\", \"%s\" FROM \"%s\"''' % (x_data, y, table_name)
        if not y in self.separate_tables and x in self.separate_tables:
            query += " JOIN MOVIE ON MOVIE.ID=\"%s\".MOVIE_ID" % (x)
        if filter != None and len(filter.keys()) > 0:
            for key in filter.keys():
                if key in self.separate_tables:
                    condition = "\"%s\"=\"%s\" AND \"%s\".ID=\"%s\".MOVIE_ID" % (key + "NAME", filter[key], table_name, key)
                    if x in self.separate_tables:
                        condition = "\"%s\"=\"%s\" AND \"%s\".MOVIE_ID=\"%s\".MOVIE_ID" % (key + "NAME", filter[key], table_name, key)
                    query += " JOIN \"%s\" ON %s" % (key, condition)
        if filter != None and len(filter.keys()) > 0:
            for key in filter.keys():
                if not key in self.separate_tables:
                    query += " WHERE \"%s\"=\"%s\"" % (key, filter[key])
        query += ";"
        return query

    def determine_date_added_bounds(self):
        max = float('-inf')
        min = float('inf')
        for i in self.table.iloc:
            try:
                year = int(i.get("date_added")[-4:])
                if year < min:
                    min = year
                if year > max:
                    max = year
            except TypeError:
                pass
        self.date_added_bounds=[min, max]

    def get_graph_data(self, data:list):
        x_data = [i[1][0] for i in data]
        y_data = [i[1][1] for i in data]
        y_labels = [i[0] for i in data]
        return x_data, y_data, y_labels

    def parse_frequency_data(self, data:list, is_date_added:bool=False):
        freq_dict = {}
        for point in data:
            y_field = point[1]
            try:
                if is_date_added:
                    y_field = int(y_field[-4:])
                if not point[0] in freq_dict.keys():
                    freq_dict[point[0]] = {}
                if not y_field in freq_dict[point[0]].keys():
                    freq_dict[point[0]][y_field] = 0
                freq_dict[point[0]][y_field] += 1
            except ValueError:
                pass
        return_list = []            
        for key in freq_dict.keys():
            append_list = [[],[]]
            total = 0
            for i in sorted(freq_dict[key]):
                append_list[0].append(i)
                append_list[1].append(freq_dict[key][i])
                total += freq_dict[key][i]
            freq_dict[key] = append_list
            return_list.append((key, freq_dict[key], total))
        return_list = sorted(return_list, key=lambda index: -index[2])
        return return_list

    def fill_database(self):
        connection = sqlite3.connect(self.sqlite_table)
        execute_string = self.build_execute_string()
        self.database_execute_query(execute_string)

        for row in range(len(self.table)):
            current = self.table.iloc[row]
            for column in self.separate_tables:
                foreign_key = connection.execute("SELECT * FROM \"MOVIE\" WHERE show_id=\"%s\"" % (current.get("show_id"))).fetchall()[0][0]
                names = str(current.get(column)).replace("'", "''").split(",")
                for name in names:
                    if name != "nan":
                        name = name.strip()
                        execute_string = '''INSERT INTO %s (\"MOVIE_ID\", \"%sNAME\") VALUES ('%s', '%s')''' % (column, column, foreign_key, name)
                        connection.execute(execute_string)
        self.close_database(connection)

    def build_execute_string(self):
        execute_string = "INSERT INTO \"MOVIE\" ("
        for column in self.table.columns:
            if not column in self.separate_tables:
                execute_string += column + ","
        execute_string = execute_string[:-1] + ")\nVALUES"
        for row in range(len(self.table)):
            current = self.table.iloc[row]
            row_info = self.build_row_info(current)
            execute_string += row_info
        execute_string = execute_string[:-1] + ";"
        return execute_string

    def build_row_info(self, current:pd.DataFrame):
        row_info = "\n("
        for column in self.table.columns:
            if not column in self.separate_tables:
                temp_info = str(current.get(column)).replace("'", "''")
                row_info += "\'" + temp_info + "\'" + ","
        row_info = row_info[:-1] + "),"
        return row_info

    def drop_tables(self):
        try:
            self.database_execute_query("DROP TABLE \"MOVIE\";")
        except sqlite3.OperationalError as e:
            print(e)
        for sub_table in self.separate_tables:
            try:
                self.database_execute_query("DROP TABLE %s;" % (sub_table))
            except sqlite3.OperationalError as e:
                print(e)

    def intialize_database(self):
        try:
            execute_string = '''CREATE TABLE \"MOVIE\" (
                ID INTEGER PRIMARY KEY,'''
            for column in self.table.columns:
                if not column in self.separate_tables:
                    if column == "show_id":
                        execute_string += '''
                        %s VARCHAR (1000) UNIQUE,''' % (column)
                    else:
                        execute_string += '''
                        %s VARCHAR (1000),''' % (column)
            execute_string = execute_string[:-1] + ");"
            self.database_execute_query(execute_string)
        except sqlite3.OperationalError as e:
            print(e)

        for sub_table in self.separate_tables:
            try:
                self.database_execute_query(
                    '''CREATE TABLE \"%s\"(
                        ID INTEGER PRIMARY KEY,
                        MOVIE_ID INT,
                        %sNAME VARCHAR(100) NOT NULL,
                        FOREIGN KEY (MOVIE_ID) REFERENCES MOVIE (ID)
                        )
                        ''' % (sub_table, sub_table)
            ) 
            except sqlite3.OperationalError as e:
                print(e)
        
    def database_query(self, query:str):
        connection = sqlite3.connect(self.sqlite_table)
        data = connection.execute(query).fetchall()
        self.close_database(connection)
        return data

    def database_execute_query(self, query:str):
        connection = sqlite3.connect(self.sqlite_table)
        connection.execute(query)
        self.close_database(connection)

    def close_database(self, database):
        database.commit()
        database.close()

    def data_grapher(self, x_data:list, y_data:list, title:str, labels=[], ylabels=[], legend:bool=False):
        plt.title(title)
        if len(labels) > 0:
            plt.xlabel(labels[0])
            plt.ylabel(labels[1])
        if len(ylabels) == 0:
            ylabels = ["" for i in range(len(y_data))]
        plt.grid()
        for y in range(len(y_data)):
            plt.plot(x_data[y], y_data[y], label=ylabels[y])
        if legend:
            plt.legend()
        plt.show()