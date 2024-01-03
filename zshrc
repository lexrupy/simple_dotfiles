# Enable Powerlevel10k instant prompt. Should stay close to the top of ~/.zshrc.
# Initialization code that may require console input (password prompts, [y/n]
# confirmations, etc.) must go above this block; everything else may go below.
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

source ~/.powerlevel10k/powerlevel10k.zsh-theme

# To customize prompt, run `p10k configure` or edit ~/.p10k.zsh.
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh

fpath=(~/.bash/zsh/functions $fpath)

autoload -U ~/.dotfiles/zsh/functions/*(:t)

HISTFILE=~/.zsh_history
HISTSIZE=1000
SAVEHIST=1000
REPORTTIME=10 # print elapsed time when more than 10 seconds

alias clock="tty-clock -C 4"

alias ls="exa --icons"

alias cat="batcat"

alias la="ls -la"
alias ll="ls -l"

alias nvimb="/usr/bin/nvim"
#
# alias lazy="NVIM_APPNAME=LazyVim nvimb"
# alias chad="NVIM_APPNAME=NvChad nvimb"
alias nvim="NVIM_APPNAME=AstroNvim nvimb"
# alias vim="nvimb"
#
function nvims() {
  items=("AstroNvim" "NvChad" "LazyVim" "default")
  config=$(printf "%s\n" "${items[@]}" | fzf --prompt=" Neovim Config  " --height=~50% --layout=reverse --border --exit-0)
  if [[ -z $config ]]; then
    echo "Nothing selected"
    return 0
  elif [[ $config == "default" ]]; then
    config=""
  fi
  NVIM_APPNAME=$config nvimb $@
}


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
}

# export MANPAGER='/usr/bin/nvim +Man!'
# export MANWIDTH=999

autoload -U compinit
compinit

# matches case insensitive for lowercase
zstyle ':completion:*' matcher-list 'm:{a-z}={A-Z}'

# pasting with tabs doesn't perform completion
zstyle ':completion:*' insert-tab pending

export PYENV_ROOT="$HOME/.pyenv"
command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"

eval "$(pyenv virtualenv-init -)"

eval "$(direnv hook zsh)"

export PATH="$HOME/.pyenv/bin:$PATH"
export PATH="$HOME/.config/emacs/bin:$PATH"
export PATH="$HOME/.local/bin:$PATH"

eval "$(pyenv init -)"

eval "$(pyenv virtualenv-init -)"

