table1 = bfrt.p4mite_switch.pipe.SwitchIngress.ipv4_lpm
entry = table1.entry_with_ipv4_forward(dst_addr=0x0A320101 , dst_mac=0x00154d1211a9, port="132").push()

#entry = table1.entry_with_ipv4_forward(dst_addr=0x0A320005 , dst_mac=0xb8599fdf07fa, port="189").push()
#entry = table1.entry_with_ipv4_forward(dst_addr=0x0A32000F , dst_mac=0xb8599fdf0800, port="189").push()

entry = table1.entry_with_ipv4_forward(dst_addr=0x0A320106 , dst_mac=0xb8599fdf07cb, port="188").push()
entry = table1.entry_with_ipv4_forward(dst_addr=0x0A320110 , dst_mac=0xb8599fdf07d1, port="188").push()

table2 = bfrt.p4mite_switch.pipe.SwitchIngress.LB
entry = table2.entry_with_LB_forward(dst_addr=0x0A320164).push()
table3 = bfrt.p4mite_switch.pipe.SwitchIngress.available_server_table
entry = table3.entry_with_available_server_action(dst_addr=0x0A320164).push()

DIP_table = bfrt.p4mite_switch.pipe.SwitchIngress.DIP_table
entry = DIP_table.entry_with_dip_calc(server_code=0, available_server_meta=0x0a320106, dip_entry=0x0a320106).push()
entry = DIP_table.entry_with_dip_calc(server_code=0, available_server_meta=0x0a320110, dip_entry=0x0a320110).push()
