def getUsers(filename='settings.txt'):
    users = []
    with open(filename, 'r') as f:
        for line in f:
            user = {}
            user['no'] = line.split(',')[0].split(':')[1].strip()
            user['psw'] = line.split(',')[1].split(':')[1].strip()
            users.append(user)
        return users
