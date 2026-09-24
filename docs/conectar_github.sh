#!/bin/bash
echo "========================================================"
echo "  Conectando o Repositório ao GitHub - Dr. Jomil Costa"
echo "  Usuário: jomilc"
echo "========================================================"

git config user.name "Jomil Costa"
git config user.email "jomilc@gmail.com"

if [ ! -d ".git" ]; then
    echo "[*] Inicializando repositório Git local..."
    git init
    git branch -M main
fi

echo "[*] Adicionando arquivos..."
git add .
git commit -m "feat: portfolio cientifico, WebSIG e integracoes de IA" 2>/dev/null

echo "[*] Conectando ao GitHub remoto..."
git remote remove origin 2>/dev/null
git remote add origin https://github.com/jomilc/portfolio-jomil-costa.git

echo "[*] Enviando para o branch main no GitHub..."
git push -u origin main
