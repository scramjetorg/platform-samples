# GitHub issues to Clickup task

- [GitHub issues to Clickup task](#github-issues-to-clickup-task)
  - [Github](#github)
    - [Get github Personal Access Token](#get-github-personal-access-token)
  - [ClickUp](#clickup)
    - [Get Clickup Token](#get-clickup-token)
    - [Create ClickUp Workspace](#create-clickup-workspace)
  - [Set config.json file](#set-configjson-file)
  - [Send Sequence to Scramjet Cloud Platform](#send-sequence-to-scramjet-cloud-platform)

## Github

### Get github Personal Access Token

- [Official instructions](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)

- [Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens)

## ClickUp

### Get Clickup Token

- [Official instructions](https://help.clickup.com/hc/en-us/articles/6303426241687-Getting-Started-with-the-ClickUp-API)
- [Settings > Apps > Generate](https://app.clickup.com/settings/apps)

### Create ClickUp Workspace

- [Official instructions](https://help.clickup.com/hc/en-us/articles/6310502590487-How-do-I-create-a-new-Workspace-)
- [Create Workspace](https://app.clickup.com/onboarding)

Create new Workspace or use existing one.

```text
Shorten the process of creating a new Workspace even further by clicking the + symbol in your Settings Menu. This will take you directly into the onboarding process for your new Workspace.
```

Set name of newly created workspace to `config.json` > `cu_workspace =`

## Set config.json file

```bash
cp python/gh-issues-to-clickup/config-example.json python/gh-issues-to-clickup/config.json
```

Edit `config.json` file:

```json
{
    "github": {
        "gh_token": "GITHUB_TOKEN",
        "gh_repos": [
            "scramjetorg/transform-hub", 
            "scramjetorg/reference-apps", 
            "scramjetorg/framework-js", 
            "scramjetorg/framework-python"
        ]
    },
    "clickup": {
        "cu_token": "CLICKUP_TOKEN",
        "cu_api_url": "https://api.clickup.com/api/v2/",
        "cu_workspace": "<ClickUp Workspace Name>"
    }
}
```

## Send Sequence to Scramjet Cloud Platform

```bash
sudo update-alternatives --config python # set python3 to 3.9 (/usr/bin/python3.9)

cd python/gh-issues-to-clickup
yarn build:refapps # build sequence
si seq deploy -f config.json dist/ # deploy and run sequence
```

Go to `clickup.com` and choosen `Workspace` and then check if the GH issues have been imported
