table1 = bfrt.round_robin.pipe.SwitchIngress.ipv4_lpm

entry = table1.entry_with_ipv4_forward(dst_addr=0x0A320101 , dst_mac=0x00154d1211a9, port="132").push()
entry = table1.entry_with_ipv4_forward(dst_addr=0x0A320106 , dst_mac=0xb8599fdf07cb, port="188").push()
entry = table1.entry_with_ipv4_forward(dst_addr=0x0A320110 , dst_mac=0xb8599fdf07d1, port="188").push()

entry = table1.entry_with_ipv4_forward(dst_addr=0x0A320105 , dst_mac=0xb8599fdf07fb, port="189").push()




table2 = bfrt.round_robin.pipe.SwitchIngress.LB
entry = table2.entry_with_LB_forward(dst_addr=0x0A320164).push()


bfrt.round_robin.pipe.circular_queue.add(0, 1)
bfrt.round_robin.pipe.circular_queue.add(1, 1)
bfrt.round_robin.pipe.circular_queue.add(2, 1)
bfrt.round_robin.pipe.circular_queue.add(3, 1)
bfrt.round_robin.pipe.circular_queue.add(4, 1)
bfrt.round_robin.pipe.circular_queue.add(5, 0)
bfrt.round_robin.pipe.circular_queue.add(6, 1)
bfrt.round_robin.pipe.circular_queue.add(7, 1)
bfrt.round_robin.pipe.circular_queue.add(8, 1)
bfrt.round_robin.pipe.circular_queue.add(9, 1)

bfrt.round_robin.pipe.queue_iterator.add(0,0)
