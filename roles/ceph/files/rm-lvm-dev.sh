#!/bin/bash

dev=$1

if [ "${dev}" == "" ]; then
    echo "Please specify a device"
    exit 1
fi

pv=`pvs | grep ${dev} | awk '{print $1}'`
if [ "${pv}" == "" ]; then
    exit 0
fi

vg=`pvs | grep ${pv} | awk '{print $2}'`

if [ "${vg}" != "" ]; then
    lv=`lvs | grep ${vg} | awk '{print $1}'`
    if [ "${lv}" != "" ]; then
        lvremove /dev/${vg}/${lv}
    fi
    vgremove ${vg}
fi

pvremove ${pv}
