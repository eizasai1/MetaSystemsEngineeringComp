import data_interpreter
import time
import matplotlib.pyplot as plt

if __name__=="__main__":
    di = data_interpreter.data_interpreter("netflix_titles.csv", "MOVIE", ["director", "cast", "country", "listed_in"])
    columns = di.get_table_columns()

    plot_columns = ["type", "country", "release_year", "rating", "duration", "listed_in"]
    ignore_columns = ["show_id", "title", "description", "date_added"]

    # di.build_pie_data("rating", 10)

    di.build_bar_data("country", 5)

    di.build_plot_data("type", "date_added", 5, title="India Show Types", filter={"country":"India"})

    #genre rating duration us and india vs world
    # di.build_pie_data("listed_in", 5, title="India Genre Percentages", filter={"country":"India"}, omit={"listed_in":"International Movies"})
    # di.build_plot_data("listed_in", "date_added", 5, title="India Genres", filter={"country":"India"}, omit={"listed_in":"International Movies"})
    # di.build_pie_data("listed_in", 5, title="United States Genre Percentages", filter={"country":"United States"})
    # di.build_pie_data("listed_in", 5, title="World Genre Percentages")

    # di.build_pie_data("rating", 5, title="India Rating Percentages", filter={"country":"India"})
    # di.build_pie_data("rating", 5, title="United States Rating Percentages", filter={"country":"United States"})
    # di.build_pie_data("rating", 5, title="World Rating Percentages")

    # di.build_pie_data("duration", 5, title="India Duration Percentages", filter={"country":"India"})
    # di.build_pie_data("duration", 5, title="United States Duration Percentages", filter={"country":"United States"})
    # di.build_pie_data("duration", 5, title="World Duration Percentages")

    #Which Genres are becoming less/more popular
    # di.build_plot_data("listed_in", "date_added", 10)
    
    #number of tv shows vs number of movies worldwide over time
    # di.build_plot_data("type", "date_added", 10)

    #number of seasons per tv show pie and plot
    di.build_plot_data("duration", "date_added", 10, title="TV Show Durations Versus Date Added", filter={"type":"TV Show"})
    # di.build_pie_data("duration", 10, title="TV Show Duration Percentages", filter={"type":"TV Show"})
    #Popular genres for tv shows and general
    di.build_bar_data("listed_in", 5, title="General Genre Percentages")
    di.build_bar_data("listed_in", 5, title="TV Show Genre Percentages", filter={"type":"TV Show"})

    #actors and directors everyone
    di.build_bar_data("director", 5, title="Director Percentages")
    di.build_bar_data("cast", 5, title="Actor Percentages")

    #Movie durations
    # di.build_plot_data("duration", "date_added", 10, title="Movie Durations Versus Date Added", filter={"type":"Movie"})
    # di.build_pie_data("duration", 6, title="Movie Duration Percentages", filter={"type":"Movie"})

    # di.build_pie_data("country", 10, title="International Movies by Countries", filter={"listed_in": "International Movies"})

    #-------

    # country_data = di.build_plot_data("country", "date_added", 10)
    # countries = country_data[-1]
    # print(countries)

    # ignore_columns.append("country")

    # for country in countries:
    #     for column in columns:
    #         if not column in ignore_columns:
    #             di.build_plot_data(column, "date_added", 10, title=country + " " + column.replace("_", " "), filter={"country":country})
    #             di.build_pie_data(column, 10, title=country + " " + column.replace("_", " "), filter={"country":country})

    # for column in columns:
    #     if not column in ignore_columns:
    #         if column in plot_columns:
    #             di.plot_multiple_graphs_with_different_filter(column, "date_added", 10, filter=countries, filter_item="country")
    #         di.pie_multiple_graphs_with_different_filter(column, 10, filter=countries, filter_item="country")
                
    #-------
            
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
