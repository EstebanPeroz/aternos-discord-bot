from python_aternos import Client

at = Client()
at.login('LeTestDeEste', 'Quentinn\'estplussigros!')

aternos = at.account
servs = aternos.list_servers()

myserv = servs[0]
myserv.start()