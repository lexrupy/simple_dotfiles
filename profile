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

# alias vi="nvim"

alias lazy="NVIM_APPNAME=LazyVim nvim"
alias chad="NVIM_APPNAME=NvChad nvim"
alias astro="NVIM_APPNAME=AstroNvim nvim"

function nvims() {
  items=("AstroNvim" "NvChad" "LazyVim" "default")
  config=$(printf "%s\n" "${items[@]}" | fzf --prompt=" Neovim Config  " --height=~50% --layout=reverse --border --exit-0)
  if [[ -z $config ]]; then
    echo "Nothing selected"
    return 0
  elif [[ $config == "default" ]]; then
    config=""
  else
    alias vi="NVIM_APPNAME=${config} nvim"
  fi
  NVIM_APPNAME=$config nvim $@
}



alias tmuxd="tmux new-session \; split-window -v -p 15\; split-window -h\; select-pane -t 1\; attach"
export PATH="$HOME/.local/bin:$PATH"
