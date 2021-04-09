-- This file can be loaded by calling `lua require('plugins')` from your init.vim

-- Only required if you have packer in your `opt` pack
vim.cmd [[packadd packer.nvim]]
-- Only if your version of Neovim doesn't have https://github.com/neovim/neovim/pull/12632 merged
-- vim._update_package_paths()

return require('packer').startup(function()
  -- Packer can manage itself as an optional plugin
  use {'wbthomason/packer.nvim', opt = true}

  use {
    'junegunn/fzf.vim',
    requires = {'junegunn/fzf'}
  }

  use {
    'ycm-core/YouCompleteMe',
    commit = '4e480a317d4858db91631c14883c5927243d4893'
  }

  use {
    'pacha/vem-tabline',
    requires = {'ryanoasis/vim-devicons'}
  }

  use {
   'glepnir/galaxyline.nvim',
    branch = 'main',
    -- your statusline
    config = function() require'statusline' end,
    -- some optional icons
    requires = {'kyazdani42/nvim-web-devicons', opt = true}
  }

  use 'glepnir/indent-guides.nvim'

  use 'f-person/git-blame.nvim'

  use 'neovim/nvim-lspconfig'
  use 'nvim-lua/completion-nvim'
  use 'jackguo380/vim-lsp-cxx-highlight'
  use {
    'neoclide/coc.nvim',
    branch = 'release'
  }

  use 'doums/darcula'
  use 'mbbill/undotree'
  use 'tpope/vim-obsession'
  use 'airblade/vim-gitgutter'

end)
