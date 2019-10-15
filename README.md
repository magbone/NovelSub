# NovelSub
A novel subscribe tool
## Build & Usage

```shell

git clone git@github.com:magbone/NovelSub.git
cd NovelSub

# Insatlled by Python3 (Only support Python3)
# For build
python3 setup.py build
# For installation
python3 setup.py install

# Run
novelsub -c your_conf_path.json
```

## Configure file

See default json as follows.
```json
{
  "mail":{
        "smtp_server": "your mail smtp server address",
        "smtp_port": "smtp server port (25 default, 465 using SSL)",
        "user": "mail acount",
        "password": "mail password"
  },
  "timeout": 5, # request timeout
  "schedule": 12, # exectue the task per 12h
  "sender": "sender mail address",
  "receiver": "receiver mail address",
  "novels":[
        {
                "name": "novel name",
                "author": "novel author", 
                "link": "novel chapters link",
                "begin_chapter": 1234 # the chapter you begin to subscribe
        }
  ]
}
```
