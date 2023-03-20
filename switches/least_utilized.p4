
/* -*- P4_16 -*- */

/*******************************************************************************
 * BAREFOOT NETWORKS CONFIDENTIAL & PROPRIETARY
 *
 * Copyright (c) Intel Corporation
 * SPDX-License-Identifier: CC-BY-ND-4.0
 */


#include <core.p4>
#if __TARGET_TOFINO__ == 2
#include <t2na.p4>
#else
#include <tna.p4>
#endif

#include "headers.p4"
#include "util.p4"

struct metadata_t {
    bit<16> checksum_udp_tmp;
    ipv4_addr_t available_server_meta;
    ipv4_addr_t tmp_address_meta;
    bit<8> tmp1_util_meta;
    bit<8> tmp2_util_meta;
}

const bit<16> TYPE_IPV4 = 0x800;
const bit<16> TYPE_AGENT = 0x1234;



// bit<32> smartnic = 0x0A32000B;

// ---------------------------------------------------------------------------
// Ingress parser
// ---------------------------------------------------------------------------
parser SwitchIngressParser(
    packet_in pkt,
    out header_t hdr,
    out metadata_t ig_md,
    out ingress_intrinsic_metadata_t ig_intr_md) {

        TofinoIngressParser() tofino_parser;
        Checksum() ipv4_checksum;
        Checksum() udp_checksum;
        state start {
            tofino_parser.apply(pkt, ig_intr_md);
            ig_md.checksum_udp_tmp = 0;
            ig_md.available_server_meta = 0;
            ig_md.tmp_address_meta = 0x0f0f0f0f;
            ig_md.tmp1_util_meta = 100;
            ig_md.tmp2_util_meta = 100;
            transition parse_ethernet;
        }

        state parse_ethernet {
            pkt.extract(hdr.ethernet);
            transition select(hdr.ethernet.ether_type) {
                TYPE_IPV4: parse_ipv4;
                TYPE_AGENT : parse_agent_information;
                default: accept;
            }
        }

        state parse_agent_information {
            pkt.extract(hdr.agent);
            transition accept;
        }

        state parse_ipv4 {
            pkt.extract(hdr.ipv4);
            ipv4_checksum.add(hdr.ipv4);

            udp_checksum.subtract({hdr.ipv4.dst_addr});
            transition select(hdr.ipv4.protocol) {
                IP_PROTOCOLS_UDP : parse_udp;
                default : accept;
            }
        }
        state parse_udp {
            // The tcp checksum cannot be verified, since we cannot compute
            // the payload's checksum.
            pkt.extract(hdr.udp);
            udp_checksum.subtract({hdr.udp.checksum});
            ig_md.checksum_udp_tmp = udp_checksum.get();
            transition accept;
        }
}

// ---------------------------------------------------------------------------
// Ingress
// ---------------------------------------------------------------------------
// Here is the bloom filter

struct pair {
    bit<32> is_valid;
    bit<32> server_address;
}


Register<pair, bit<16>>(50000) bloom_filter;
// Register<bit<32>, _>(256) server_table;
// Register<bit<32>, _>(256) accelerator_0;
// Register<bit<32>, _>(256) accelerator_1;

struct status_struct {
    bit <32> least_util;
    bit <32> device_util;
}

Register<bit<32>, _>(1) device1_status;
Register<bit<32>, _>(1) device2_status;
Register<bit<32>, _>(1) device3_status;


Register<bit<32>, _>(1) available_device_address;

control SwitchIngress(
        inout header_t hdr,
        inout metadata_t ig_md,
        in ingress_intrinsic_metadata_t ig_intr_md,
        in ingress_intrinsic_metadata_from_parser_t ig_intr_prsr_md,
        inout ingress_intrinsic_metadata_for_deparser_t ig_intr_dprsr_md,
        inout ingress_intrinsic_metadata_for_tm_t ig_intr_tm_md) {


    ipv4_addr_t final_addr;
    bit<32> vip = 0x0A320064;
    bit<32> min_tmp;
    bit<32> dev1;
    bit<32> dev2;

    RegisterAction<bit<32>, _, bit<32>>(available_device_address) read_available_device_address= {
    void apply(inout bit<32> value, out bit<32> rv) {
            rv = value;
        }
    };

    RegisterAction<bit<32>, _, bit<32>>(available_device_address) Update_Device = {
    void apply(inout bit<32> value, out bit<32> rv) {
            value = final_addr;
            rv = value;
        }
    };


    RegisterAction<bit<32>, _,bit<32>>(device1_status) update_device1_status = {
        void apply(inout bit<32> value, out bit<32> rv) {
            if(hdr.agent.src_addr == 1){
                value = hdr.agent.cpu_util;
            }
            rv = value;
        }
    };

    RegisterAction<bit<32>, _,bit<32>>(device2_status) update_device2_status = {
        void apply(inout bit<32> value, out bit<32> rv) {
            if(hdr.agent.src_addr == 2){
                value = hdr.agent.cpu_util;
            }
            rv = value;
        }
    };

    RegisterAction<bit<32>, _,bit<32>>(device3_status) update_device3_status = {
        void apply(inout bit<32> value, out bit<32> rv) {
            if(hdr.agent.src_addr == 3){
                value = hdr.agent.cpu_util;
            }
            rv = value;
        }
    };


    RegisterAction<pair, bit<16>, bit<32>>(bloom_filter) read = {
    void apply(inout pair value, out bit<32> rv) {
        if (value.is_valid == 0) {
            value.is_valid = 1;
            value.server_address = ig_md.available_server_meta;
        }
        rv = value.server_address;
        if (hdr.ipv4.total_len==28) {
            value.is_valid = 0;}
        }
    };


    DirectCounter<bit<32>>(CounterType_t.PACKETS) pktcount;
    Hash<bit<16>>(HashAlgorithm_t.CRC16) hash;
    action LB_forward() {
        bit<16> index = hash.get({ hdr.udp.src_port, hdr.ipv4.src_addr});
        hdr.ipv4.dst_addr = read.execute(index);
        // hdr.ipv4.dst_addr = 0x0A320106;
        pktcount.count();
    }

    action Nothing() {pktcount.count();}

    table LB {
        key = {hdr.ipv4.dst_addr: exact;}
        actions = {LB_forward; Nothing;}
        size = 1024;
        counters = pktcount;
        default_action = Nothing;
    }

    DirectCounter<bit<32>>(CounterType_t.PACKETS) pktcount2;
    action route (PortId_t port, mac_addr_t dst_mac) {
        ig_intr_tm_md.ucast_egress_port = port;
        hdr.ethernet.dst_addr = dst_mac;
        hdr.ipv4.ttl = hdr.ipv4.ttl - 1;
        pktcount2.count();
    }
    action drop_routing() {
        ig_intr_dprsr_md.drop_ctl = 0;
        pktcount2.count();
    }
    table routing {
        key = {hdr.ipv4.dst_addr: exact;}
        actions = {route; drop_routing;}
        size = 1024;
        counters = pktcount2;
        default_action = drop_routing();
    }

    action server_decision() {
        ig_md.available_server_meta = read_available_device_address.execute(0);
    }

    apply {
        if (hdr.agent.isValid()) {
             dev1 = update_device1_status.execute(0);
             dev2 = update_device2_status.execute(0);
             min_tmp = min(dev1, dev2);
             final_addr = 0x0A320110;          //device 2 destination
             if (min_tmp == dev1){
             	  final_addr = 0x0A320106;      //device 1 destination
             }
             dev1 = update_device3_status.execute(0);
             min_tmp = min(dev1, min_tmp);
             if (min_tmp == dev1){
             	  final_addr = 0x0A320111;      //device 3 destination
             }
	     ig_md.available_server_meta = Update_Device.execute(0);
 	   }
        else {
                server_decision();
                LB.apply();
                routing.apply();
        }
        ig_intr_tm_md.bypass_egress = 1w1;
    }
}



// ---------------------------------------------------------------------------
// Ingress Deparser
// ---------------------------------------------------------------------------
control SwitchIngressDeparser(
        packet_out pkt,
        inout header_t hdr,
        in metadata_t ig_md,
        in ingress_intrinsic_metadata_for_deparser_t ig_intr_dprsr_md) {

    Checksum() ipv4_checksum;
    Checksum() udp_checksum;
    apply {
        hdr.ipv4.hdr_checksum = ipv4_checksum.update(
            {hdr.ipv4.version,
            hdr.ipv4.ihl,
            hdr.ipv4.diffserv,
            hdr.ipv4.total_len,
            hdr.ipv4.identification,
            hdr.ipv4.flags,
            hdr.ipv4.frag_offset,
            hdr.ipv4.ttl,
            hdr.ipv4.protocol,
            hdr.ipv4.src_addr,
            hdr.ipv4.dst_addr});

        hdr.udp.checksum = udp_checksum.update(data = {
            hdr.ipv4.dst_addr,
            ig_md.checksum_udp_tmp
            }, zeros_as_ones = true);
        // UDP specific checksum handling

        pkt.emit(hdr.ethernet);
        pkt.emit(hdr.ipv4);
        pkt.emit(hdr.udp);
    }
}

Pipeline(SwitchIngressParser(),
         SwitchIngress(),
         SwitchIngressDeparser(),
         EmptyEgressParser(),
         EmptyEgress(),
         EmptyEgressDeparser()) pipe;

Switch(pipe) main;
