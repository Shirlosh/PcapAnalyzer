from PacketHandler import PacketsFactory
from PacketHandler.Packet import Packet


class HTTPResponsePacket(Packet):
    RESPONSE_CODE = 'response code'

    def __init__(self, src_dst_ip, src_dst_proto, src_geoip, dst_geoip, http_data):
        super().__init__(src_dst_ip, src_dst_proto, src_geoip, dst_geoip)
        self.__res_data = http_data
        self.__PROTOCOL = PacketsFactory.PacketsFactory.HTTP_RES

    def get_specific_protocol_data_dict(self):
        return {self.RESPONSE_CODE: self.get_response_code()}

    @staticmethod
    def get_empty_data_dict():
        return {HTTPResponsePacket.RESPONSE_CODE: None}

    def get_protocol(self):
        return self.__PROTOCOL

    def get_response_code(self):
        x, req = self.__res_data
        return req.status
