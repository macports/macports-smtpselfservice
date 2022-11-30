"""
GitHub API wrapper to obtain the localpart of our preferred email domain.
"""
# SPDX-License-Identifier: BSD-2-Clause

import requests


class GitHubApiError(Exception):
    """
    Error while obtaining the user's email addresses from GitHub.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self)

    def __str__(self):
        return self.message


def get_user(token, domain):
    """
    Obtain the user's localpart under the given domain using the given GitHub
    access token with the user:email scope.
    """
    if not token:
        raise GitHubApiError(
            "Did not receive GitHub OAuth2 access token from upstream server."
        )
    if not domain:
        raise GitHubApiError("The email domain is not set in the server configuration.")
    try:
        req = requests.get(
            "https://api.github.com/user/emails",
            headers={
                "authorization": f"token {token}",
                "accept": "application/vnd.github.v3+json",
                "per_page": "100",
            },
            timeout=30,
        )
        req.raise_for_status()
        for item in req.json():
            if item.get("verified", False):
                email = item.get("email", "")
                needle = f"@{domain}"
                if email.endswith(needle):
                    return (email[: -len(needle)], domain)
    except requests.RequestException as requests_exc:
        raise GitHubApiError(
            f"Error querying your email addresses from GitHub: {requests_exc!s}"
        ) from requests_exc
    raise GitHubApiError(
        f"Could not determine your @{domain} email address. "
        "Make sure it is added to your GitHub account and verified."
    )
