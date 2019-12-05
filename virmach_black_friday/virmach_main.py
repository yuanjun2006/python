# https://www.learnpyqt.com/courses/adanced-ui-features/system-tray-mac-menu-bar-applications-pyqt/

import sys
import time
import threading

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from scraper import virmach_get_black_fridy_price

app = None
timer = None

good_vm = False
tray = None
tray_flag = 0

icon_working = None
icon_vm_ok_1 = None
icon_vm_ok_2 = None

t = None
t_quit = False

def timer_handler_func():
    global tray
    global tray_flag

    global icon_vm_ok_1
    global icon_vm_ok_2

    if not good_vm:
        return

    if tray_flag == 0:
        tray_flag = 1
        tray.setIcon(icon_vm_ok_1)
    else:
        tray_flag = 0
        tray.setIcon(icon_vm_ok_2)

    timer = threading.Timer(0.5, timer_handler_func)
    timer.start()

def scraper_thread_func():
    global good_vm
    global t_quit

    while not t_quit:
        vm = virmach_get_black_fridy_price()

        if not vm.valid:
            time.sleep(2)
            continue
        
        if vm.ended:
            print('Switching Soon ... Previous One Is [ PRICE : %.2f, CPU : %d, RAM : %d, HDD : %d, BW : %d, LOC : (%s, %s) ]' % 
                        (vm.price, vm.cpu, vm.ram, vm.hdd, vm.bw, vm.city, vm.state))            
            good_vm = False
            time.sleep(2)
            continue

        print('[ PRICE : %.2f, CPU : %d, RAM : %d, HDD : %d, BW : %d, LOC : (%s, %s) ]' % 
              (vm.price, vm.cpu, vm.ram, vm.hdd, vm.bw, vm.city, vm.state))

        # 'CA', < $20.00, >= 500GB, >= 15GB
        if vm.state == 'CA' and vm.price < 20.0 and vm.bw >= 500 and vm.hdd >= 15:
            print('[ PRICE : %.2f, CPU : %d, RAM : %d, HDD : %d, BW : %d, LOC : (%s, %s) ]' % 
                        (vm.price, vm.cpu, vm.ram, vm.hdd, vm.bw, vm.city, vm.state))
            if not good_vm:
                good_vm = True
                timer = threading.Timer(0.5, timer_handler_func)
                timer.start()
            delay = 5
        else:
            delay = 2
        time.sleep(delay)

def action_exit():
    global t
    global t_quit

    t_quit = True
    t.join()
    app.quit()

def action_clean():
    global good_vm
    good_vm = False

def main():
    global app
    global tray
    global icon_working
    global icon_vm_ok_1
    global icon_vm_ok_2

    global t

    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)

    icon_working  = QIcon("working.png")
    icon_vm_ok_1 = QIcon("vm_ok_1.png")
    icon_vm_ok_2 = QIcon("vm_ok_2.png")
    # Create the icon

    # Create the tray
    tray = QSystemTrayIcon()
    tray.setIcon(icon_working)
    tray.setVisible(True)

    # Create the menu
    menu = QMenu()
    a = QAction("&Exit")
    a.triggered.connect(action_exit)
    menu.addAction(a)

    b = QAction("&Clean")
    b.triggered.connect(action_clean)
    menu.addAction(b)    

    # Add the menu to the tray
    tray.setContextMenu(menu)

    # start scraper thread
    t = threading.Thread(target=scraper_thread_func)
    t.start()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
