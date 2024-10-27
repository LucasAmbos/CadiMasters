@echo off
setlocal enabledelayedexpansion

:: Verifica se um argumento foi passado
if "%~1"=="" (
    echo Por favor, forneça o nome do usuário como argumento.
    exit /b 1
)

:: Usa o primeiro argumento como o nome do usuário
set "username=%~1"
echo Procurando pelo usuário: %username%

set regPath=HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList
set userFolder=C:\Users

:: Verifica se a pasta do usuário existe e renomeia
if exist "%userFolder%\%username%" (
    set "oldUserFolder=%userFolder%\old.%username%"
    echo Renomeando a pasta do usuário: %userFolder%\%username% para %oldUserFolder%
    ren "%userFolder%\%username%" "old.%username%"
    if !errorlevel! neq 0 (
        echo Erro ao renomear a pasta: %userFolder%\%username%
    ) else (
        echo Pasta renomeada para: %oldUserFolder%
    )
) else (
    echo A pasta do usuário "%username%" não foi encontrada em "%userFolder%".
    pause
    exit /b 1
)

:: Procura a chave de registro correspondente ao usuário e renomeia
for /f "tokens=*" %%i in ('reg query "%regPath%" /s /f "%username%" ^| findstr "HKEY_LOCAL_MACHINE"') do (
    set "currentKey=%%i"
    
    for /f "tokens=2,*" %%j in ('reg query "%%i" /v ProfileImagePath 2^>nul') do (
        set "profilePath=%%k"
        if /i "!profilePath:%username%=!" neq "!profilePath!" (
            echo Alterando a chave: %%i
            set "newKeyName=old.%%~nxi"
            set "newKeyPath=%regPath%\!newKeyName!"
            echo Renomeando a chave: %%i para !newKeyPath!
            reg copy "%%i" "!newKeyPath!" /f >nul 2>&1
            if !errorlevel! neq 0 (
                echo Erro ao copiar a chave: %%i
            ) else (
                reg delete "%%i" /f >nul 2>&1
                echo Chave renomeada para: !newKeyPath!
            )
        )
    )
)

echo Processo concluído.
pause
