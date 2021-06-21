set runtimepath^=~/.vim runtimepath+=~/.vim/after runtimepath+=~/.config/nvim/
let &packpath = &runtimepath
source ~/.vimrc
lua require('plugins')
let g:gitblame_enabled  = 0
set ts=4 sw=4 expandtab
set number
colorscheme darcula
set termguicolors
set hidden

set undodir=~/.undodir
set undofile

nnoremap <F6> :UndotreeToggle<CR>
tnoremap <Esc> <C-\><C-n><CR>

" Use <Tab> and <S-Tab> to navigate through popup menu
inoremap <expr> <Tab>   pumvisible() ? "\<C-n>" : "\<Tab>"
inoremap <expr> <S-Tab> pumvisible() ? "\<C-p>" : "\<S-Tab>"

" use <Tab> as trigger keys
imap <Tab> <Plug>(completion_smart_tab)
imap <S-Tab> <Plug>(completion_smart_s_tab)

let g:rustfmt_autosave = 1

" https://sharksforarms.dev/posts/neovim-rust/
syntax enable
filetype plugin indent on
runtime rust_analyzer.vim

