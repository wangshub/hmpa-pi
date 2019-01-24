import yagmail


class Email(object):
    def __init__(self, user, password, host, port):
        self.yag = yagmail.SMTP(user=user,
                                password=password,
                                host=host,
                                port=port)

    def send(self, to_user, title, contents):
        self.yag.send(to_user,
                      subject=title,
                      contents=contents)


def send(user, password, host, port, to_user, title, contents):
    """mail sender"""
    yag = yagmail.SMTP(user=user,
                       password=password,
                       host=host,
                       port=port)
    yag.send(to_user,
             subject=title,
             contents=contents)
