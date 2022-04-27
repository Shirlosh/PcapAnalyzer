from asserts.CSVPrinter import CSVPrinter
from pcapAnalyzer import pcapAnalyzer

INFECTED_HOST = "172.16.4.205"
INFECTIOUS_CLIENT_1 = "185.243.115.84"
INFECTIOUS_CLIENT_2 = "31.7.62.214"


def main():
    pcap = pcapAnalyzer("IO/pcap.pcap", INFECTED_HOST, [INFECTIOUS_CLIENT_1, INFECTIOUS_CLIENT_2])
    csv_printer = CSVPrinter('IO/csv_file.csv')

    dict_data = pcap.Analyze_pcap()
    csv_printer.printCSV(dict_data)


if __name__ == '__main__':
    main()