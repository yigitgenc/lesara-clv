# lesara-clv

Dockerized Lesara Customer Value Project

# Installation

* [Running on __your computer__](#running-on-your-computer)
    * [Installing](#installing)
    * [Running](#running)
    * [Debugging](#debugging)
    * [Logging](#logging)
    * [Tests](#tests)

### Installing

Get Docker first:
* <a href="https://download.docker.com/mac/stable/Docker.dmg" target="_blank">Docker CE for Mac</a>
* <a href="https://download.docker.com/win/stable/Docker%20for%20Windows%20Installer.exe" target="_blank">Docker CE for Windows</a>
* <a href="https://docs.docker.com/engine/installation/linux/docker-ce/centos/" target="_blank">Docker CE for CentOS</a>
* <a href="https://docs.docker.com/engine/installation/linux/docker-ce/debian/" target="_blank">Docker CE for Debian</a>
* <a href="https://docs.docker.com/engine/installation/linux/docker-ce/fedora/" target="_blank">Docker CE for Fedora</a>
* <a href="https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/" target="_blank">Docker CE for Ubuntu</a>

And clone the repo by using `git` or download the master [tarball](https://github.com/yigitgenc/lesara-clv/archive/master.zip) to your computer:
```
$ cd lesara-clv/
```

Apply the following commands respectively.
```
$ docker-compose build
```
> Building `predict` service may take longer than expected, please be patient. (<a href="https://stackoverflow.com/questions/49037742/why-does-it-take-ages-to-install-pandas-on-alpine-linux?rq=1">See here</a>)

### Running

```
$ docker-compose up -d
```
> To stop project; use `docker-compose stop` command.

Check processes by doing `docker ps`. You should see something like this:
```
CONTAINER ID        IMAGE                COMMAND                  CREATED                  STATUS              PORTS                    NAMES
083e8970d241        lesara-clv_predict   "python main.py"         Less than a second ago   Up 5 seconds                                 lesara-clv_predict_1
25907e5f28b6        lesara-clv_api       "python api.py"          Less than a second ago   Up About a minute   0.0.0.0:5000->5000/tcp   lesara-clv_api_1
fa1a95628353        redis:4.0.9-alpine   "docker-entrypoint.s…"   7 minutes ago            Up 9 minutes        6379/tcp                 lesara-clv_redis_1
```

Check again your docker processes for a while later. You will see the `predict` container disappeared (completed).
```
CONTAINER ID        IMAGE                COMMAND                  CREATED             STATUS              PORTS                    NAMES
25907e5f28b6        lesara-clv_api       "python api.py"          40 seconds ago      Up 2 minutes        0.0.0.0:5000->5000/tcp   lesara-clv_api_1
fa1a95628353        redis:4.0.9-alpine   "docker-entrypoint.s…"   8 minutes ago       Up 10 minutes       6379/tcp                 lesara-clv_redis_1
```
> If you want to re-run `predict` service again; just type `$ docker-compose up -d predict`. Generated scores will be updated.

Now you are ready to access predicted scores through the API.
```
$ curl http://localhost:5000/api/customers/0867716461bb557156b6f22ae2ee8122
```

You should see something like this:
```
{
    "customer_id": "0867716461bb557156b6f22ae2ee8122",
    "predicted_clv": "292.951564"
}
```

### Tests
```
$ docker-compose run --rm predict pytest --verbosity=3
```

Cheers! :beers: