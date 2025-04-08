# Postup na cviceni

- pripojit se na client-1 a kouknout se na promennou (nic neni videt)
```
[vagrant@client-1 ~]$ echo $ZOO_SERVERS

[vagrant@client-1 ~]$ exit
logout
```

- připojíme se jiným způsobem protože přes vagrant ssh client1 jako minule ty výpisy nefungovaly
```
(base) bohdanteply@Bohdan-MacBook-Pro-5 demo-4 % docker exec -it client-1 bash
[root@client-1 /]# echo $ZOO_SERVERS
10.0.1.100
```

- přejdeme do složky se skripty
- spustíme skript což vyhodí chybu protože v GUI kazoo musíme přidat patřičné složku `dsa` a v ní pak složky `jedna`, `dva`, `tri`, `clients`
- připojení do GUI `10.0.1.100:2181` (tohle je login, heslo není)
```
[root@client-1 /]# cd /opt/zk/client/
[root@client-1 client]# ls
zk-client-1.py  zk-client-2.py  zk-client-3.py
[root@client-1 client]# python3 zk-client-1.py
Client will use these servers: 10.0.1.100.
Traceback (most recent call last):
  File "/opt/zk/client/zk-client-1.py", line 25, in <module>
    main()
  File "/opt/zk/client/zk-client-1.py", line 19, in main
    children = zk.get_children("/dsa")
  File "/usr/local/lib/python3.9/site-packages/kazoo/client.py", line 1291, in get_children
    return self.get_children_async(
  File "/usr/local/lib/python3.9/site-packages/kazoo/handlers/utils.py", line 78, in get
    raise self._exception
kazoo.exceptions.NoNodeError
```

- spouštíme odpovídající skripty zk čimž nahodíme nodey a díváme se jak se v GUI vytvářejí a mažou složky atd