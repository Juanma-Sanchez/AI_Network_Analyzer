sed -i 's/hostname.*/hostname '$HOSTNAME'/' /etc/frr/frr.conf

interfaces=$(ip link show | grep ' eth' | awk -F: '{print $2}')
for intf in $interfaces; do
  echo "  interface $intf"
  echo "    ip router isis FOO"
done >> /etc/frr/frr.conf

echo ! >> /etc/frr/frr.conf

/usr/lib/frr/zebra -f /etc/frr/frr.conf -d & /usr/lib/frr/isisd -f /etc/frr/frr.conf -d & service frr start & service snmpd restart & tail -f /dev/null