import yagmail


def send_mail(user, password, host, port, to_user, contents):
    """mail sender"""
    yag = yagmail.SMTP(user=user,
                       password=password,
                       host=host,
                       port=port)
    yag.send(to_user,
             subject=contents[0],
             contents=contents)
