# Sequence suggesting keywords for header in *.md

Easy example of usage Kaffka with Scramjet platform.

Build this sample with `yarn` command

```bash
yarn build:refapps
```

Once you've built it, you need to deploy it.

```bash
si seq deploy keywords/dist
```

Now you can pass *.md file to instance input.

```bash
si inst input - <path_to_file>
```

Now you should be able to see output on STH logs in first terminal.
