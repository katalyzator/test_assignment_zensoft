import webbrowser
from sys import argv

import requests
import json


class PullRequestHelper(object):
    USER_REPOS_URL = 'https://api.github.com/users/%s/repos'
    REPO_PULL_REQUESTS_URL = 'https://api.github.com/repos/%s/%s/pulls?state=open'

    def _do_request(self, url, auth_params):
        return requests.get(url, auth=auth_params)

    def _get_pull_requests_links(self, username, repo, auth_params):
        res = self._do_request(url=self.REPO_PULL_REQUESTS_URL % (username, repo), auth_params=auth_params)

        if res.status_code == 404:
            raise Exception('Repository %s not found. Please try again...' % repo)
        elif res.status_code == 403 or res.status_code == 401:
            raise Exception('Failed to authenticate...')
        elif res.status_code == 200:
            prs = json.loads(res.content)

            return [p['html_url'] for p in prs]
        else:
            raise Exception('Unknown error.')

    def _get_user_repos(self, username, auth_params):
        res = self._do_request(url=self.USER_REPOS_URL % username, auth_params=auth_params)

        if res.status_code == 403 or res.status_code == 401:
            raise Exception('Failed to authenticate...')
        elif res.status_code == 404:
            raise Exception('Not found')
        elif res.status_code == 200:
            repos = json.loads(res.content)
            return [r['name'] for r in repos]
        else:
            raise Exception('Unknown error...')

    def run(self):
        if len(argv) < 3:
            raise Exception('Please provide username and password in command line...')

        username = argv[1]
        password = argv[2]
        auth_params = (username, password)

        if len(argv) > 3:
            repository_names = [name for name in argv[3:]]
        else:
            repository_names = self._get_user_repos(username=username, auth_params=auth_params)

        pull_requests = []
        for repo in repository_names:
            print(repo)
            for pr in self._get_pull_requests_links(username, repo, auth_params=auth_params):
                pull_requests.append(pr)

                if len(pull_requests) > 10:
                    raise Exception('Too many pull requests, try to filter by repo...')

            for url in pull_requests:
                webbrowser.open_new_tab(url)

        if len(pull_requests) == 0:
            raise Exception('There are no pull requests in your repositories...')


def main():
    pr_helper = PullRequestHelper()

    try:
        pr_helper.run()
    except Exception as e:
        print('Error occurred: ' + str(e))


if __name__ == '__main__':
    main()
