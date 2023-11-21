import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import sqlite3

class data_interpreter():
    table=None
    sqlite_table="test.db"
    separate_tables=[]
    main_table_name=""
    date_added_bounds=[]

    def __init__(self, file_name:str, main_table_name:str, separate_tables:list):
        self.table = pd.read_csv(file_name)
        self.main_table_name = main_table_name
        self.separate_tables = separate_tables
        print(self.table.columns)
        self.drop_tables()
        self.intialize_database()
        self.fill_database()

        self.determine_date_added_bounds()

    def get_filter_options_for_column(self, column:str):
        if column in self.separate_tables:
            result = self.database_query("SELECT %s FROM %s" % (column + "NAME", column))
        else:
            result = self.database_query("SELECT %s FROM %s" % (column, self.main_table_name))
        hash_set = set()
        for row in result:
            new_item = row[0]
            if column == "duration":
                if new_item.endswith("min"):
                    new_item = str((int(new_item.split(" ")[0]) // 30)*30) + "-" + str((int(new_item.split(" ")[0]) // 30)*30 + 30) + " mins"
            elif column == "date_added":
                new_item = new_item[-4:]
            hash_set.add(new_item)
        return hash_set

    def get_table_columns(self):
        return self.table.columns

    def build_pie_data(self, x:str, points:int, title:str="", filter:dict=None, omit:dict=None, percentage:bool=True):
        query = self.build_filtered_pie_query(x, filter, omit)
        print(query)
        counts = self.database_query(query)
        parsed_data = self.parse_pie_data(counts, x=="duration")
        pie_data = self.get_pie_data(parsed_data[:points])
        title = self.check_title(title, x, "")
        self.pie_grapher(x.replace("_", " ").capitalize(), pie_data[1], pie_data[0], title=title, percentage=percentage)
        return pie_data

    def check_title(self, title, x, y):
        if len(title) == 0:
            if len(y) == 0:
                return x.replace("_", " ").capitalize() + " Percentages"
            else:
                return x.replace("_", " ").capitalize() + " Versus " + y.replace("_", " ").capitalize()
        return title

    def check_labels(self, labels:list, y:str):
        if len(labels) < 2:
            return [y.replace("_", " ").capitalize(), "Number of Movies"]
        return labels

    def get_pie_data(self, data:list):
        return_lists = [[],[]]
        for point in data:
            return_lists[0].append(point[0])
            return_lists[1].append(point[1])
        return return_lists

    def parse_pie_data(self, data:list, is_duration:bool=False):
        count_dict = {}
        for point in data:
            field = point[0]
            if is_duration:
                if field.endswith("min"):
                    field = str((int(field.split(" ")[0]) // 30)*30) + "-" + str((int(field.split(" ")[0]) // 30)*30 + 30) + " mins"
            if not field in count_dict.keys():
                count_dict[field] = 0
            count_dict[field] += 1
        count_list = [(key, count_dict[key]) for key in sorted(count_dict.keys(), key=lambda x: -count_dict[x])]
        return count_list

    def build_filtered_pie_query(self, x:str, filter:dict=None, omit:dict=None):
        table_name = x
        x_data = x
        if x in self.separate_tables:
            x_data = x + "NAME"
        else:
            table_name = self.main_table_name
        query = '''SELECT * FROM \"%s\"''' % (table_name)
        query = self.filter_data(x, filter, omit, table_name, query)
        query = '''SELECT \"%s\" FROM (%s)''' % (x_data, query)
        query += ";"
        return query

    def build_plot_data(self, x:str, y:str, points:int, labels:list=[], title:str="", filter:dict=None, omit:dict=None, scatter:bool=False):
        query = self.build_filtered_query(x, y, filter, omit)
        print(query)
        frequent = self.database_query(query)
        parsed_data = self.parse_frequency_data(frequent, True, x=="duration")
        for point in range(len(parsed_data)):
            parsed_data[point] = (parsed_data[point][0], self.fill_in_blank_year_data(parsed_data[point][1]), parsed_data[point][2])
        plot_data = self.get_graph_data(parsed_data[:points])
        title = self.check_title(title, x, y)
        labels = self.check_labels(labels, y)
        if scatter:
            self.data_scatter(plot_data[0], plot_data[1], title=title, labels=labels, ylabels=plot_data[2], legend=True)
        else:
            self.data_plotter(plot_data[0], plot_data[1], title=title, labels=labels, ylabels=plot_data[2], legend=True)
        return plot_data

    def fill_in_blank_year_data(self, data):
        full_data = [(data[0][i], data[1][i]) for i in range(len(data[0]))]
        for year in range(self.date_added_bounds[0], self.date_added_bounds[1] + 1):
            if not year in data[0]:
                full_data.append((year, 0))
        full_data = sorted(full_data, key=lambda x: x[0])
        return [[i[0] for i in full_data],[i[1] for i in full_data]]

    def build_filtered_query(self, x:str, y:str, filter:dict=None, omit:dict=None):
        table_name = x
        x_data = x
        if x in self.separate_tables:
            x_data = x + "NAME"
        else:
            table_name = self.main_table_name
        query = '''SELECT * FROM \"%s\"''' % (table_name)
        if not y in self.separate_tables and x in self.separate_tables:
            query += " JOIN \"%s\" ON %s.ID=\"%s\".%s_ID" % (self.main_table_name, self.main_table_name, x, self.main_table_name)
        query = self.filter_data(x, filter, omit, table_name, query)
        query = '''SELECT \"%s\", \"%s\" FROM (%s);''' % (x_data, y, query)
        return query

    def filter_data(self, x:str, filter:dict, omit:dict, table_name:str, query:str):
        if filter != None and len(filter.keys()) > 0:
            query = self.filter_sep_table(x, filter, table_name, query)
            query = self.filter_main_table(filter, query)
        if omit != None and len(omit.keys()) > 0:
            query = self.omit_data(x, table_name, omit, query)
        return query

    def omit_data(self, x:str, table_name:str, omit:dict, query:str):
        for key in omit.keys():
            if key in self.separate_tables and key != x:
                if type(omit[key]) == list:
                    condition = "("
                    for element in omit[key]:
                        condition += "\"%s\"<>\"%s\" AND " % (key + "NAME", element)
                    condition = condition[:-5] + ")"
                else:
                    condition = "\"%s\"<>\"%s\"" % (key + "NAME", omit[key])
                if x in self.separate_tables:
                    condition = "%s AND \"%s\".%s_ID=\"%s\".%s_ID" % (condition, table_name, self.main_table_name, key, self.main_table_name)
                else:
                    condition = "%s AND \"%s\".ID=\"%s\".%s_ID" % (condition, table_name, key, self.main_table_name)
                query += " JOIN \"%s\" ON %s" % (key, condition)
        try:
            omit[table_name]
            key = table_name
            if table_name == self.main_table_name:
                query = " SELECT * FROM (%s) WHERE \"%s\"<>\"%s\"" % (self.main_table_name, query, key, omit[key])
            else:
                query = ''' SELECT * FROM \"%s\", (%s) WHERE \"%s\".%s_ID=ID''' % (key, query, key, self.main_table_name)        
        except KeyError:
            pass
        return query

    def filter_main_table(self, filter, query):        
        for key in filter.keys():
            if not key in self.separate_tables:
                query += " WHERE \"%s\"=\"%s\"" % (key, filter[key])
            elif key == "only_data_for":
                query += " WHERE \"%s\"=\"%s\"" % (key + "NAME", filter[key])
        return query

    def filter_sep_table(self, x, filter, table_name, query):
        x_key = False
        for key in filter.keys():
            if key in self.separate_tables and key != x:
                if type(filter[key]) == list:
                    condition = "("
                    for element in filter[key]:
                        condition += "\"%s\"=\"%s\" OR " % (key + "NAME", element)
                    condition = condition[:-4] + ")"
                else:
                    condition = "\"%s\"=\"%s\"" % (key + "NAME", filter[key])
                if x in self.separate_tables:
                    condition = "%s AND \"%s\".%s_ID=\"%s\".%s_ID" % (condition, table_name, self.main_table_name, key, self.main_table_name)
                else:
                    condition = "%s AND \"%s\".ID=\"%s\".%s_ID" % (condition, table_name, key, self.main_table_name)
                query += " JOIN \"%s\" ON %s" % (key, condition)
            elif key == x:
                x_key = True       
        if x_key:
            query = '''SELECT * FROM \"%s\", (%s) WHERE \"%s\".%s_ID=ID''' % (key, query, key, self.main_table_name)
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

    def parse_frequency_data(self, data:list, is_date_added:bool=False, is_duration:bool=False):
        freq_dict = {}
        for point in data:
            y_field = point[1]
            x_field = point[0]
            if is_duration:
                if x_field.endswith("min"):
                    x_field = str((int(x_field.split(" ")[0]) // 30)*30) + "-" + str((int(x_field.split(" ")[0]) // 30)*30 + 30) + " mins"
            try:
                if is_date_added:
                    y_field = int(y_field[-4:])
                if not x_field in freq_dict.keys():
                    freq_dict[x_field] = {}
                if not y_field in freq_dict[x_field].keys():
                    freq_dict[x_field][y_field] = 0
                freq_dict[x_field][y_field] += 1
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
                foreign_key = connection.execute("SELECT * FROM \"%s\" WHERE show_id=\"%s\"" % (self.main_table_name, current.get("show_id"))).fetchall()[0][0]
                names = str(current.get(column)).replace("'", "''").split(",")
                for name in names:
                    if name != "nan":
                        name = name.strip()
                        execute_string = '''INSERT INTO %s (\"%s_ID\", \"%sNAME\") VALUES ('%s', '%s')''' % (column, self.main_table_name, column, foreign_key, name)
                        connection.execute(execute_string)
        self.close_database(connection)

    def build_execute_string(self):
        execute_string = "INSERT INTO \"%s\" (" % (self.main_table_name)
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
            self.database_execute_query("DROP TABLE \"%s\";"  % (self.main_table_name))
        except sqlite3.OperationalError as e:
            print(e)
        for sub_table in self.separate_tables:
            try:
                self.database_execute_query("DROP TABLE %s;" % (sub_table))
            except sqlite3.OperationalError as e:
                print(e)

    def intialize_database(self):
        try:
            execute_string = '''CREATE TABLE \"%s\" (
                ID INTEGER PRIMARY KEY,''' % (self.main_table_name)
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
                        %sID INTEGER PRIMARY KEY,
                        %s_ID INT,
                        %sNAME VARCHAR(100) NOT NULL,
                        FOREIGN KEY (%s_ID) REFERENCES %s (ID)
                        )
                        ''' % (sub_table, sub_table, self.main_table_name, sub_table, self.main_table_name, self.main_table_name)
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

    def data_plotter(self, x_data:list, y_data:list, title:str, labels=[], ylabels=[], legend:bool=False):
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

    def original_value_from_percent(self, pct, allvals):
        absolute = int(np.round(pct/100.*np.sum(allvals)))
        return str(absolute)

    def pie_grapher(self, x_name:str, x:list, labels:list, title:str, percentage:bool=True):
        plt.title(title)
        if percentage:
            wedges, texts, autotexts = plt.pie(x, autopct="%1.1f%%", startangle=0)
        else:
            wedges, texts, autotexts = plt.pie(x, autopct=lambda pct: self.original_value_from_percent(pct, x), startangle=0)
        plt.legend(wedges, labels, title=x_name)
        plt.show()
    
    def data_scatter(self, x_data:list, y_data:list, title:str, labels=[], ylabels=[], legend:bool=False):
        plt.title(title)
        if len(labels) > 0:
            plt.xlabel(labels[0])
            plt.ylabel(labels[1])
        if len(ylabels) == 0:
            ylabels = ["" for i in range(len(y_data))]
        plt.grid()
        for y in range(len(y_data)):
            plt.scatter(x_data[y], y_data[y], label=ylabels[y])
        if legend:
            plt.legend()
        plt.show()