#!/bin/bash
# Validar glosario.bib para detectar entradas duplicadas

GLOSARIO="glosario.bib"
ERRORS=0

echo "Validando $GLOSARIO..."
echo ""

# Extraer todas las claves de entrada (@entry{...})
KEYS=$(grep "^@entry{" "$GLOSARIO" | sed 's/@entry{\(.*\),/\1/' | sort)

# Detectar duplicadas
DUPLICATES=$(echo "$KEYS" | uniq -d)

if [ -n "$DUPLICATES" ]; then
  echo "❌ ENTRADAS DUPLICADAS ENCONTRADAS:"
  echo ""
  while IFS= read -r dup; do
    echo "  - $dup"
    grep -n "^@entry{$dup," "$GLOSARIO"
  done <<< "$DUPLICATES"
  echo ""
  ERRORS=$((ERRORS + 1))
fi

# Verificar sintaxis básica
UNCLOSED=$(grep -c "^@entry{" "$GLOSARIO")
CLOSED=$(grep -c "^}" "$GLOSARIO")

if [ "$UNCLOSED" -ne "$CLOSED" ]; then
  echo "❌ ERROR: Entradas abiertas ($UNCLOSED) ≠ Cerradas ($CLOSED)"
  ERRORS=$((ERRORS + 1))
fi

if [ $ERRORS -eq 0 ]; then
  echo "✓ glosario.bib válido"
  echo "  - $(echo "$KEYS" | wc -l) entradas únicas"
  exit 0
else
  echo ""
  echo "❌ $ERRORS errores encontrados en glosario.bib"
  exit 1
fi
