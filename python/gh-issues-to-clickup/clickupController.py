import requests
import logging
import json
import asyncio

class Clickup:

    def __init__(self, apiUrl, cuToken, repository=None):
        self.apiUrl = apiUrl
        self.cuToken = cuToken
        self.repository = None

    def background(f):
        def wrapped(*args, **kwargs):
            return asyncio.get_event_loop().run_in_executor(None, f, *args, **kwargs)

        return wrapped

    def getWorkspace(self):

    
        r = requests.get(self.apiUrl+'team/', headers={'Content-Type':'application/json',
                    'Authorization': '{}'.format(self.cuToken)})

        response = r.text
        logging.debug('getWorkspace: %s', response)

        try:
            r.raise_for_status()

        except requests.exceptions.HTTPError as err:
            logging.error("%s, %s", err, response)

        return json.dumps(json.loads(response))


    def getSpaces(self, cuWorkspaceId):


        r = requests.get(self.apiUrl+'team/{}/space'.format(cuWorkspaceId), headers={'Content-Type':'application/json',
                    'Authorization': '{}'.format(self.cuToken)})
        response = r.text
        logging.debug('getSpaces: %s', response)

        try:
            r.raise_for_status()

        except requests.exceptions.HTTPError as err:
            logging.error("%s | %s", err, response)

        return json.dumps(json.loads(response))

    def getList(self, cuSpaceId):

        r = requests.get(self.apiUrl+'space/{}/list?archived=false'.format(cuSpaceId), headers={'Content-Type':'application/json',
                    'Authorization': '{}'.format(self.cuToken)})
        response = r.text
        logging.debug('getList: %s', response)

        try:
            r.raise_for_status()

        except requests.exceptions.HTTPError as err:
            logging.error("%s, %s", err, response)

        return json.dumps(json.loads(response))

    def getTask(self, cuListId):


        r = requests.get(self.apiUrl+'list/{}/task'.format(cuListId), headers={'Content-Type':'application/json',
                    'Authorization': '{}'.format(self.cuToken)})
        response = r.text
        logging.debug('getTask: %s', response)

        try:
            r.raise_for_status()

        except requests.exceptions.HTTPError as err:
            logging.error("%s, %s", err, response)

        return json.dumps(json.loads(response))

    def searchSpace(self, repository, cuWorkspaceId):
        # Get Spaces
        space = json.loads(self.getSpaces(cuWorkspaceId))

        spaceLenght = len(space['spaces'])

        for i in range(spaceLenght):
            if repository == space['spaces'][i]['name']:
                return  space['spaces'][i]['id']
            else:
                pass

    def searchWorkspace(self, cuWorkspace):
        # Get Workspace
        workspace = json.loads(self.getWorkspace())

        workspaceLenght = len(workspace['teams'])

        for i in range(workspaceLenght):
            if cuWorkspace == workspace['teams'][i]['name']:
                logging.debug('searchWorkspace: %s', workspace['teams'][i]['id'])
                return workspace['teams'][i]['id']
            else:
                pass

    def searchList(self, repository, cuSpaceId):
        # Get Lists
        list = json.loads(self.getList(cuSpaceId))
        logging.debug('searchList: %s',  list)
        listLenght = len(list['lists'])

        for i in range(listLenght):
            if "Issues "+repository == list['lists'][i]['name']:
                logging.debug('searchList: %s',  list['lists'][i]['id'])
                return  list['lists'][i]['id']
            else:
                pass

    def createCuSpace(self, repository, cuWorkspaceId ):

        values = '''
        {{
            "name": "{0}",
            "multiple_assignees": true,
            "features": {{
            "due_dates": {{
                "enabled": true,
                "start_date": false,
                "remap_due_dates": true,
                "remap_closed_due_date": false
            }},
            "time_tracking": {{
                "enabled": false
            }},
            "tags": {{
                "enabled": true
            }},
            "time_estimates": {{
                "enabled": true
            }},
            "checklists": {{
                "enabled": true
            }},
            "custom_fields": {{
                "enabled": true
            }},
            "remap_dependencies": {{
                "enabled": true
            }},
            "dependency_warning": {{
                "enabled": true
            }},
            "portfolios": {{
                "enabled": true
            }}
            }}
        }}'''
        jsonData = values.format(repository)


        r = requests.post(self.apiUrl+'team/{}/space'.format(cuWorkspaceId), headers={'Content-Type':'application/json',
                    'Authorization': '{}'.format(self.cuToken)},
                    data=jsonData )
        response = r.text
        logging.debug('createCuSpace: %s', response)

        try:
            r.raise_for_status()

        except requests.exceptions.HTTPError as err:
            logging.error("%s, %s", err, response)


    def createCuList(self, repository, cuSpaceId ):

        values = """
        {{
            "name": "Issues {0}",
            "content": "GitHub {0} issues",
            "due_date": 1567780450202,
            "due_date_time": false,
            "priority": 3,
            "status": "red"
        }}
        """
        jsonData = values.format(repository)

        r = requests.post(self.apiUrl+'space/{0}/list'.format(cuSpaceId), headers={'Content-Type':'application/json',
                    'Authorization': '{}'.format(self.cuToken)},
                    data=jsonData )
        response = r.json()
        logging.debug('createCuList: %s', response)

        try:
            r.raise_for_status()

        except requests.exceptions.HTTPError as err:
            logging.error("%s, %s", err, response)

    @background
    def createCuTask(self, repository, cuListId, title, issueDesc, issueNo ):
        values = """
        {{
            "name": {0},
            "description": "{1}",
            "tags": [
            "github",
            "repo/{2}",
            "issue/{3}"
            ],
            "priority": 3,
            "due_date": 1508369194377,
            "due_date_time": false,
            "time_estimate": 8640000,
            "start_date": 1567780450202,
            "start_date_time": false,
            "notify_all": true,
            "parent": null,
            "links_to": null,
            "check_required_custom_fields": true,
            "custom_fields": []
        }}
        """

        jsonData = values.format(json.dumps(title), issueDesc, repository, issueNo)
        r = requests.post(self.apiUrl+'list/{0}/task'.format(cuListId), headers={'Content-Type':'application/json',
                    'Authorization': '{}'.format(self.cuToken)},
                    data=jsonData )
        response = r.json()
        logging.debug('createCuTask: %s', response)

        try:
            r.raise_for_status()

        except requests.exceptions.HTTPError as err:
            logging.error("%s, %s", err, response)
