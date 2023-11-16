import data_interpreter

if __name__=="__main__":
    di = data_interpreter.data_interpreter("netflix_titles.csv")
    di.build_plot_data("rating", "date_added", 10, "Rating in US Frequency", labels=["Year Added", "Number of Movies"], filter={"country": "United States"})
    di.build_plot_data("rating", "date_added", 10, "Rating in US Frequency", labels=["Year Added", "Number of Movies"])
    di.build_plot_data("release_year", "date_added", 10, "Release Year and Date Added", labels=["Year Added", "Number of Movies"], filter={"country":"India"})
