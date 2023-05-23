vim.cmd('command! W execute "w !sudo tee % > /dev/null" <bar> edit!')
vim.cmd('let &colorcolumn=join(range(81,82),",")')
vim.opt.number = true
vim.opt.relativenumber = true
vim.opt.splitbelow = true
vim.opt.splitright = true
vim.opt.formatoptions = "jql"
vim.cmd('let g:minimap_width = 8')
vim.cmd('let g:minimap_auto_start = 1')
vim.cmd('let g:minimap_auto_start_win_enter = 1')
vim.cmd('let g:minimap_highlight_range = 1')
vim.cmd('let g:minimap_git_colors = 1')
lvim.autocommands = {
  {
    { "ColorScheme" },
    {
      pattern = "*",
      callback = function()
        vim.api.nvim_set_hl(0, "minimapCursor", { bg = "#49515f" })
        vim.api.nvim_set_hl(0, "minimapRange", { bg = "#282c34" })
        vim.api.nvim_set_hl(0, "minimapDiffRemoved", { fg = "#e06c75" })
        vim.api.nvim_set_hl(0, "minimapDiffAdded", { fg = "#98c379" })
        vim.api.nvim_set_hl(0, "minimapDiffLine", { fg = "#98c379" })
        vim.api.nvim_set_hl(0, "minimapCursorDiffRemoved", { bg = "#49515f", fg = "#e06c75" })
        vim.api.nvim_set_hl(0, "minimapCursorDiffAdded", { bg = "#49515f", fg = "#98c379" })
        vim.api.nvim_set_hl(0, "minimapCursorDiffLine", { bg = "#49515f", fg = "#98c379" })
        vim.api.nvim_set_hl(0, "minimapRangeDiffRemoved", { bg = "#282c34", fg = "#e06c75" })
        vim.api.nvim_set_hl(0, "minimapRangeDiffAdded", { bg = "#282c34", fg = "#98c379" })
        vim.api.nvim_set_hl(0, "minimapRangeDiffLine", { bg = "#282c34", fg = "#98c379" })
      end,
    },
  },
}
local lastaccessed
vim.api.nvim_create_autocmd({ 'WinEnter' }, {
  callback = function()
    local minimapname = '-MINIMAP-'
    if string.sub(vim.api.nvim_buf_get_name(0), -string.len(minimapname)) == minimapname then
      local wins = vim.api.nvim_list_wins()
      vim.api.nvim_set_current_win(lastaccessed)
    else
      lastaccessed = vim.api.nvim_eval("win_getid(winnr('#'))")
    end
  end
})
lvim.colorscheme = "onedark"
lvim.builtin.treesitter.rainbow.enable = true
lvim.builtin.lualine.style = "lvim"
lvim.builtin.lualine.sections.lualine_a = { "mode" }
lvim.format_on_save.enabled = true
lvim.keys.normal_mode["<Q>"] = "<Nop>"
lvim.keys.normal_mode["<J>"] = "mzJ`z"
lvim.keys.normal_mode["<C-d>"] = "<C-d>zz"
lvim.keys.normal_mode["<C-u>"] = "<C-u>zz"
lvim.keys.normal_mode["<C-x>"] = "dd"
lvim.builtin.which_key.mappings["x"] = { "<cmd>!chmod +x %<CR>", "chmod +x it" }
lvim.builtin.which_key.mappings["t"] = { "<cmd>:ToggleTerm size=80 direction=vertical<CR>", "terminal > right" }
lvim.builtin.which_key.mappings["r"] = { [[:%s/\<<C-r><C-w>\>/<C-r><C-w>/gI<Left><Left><Left>]], "regex magics" }
lvim.builtin.which_key.mappings["y"] = { [["+y]], "yank char to system clipboard" }
lvim.builtin.which_key.mappings["Y"] = { [["+Y]], "yank line to system clipboard" }
lvim.plugins = {
  {
    "zbirenbaum/copilot.lua",
    cmd = "Copilot",
    event = "InsertEnter",
    config = function()
      vim.defer_fn(function()
        require("copilot").setup({
          suggestion = {
            enabled = true,
            auto_trigger = true,
            debounce = 75,
            keymap = {
              accept = "<M-CR>",
              accept_word = false,
              accept_line = false,
              next = "<M-]>",
              prev = "<M-[>",
              dismiss = "<M-\\>",
            },
          },
        })
      end, 100)
    end,
  },
  {
    "romgrk/nvim-treesitter-context",
    config = function()
      require("treesitter-context").setup {
        enable = true,   -- Enable this plugin (Can be enabled/disabled later via commands)
        throttle = true, -- Throttles plugin updates (may improve performance)
        max_lines = 0,   -- How many lines the window should span. Values <= 0 mean no limit.
        patterns = {
          default = {
            'class',
            'function',
            'method',
          },
        },
      }
    end
  },
  {
    "Bekaboo/deadcolumn.nvim",
    config = function()
      require('deadcolumn').setup({
        scope = 'visible',
        warning = {
          alpha = 1.0,
          offset = 0,
          colorcode = '#282c34',
          hlgroup = {
            'Error',
            'background',
          },
        },
      })
    end
  },
  {
    "wfxr/minimap.vim",
    build = "cargo install --locked code-minimap",
  },
  {
    "navarasu/onedark.nvim",
    config = function()
      require('onedark').setup {
        style = 'darker',
      }
    end
  },
  {
    "mg979/vim-visual-multi",
  },
}
