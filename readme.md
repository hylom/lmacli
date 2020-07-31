# LINE messaging API Command-Line Client

This is Command-Line Client (CLI) to use LINE messaging API.

LINE messaging API is:
https://developers.line.biz/en/docs/messaging-api/

 **warning: THIS IS NOT AN OFFICIAL LINE PRODUCT!**

## Requirement

 * Python 3 (confirmed with Python 3.8.x)
 * python-jose ( https://pypi.org/project/python-jose/ )
 * line-bot-sdk ( https://github.com/line/line-bot-sdk-python )

## How to Use

1. create venv and install dependencies.

```bash
$ python3 -m venv venv
$ pip3 install -e .
```

2. copy `config.ini.sample` to `config.ini` and edit.

```ini
[default]
ChannelSecret = ...
ChannelAccessToken = ...
ChannelId = ...
AssertionKeyFile = assertion_key.json
```

3. prepare assertion signing key if use from LINE Developers site (optional)

4. check command line help

```shell
$ ./bin/cli -h
usage: cli [-h] {token,user,push,insight,audience,richmenu} ...

LINE Message API CLI.

positional arguments:
  {token,user,push,insight,audience,richmenu}

optional arguments:
  -h, --help            show this help message and exit
```

```
$ ./bin/cli push -h
usage: cli push [-h] [-m [MESSAGE [MESSAGE ...]]] [-t TEXT] {message,multicast,narrowcast,broadcast} ...

positional arguments:
  {message,multicast,narrowcast,broadcast}

optional arguments:
  -h, --help            show this help message and exit
  -m [MESSAGE [MESSAGE ...]], --message [MESSAGE [MESSAGE ...]]
                        message json file to send
  -t TEXT, --text TEXT  text to send
```

## License

MIT License.

