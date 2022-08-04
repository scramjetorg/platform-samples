from github import Github
import logging
import json


class GhClass:
    def __init__(self, gh_token, repository=None):
        self.gh_token = gh_token
        self.repository = None

    def get_gh_issues(self, repository):
        g = Github(self.gh_token)
        repo = g.get_repo(repository)
        open_issues = repo.get_issues(state='open')
        issue_list = []
        for issue in open_issues:
            url = "https://github.com/"+repository+"/issues/"+str(issue.number)
            values = """
            {{
                "issue_no": "{0}",
                "title": {1},
                "repo": "{2}",
                "url": "{3}"
            }}
            """
            title = json.dumps(issue.title)
            json_data = json.loads(
                values.format(issue.number, title, repository, url))
            issue_list.append(json_data)
        logging.debug('get_gh_issues: %s', issue_list)

        return issue_list
