from anon_requests import RotatingTorSession


# Choose a proxy port, a control port, and a password.
# Defaults are 9050, 9051, and None respectively.
# If there is already a Tor process listening the specified
# ports, TorSession will use that one.
# Otherwise, it will create a new Tor process,
# and terminate it at the end.
with RotatingTorSession(proxy_port=9050, ctrl_port=9051,
                        password="MYSUPERSAFEPSWD") as session:
    for i in range(0, 5):
        try:
            response = session.get('https://ipecho.net/plain')
            print(response.text)  # not your IP address, different every time
        except KeyboardInterrupt:
            break
