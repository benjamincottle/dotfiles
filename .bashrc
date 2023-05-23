#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

export HISTCONTROL=ignoredups:erasedups
HISTSIZE=-1
HISTFILESIZE=-1

### SETTING OTHER ENVIRONMENT VARIABLES
if [ -z "$XDG_CONFIG_HOME" ] ; then
    export XDG_CONFIG_HOME="$HOME/.config"
fi
if [ -z "$XDG_DATA_HOME" ] ; then
    export XDG_DATA_HOME="$HOME/.local/share"
fi
if [ -z "$XDG_CACHE_HOME" ] ; then
    export XDG_CACHE_HOME="$HOME/.cache"
fi
if [ -d "$HOME/.local/bin" ] ; then
    export PATH="$HOME/.local/bin:$PATH"
fi
if [ -d "$HOME/.cargo/bin" ] ; then
    export PATH="$HOME/.cargo/bin:$PATH"
fi

shopt -s autocd # change to named directory
shopt -s cdspell # autocorrects cd misspellings
shopt -s dirspell # attempt spelling correction on directory names during word completion
shopt -s cmdhist # save multi-line commands in history as single line
shopt -s dotglob # include filenames beginning with a ‘.’ in the results of filename expansion
shopt -s histappend # do not overwrite history
shopt -s expand_aliases # expand aliases
shopt -s checkwinsize # checks term size when bash regains control

alias ls="ls --color=auto"
alias grep="grep --color=auto"
alias fgrep="fgrep --color=auto"
alias egrep="egrep --color=auto"
alias cp="cp -i"
alias mv="mv -i"
alias rm="rm -i"
alias jctl="journalctl -p 3 -xb"
alias vi="lvim"
alias vim="lvim"
alias config="/usr/bin/git --git-dir=$HOME/.dotfiles/ --work-tree=$HOME"

# navigation
up () {
  local d=""
  local limit="$1"

  # Default to limit of 1
  if [ -z "$limit" ] || [ "$limit" -le 0 ]; then
    limit=1
  fi

  for ((i=1;i<=limit;i++)); do
    d="../$d"
  done

  # perform cd. Show error if cd fails
  if ! cd "$d"; then
    echo "Couldn't go up $limit dirs.";
  fi
}

PS1="[\u@\h \W]\$ "

test -r "~/.dir_colors" && eval $(dircolors ~/.dir_colors)

# pretty colour bars :D
echo
for f in {0..6}; do
	echo -en "\033[$((f+41))m\033[$((f+30))m██▓▒░"
done
echo -en "\033[37m██\n"
echo
for f in {0..6}; do
	echo -en "\033[$((f+41))m\033[1;$((f+90))m██▓▒░"
done
echo -en "\033[1;37m██"
echo -e "\033[0m"
echo

source /usr/share/nvm/init-nvm.sh

