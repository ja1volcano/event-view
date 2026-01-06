# AWDB Event Logs API

This API pulls from awdb's event logs to provide a simple interface for debugging problematic issues.

## Authors

-   [@beautah](https://github.com/beautah)

## Environment Variables

This project can be modified by the following variables, a .env file is used to set them

> [!TIP]
> All env vars, especially the password, should be wrapped in quotes to avoid issues with special characters, escape any double quotes in variables with back slashes.

`PACCOUNT` - paccount username (required)

`PASSWORD` - paccount password (required)

`HOST` - host name or ip for one of the database instances (required)

`PORT` - port to communicate with database over (required)

`DBNAME` - name of the database, defaults to awdb (optional)

e.g.

> [!IMPORTANT]
> example contents of .env within root folder

```
PASSWORD="sup3\"r5ecre7P@55w0r&"
PACCOUNT="puser01"
HOST="127.0.0.1"
PORT="1433"
DBNAME="awdb"
```

## Setting up the API

To install reqs

-   Linux

```bash
  python3 -m venv .venv
  source .venv/bin/activate
  python -m pip install --upgrade pip
  python pip -r requirements.txt
```

-   Windows

```powershell
  python3 -m venv .venv
  source \.venv\Scripts\activate.ps1
  python -m pip install --upgrade pip
  python pip -r requirements.txt
```

## Running the API

To run API in debug (suggested)

```
flask run --debug --port 5000
```

Navigate to

[localhost:5000](http://localhost:5000)
