@echo off
rem Captura o ID do usuário logado
for /f "tokens=3" %%i in ('query user %USERNAME%') do set UserID=%%i

rem Salva o arquivo .txt no diretório atual onde o .bat foi executado
echo %UserID% > "%~dp0id_usuario.txt"

rem Exibe o ID do usuário para confirmação
echo ID do usuário: %UserID%

exit
