#!/bin/bash
PC_UUID=$(sudo cat /sys/class/dmi/id/product_uuid 2>/dev/null || echo "UUID_NO_DEFINIDO")
echo "PC_UUID=$PC_UUID" > .env
docker compose up -p control-host --build