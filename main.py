from readData import read_values
from dbOperations import create_table


if __name__ == "__main__":
    # Get all the required data from our Json file
    table_values = read_values()
    # Create a table with our data in our PSQL database
    create_table(table_values)
