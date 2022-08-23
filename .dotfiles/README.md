# dotfiles

## Setup
```sh
git init --bare $HOME/.dotfiles
alias config='git --git-dir=$HOME/.dotfiles/ --work-tree=$HOME'
config remote add origin git@github.com:benjamincottle/dotfiles.git
```

## Replication
```sh
git clone --separate-git-dir=$HOME/.dotfiles https://github.com/benjamincottle/dotfiles.git dotfiles-tmp
rsync --recursive --verbose --exclude '.git' dotfiles-tmp/ $HOME/
rm --recursive dotfiles-tmp
```

## Configuration
```sh
config config status.showUntrackedFiles no
```

## Usage
```sh
config status
config add .bashrc
config commit -m 'Add .bashrc'
config push --set-upstream origin main
```