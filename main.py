import data_interpreter

if __name__=="__main__":
    di = data_interpreter.data_interpreter("netflix_titles.csv", "MOVIE")
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
    di.build_pie_data("cast", 10, omit={"country":["India", "United States"], "rating":"R"})
    # di.build_pie_data("cast", 10, filter={"country":"United States"})
    # di.build_plot_data("country", "release_year", 10, filter={"country":"United States"})
