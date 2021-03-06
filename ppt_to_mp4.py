import win32com.client
import time
import os
import shutil

def ppt_to_mp4(ppt_path,mp4_target,resolution = 720,frames = 24,quality = 60,timeout = 120):
    # status:Convert result. 0:failed. -1: timeout. 1:success.
    time_per_slide = 3
    status = 0
    if ppt_path == '' or mp4_target == '':
        return status
    start_tm = time.time()

    sdir = mp4_target[:mp4_target.rfind('\\')]
    if not os.path.exists(sdir):
        os.makedirs(sdir)
    ppt = win32com.client.Dispatch('PowerPoint.Application')
    presentation = ppt.Presentations.Open(ppt_path,WithWindow=False)
    presentation.CreateVideo(mp4_target,-1,time_per_slide,resolution,frames,quality)
    while True:
        try:
            time.sleep(0.1)
            if time.time() - start_tm > timeout:
                # Converting time out. Killing the PowerPoint process(An exception will be threw out).
                os.system("taskkill /f /im POWERPNT.EXE")
                status = -1
                break
            if os.path.exists(mp4_path) and os.path.getsize(mp4_target) == 0:
                continue
            status = 1
            break
        except Exception as e:
            print ('Error! Code: {c}, Message, {m}'.format(c = type(e).__name__, m = str(e)))
            break
    print (time.time()-start_tm)
    if status != -1:
        ppt.Quit()

    return status
    
if __name__ == '__main__':
    quality = 60
    resolution = 720
    frames = 24
    ppt_path = os.path.abspath('C:/Users/DESKTOP/Downloads/sample.ppt')
    mp4_path = os.path.abspath('C:/Users/DESKTOP/Downloads/test2.mp4')

    ie_temp_dir = ''

    status = 0
    timeout = 4*60
    try:
        status = ppt_to_mp4(ppt_path,mp4_path,resolution,frames,quality,timeout)
        if ie_temp_dir != '':
            shutil.rmtree(ie_temp_dir, ignore_errors=True)
    except Exception as e:
        print ('Error! Code: {c}, Message, {m}'.format(c = type(e).__name__, m = str(e)))
    if status == -1:
        print ('Failed:timeout.')
    elif status == 1:
        print ('Success!')
    else:
        if os.path.exists(mp4_path):
            os.remove(mp4_path)
        print ('Failed:The ppt may have unknow elements. You can try to convert it manual.')