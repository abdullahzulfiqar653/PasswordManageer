import json
import requests
from django.conf import settings

headers = {
    "accept": "application/json",
    "X-API-Key": settings.MAIL_SERVER_API_KEY,
    "Content-Type": "application/json",
}


def create_mail_box(local_part, password, domain):
    url = f"{settings.MAIL_SERVER_BASE_URL}/add/mailbox"

    # Data for the POST request
    data = {
        "domain": domain,
        "local_part": local_part,
        "name": local_part,
        "password": password,
        "password2": password,
    }

    response = requests.post(url, headers=headers, json=data)
    error = (
        "Unable to create mailbox please try again or contact Neuromail help center."
    )
    if response.status_code == 200:
        try:
            # Decode the _content from bytes to string and load it as JSON
            response_content = json.loads(response.content.decode("utf-8"))
            for item in response_content:
                if item["type"] == "success":
                    email_added = item["msg"][1]  # The email address that was added
                    return True, {
                        "success": f"Mailbox {email_added} created successfully.",
                    }
            return False, {"error": error}
        except json.JSONDecodeError:
            return False, {"error": error}
    else:
        return False, {"error": error}


def delete_mail_box(emails):
    url = f"{settings.MAIL_SERVER_BASE_URL}/delete/mailbox"

    data = emails
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        try:
            response_content = response.json()
            success_msgs = []
            for item in response_content:
                if item.get("type") == "success":
                    success_msgs.append(item["msg"][1])

            return True, f"Mailboxes removed: {', '.join(success_msgs)}"

        except requests.exceptions.JSONDecodeError:
            return False, {
                "error": "Failed to delete mailbox, please try again on contact Neuromail."
            }

    else:
        return False, {
            "error": "Authentication failed please try again on contact Neuromail."
        }
