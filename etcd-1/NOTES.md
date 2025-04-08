# COMMANDS FROM THE EXERCISE

This file containes output from the command line which was used during exercise. During exercise were running 3 etcd nodes on which we were connected and on them we were executing commands shown bellow.

## ETCD-1
``` 
[vagrant@etcd-1 ~]$ /opt/etcd/etcdctl lock mutex1
mutex1/234095d6f3705305

^C[vagrant@etcd-1 ~]$ /opt/etcd/etcdctl put db db.server
OK

[vagrant@etcd-1 ~]$ /opt/etcd/etcdctl elect v2025 l_1
v2025/234095d6f370530e

^C[vagrant@etcd-1 ~]$ /opt/etcd/etcdctl elect v2025 l_1
^CError: context canceled
[vagrant@etcd-1 ~]$ Connection to 127.0.0.1 closed by remote host.
l_1
``` 

## ETCD-2

``` 
[vagrant@etcd-2 ~]$ /opt/etcd/etcdctl lock mutex1
mutex1/6c4595d6f3780104

^C[vagrant@etcd-2 ~]$ /opt/etcd/etcdctl get db
db
db.server
[vagrant@etcd-2 ~]$ /opt/etcd/etcdctl elect v2025 l_2
v2025/6c4595d6f378010d
l_2
[vagrant@etcd-2 ~]$ ^C
[vagrant@etcd-2 ~]$ Connection to 127.0.0.1 closed by remote host.
(base) bohdanteply@Bohdan-MacBook-Pro-5 etcd-1 % vagrant ssh etcd-2
```

## ETCD-3

``` 
[vagrant@etcd-3 ~]$ /opt/etcd/etcdctl lock mutex1
mutex1/748195d6f3806904

^C[vagrant@etcd-3 ~]/opt/etcd/etcdctl elect v2025 l_3
v2025/748195d6f380690c
l_3
^C[vagrant@etcd-3 ~]$ Connection to 127.0.0.1 closed by remote host.
```