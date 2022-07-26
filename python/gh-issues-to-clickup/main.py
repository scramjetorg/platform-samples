import argparse
import configparser
from genericpath import exists
import json
from clickupController import Clickup
from githubController import GhClass
import logging

def run(context=None, input=None ):
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', default='config.ini', required=False)
    parser.add_argument('-l', '--loglevel', default='INFO', choices=['INFO', 'DEBUG', 'ERROR'])


    args = parser.parse_args()
    config = configparser.ConfigParser()
    config.read(args.config)

    if args.loglevel.upper() == 'DEBUG':
        FORMAT = "[%(asctime)s %(filename)s->%(name)s->%(funcName)s():%(lineno)s ] %(levelname)s: %(message)s "
    else:
        FORMAT = "[%(asctime)s] %(levelname)s: %(message)s "
    logging.basicConfig(format=FORMAT, level=args.loglevel.upper())


    ghToken = config['github']['ghToken']
    ghRepos = json.loads(config.get("github","ghRepos"))
    cuToken = config['clickup']['cuToken']
    cuApiUrl = config['clickup']['cuApiUrl']
    cuWorkspace = config['clickup']['cuWorkspace']

    while True:
        for repository in ghRepos:
            logging.info("Checking new issues in %s",repository)
            gh = GhClass(ghToken, repository)
            
            cu = Clickup(cuApiUrl, cuToken)
            cuWorkspaceId = cu.searchWorkspace(cuWorkspace)

            cu.createCuSpace(repository, cuWorkspaceId )
            spaceId = cu.searchSpace(repository, cuWorkspaceId )

            cu.createCuList(repository, spaceId)
            listId = cu.searchList(repository, spaceId)

            issues = gh.getGhIssues(repository)
            task = json.loads(cu.getTask(listId))

            for i in range(len(issues)):
                issueTitle = issues[i]['title']
                issueDesc = issues[i]['url']
                issueNo = issues[i]['issueNo']
                url = "https://github.com/"+repository+"/issues/"+issueNo
                #check if ticket is already imported
                check = [x for x in task["tasks"] if x["text_content"]=="{}".format(url)]
                if not check:
                    logging.info("Importing %s issue #%s",repository, issueNo)
                    cu.createCuTask(repository, listId, issueTitle, issueDesc, issueNo)
                else:
                    pass
