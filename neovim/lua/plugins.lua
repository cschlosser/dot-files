-- This file can be loaded by calling `lua require('plugins')` from your init.vim

-- Only required if you have packer in your `opt` pack
vim.cmd [[packadd packer.nvim]]
-- Only if your version of Neovim doesn't have https://github.com/neovim/neovim/pull/12632 merged
-- vim._update_package_paths()

return require('packer').startup(function()
  -- Packer can manage itself as an optional plugin
  use {'wbthomason/packer.nvim', opt = true}

  -- vim appearance
  use {
    'junegunn/fzf.vim',
    requires = {'junegunn/fzf'}
  }
  use {
    'pacha/vem-tabline',
    requires = {'ryanoasis/vim-devicons'}
  }
  use 'doums/darcula'
  use {
   'glepnir/galaxyline.nvim',
    branch = 'main',
    -- your statusline
    config = function() require'statusline' end,
    -- some optional icons
    requires = {'kyazdani42/nvim-web-devicons', opt = true}
  }
  use 'glepnir/indent-guides.nvim'
  use 'airblade/vim-gitgutter'

  -- extensions/additional utility
  use 'mbbill/undotree'
  use 'tpope/vim-obsession'
  use 'tpope/vim-surround'
  use 'f-person/git-blame.nvim'

  -- languages
  -- general
  use 'neovim/nvim-lspconfig'
  use 'nvim-lua/completion-nvim'
  use {
    'neoclide/coc.nvim',
    branch = 'release',
    -- rls: rust
    -- clangd: c++
    run = ':CocInstall coc-rls coc-clangd coc-lua coc-tsserver coc-json'
  }

  -- c++
  use 'jackguo380/vim-lsp-cxx-highlight'
  use 'grailbio/bazel-compilation-database'

  -- rust
  use 'rust-lang/rust.vim'

end)
