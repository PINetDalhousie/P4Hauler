from scapy.all import Ether, StrFixedLenField, XByteField, IntField, Packet, bind_layers, IPField


class status(Packet):
    name = "status"
    fields_desc = [
                    # StrFixedLenField("P", "P", length=1),
                    # StrFixedLenField("Four", "4", length=1),
                    IntField("device_ip", "0"),
                    IntField("cpu_util", 0),
                    IntField("cpu_load", 0),
                    IntField("mem_usage", 0),
                    IntField("disk_util", 0),
                    IntField("net_util", 0)]

bind_layers(Ether, status, type=0x1235)
