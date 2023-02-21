#!/bin/bash

power=$(vcgencmd display_power | egrep -o '[0-9]')

if [ $power -eq 1 ];
then
 sudo vcgencmd display_power 0
else
 sudo vcgencmd display_power 1
fi


