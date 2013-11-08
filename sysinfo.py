#!/usr/bin/env python

import os
import time
import psutil

def uptime():
    date_time = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())
    date = date_time.split()[0]
    current_time = date_time.split()[1]
    with open('/proc/uptime', 'r') as f:
        uptime_data = float(f.read().split()[0])
    min1, min5, min15 = os.getloadavg()
    print '\n' 
    print "Date: %s, Time: %s, Uptime: %s sec, Load Average: %s, %s, %s " % (date,current_time,uptime_data,min1,min5,min15)

def tasks():
    running = psutil.STATUS_RUNNING
    sleep = psutil.STATUS_SLEEPING
    stop = psutil.STATUS_STOPPED
    zombie = psutil.STATUS_ZOMBIE
    total = running + sleep + stop + zombie
    print "Tasks: %d total, %d sleeping, %d running, %d stopped, %d zombie" % (total,sleep,running,stop,zombie)
    
def mem_data():
    vert_mem = psutil.virtual_memory()
    swap_mem = psutil.swap_memory()
    print "Virt Mem: %s total, %s used, %s free, %s buffers" % (vert_mem.total,vert_mem.used,vert_mem.free,vert_mem.buffers)
    print "Swap Mem: %s total, %s used, %s free" % (swap_mem.total,swap_mem.used,swap_mem.free)
    print '\n'
               
def process_data(process):
    pid = process.pid
    user = process.username
    ni = process.get_nice()
    virt = int(process.get_memory_info().vms)/1024
    res = int(process.get_memory_info().rss)/1024
    state = process.status
    times = process.get_cpu_times().user + process.get_cpu_times().system
    name = process.name
    mempercent = process.get_memory_percent()
    print "%5s %7s %3s %7s %6s %10s %15s %8s %s" % (pid,user,ni,virt,res,state,mempercent,times,name)
    
   
if __name__ == '__main__':
   while(True):
        all_processes = list(psutil.process_iter()) 
        uptime()
        tasks()
        mem_data()
        print "  PID    USER   NI   VIRT    RES    STATE          MEM%        TIMES NAME"
        for proc in all_processes:
            process_data(proc)   
        time.sleep(60)
        
