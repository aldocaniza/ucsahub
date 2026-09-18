#!/usr/bin/env bash
# UCSA Hub — levanta la landing en LAN para acceso vía Tailscale.
# Uso: ./run_lan.sh [puerto]   (default: 8989)
set -euo pipefail

PORT="${1:-8989}"
HOST="0.0.0.0"
cd "$(dirname "$0")"

# IP preferida: Tailscale (acceso remoto). Fallback: IP de LAN local.
TAILSCALE_IP="$(tailscale ip -4 2>/dev/null | head -1 || true)"
if [[ -n "${TAILSCALE_IP}" ]]; then
    REPORT_IP="${TAILSCALE_IP}"
    NET="Tailscale"
else
    REPORT_IP="$(ip -4 addr show scope global 2>/dev/null | awk '/inet /{print $2}' | cut -d/ -f1 | head -1)"
    NET="LAN local (Tailscale no detectado)"
fi

# Puerto libre si el pedido está ocupado
while ss -tln 2>/dev/null | grep -q ":${PORT} "; do
    echo "⚠  Puerto ${PORT} ocupado → pruebo $((PORT + 1))"
    PORT=$((PORT + 1))
done

echo ""
echo "  █ UCSA Hub"
echo "  ─────────────────────────────────────────────"
echo "  Red:      ${NET}"
echo "  URL:      http://${REPORT_IP}:${PORT}"
echo "  Puerto:   ${PORT} (0.0.0.0)"
echo "  ─────────────────────────────────────────────"
echo "  Abrí esa URL desde cualquier dispositivo del"
echo "  mismo Tailscale para ver la landing completa."
echo ""

exec streamlit run app.py \
    --server.address "${HOST}" \
    --server.port "${PORT}" \
    --server.headless true \
    --browser.gatherUsageStats false