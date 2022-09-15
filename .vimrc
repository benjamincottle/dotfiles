" Don't try to be vi compatible
set nocompatible

" No arrow keys
for key in ['<Up>', '<Down>', '<Left>', '<Right>', '<PageUp>', '<PageDown>']
  exec 'nnoremap' key '<Nop>'
  exec 'inoremap' key '<Nop>'
  exec 'cnoremap' key '<Nop>'
  exec 'vnoremap' key '<Nop>'
endfor

" Turn on syntax highlighting
syntax on

" Sets how many lines of history VIM has to remember
set history=500

" Enable filetype plugins
filetype plugin on
filetype indent on

"  The leader key
let mapleader=","

" Security
set modelines=0

" Line numbering
set number
set relativenumber

" Show file stats
set ruler

" Fast saving
nmap <leader>w :w!<cr>

" :W sudo saves the file
command! W execute 'w !sudo tee % > /dev/null' <bar> edit!

" Set N lines to the cursor - when moving vertically using j/k
set scrolloff=10
"
" Turn on the Wild menu
set wildmenu

" Make wildmenu behave like similar to Bash completion.
set wildmode=list:longest

" Wildmenu will ignore files with these extensions.
set wildignore=*.docx,*.jpg,*.png,*.gif,*.pdf,*.pyc,*.exe,*.flv,*.img,*.xlsx,*.o,*~,*.pyc,*/.git/*,*/.hg/*,*/.svn/*,*/.DS_Store

" Highlight cursor line underneath the cursor horizontally.
set cursorline

" Height of the command bar
set cmdheight=1

" A buffer becomes hidden when it is abandoned
set hidden

" Configure backspace so it acts as it should act
set backspace=eol,start,indent
set whichwrap+=<,>,h,l

" Ignore case when searching
set ignorecase

" When searching try to be smart about cases
set smartcase

" Highlight search results
set hlsearch

" Makes search act like search in modern browsers
set incsearch

" Don't redraw while executing macros (good performance config)
set lazyredraw

" For regular expressions turn magic on
set magic

" Show matching brackets when text indicator is over them
set showmatch

" How many tenths of a second to blink when matching brackets
set matchtime=2

" No annoying sound on errors
set noerrorbells
set novisualbell
set t_vb=
set timeoutlen=500

" Encoding
set encoding=utf-8

" netrw settings
let g:netrw_banner = 0
let g:netrw_liststyle = 3

" Turn backup off
set nobackup
set nowritebackup
set noswapfile

" Use spaces instead of tabs
set expandtab

" Be smart when using tabs ;)
set smarttab

" 1 tab == 4 spaces
set shiftwidth=4
set tabstop=4

"Auto indent
set autoindent

"Smart indent
set smartindent

"No line wrap
set nowrap

" Rendering
set ttyfast

" Statusline
set statusline=
set statusline+=\ %n\ %F\ %l:%c\ %M\ %Y\ %R
set statusline+=%=
set statusline+=%2.2(%{matchstr(getline('.'),\ '\\%'\ .\ col('.')\ .\ 'c.')}%)\ %b\ 0x%B\ %l/%LL\ 

" Show the status on the second to last line.
set laststatus=2

" Last line
set showmode
set showcmd

" clear search
map <leader><space> :nohlsearch<cr>

" Move a line of text using ALT+[jk]
execute "set <M-j>=\ej"
execute "set <M-k>=\ek"
nmap <M-j> mz:m+<cr>`z
nmap <M-k> mz:m-2<cr>`z
vmap <M-j> :m'>+<cr>`<my`>mzgv`yo`z
vmap <M-k> :m'<-2<cr>`>my`<mzgv`yo`z

" Split below and to the right y default
set splitbelow
set splitright

" You can split the window in Vim by typing :split or :vsplit.
" Navigate the split view easier by pressing CTRL+j, CTRL+k, CTRL+h, or CTRL+l.
nnoremap <c-j> <c-w>j
nnoremap <c-k> <c-w>k
nnoremap <c-h> <c-w>h
nnoremap <c-l> <c-w>l

" Resize split windows using arrow keys by pressing:
" CTRL+UP, CTRL+DOWN, CTRL+LEFT, or CTRL+RIGHT.
noremap <c-up> <c-w>+
noremap <c-down> <c-w>-
noremap <c-left> <c-w>>
noremap <c-right> <c-w><

" Display cursorline ONLY in active window.
augroup cursor_off
    autocmd!
    autocmd WinLeave * set nocursorline
    autocmd WinEnter * set cursorline
augroup END

" If the current file type is HTML, set indentation to 2 spaces.
autocmd Filetype html setlocal tabstop=2 shiftwidth=2 expandtab

" If the current file type is Python, show colcursorline
"autocmd Filetype python setlocal cursorcolumn

" Disable automatic comment insertion
autocmd FileType * setlocal formatoptions-=c formatoptions-=r formatoptions-=o

"Toggle comment
map gc :call Toggle()<CR>

function! Comment()
	let ft = &filetype
	if ft == 'php' || ft == 'ruby' || ft == 'sh' || ft == 'make' || ft == 'python' || ft == 'perl'
		silent s/^/\#/
	elseif ft == 'javascript' || ft == 'c' || ft == 'cpp' || ft == 'java' || ft == 'objc' || ft == 'scala' || ft == 'go'
		silent s:^:\/\/:g
	elseif ft == 'tex'
		silent s:^:%:g
	elseif ft == 'vim'
		silent s:^:\":g
	endif
endfunction

function! Uncomment()
	let ft = &filetype
	if ft == 'php' || ft == 'ruby' || ft == 'sh' || ft == 'make' || ft == 'python' || ft == 'perl'
		silent s/^\#//
	elseif ft == 'javascript' || ft == 'c' || ft == 'cpp' || ft == 'java' || ft == 'objc' || ft == 'scala' || ft == 'go'
		silent s:^\/\/::g
	elseif ft == 'tex'
		silent s:^%::g
	elseif ft == 'vim'
		silent s:^\"::g
	endif
endfunction

function! Toggle()
	try
		call Uncomment()
	catch
		call Comment()
	endtry
endfunction

" Visualize tabs and newlines
let &showbreak="\u21aa "
"set showbreak=↪\ 
set listchars=tab:»\ ,eol:¬,nbsp:␣,trail:•,extends:⟩,precedes:⟨
" Uncomment this to enable by default:
set list " To enable by default
" Or use your leader key + l to toggle on/off
map <leader>l :set list!<CR> " Toggle tabs and EOL

" Color scheme (terminal)
set background=dark
colorscheme nord
autocmd BufRead,BufNewFile *.north set filetype=north

