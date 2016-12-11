from lab_2.djangomongo.helper import insert_random_messages, insert_random_users

import lab_2.djangomongo.data.supplier as supplier

# supplier.users.drop()
# supplier.messages.drop()

# insert_random_users(1000)

import threading
import multiprocessing
from  multiprocessing import Process
from threading import Thread


def execute():
    insert_random_messages(25000)


cpu_count = multiprocessing.cpu_count()
print('Number of CPU:', cpu_count)
for i in range(cpu_count):
    Process(target=execute).start()
