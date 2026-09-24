@echo off
chcp 65001 > nul
echo ========================================================
echo   Conectando o Repositorio ao GitHub - Dr. Jomil Costa
echo   Repositorio: https://github.com/jomilc/portifolio.git
echo ========================================================
echo.

git config user.name "Jomil Costa"
git config user.email "jomilc@gmail.com"

if not exist .git (
    echo [*] Inicializando repositorio Git local...
    git init
    git branch -M main
)

echo [*] Adicionando e preparando arquivos...
git add .
git commit -m "feat: portfolio cientifico, WebSIG e integracoes de IA" 2>nul

echo [*] Vinculando ao repositorio remoto...
git remote remove origin 2>nul
git remote add origin https://github.com/jomilc/portifolio.git

echo [*] Enviando arquivos para a branch main no GitHub...
git push -u origin main

echo.
if %ERRORLEVEL% EQU 0 (
    echo ========================================================
    echo   [SUCESSO] Repositorio publicado com sucesso!
    echo   Acesse: https://github.com/jomilc/portifolio
    echo ========================================================
) else (
    echo --------------------------------------------------------
    echo   Dica: Se solicitou autenticacao, utilize o navegador
    echo   ou cole o Personal Access Token (PAT) do GitHub.
    echo --------------------------------------------------------
)
pause
