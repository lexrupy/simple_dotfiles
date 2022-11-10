# Configuration
. ~/.bash/config
# Completions
. ~/.bash/completion/_git
complete -C ~/.bash/completion/_rake -o default rake
complete -C ~/.bash/completion/_project -o default p
complete -C ~/.bash/completion/_py_venv -o default activate
# Funcao para levar ao diretorio do projeto
function p { cd ~/projects/$1; }

function activate { 
    if [ ! -z "$1" ]
    then
        if [ -d "$HOME/.venvs/$1" ]
        then
            source ~/.venvs/$1/bin/activate; 
            source ~/.bash/profile;    
        fi
    fi
    
}

