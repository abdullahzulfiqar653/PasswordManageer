import threading


class EmailSendThread(threading.Thread):
    def __init__(
        self, emailMethod, subject, body, email, password, recipients, attachments
    ) -> None:
        self.emailMethod = emailMethod
        self.subject = subject
        self.body = body
        self.email = email
        self.password = password
        self.recipients = recipients
        self.attachments = attachments

        threading.Thread.__init__(self)

    def run(self) -> None:
        self.emailMethod(
            self.subject,
            self.body,
            self.email,
            self.password,
            self.recipients,
            self.attachments,
        )


class InboxRecieverThread(threading.Thread):
    def __init__(self, inboxMethod, mailbox, user) -> None:
        self.inboxMethod = inboxMethod
        self.mailbox = mailbox
        self.user = user

        threading.Thread.__init__(self)

    def run(self) -> None:
        self.inboxMethod(self.mailbox, self.user)
