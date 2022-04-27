import csv


class CSVPrinter:

    def __init__(self, csv_path):
        self.__csv_path = csv_path

    def printCSV(self, dict_data):
        csv_columns = dict_data[0].keys()

        try:
            with open(self.__csv_path, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writeheader()
                for data in dict_data:
                    writer.writerow(data)
        except IOError:
            print("I/O error")
