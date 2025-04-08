import etcd3 # visuals studio does not see it but in the container it is installed
import time

etcd = etcd3.client(host="10.0.1.11")

etcd.put("foo", "bar")

etcd.put("jdbc.host", "db.servers.net")
etcd.put("jdbc.port", "3306")
etcd.put("jdbc.user", "admin")
etcd.put("jdbc.password", "password")
etcd.put("jdbc.database", "mydb")

value, metadata = etcd.get("jdbc.user")
results = etcd.get_prefix("jdbc.")

# Convert the generator to a list to avoid exhausting it
results_list = list(results)

# Print the count of results
print("Počet výsledků:", len(results_list))

# Print all values in the results_list
print("Results:")
for value, metadata in results_list:
    print(f"Key: {metadata.key.decode()}, Value: {value.decode()}")

while True:
    print("Trying to enter critical section.")

    # Vytvoření zámku
    lock = etcd.lock('critical-section-1', ttl=20)
    
    try:
        # Pokus o získání zámku
        success = False
        try:
            success = lock.acquire()
        except Exception as e:
            print(f"Error acquiring lock: {e}")
            time.sleep(5)
            continue
            
        if success:
            print("Lock acquired:", success)
            print("Doing something in the critical section...")
            time.sleep(5)
            
            try:
                lock.refresh()
            except Exception as e:
                print(f"Error refreshing lock: {e}")
    except Exception as e:
        print(f"Error in critical section: {e}")
    finally:
        try:
            # Pokus o uvolnění zámku
            lock.release()
            print("Lock released.")
        except Exception as e:
            print(f"Error releasing lock: {e}")
    
    time.sleep(5)

# Print the single value we got earlier
print("User value:", value.decode())
