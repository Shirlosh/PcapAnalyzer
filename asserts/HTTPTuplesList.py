from PacketHandler.Packet import Packet
from PacketHandler.PacketTypes.HTTPRequestPacket import HTTPRequestPacket
from PacketHandler.PacketTypes.HTTPResponsePacket import HTTPResponsePacket
from PacketHandler.PacketsFactory import PacketsFactory


class HTTPTuplesList:
    COUNT = 'packets count'

    def __init__(self):
        self.__t_list = []

    def add_HTTP(self, packet: Packet):
        src, dst = packet.get_src_dst_ip()
        src_p, dst_p = packet.get_src_dst_port()
        item = self.__tuple_exist(src, dst, src_p, dst_p, packet.get_protocol())

        if item is not None:
            self.__update_dict(item, packet)
        else:
            self.__add_to_dict(packet)

    # update an exist tuple
    def __update_dict(self, item, packet):

        if packet.get_protocol() == PacketsFactory.HTTP_RES:
            filtered_dict = packet.get_general_data_dict()
            filtered_dict.update(packet.get_specific_protocol_data_dict())
        else:
            filtered_dict = packet.get_specific_protocol_data_dict()

        for key, value in filtered_dict.items():
            item[key] = value

        item[self.COUNT] = item[self.COUNT] + 1

    # add a new tuple to the dict
    def __add_to_dict(self, packet):
        new_tuple = packet.get_general_data_dict()

        if packet.get_protocol() == PacketsFactory.HTTP_REQ:
            req_dict = packet.get_specific_protocol_data_dict()
            res_dict = HTTPResponsePacket.get_empty_data_dict()

        else:
            res_dict = packet.get_specific_protocol_data_dict()
            req_dict = HTTPRequestPacket.get_empty_data_dict()

        new_tuple.update(req_dict)
        new_tuple.update(res_dict)
        new_tuple.update({self.COUNT: 1})

        self.__t_list.append(new_tuple)

    # checks if the tuple exist,
    # check for a http flow (request response match)
    def __tuple_exist(self, src_ip, dst_ip, src_por, dst_por, protocol):
        if protocol == PacketsFactory.HTTP_RES:
            tpl = self.__search_tuple(dst_ip, src_ip, dst_por, src_por)  # check if a request is already existed
            if tpl is None:
                tpl = self.__search_tuple(src_ip, dst_ip, src_por, dst_por)  # search a matching http response
        else:
            tpl = self.__search_tuple(src_ip, dst_ip, src_por, dst_por)
        return tpl

    # search a tuple with similar src ip and port, dst ip and port
    def __search_tuple(self, src_ip, dst_ip, src_por, dst_por):
        try:
            itm = next(item for item in self.__t_list if item[Packet.DST_IP] == dst_ip and
                       item[Packet.SRC_IP] == src_ip and item[Packet.DST_PORT] == dst_por and
                       item[Packet.SRC_PORT] == src_por)

        except BaseException:
            itm = None
        return itm

    def get_dict(self):
        return self.__t_list
