syntax on

" encoding and language
set encoding=utf-8
set langmenu=en.utf-8
set helplang=en

" show line number
set number

" tab config
set smarttab
set tabstop=4
set softtabstop=4
set shiftwidth=4

" replace tab with space
set expandtab

" search with highlight
set hlsearch
set incsearch

" search case insensitive
set ignorecase
set smartcase

" confirm when leaving with unsaved or readonly files
set confirm

" toggle paste mode with F3 key
" set paste
set pastetoggle=<F3>

" use vim keyboard mode rather then vi
set nocompatible

" set theme
set background=light

" no error bell
set noeb
set vb t_vb=
set noerrorbells

" no visual bell
set novisualbell

" auto indent
set autoindent
set cindent

" save histories
set history=100

" no .swp file
set nobackup
set noswapfile

" status line
set statusline=%F%m%r%h%w\ [FORMAT=%{&ff}]\ [TYPE=%Y]\ [POS=%l,%v][%p%%]
set laststatus=2

" show ruler while editing
set ruler

" load filetype
filetype on
filetype plugin on
filetype indent on

" keep global variables
"set viminfo+=!

" split mode
set iskeyword+=_,$,@,%,#,-

set linespace=0

set wildmenu

" backspace indent, eol, start
set backspace=2

" allow cursor and backspace wrap
set whichwrap+=<,>,h,l

" using command, find which lines have been changed?
set report=0

" no tip when starting vim
set shortmess=atI

" show space between splitted windows
set fillchars=vert:\ ,stl:\ ,stlnc:\

" show matched braces
set showmatch
set matchtime=3

" keep lines off the cursor
set scrolloff=3

if has("autocmd")
  au BufReadPost * if line("'\"") > 1 && line("'\"") <= line("$") | exe "normal! g'\"" | endif
endif
