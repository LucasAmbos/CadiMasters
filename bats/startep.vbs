Set objShell = CreateObject("Shell.Application")

' Obtém o caminho do diretório onde o script está sendo executado
scriptPath = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)

' Define o caminho completo para o arquivo install_epson.exe
installerPath = scriptPath & "\install_epson.exe"

' Executa o instalador com elevação
objShell.ShellExecute installerPath, "", "", "runas", 1
