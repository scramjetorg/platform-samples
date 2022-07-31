import argparse
import json
from clickupController import Clickup
from githubController import GhClass
import logging


def run(context=None, input=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--loglevel', default='INFO',
                        choices=['INFO', 'DEBUG', 'ERROR'])

    args = parser.parse_args()
    config = context.config

    if args.loglevel.upper() == 'DEBUG':
        FORMAT = "[%(asctime)s %(filename)s->%(name)s->%(funcName)s():%(lineno)s ] %(levelname)s: %(message)s "
    else:
        FORMAT = "[%(asctime)s] %(levelname)s: %(message)s "
    logging.basicConfig(format=FORMAT, level=args.loglevel.upper())

    gh_token = config['github']['gh_token']
    gh_repos = config['github']['gh_repos']
    cu_token = config['clickup']['cu_token']
    cu_api_url = config['clickup']['cu_api_url']
    cu_workspace = config['clickup']['cu_workspace']

    while True:
        for repository in gh_repos:
            logging.info("Checking new issues in %s", repository)
            gh = GhClass(gh_token, repository)

            cu = Clickup(cu_api_url, cu_token)
            cu_workspace_id = cu.search_workspace(cu_workspace)

            cu.create_cu_space(repository, cu_workspace_id)
            space_id = cu.search_space(repository, cu_workspace_id)

            cu.create_cu_list(repository, space_id)
            list_id = cu.search_list(repository, space_id)

            issues = gh.get_gh_issues(repository)
            task = json.loads(cu.get_task(list_id))

            for i in range(len(issues)):
                issue_title = issues[i]['title']
                issue_desc = issues[i]['url']
                issue_no = issues[i]['issue_no']
                url = "https://github.com/"+repository+"/issues/"+issue_no
                # check if ticket is already imported
                check = [x for x in task["tasks"] if x["text_content"] == "{}".format(url)]
                if not check:
                    logging.info("Importing %s issue #%s", repository, issue_no)
                    cu.create_cu_task(repository, list_id, issue_title, issue_desc, issue_no)
