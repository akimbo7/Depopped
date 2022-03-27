
# Depopped

[![MIT License](https://img.shields.io/github/last-commit/akimbo7/Depopped?color=%231B065E&style=flat-square)](https://github.com/akimbo7/Depopped)
[![MIT License](https://img.shields.io/github/repo-size/akimbo7/Depopped?color=%23FF47DA&style=flat-square)](https://github.com/akimbo7/Depopped)
[![MIT License](https://img.shields.io/github/v/release/akimbo7/Depopped?color=%23F5ECCD&style=flat-square)](https://github.com/akimbo7/Depopped/releases)

![LOGO](https://cdn.discordapp.com/attachments/935638977707376674/957708797009342494/New_Project_8.png)

A simple API Wrapper for Depop.

Depopped is an expanding collection of private API endpoints, allowing you to automate your account. It works by mimicing a mobile client with the use of mobile User Agents and Depops' mobile API.

If you experience any problems, open an issue.

*Have fun :)*


## Installation

```
python3 -m pip install --user --upgrade git+https://github.com/akimbo7/Depopped.git#egg=depopped
```

**Requirements**:

- colorama >= 0.4.4
- requests >= 2.27.1
- uuid >= 1.30

## Remove

```
python3 -m pip uninstall git+https://github.com/akimbo7/Depopped.git#egg=depopped
```

## Example Usage

```python
from Depopped import depopped

client = depopped.Client(log = True, agent = 'ios')

username = 'akimbo7'
password = 'Password123'

#returns the requests.py response
x = client.login(username = email, password = password)

if x.status_code == 200:
    print(f'Logged in as {username}')
else:
    print(f'Error logging in, json: {x.json()}')
```

**Check out the full feature list [here](https://github.com/akimbo7/Depopped/blob/main/usage/USAGE.md)**
