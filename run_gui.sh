#!/bin/bash
# Script para executar a GUI em Linux/macOS

APP_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_PYTHON="$APP_DIR/.venv/bin/python"

# Verifica se o venv existe
if [ ! -f "$VENV_PYTHON" ]; then
    echo "Erro: Python do venv não encontrado em $VENV_PYTHON"
    echo "Execute primeiro: python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Executa o script GUI
"$VENV_PYTHON" "$APP_DIR/run_gui.py" "$@"