import pyaudio

def search_microphone_index():
    myPyAudio = pyaudio.PyAudio()
    devices = myPyAudio.get_device_count()
    for i in range(0,devices):
        name = myPyAudio.get_device_info_by_index(i)['name'].split(':')[0]
        if(name=='USB PnP Sound Device'):
            return i
    return -1
        

def main():
    myPyAudio = pyaudio.PyAudio()
    print(myPyAudio.get_device_count())
    name = myPyAudio.get_device_info_by_index(2)['name'].split(':')[0]
    print(name)
    index = search_microphone_index()
    print(index)

main()