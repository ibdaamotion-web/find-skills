import sys, json
from faster_whisper import WhisperModel
import subprocess, numpy as np
def load(p):
    b=subprocess.run(['ffmpeg','-v','error','-i',p,'-f','s16le','-ac','1','-ar','16000','-'],capture_output=True).stdout
    return np.frombuffer(b,np.int16).astype(np.float32)/32768
m = WhisperModel("large-v3", device="cpu", compute_type="int8", cpu_threads=4)
out={}
for p in sys.argv[2:]:
    segs,_ = m.transcribe(load(p), language="ar", word_timestamps=True, vad_filter=True, beam_size=5,
        initial_prompt="كفاية بقى يا عين دموع على الغاليين راحت مني أمي")
    out[p]=[{"s":s.start,"e":s.end,"t":s.text,"w":[(w.start,w.end,w.word) for w in s.words]} for s in segs]
json.dump(out, open(sys.argv[1],"w"), ensure_ascii=False)
