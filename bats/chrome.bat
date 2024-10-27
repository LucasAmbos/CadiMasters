@echo off
:: Fechar todas as instâncias do Google Chrome
taskkill /F /IM chrome.exe

:: Caminho para os perfis do Google Chrome
set profilesPath=%LOCALAPPDATA%\Google\Chrome\User Data

:: Verifica se o diretório de perfis existe
if exist "%profilesPath%" (
    echo Excluindo cache de todos os perfis do Google Chrome...
    for /d %%p in ("%profilesPath%\Profile*") do (
        if exist "%%p\Cache" (
            rmdir /s /q "%%p\Cache"
            echo Cache excluído para: %%p
        )
    )
    if exist "%profilesPath%\Default\Cache" (
        rmdir /s /q "%profilesPath%\Default\Cache"
        echo Cache excluído para o perfil padrão.
    )
    echo Cache excluído com sucesso.
) else (
    echo O diretório de perfis não foi encontrado.
)

exit
