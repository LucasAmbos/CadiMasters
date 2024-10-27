@echo off
:: Excluir cache de todos os perfis do Microsoft Edge

:: Fechar todas as instâncias do Microsoft Edge
taskkill /F /IM msedge.exe

:: Caminho para os perfis do Microsoft Edge
set profilesPath=%LOCALAPPDATA%\Microsoft\Edge\User Data

:: Verifica se o diretório de perfis existe
if exist "%profilesPath%" (
    echo Excluindo cache de todos os perfis do Microsoft Edge...
    for /d %%p in ("%profilesPath%\*") do (
        if exist "%%p\Cache" (
            rmdir /s /q "%%p\Cache"
            echo Cache excluído para: %%p
        )
    )
    echo Cache excluído com sucesso.
) else (
    echo O diretório de perfis não foi encontrado.
)

start edge "https://sso.cloud.pje.jus.br/auth/realms/pje/protocol/openid-connect/auth?client_id=marketplace-frontend&redirect_uri=https%3A%2F%2Fmarketplace.pdpj.jus.br%2F&state=519ad137-67f9-466c-baa1-a66a265903ed&response_mode=fragment&response_type=code&scope=openid&nonce=ea771941-1807-4e79-918c-be79fc47a6c9"

exit
