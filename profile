# Configuration
. ~/.bash/config
# Completions
. ~/.bash/completion/_git
complete -C ~/.bash/completion/_rake -o default rake
complete -C ~/.bash/completion/_project -o default p
# Funcao para levar ao diretorio do projeto
function p { cd ~/code/$1; }

