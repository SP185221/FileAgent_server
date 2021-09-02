import socket, tqdm
from tkinter import*
from threading import Thread
from tkinter import filedialog
import requests
import wget, os
from PIL import Image
from time import sleep 
from zipfile import ZipFile
import signal
import subprocess
#import pm_app_fxn as pm

output1 = ['']*1
list_of_sent_files = []

class main_App(Thread):
    def __init__(self):
        Thread.__init__(self)

    def browse_button(self):
        filename = filedialog.askdirectory()
        temp =  self.entry_path.get()
        self.entry_path.delete('0', 'end')
        self.entry_path.insert(0,filename)
        return filename

    def output(self, value):
        #value = sample_text.get(1.0, "end-1c")
        self.output_data.insert(END, value)

    def output_screen(self):
        value = output1[0]
        self.output(value)
        #self.entry_2.insert(1.0, value+'\n')

    def start_server(self):
        server_ip = socket.gethostbyname(socket.gethostname())
        server_port = self.server_port.get()
        self.server_ip.delete('0', 'end')
        self.server_ip.insert(0, server_ip)
        folder_location = self.entry_path.get()
        print(folder_location)
        self.output(f"Server Started at {server_ip} & Port {server_port} \nAll downloaded files will be stored at {folder_location} \n")
        s_run = server_run(server_ip , server_port, folder_location )
        s_run.start()   

    def stop_server(self):
        server_ip = socket.gethostbyname(socket.gethostname())
        #print("Stop Server command is bing execute... ")
        self.output("Stop Server command is being execute... ")
        server_port = self.server_port.get()
        folder_location = self.entry_path.get()
        stop_server = TRUE
        s_run = server_run(server_ip , server_port, folder_location, stop_server )
        s_run.start()
  
    def run(self):
        self.filename1 = ['']*1
        self.data1 = ['']*1
        self.root = Tk()
        #self.entry_0 = Text(self.root, height = 10, width = 250)
        self.entry_path = Entry(self.root, width=55)
        #self.entry_2 = Text(self.root, height = 10, width = 250)
        
        #self.root = Tk()
        self.root.geometry('900x500')
        self.root.title("File Agent - Send your files to specified server")
        # Server IP
        Label(self.root, text = "Server IP:").place(x = 100, y = 50) 
        self.server_ip = Entry(self.root, width=20)
        self.server_ip.place(x=170,y=50)
        self.server_ip.insert(0, "Auto Detect")
        # Port Number
        Label(self.root, text = "Port No: ").place(x = 100, y = 100) 
        self.server_port = Entry(self.root, width=20)
        self.server_port.place(x=170,y=100)
        self.server_port.insert(0, "5003")
        #Connect Button
        Button(self.root, text='Start Server',command = self.start_server, height = 4, width=64,bg='Green',fg='white').place(x=350,y=50)
        
        # File path selector
        #Button(self.root, text='Choose path of folder where file available',command = self.browse_button, width=35,bg='brown',fg='white').place(x=90,y=150)
        self.entry_path = Entry(self.root, width=55)
        self.entry_path.place(x=350,y=150)
        #Default
        self.entry_path.insert(0, "Select Folder path")
        Label(self.root, text = "Interval: ").place(x=690,y=150) 
        self.entry_interval = Entry(self.root, width=10 )
        #Default value
        self.entry_interval.insert(0, " 5")
        self.entry_interval.place(x=740,y=150)
        Button(self.root, text='Choose path of folder where file to download',command = self.browse_button, width=35,bg='brown',fg='white').place(x=90,y=150)
        
        # Action using button
        Button(self.root, text='Stop Server',command = self.stop_server, height = 3, width=47,bg='pink',fg='white').place(x=90,y=200)
        Button(self.root, text='EXIT ',command = self.root.quit, height = 3, width=47,bg='red',fg='white').place(x=470,y=200)
        # Display Logs
        # Action to download
        self.output_data = Text(self.root, height = 8, width = 90)
        self.output_data.place(x=90,y=280)
        self.root.mainloop()
        print("\nProgram Exit")



class server_run(Thread):
    def __init__(self,server_ip, server_port, folder_location, stop_server = False ):
        Thread.__init__(self)
        self.server_ip = server_ip
        self.server_port = int(server_port)
        self.folder_location = folder_location
        self.stop_server = stop_server
        
    def run(self):
        # device's IP address
        SERVER_HOST = self.server_ip 
        SERVER_PORT = self.server_port
        # receive 4096 bytes each time
        BUFFER_SIZE = 4096
        SEPARATOR = "<SEPARATOR>"
        # create the server socket
        # TCP socket
      
        s = socket.socket()
        if self.stop_server == False:
            # bind the socket to our local address
            s.bind((SERVER_HOST, SERVER_PORT))
        
            # enabling our server to accept connections
            # 5 here is the number of unaccepted connections that
            # the system will allow before refusing new connections
       
            while True:
                s.listen(5)
                print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
                # accept connection if there is any
                client_socket, address = s.accept() 
                # if below code is executed, that means the sender is connected
                print(f"[+] {address} is connected.")
                main_App.output(sr,f"\n[+] {address} is connected")
                # receive the file infos
                # receive using client socket, not server socket
                received = client_socket.recv(BUFFER_SIZE).decode()
                filename, filesize = received.split(SEPARATOR)
                # remove absolute path if there is
                filename = os.path.basename(filename)
                #filename = self.filename
                fl = self.folder_location.split('/')
                sp = '\\'
                location = sp.join(fl)
                #location = 'C:\\Users\\Shailesh\\Desktop\\'
                location = location+'\\'+address
                if not os.path.exists(location):
                    os.mkdir(location)
                filename = location+'\\'+filename
                # convert to integer
                filesize = int(filesize)

                # start receiving the file from the socket
                # and writing to the file stream
                progress = tqdm.tqdm(range(filesize), f"\nReceiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
                main_App.output(sr,f"Receiving {filename}")
                with open(filename, "wb") as f:
                    for _ in progress:
                        # read 1024 bytes from the socket (receive)
                        bytes_read = client_socket.recv(BUFFER_SIZE)
                        if not bytes_read:    
                            # nothing is received
                            # file transmitting is done
                            break
                        # write to the file the bytes we just received
                        f.write(bytes_read)
                        # update the progress bar
                        progress.update(len(bytes_read))

                # close the client socket
                client_socket.close()
                s.shutdown(socket.SHUT_RDWR)
        else:
            #s.close()
            command = f"netstat -ano | findstr {SERVER_PORT}"
            c = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr = subprocess.PIPE)
            stdout, stderr = c.communicate()
            print(stdout)
            pid = int(stdout.decode().strip().split(' ')[-1])
            print(pid)
            os.kill(pid, signal.SIGTERM)
            #s.shutdown(socket.SHUT_RDWR)
            print("Server Closed")
            main_App.output(sr,"\nServer Closed....\n")

sr = main_App()
sr.start()
