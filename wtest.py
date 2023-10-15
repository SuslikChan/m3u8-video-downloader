import urllib.request
from multiprocessing  import Process, Pipe
from time import sleep
import logging


link = 'https://.../561cd0a03fa/'
download_path = '...'

video_name = 'hls-360p-dff8c'
playlist_name = f'{video_name}.m3u8'

fragment_range = 20

logging.basicConfig(filename=download_path+'log.txt')
loger = logging.getLogger()
loger.setLevel(logging.DEBUG)

fragment_name_list = [f'{video_name}{i}.ts' for i in range(fragment_range)]
fragment_link_list = [link + name for name in fragment_name_list]
fragment_path_list = [download_path + name for name in fragment_name_list]

def Download_process(conn, loger, data, name):

  for i in data:
      #sleep(0.1)
      loger.info(f'worker{name}: {i[0]} >>> {i[1]}')
      urllib.request.urlretrieve( i[0], i[1] )
      

  conn.close()
    
def separate_packets(data, num):
    
    fragment_range = len(data)
    
    lens =  [ fragment_range // num_process for i in range(num_process)]
    lens[0] = lens[0] + (fragment_range - sum(lens))
    
    for i in lens:
        data.append(data[:i])
        data = data[i:]
        
    return(data)
    

if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    
    num_process = 4

    packets = separate_packets(list(zip(fragment_link_list, fragment_path_list)), num_process)
    processes = [Process(target=Download_process, args=(child_conn, loger, packets[i], i)) for i in range(num_process)]
    for process in processes: process.start()
    for process in processes: process.join()
