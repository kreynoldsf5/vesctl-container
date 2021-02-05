# vesctl-container
Repo for the lazy to run vesctl from docker (or someone who doesn't want to add an untrusted code signing cert to MacOS).

```shell
docker run -v ~/.vesconfig:/root/.vesconfig kreynoldsf5/vesctl:latest
```

## Configure vesctl

Follow the instructions [here](https://gitlab.com/volterra.io/vesctl) to grab API credentials from VoltConsole. Export the P12 password. Write a config file.


```shell
$ export VES_P12_PASSWORD=myp12password
$ cat $HOME/.vesconfig
server-urls: https://acmecorp.ves.console.volterra.io/api
p12-bundle: /root/acmecorp.ves.volterra.io.api-creds.p12
```

Note that my p12 is stored locally and .vesconfig has specified the file as the target of a volume mount.

## Alias
Alias the `vesctl` command to a docker run command that passes in the local ENV variable for your P12 password, volume mounts for `vesconfig` and your p12 cert.

```shell
alias vesctl='docker run --env VES_P12_PASSWORD -v ~/.vesconfig:/root/.vesconfig -v ~/Downloads/acmecorp.ves.volterra.io.api-creds.p12:/root/acmecorp.ves.volterra.io.api-creds.p12 --rm -it kreynoldsf5/vesctl:latest'
```

## Use it
```shell
$vesctl configuration get user -n system
system
+-----------+-----------------------+--------+
| NAMESPACE |         NAME          | LABELS |
+-----------+-----------------------+--------+
| system    | me@me.com             | <None> |
+-----------+-----------------------+--------+
```

