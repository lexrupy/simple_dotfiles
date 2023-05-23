# Configuration
#. ~/.bash/config
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
        if [ -f "$HOME/.venvs/$1/bin/activate" ]
        then
            source ~/.venvs/$1/bin/activate; 
        fi
    else
        if [ -f ".env/bin/activate" ]
        then
            source ./.env/bin/activate;
        elif [ -f ".venv/bin/activate" ]
        then
            source ./.venv/bin/activate;
        fi
    fi
    source ~/.bash/profile;
}

