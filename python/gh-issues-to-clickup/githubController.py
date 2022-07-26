from github import Github
import logging
import json

class GhClass:

    def __init__(self, ghToken, repository=None):
        self.ghToken = ghToken
        self.repository = None


    def getGhIssues(self, repository):

        g = Github(self.ghToken)
        repo = g.get_repo(repository)
        open_issues = repo.get_issues(state='open')
        issueList = []
        for issue in open_issues:
            url = "https://github.com/"+repository+"/issues/"+str(issue.number)
            values = """
            {{
                "issueNo": "{0}",
                "title": {1},
                "repo": "{2}",
                "url": "{3}"
            }}
            """
            title=json.dumps(issue.title)
            jsonData = json.loads(values.format(issue.number, title, repository, url))
            issueList.append(jsonData)
        logging.debug('getGhIssues: %s', issueList)

        return issueList
