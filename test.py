import unittest

import api

pr_test = api.PullRequestHelper()


class PullRequestHelperTest(unittest.TestCase):
    def test_get_pull_request_links(self):
        username = 'katalyzator'
        password = ''
        auth_params = (username, password)
        repo = 'something_repo_name'
        with self.assertRaises(Exception) as context:
            pr_test._get_pull_requests_links(username, repo, auth_params)
        self.assertTrue('Repository %s not found. Please try again...' % repo in context.exception)
        print context.exception


def main():
    unittest.main()


if __name__ == '__main__':
    main()
