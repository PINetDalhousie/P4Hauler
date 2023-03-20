table1 = bfrt.least_utilized.pipe.SwitchIngress.routing
table2 = bfrt.least_utilized.pipe.SwitchIngress.LB


entry = table1.entry_with_route(dst_addr=0x0A320101 , dst_mac=0x00154d1211a9, port="132").push()
entry = table1.entry_with_route(dst_addr=0x0A320106 , dst_mac=0xb8599fdf07cb, port="188").push()
entry = table1.entry_with_route(dst_addr=0x0A320110 , dst_mac=0xb8599fdf07d1, port="188").push()


entry = table2.entry_with_LB_forward(dst_addr=0x0A320164).push()

table1.dump(from_hw=1)
table2.dump(from_hw=1)


bfrt.least_utilized.pipe.available_device_address.clear()
bfrt.least_utilized.pipe.device1_status.clear()
bfrt.least_utilized.pipe.device2_status.clear()
bfrt.least_utilized.pipe.device3_status.clear()

bfrt.least_utilized.pipe.available_device_address.dump(from_hw=1)
bfrt.least_utilized.pipe.device1_status.dump(from_hw=1)
bfrt.least_utilized.pipe.device2_status.dump(from_hw=1)
bfrt.least_utilized.pipe.device3_status.dump(from_hw=1)

# bfrt.least_utilized.pipe.bloom_filter.dump(from_hw=1)
# bfrt.least_utilized.pipe.bloom_filter.clear()


# table3 = bfrt.p4mite_switch.pipe.SwitchIngress.available_server_table
# entry = table3.entry_with_available_server_action(dst_addr=0x0A320164).push()

# DIP_table = bfrt.p4mite_switch.pipe.SwitchIngress.DIP_table
# entry = DIP_table.entry_with_dip_calc(server_code=0, available_server_meta=0x0a320106, dip_entry=0x0a320106).push()
# entry = DIP_table.entry_with_dip_calc(server_code=0, available_server_meta=0x0a320110, dip_entry=0x0a320110).push()
