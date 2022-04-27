import dpkt
import requests
from PacketHandler.PacketsFactory import PacketsFactory
from asserts.HTTPTuplesList import HTTPTuplesList


class pcapAnalyzer:

    def __init__(self, pcap_filepath, infected_host, infectious_clients):
        self.__pcap_path = pcap_filepath
        self.__infected_host = infected_host
        self.__infectious_clients = infectious_clients
        self.__file = open(pcap_filepath, 'rb')
        self.__pcap = dpkt.pcap.Reader(self.__file)

    # analyze pcap file, returns a list of tuples - differ in src(ip and port), dst(ip and port)
    # each tuple contains the following data: host
    def Analyze_pcap(self):
        t_dict = HTTPTuplesList()
        geoip_list = self.__init_geoip_list() # geoip array initialized once in order to prevent server errors and preserve program performance
        src_geoip = self.__get_geoIP(self.__infected_host)

        for timestamp, buf in self.__pcap:
            factory = PacketsFactory(buf, timestamp)
            packet = factory.get_packet()

            if packet is None:
                continue

            src, dst = packet.get_src_dst_ip()
            client_idx = self.__ip_condition_checker(src, dst)
            # client_idx = 1 - # DEBUG GET ALL IP's
            protocol = packet.get_protocol()

            # if there is a match between infected, infectious ip add and packet ip's AND the packet type is HTTP
            if client_idx >= 0 and (protocol == PacketsFactory.HTTP_REQ or protocol == PacketsFactory.HTTP_RES):
                packet.set_geoip(src_geoip, geoip_list[client_idx])
                t_dict.add_HTTP(packet)

        result = t_dict.get_dict()
        return result

    # checks if the infected_host ip match to src and infectious client ip to dst
    def __ip_condition_checker(self, src, dst):
        client_idx = self.__compare_ip(src, dst)
        if client_idx == -1:
            client_idx = self.__compare_ip(dst, src)

        return client_idx

    # returns the index of the equal ip or -1 if the condition doesn't fit
    def __compare_ip(self, src, dst):
        index = -1
        if src != self.__infected_host:
            return index

        for i in range(0, len(self.__infectious_clients)):
            if dst == self.__infectious_clients[i]:
                index = i
                return index

        return index

    # run over infectious clients list and get the geoip of each ip
    def __init_geoip_list(self):
        res = []
        for obj in self.__infectious_clients:
            res.append(self.__get_geoIP(obj))
        return res

    # get geoip from geolocation-db server
    @staticmethod
    def __get_geoIP(ip):
        url = "https://geolocation-db.com/json/%&position=true"
        url = url.replace('%', ip)
        response = requests.get(url).json()
        return response['country_name']
