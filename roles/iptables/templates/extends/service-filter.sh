#!/bin/bash

set -e

one_chain=one
iptables=/sbin/iptables
ip6tables=/sbin/ip6tables

flush_rules() {
    local bin=$1

    if [ ! -f /proc/net/ip_tables_names ]; then
        echo "Warning: skipping IPv4 (no module loaded)"
    elif [ -x "${bin}" ]; then
        for chain in INPUT FORWARD OUTPUT
        do
            "${bin}" -P "${chain}" ACCEPT
        done
        for param in F Z X; do "${bin}" -$param; done
        for table in $(cat /proc/net/ip_tables_names)
        do
            "${bin}" -t "${table}" -F
            "${bin}" -t "${table}" -Z
            "${bin}" -t "${table}" -X
        done
    fi
}

flush_one_chain() {
    local bin=$1

    if "${bin}" -nL "${one_chain}" 1>2 2>/dev/null; then
        "${bin}" -D INPUT -i {{ int_mgmt }} -j "${one_chain}"
        for i in F Z X; do "${bin}" -$i "${one_chain}"; done
    fi
{% block extra_flush %}{% endblock %}
}

apply_rules() {
    "${iptables}" -N "${one_chain}"
    "${ip6tables}" -N "${one_chain}"

    # common
    "${iptables}" -A "${one_chain}" -i lo -j ACCEPT
    "${iptables}" -A "${one_chain}" -p icmp --icmp-type echo-request -j ACCEPT
    "${iptables}" -A "${one_chain}" -m state --state RELATED,ESTABLISHED -j ACCEPT
    "${ip6tables}" -A "${one_chain}" -i lo -j ACCEPT
    "${ip6tables}" -A "${one_chain}" -p icmp -j ACCEPT
    "${ip6tables}" -A "${one_chain}" -m state --state RELATED,ESTABLISHED -j ACCEPT

{% block rules %}{% endblock %}

    if [ "$2" = "debug" ]; then
        "${iptables}" -A "${one_chain}" -j LOG --log-prefix "IPTABLES_DEBUG "
        "${ip6tables}" -A "${one_chain}" -j LOG --log-prefix "IPTABLES_DEBUG "
    fi
    "${iptables}" -A "${one_chain}" -j DROP
    "${ip6tables}" -A "${one_chain}" -j DROP

    # apply
    "${iptables}" -I INPUT -i {{ int_mgmt }} -j "${one_chain}"
    "${ip6tables}" -I INPUT -i {{ int_mgmt }} -j "${one_chain}"
{% block extra_rules %}{% endblock %}
}

case $1 in
start|reload|restart)
    flush_one_chain "${iptables}"
    flush_one_chain "${ip6tables}"
    apply_rules
    ;;
debug)
    flush_one_chain "${iptables}"
    flush_one_chain "${ip6tables}"
    apply_rules debug
    ;;
stop)
    flush_one_chain "${iptables}"
    flush_one_chain "${ip6tables}"
    ;;
flushall)
    flush_rules "${iptables}"
    flush_rules "${ip6tables}"
    ;;
*)
    echo "Usage: ${0} (start|stop|reload|restart|flushall|debug)"
    exit 1
    ;;
esac
