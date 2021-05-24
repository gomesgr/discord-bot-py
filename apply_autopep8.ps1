# Apply autopep8 to all .py associations on current directory utilizing .ps1 script
Get-Childitem *py | ForEach-Object { python -m autopep8 --in-place --aggressive --aggressive $_.fullname }
Write-Output "Done"