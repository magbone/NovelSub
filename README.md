# NovelSub
A novel subscribe tool
## Build & Usage

```shell

git clone git@github.com:magbone/NovelSub.git
cd ./NovelSub/novelsub

python subscribe.py -c conf.json

```

## Configure file

See default json configure file in **/novelsub** directory 
```
mail(Obj):
        smtp_host(Str): smtp server address
        smtp_port(Int): smtp server port (25 is default and 476 is used SSL)
sender(Str): sender mail address
receivers(Str): receiver mail addresses
timeout(Int): request the html timeout
schedule(Int): the task execute time (hour)
novels(Array Obj):
        link(Str): the novel chapter address
        name(Str): the novel name
        author(Str): the novel author name
        begin_chapter(Int): the novel chapter you want to begin subscribe
```
