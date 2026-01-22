$UUID = (Get-CimInstance Win32_ComputerSystemProduct).UUID
"PC_UUID=$UUID" | Set-Content .env
docker compose -p control-host up --build