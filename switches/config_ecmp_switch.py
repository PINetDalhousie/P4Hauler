table1 = bfrt.ecmp_switch.pipe.SwitchIngress.ipv4_lpm

entry = table1.entry_with_ipv4_forward(dst_addr=0x0A320101 , dst_mac=0x00154d1211a9, port="132").push()
entry = table1.entry_with_ipv4_forward(dst_addr=0x0A320106 , dst_mac=0xb8599fdf07cb, port="188").push()
entry = table1.entry_with_ipv4_forward(dst_addr=0x0A320110 , dst_mac=0xb8599fdf07d1, port="188").push()



lag_ecmp = bfrt.ecmp_switch.pipe.SwitchIngress.lag_ecmp


mbr_base = 200000
dest_1 = mbr_base + 1; lag_ecmp.entry_with_send(dest_1, dest=0x0A320106).push() #Should set IP1


dest_2 = mbr_base + 2; lag_ecmp.entry_with_send(dest_2, dest=0x0A320110).push() #Should set IP2


lag_ecmp_sel = bfrt.ecmp_switch.pipe.SwitchIngress.lag_ecmp_sel






lag_1 = 2000;
lag_ecmp_sel.entry(SELECTOR_GROUP_ID=lag_1,
                       ACTION_MEMBER_ID=[dest_1, dest_2],
                       ACTION_MEMBER_STATUS=[True, True]).push()




nexthop = bfrt.ecmp_switch.pipe.SwitchIngress.nexthop
nexthop.entry(dst_addr=0x0A320164, SELECTOR_GROUP_ID=lag_1).push()
