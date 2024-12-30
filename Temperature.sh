#!/bin/sh
# - from Bob, N6TV (http://www.kkn.net/~n6tv/xadc.sh)
# - updated by Michael Hirsch, Ph.D.
# - (2020/07/05) upgraded with long-term monitoring log functionality (min/max values) by Saki, DD5XX

######################################
# path to IIO device
######################################

XADC_PATH=/sys/bus/iio/devices/iio:device0

######################################
# read temperature from STEMlab board
######################################

OFF=$(cat $XADC_PATH/in_temp0_offset)
RAW=$(cat $XADC_PATH/in_temp0_raw)
SCL=$(cat $XADC_PATH/in_temp0_scale)
FORMULA="(($OFF+$RAW)*$SCL)/1000.0"
TEMP=$(echo "scale=2;${FORMULA}" | bc)
echo ${TEMP}

