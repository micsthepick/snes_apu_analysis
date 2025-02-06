# SNES APU Analysis:

for best results, use reaper
don't forget to make a note of the recording samplerate and first slider value while running, you WILL need these later!

## tutorial:

record the output of spctest/spctest.sfc (as run by the console) at at lest 32 KHz (16 would be slightly too low)
apply the FX to the audio (select the track, right click, Apply track/take FX if unsure how to do this)
then making sure to remember what samplerate the effect was running under, use the following command:

```
python ./visualize.py -i <input file> -r <srate as reported by plugin> -s <bias (first slider's value)> [<-o optional_output_file>]
```

## THANKS
- NobodyNada - spctest code based on my specified waveform
