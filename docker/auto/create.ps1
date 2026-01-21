$UUID = (Get-CimInstance Win32_ComputerSystemProduct).UUID
"PC_UUID=$UUID" | Set-Content .env
docker compose -p Control-Host up --build