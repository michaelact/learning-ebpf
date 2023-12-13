#include <linux/bpf.h>
#include <bpf/bpf_helpers.h>

int counter = 0;

SEC("xdp")
int drop(struct xdp_md *ctx) {
    bpf_printk("Dropped %d", counter);
    counter++;
    return 0;
}

char LICENSE[] SEC("license") = "Dual BSD/GPL";