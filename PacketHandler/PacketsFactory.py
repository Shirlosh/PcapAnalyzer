import dpkt
import socket

from PacketHandler.PacketTypes.HTTPRequestPacket import HTTPRequestPacket
from PacketHandler.PacketTypes.HTTPResponsePacket import HTTPResponsePacket


# this factory gets a buf and a timestamp and create a relevant packet-by-protocol object
class PacketsFactory:
    HTTP_REQ = "HTTP Request"
    HTTP_RES = "HTTP Response"

    def __init__(self, buf, timestamp):
        self.__buf = buf
        self.__timestamp = timestamp
        self.__ethernet = dpkt.ethernet.Ethernet(buf)
        self.__init_ip()
        self.__tcp = self.__ip.data
        self.__http_data = None

    # returns the relevant packet-protocol object
    def get_packet(self, src_geoip=None, dst_geoip=None):
        protocol = self.__get_protocol()
        res = None

        if protocol == self.HTTP_REQ:
            res = HTTPRequestPacket(self.__get_src_dst_ip(), self.__get_src_dst_port(), src_geoip, dst_geoip,
                                    self.__http_data)

        elif protocol == self.HTTP_RES:
            res = HTTPResponsePacket(self.__get_src_dst_ip(), self.__get_src_dst_port(), src_geoip, dst_geoip,
                                     self.__http_data)

        return res

    def __init_ip(self):
        if isinstance(self.__ethernet.data, dpkt.ip.IP):
            self.__ip = self.__ethernet.data
            self.__src = self.__ethernet.data.src
            self.__dst = self.__ethernet.data.dst
        else:
            raise ValueError('Non IP Packet type not supported %s\n' % self.__ethernet.data.__class__.__name__)

    def __get_http_data(self):
        if self.__http_data is None:
            try:
                self.__http_data = (self.HTTP_REQ, dpkt.http.Request(self.__tcp.data))
            except (dpkt.dpkt.NeedData, dpkt.dpkt.UnpackError):
                try:
                    self.__http_data = (self.HTTP_RES, dpkt.http.Response(self.__tcp.data))
                except (dpkt.dpkt.NeedData, dpkt.dpkt.UnpackError):
                    self.__http_data = (self.__ip.get_proto(self.__ip.p).__name__, None)
                    raise ValueError("protocol isn't http")
        r1eq_type, req = self.__http_data
        return req

    def __get_protocol(self):
        try:
            self.__get_http_data()
        except ValueError:
            pass
        req_type, req = self.__http_data
        return req_type

    def __get_src_dst_ip(self):
        return self.__inet_to_str(self.__src), self.__inet_to_str(self.__dst)

    def __get_src_dst_port(self):
        src = self.__ip.data.sport
        dst = self.__ip.data.sport
        return src, dst

    # decode ip byte string to ascii
    @staticmethod
    def __inet_to_str(inet):
        try:
            return socket.inet_ntop(socket.AF_INET, inet)
        except ValueError:
            return socket.inet_ntop(socket.AF_INET6, inet)
