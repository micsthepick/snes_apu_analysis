
from matplotlib import pyplot as plt
import matplotlib.ticker as mticker
from pydub import AudioSegment
from argparse import ArgumentParser
import numpy as np

def main(in_file, out_file, bias, srate):
    stream = AudioSegment.from_file(in_file)
    samples = np.array(stream.get_array_of_samples())

    dtype = samples.dtype

    if stream.channels > 1:
        samples = samples[::stream.channels]

    if (samples.dtype not in [np.float32, np.float64]):
        max_val = np.iinfo(dtype).max
        min_val = np.iinfo(dtype).min
        samples = ((np.array(samples, dtype=np.float64) - min_val) / (max_val - min_val) * 2 - 1) * (srate if srate > 0 else stream.frame_rate) + bias

    if out_file is not None:
        with open(out_file, 'wb') as of:
            of.write(samples.tobytes())

    t = np.arange(len(samples))/stream.frame_rate

    plt.plot(t, samples/1000)
    plt.ylabel(("delta " if bias == 0 else "") + "frequency (KHz)")
    ax = plt.gca()  # Get current axis
    formatter = mticker.ScalarFormatter(useOffset=False, useMathText=False)
    formatter.set_scientific(False)
    ax.yaxis.set_major_formatter(formatter)
    plt.xlabel("time (s)")
    plt.show()

if __name__ == "__main__":
    ap = ArgumentParser(
        prog='SNES_APU_Visualize',
        description='converts the output of snes_apu.jsfx and displays with matplotlib'
    )
    ap.add_argument(
        "-i",
        "--infile",
        required=True,
        help="the file to process"
    )
    ap.add_argument(
        "-s",
        "--sum",
        type=float,
        default=0,
        help="the bias (target freq) that was originally applied."
         " will be added to the multiplied signal to recover the actual frequency if provided."
    )
    ap.add_argument(
        "-r",
        "--srate",
        type=float,
        default=0,
        help="the samplerate that the effect was originally applied with."
    )
    ap.add_argument(
        "-o",
        "--outfile",
        default=None,
        help="the file (raw) to output scaled signal to, if not provided will just visualize the output"
    )
    config = ap.parse_args()
    in_file = config.infile.strip()
    out_file = None if config.outfile is None else config.outfile.strip()
    bias = config.sum
    srate = config.srate
    main(in_file, out_file, bias, srate)
