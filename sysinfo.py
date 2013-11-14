#!/usr/bin/env python

import os
import time
import psutil
import requests

def uptime():
    date_time = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())
    date = date_time.split()[0]
    current_time = date_time.split()[1]
    with open('/proc/uptime', 'r') as f:
        uptime_data = float(f.read().split()[0])
    min1, min5, min15 = os.getloadavg()
    uptime_data = {
       'date' : date,
       'current_time' : current_time,
       'uptime_data' : uptime_data,
       'min1' : min1,
       'min5' : min5,
       'min15' : min15,
    }
    return uptime_data

def tasks():
    running = psutil.STATUS_RUNNING
    sleep = psutil.STATUS_SLEEPING
    stop = psutil.STATUS_STOPPED
    zombie = psutil.STATUS_ZOMBIE
    total = running + sleep + stop + zombie
    task_data = {
       'total' : total,
       'sleep' : sleep,
       'running' : running,
       'stop' : stop,
       'zombie': zombie,
    }
    return task_data

def memory():
    vert_mem = psutil.virtual_memory()
    swap_mem = psutil.swap_memory()
    mem_data = {
      'virtmem_total' : vert_mem.total,
      'virtmem_used' : vert_mem.used,
      'virtmem_free' : vert_mem.free,
      'virtmem_buffers' : vert_mem.buffers,
      'swapmem_total': swap_mem.total,
      'swapmem_used' : swap_mem.used,
      'swapmem_free' : swap_mem.free,
    }
    return mem_data
               
def processes(process):
    pid = process.pid
    user = process.username
    ni = process.get_nice()
    virt = int(process.get_memory_info().vms)/1024
    res = int(process.get_memory_info().rss)/1024
    state = process.status
    times = process.get_cpu_times().user + process.get_cpu_times().system
    name = process.name
    mempercent = process.get_memory_percent()
    process_data = {
       'pid' : pid,
       'user' : user,
       'ni' : ni,
       'virt' : virt,
       'res' : res,
       'state' : state,
       'mempercent' : mempercent,
       'times' : times,
       'name' : name,
    }
    return process_data
   
def main():
   while(True):
        all_processes = list(psutil.process_iter()) 
        uptime_data = uptime()
        tasks_data = tasks()
        mem_data = memory()
        process_list = []
        for proc in all_processes:
            process_list.append(processes(proc))
        payload = {
          'uptime': uptime_data,
          'tasks' : tasks_data,
          'memdata' : mem_data,
          'process' : process_list,
        }
        post_url = 'http://127.0.0.1:5000/'
        post_request = requests.post(post_url, data=payload)
        time.sleep(60)

if __name__ == '__main__':
    main()
