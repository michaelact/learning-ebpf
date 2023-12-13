# Chapter 3 - Anatomy of an eBPF Program

## Exercise 5: Dropping Network Packets

If you attempt to modify the program to return 0 and connect it to a virtual machine's eth0 interface, all network packets will be dropped.

To simulate this, I use a container that automatically creates its own network interface.

### Provisioning

1. Create an nginx container:
```shell
sudo docker run -p 8080:80 -d nginx:stable
```

2. Access http://IP_ADDRESS:8080/

### Dropping Packets

1. Check which network interfaces were created by Docker:
```shell
sudo ip add
--- TRUNCATED
7: veth7eb4864@if6: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 xdp/id:141 qdisc noqueue master docker0 state UP group default
    link/ether 92:01:99:63:26:9d brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet6 fe80::9001:99ff:fe63:269d/64 scope link
       valid_lft forever preferred_lft forever
--- TRUNCATED
```

`veth7eb4864` is the interface name.

2. Compile the program:
```shell
sudo make

clang-18 \
    -target bpf \
        -I/usr/include/x86_64-linux-gnu \
        -g \
    -O2 -o exercise-5.bpf.o -c exercise-5.bpf.c
```

3. Attach the program:
```shell
sudo ip link set dev ens5 xdp obj exercise-5.bpf.o sec xdp
```

4. Access http://IP_ADDRESS:8080/ , and if you can't open it, it means the program was successfully attached.
