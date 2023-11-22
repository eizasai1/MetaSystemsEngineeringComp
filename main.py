import data_interpreter
import time
import matplotlib.pyplot as plt

if __name__=="__main__":
    di = data_interpreter.data_interpreter("netflix_titles.csv", "MOVIE", ["director", "cast", "country", "listed_in"])
    columns = di.get_table_columns()

    plot_columns = ["type", "country", "release_year", "rating", "duration", "listed_in"]
    ignore_columns = ["show_id", "title", "description", "date_added"]

    country_data = di.build_plot_data("country", "date_added", 10)
    countries = country_data[-1]
    print(countries)

    ignore_columns.append("country")

    for column in columns:
        if not column in ignore_columns:
            if column in plot_columns:
                di.plot_multiple_graphs_with_different_filter(column, "date_added", 10, filter=countries, filter_item="country")
                di.pie_multiple_graphs_with_different_filter(column, 10, filter=countries, filter_item="country")
                
            

    # for column in columns:
    #     if not column in ignore_columns:
    #         di.build_plot_data(column, "date_added", 10)
    #         di.build_pie_data(column, 10)    
    
    # ignore_columns = ["show_id", "title", "description", "director", "cast"]
    # for column in columns:
    #     if not column in ignore_columns:
    #         set = di.get_filter_options_for_column(column)
    #         print(column, set)

    # di.build_plot_data("duration", "date_added", 10, filter={"type":"Movie"})
    # di.build_pie_data("duration", 10, filter={"type":"Movie"})
    # di.build_plot_data("duration", "date_added", 10, filter={"type":"TV Show"})
    # di.build_pie_data("duration", 10, filter={"type":"TV Show"})


    # di.build_plot_data("rating", "date_added", 10, filter={"country": "United States"})
    # di.build_plot_data("rating", "date_added", 10)
    # di.build_plot_data("release_year", "date_added", 10)
    # di.build_plot_data("type", "date_added", 10, filter={"country":"United States", "rating":"TV-MA"})
    # di.build_plot_data("director", "date_added", 10, filter={"country":"United States"})
    # di.build_plot_data("director", "date_added", 10, filter={"country":"Japan"})
    # di.build_plot_data("cast", "date_added", 10, filter={"country":"Japan"}, scatter=True)
    # di.build_pie_data("rating", 5, filter={"country":"United States", "country":"India", "type":"Movie"})
    # di.build_pie_data("duration", 10, filter={"country":"United States", "country":"India", "type":"Movie"}, percentage=False)
    # di.build_plot_data("listed_in", "date_added", 10, filter={"country": "United States"})
    # di.build_plot_data("release_year", "date_added", 100, filter={"country": "United States"})
    # di.build_pie_data("cast", 10, omit={"country":["India", "United States"], "rating":"R"})
    # di.build_pie_data("cast", 10, filter={"country":"United States"})
    # di.build_plot_data("country", "release_year", 10, filter={"country":"United States"})
