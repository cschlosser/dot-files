set runtimepath^=~/.vim runtimepath+=~/.vim/after
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

