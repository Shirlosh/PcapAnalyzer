from abc import abstractmethod


# a packet super class contains a packet necessary methods, and general packet data
class Packet(object):
    SRC_IP = 'src ip'
    DST_IP = 'dst ip'
    SRC_PORT = 'src port'
    DST_PORT = 'dst port'
    DST_GEOIP = 'dst geo ip'
    SRC_GEOIP = 'src geo ip'

    def __init__(self, src_dst_ip, src_dst_proto, src_geoip=None, dst_geoip=None):
        self.__src_ip, self.__dst_ip = src_dst_ip
        self.__src_proto, self.__dst_proto = src_dst_proto
        self.__src_geoip = src_geoip
        self.__dst_geoip = dst_geoip

    # return a dictionary with packet's general data
    def get_general_data_dict(self):
        res = {self.SRC_IP: self.__src_ip, self.DST_IP: self.__dst_ip, self.SRC_PORT: self.__src_proto,
               self.DST_PORT: self.__dst_proto, self.SRC_GEOIP: self.__src_geoip, self.DST_GEOIP: self.__dst_geoip}
        return res

    # returns a dictionary contains packet's unique data (unique by protocol)
    @abstractmethod
    def get_specific_protocol_data_dict(self):
        pass

    # return's an empty dictionary with the packet unique field
    @staticmethod
    @abstractmethod
    def get_empty_data_dict():
        pass

    @abstractmethod
    def get_protocol(self):
        pass

    def get_src_dst_ip(self):
        return self.__src_ip, self.__dst_ip

    def get_src_dst_port(self):
        return self.__src_proto, self.__dst_proto

    def set_geoip(self, src_geoip, dst_geoip):
        self.__src_geoip = src_geoip
        self.__dst_geoip = dst_geoip
