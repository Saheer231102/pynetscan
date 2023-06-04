import socket
import sys
import threading
import time
import tkinter as tk
from tkinter import ttk


# Global Variables / Scanning Variables
ip_start = 1
ip_finish = 1024
log = []
ports = []
target = "localhost"


# FUNCTIONS
def ScanPorts(target, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(4)
        c = s.connect_ex((target, port))
        if c == 0:
            m = "Port %d \t[open]" % (port)
            log.append(m)
            ports.append(port)
            listbox.insert("end", str(m))
            updateResult()
        s.close()
    except OSError:
        print("> TOO many open sockets port" + str(port))
    except:
        s.close()
        sys.exit()


def updateResult():
    result_text = ""+str(target)+" [" + str(len(ports)) + "/" + str(ip_finish) + "]"
    l27.configure(text=result_text)

def StartScan():
    global ports, log, target, ip_finish
    ClearScan()
    ports = []
    # GET PORT RANGES FROM GUI
    ip_start = int(l24.get())
    ip_finish = int(l25.get())
    # DUMP INTO LOG FILE
    log.append("> Port Scanner")
    log.append('=' * 14 + '\n')
    log.append('Target:\t' + str(target))

    try:
        target = socket.gethostbyname(str(l22.get()))
        log.append("IP Adr: \t" + str(target))
        log.append("Ports:\t[" + str(ip_start) + '/' + str(ip_finish) + ']')
        log.append("\n")
        print("scan started for",target ,"from port", ip_start, "to" ,ip_finish)
        # Start scanning ports
        while ip_start <= ip_finish:
            try:
                scan = threading.Thread(target=ScanPorts, args=(target, ip_start))
                scan.daemon = True
                scan.start()
            except:
                time.sleep(0.01)
            ip_start += 1  # Increment ip_start here
        print("Scan Ended, found "+str(len(ports))+" Open ports \nCheck gui for more" )
    except:
        m = '> Target' + str(l22.get()) + 'not found'
        log.append(m)
        listbox.insert(0, str(m))


def SaveScan():
    global log, target, ports, ip_finish
    log[5] = "Result:\t[" + str(len(ports)) + '/' + str(ip_finish) + "]\n"
    with open("portscan-" + str(target) + '.txt', mode='wt', encoding='utf-8') as myfile:
        myfile.write("\n".join(log))


def ClearScan():
    listbox.delete(0, 'end')


# ======GUI======#
gui = tk.Tk()
gui.title("PORT SCANNER")
gui.geometry("800x600+20+20")

# Colors
background_color = "#000000"
foreground_color = "#ffffff"
accent_color = "#1565c0"

gui.configure(bg=background_color)

# Styling
style = ttk.Style()
style.configure("TLabel", background=background_color, foreground=foreground_color, font=("Arial", 14))
style.configure("TEntry", fieldbackground=foreground_color, font=("Arial", 14))
style.configure("TButton", background=accent_color, foreground=background_color, font=("Arial", 14))

# Heading
heading = ttk.Label(gui, text="GUI PORT SCANNER", font=("Arial", 26, "bold"))
heading.place(relx=0.5, rely=0.1, anchor="center")

# Target
l21 = ttk.Label(gui, text="Target:")
l21.place(x=50, y=180, anchor="w")

l22 = ttk.Entry(gui)
l22.place(x=200, y=180, anchor="w", width=400)
l22.insert(0, "localhost")

# Ports
l23 = ttk.Label(gui, text="Ports:")
l23.place(x=50, y=250, anchor="w")

l24 = ttk.Entry(gui)
l24.place(x=200, y=250, anchor="w", width=150)
l24.insert(0, "1")

l25 = ttk.Entry(gui)
l25.place(x=400, y=250, anchor="w", width=150)
l25.insert(0, "1024")

# Results
l26 = ttk.Label(gui, text="Results:")
l26.place(x=50, y=320, anchor="w")

l27 = ttk.Label(gui, text="[Start the scan to view]")
l27.place(x=200, y=320, anchor="w")

# Listbox for ports
listbox_frame = tk.Frame(gui, bg=background_color)
listbox_frame.place(x=50, y=380, relwidth=0.9, relheight=0.4)
listbox = tk.Listbox(listbox_frame, bg=foreground_color, fg=background_color, font=("Arial", 12), selectbackground=accent_color, selectforeground=background_color)
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox.config(yscrollcommand=scrollbar.set)

# Buttons
b11 = ttk.Button(gui, text="Start Scan", command=StartScan)
b11.place(relx=0.5, rely=0.85, anchor="center", width=200)

b21 = ttk.Button(gui, text="Save Results", command=SaveScan)
b21.place(relx=0.5, rely=0.92, anchor="center", width=200)

# Start GUI
gui.mainloop()
