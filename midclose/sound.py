import winsound

wav=r'complete.wav'

def complete(i):
    for i in range(0,i):
        winsound.PlaySound(wav, winsound.SND_NODEFAULT)

if __name__ == '__main__':
    complete(3)
