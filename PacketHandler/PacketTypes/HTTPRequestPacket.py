from PacketHandler import PacketsFactory
from PacketHandler.Packet import Packet


class HTTPRequestPacket(Packet):
    METHOD = 'method'
    URI = 'uri'
    AGENT = 'user-agent'
    HOST = 'host'

    def __init__(self, src_dst_ip, src_dst_proto, src_geoip, dst_geoip, http_data):
        super(HTTPRequestPacket, self).__init__(src_dst_ip, src_dst_proto, src_geoip, dst_geoip)
        self.__req_data = http_data
        self.__PROTOCOL = PacketsFactory.PacketsFactory.HTTP_REQ

    def get_specific_protocol_data_dict(self):
        return {self.METHOD: self.get_method(), self.AGENT: self.get_user_agent(), self.URI: self.get_uri(),
                self.HOST: self.get_host()}

    @staticmethod
    def get_empty_data_dict():
        return {HTTPRequestPacket.METHOD: None, HTTPRequestPacket.AGENT: None, HTTPRequestPacket.URI: None, HTTPRequestPacket.HOST: None}

    def get_protocol(self):
        return self.__PROTOCOL

    def get_user_agent(self):
        x, req = self.__req_data
        if self.AGENT in req.headers:
            return req.headers[self.AGENT]
        else:
            return None

    def get_uri(self):
        x, req = self.__req_data
        return req.uri

    def get_host(self):
        x, req = self.__req_data
        if self.HOST in req.headers:
            return req.headers[self.HOST]
        else:
            return None

    def get_method(self):
        x, req = self.__req_data
        return req.method
