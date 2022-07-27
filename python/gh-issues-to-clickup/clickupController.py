import requests
import logging
import json
import asyncio


class Clickup:
    def __init__(self, api_url, cu_token, repository=None):
        self.api_url = api_url
        self.cu_token = cu_token
        self.repository = None

    def background(f):
        def wrapped(*args, **kwargs):
            return asyncio.get_event_loop().run_in_executor(
                None, f, *args, **kwargs)

        return wrapped

    def get_workspace(self):
        r = requests.get(self.api_url+'team/', headers={
            'Content-Type': 'application/json',
            'Authorization': '{}'.format(self.cu_token)})

        response = r.text
        logging.debug('get_workspace: %s', response)

        try:
            r.raise_for_status()

        except requests.exceptions.HTTPError as err:
            logging.error("%s, %s", err, response)

        return json.dumps(json.loads(response))

    def get_spaces(self, cu_workspace_id):
        r = requests.get(
            self.api_url+'team/{}/space'.format(cu_workspace_id), headers={
                'Content-Type': 'application/json',
                'Authorization': '{}'.format(self.cu_token)})

        response = r.text
        logging.debug('get_spaces: %s', response)

        try:
            r.raise_for_status()

        except requests.exceptions.HTTPError as err:
            logging.error("%s | %s", err, response)

        return json.dumps(json.loads(response))

    def get_list(self, cu_space_id):
        r = requests.get(
            self.api_url+'space/{}/list?archived=false'.format(cu_space_id), headers={
                'Content-Type': 'application/json',
                'Authorization': '{}'.format(self.cu_token)})
        response = r.text
        logging.debug('get_list: %s', response)

        try:
            r.raise_for_status()

        except requests.exceptions.HTTPError as err:
            logging.error("%s, %s", err, response)

        return json.dumps(json.loads(response))

    def get_task(self, culist_id):
        r = requests.get(
            self.api_url+'list/{}/task'.format(culist_id), headers={
                'Content-Type': 'application/json',
                'Authorization': '{}'.format(self.cu_token)})
        response = r.text
        logging.debug('get_task: %s', response)

        try:
            r.raise_for_status()

        except requests.exceptions.HTTPError as err:
            logging.error("%s, %s", err, response)

        return json.dumps(json.loads(response))

    def search_space(self, repository, cu_workspace_id):
        # Get Spaces
        space = json.loads(self.get_spaces(cu_workspace_id))

        space_lenght = len(space['spaces'])

        for i in range(space_lenght):
            if repository == space['spaces'][i]['name']:
                return space['spaces'][i]['id']

    def search_workspace(self, cu_workspace):
        # Get Workspace
        workspace = json.loads(self.get_workspace())

        workspace_lenght = len(workspace['teams'])

        for i in range(workspace_lenght):
            if cu_workspace == workspace['teams'][i]['name']:
                logging.debug('search_workspace: %s', workspace['teams'][i]['id'])

                return workspace['teams'][i]['id']

    def search_list(self, repository, cu_space_id):
        # Get Lists
        list = json.loads(self.get_list(cu_space_id))
        logging.debug('search_list: %s',  list)
        list_lenght = len(list['lists'])

        for i in range(list_lenght):
            if "Issues "+repository == list['lists'][i]['name']:
                logging.debug('search_list: %s',  list['lists'][i]['id'])
                return list['lists'][i]['id']

    def create_cu_space(self, repository, cu_workspace_id):
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
        json_data = values.format(repository)

        r = requests.post(
            self.api_url+'team/{}/space'.format(cu_workspace_id), headers={
                'Content-Type': 'application/json',
                'Authorization': '{}'.format(self.cu_token)}, data=json_data)
        response = r.text
        logging.debug('create_cu_space: %s', response)

        try:
            r.raise_for_status()

        except requests.exceptions.HTTPError as err:
            logging.error("%s, %s", err, response)

    def create_cu_list(self, repository, cu_space_id):
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
        json_data = values.format(repository)

        r = requests.post(
            self.api_url+'space/{0}/list'.format(cu_space_id), headers={
                'Content-Type': 'application/json',
                'Authorization': '{}'.format(self.cu_token)}, data=json_data)
        response = r.json()
        logging.debug('create_cu_list: %s', response)

        try:
            r.raise_for_status()

        except requests.exceptions.HTTPError as err:
            logging.error("%s, %s", err, response)

    @background
    def create_cu_task(
            self, repository, culist_id, title, issue_desc, issue_no):
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

        json_data = values.format(
                        json.dumps(title), issue_desc, repository, issue_no)

        r = requests.post(
            self.api_url+'list/{0}/task'.format(culist_id), headers={
                'Content-Type': 'application/json',
                'Authorization': '{}'.format(self.cu_token)}, data=json_data)
        response = r.json()
        logging.debug('create_cu_task: %s', response)

        try:
            r.raise_for_status()

        except requests.exceptions.HTTPError as err:
            logging.error("%s, %s", err, response)
