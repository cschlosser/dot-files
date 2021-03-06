# dot is a simple json based dotfile manager

(it also can be used as a **very** basic system bootstrapper)

Key features:

* Install packages on your system
* Create symlinks for all your dot files
* Refresh your configs from your `dot.json` (see [Limitations](#limitations))

## How to

### First setup

1. Fork this repository or [use it as template](https://github.com/cschlosser/dot/generate)

2. Edit [dot.json](dot.json). My personal example can be found [here](https://github.com/cschlosser/dot-files/blob/master/dot.json)

3. Run `bootstrap.sh` it will walk you through the process and you can rerun it all the time

4. Commit your changes and push them

### Integrate changes from the main [dot](https://github.com/cschlosser/dot) framework

1. Run `git remote add dot https://github.com/cschlosser/dot && git fetch --all`

2.1 If you forked the repository run `git merge dot/master`

2.2 If you used the repository template run `git merge dot/master --allow-unrelated`

3. Resolve merge conflicts if there are any

### Updating your `dot.json`

If you want to add new packages or add new configs to existing packages you can do so easily by editing [dot.json](dot.json) and rerunning `bootstrap.sh`. The shell scripts generated are aware of changes to some extent

## dot.json syntax

Everything starts with a `json` object containing a `version` and `packages` object.

The `version` has to match the one of [dot](https://github.com/cschlosser/dot) you're using.

```json
{
  "version": 1,
  "packages": [
  ]
}
```

Now we can start adding packages

```diff
{
  "version": 1,
  "packages": [
+   {
+     "name": "neovim"
+   }
  ]
}
```

This will install the `neovim` package from your system package manager specified in [providers.json](providers.json). If you're missing the package manager for your platform feel free to create a Pull Request for adding it to the file for all users of [dot](https://github.com/cschlosser/dot).

If your package is only available on one platform and you intend to use this repository for different ones you can specify them with the `os` object.

```diff
{
  "version": 1,
  "packages": [
+    {
+      "name": "herbstluft",
+      "os": "Linux"
+    }
  ]
}
```

The value of the `os` object should contain the string from Python's `platform.system()`.

If the package is named differently for a package manager you can provide an alternative name

```diff
{
  "version": 1,
  "packages": [ 
    {
      "name": "herbstluft",
-      "os": "Linux" 
+      "os": "Linux",
+      "providers": [
+        {
+          "apt-get": "herbstluftwm"
+        }
+      ]
    }
  ]
}
```

If you have to run some command prior to installing your package you can put it into the `pre_install` array where each object should have a key with the id of your package manager and the value is the command you want to run.

```diff
{
  "version": 1,
  "packages": [
+    {
+      "name": "fish",
+      "pre_install": [
+        {
+          "apt-get": "apt-add-repository ppa:fish-shell/release-3"
+        }
+      ]
+    }
  ]
}
```

Now for the config files:

```diff
{
  "version": 1,
  "packages": [
    {
      "name": "neovim"
+      "configs": [
+        {     
+          "init.vim": "$HOME/.config/nvim/init.vim"
+        }       
+      ]       
    }
  ]
}
```
The config files have to be stored in your repository in a folder named like the `name` object in your `packages` array.

```bash
.
├── LICENSE.txt
├── booststrap.sh
├── dot.json
├── gen_configure.py
├── gen_install.py
├── neovim
│   └── init.nvim
├── providers.json
└── third_party
    └── jinja
...
```

Each object in the `configs` array is going to be linked from the key to the value.

Let's say you store your personal dot file repository in `$HOME/dot-files`.

For our example above it will create a link from `$HOME/.config/nvim/init.vim` to `$HOME/dot-files/neovim/init.vim` creating any directories if necessary and creating a backup if the file already exists.

Folders and files can both be specified as key/value for objects in the `configs` array.

## Limitations

* There is no way to detect removed packages/configs
* No `post_install` command
