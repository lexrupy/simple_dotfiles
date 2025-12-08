
#!/bin/bash

SECRET_FILE="$HOME/.secrets/secrets.txt"

get_totp() {
  oathtool --base32 --totp "$1"
}

# Cálculo de segundos restantes do intervalo TOTP (30s)
now=$(date +%s)
seconds_remaining=$((30 - (now % 30)))
seconds_remaining=$(printf "%02d" "$seconds_remaining")

output=""

# Ler o arquivo linha a linha
while IFS= read -r line; do
  # Ignora linhas vazias e comentários
  [[ -z "$line" || "$line" =~ ^# ]] && continue
  
  label="${line%%:*}"
  secret="${line#*:}"
  
  code=$(get_totp "$secret")

  # Se faltar 5s ou menos → label fica vermelho
  if (( seconds_remaining <= 5 )); then
    label_fmt="%{F#FF0000}${label}:%{F-}"
  else
    label_fmt="${label}:"
  fi

  output+="$label_fmt $code "
done < "$SECRET_FILE"

echo "$output[$seconds_remaining]"




# #!/bin/bash
#
# SECRET_FILE="$HOME/.secrets/secrets.txt"
#
# get_totp() {
#   oathtool --base32 --totp "$1"
# }
#
# # Cálculo de segundos restantes do intervalo TOTP (30s)
# now=$(date +%s)
# seconds_remaining=$((30 - (now % 30)))
# seconds_remaining=$(printf "%02d" "$seconds_remaining")
#
# output=""
#
# # Ler o arquivo linha a linha
# while IFS= read -r line; do
#   # Ignora linhas vazias e comentários
#   [[ -z "$line" || "$line" =~ ^# ]] && continue
#   
#   label="${line%%:*}"
#   secret="${line#*:}"
#   
#   code=$(get_totp "$secret")
#   output+="$label: $code "
# done < "$SECRET_FILE"
#
# echo "$output[$seconds_remaining]"
#
