@echo off
setlocal
set hostname=%1
set installer_path=%2

:: Verifica se o hostname e o caminho do instalador foram passados
if "%hostname%"=="" (
    echo Por favor, forneça o hostname.
    exit /b 1
)

if "%installer_path%"=="" (
    echo Por favor, forneça o caminho do instalador.
    exit /b 1
)

:: Lê o ID da sessão do arquivo temporário
set /p session_id=<session_id.txt

:: Tenta executar o instalador com o parâmetro de instalação silenciosa
psexec -i %session_id% -s \\%hostname% cmd /c "%installer_path%" /S /silent
exit /b 0
