
from matplotlib import pyplot as plt
from pydub import AudioSegment
from argparse import ArgumentParser
import numpy as np

def main(in_file, out_file, bias):
    stream = AudioSegment.from_file(in_file)
    sample_range = stream.sample_width
    mapping = {1: np.uint8, 2: np.int16, 4: np.int32}
    dtype = mapping[sample_range]
    samples = np.array(stream.get_array_of_samples(), dtype=np.float32)

    if stream.channels > 1:
        samples = samples[::stream.channels]

    max_val = np.iinfo(dtype).max
    min_val = np.iinfo(dtype).min
    print(stream.frame_rate)
    samples = ((samples - min_val) / (max_val - min_val) * 2 - 1) * stream.frame_rate + bias

    if out_file is not None:
        with open(out_file, 'wb') as of:
            of.write(samples.tobytes())

    t = np.arange(len(samples))/stream.frame_rate

    plt.plot(t, samples)
    plt.ylabel("delta " if bias == 0 else "" + "frequency (Hz)")
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
        "-o",
        "--outfile",
        default=None,
        help="the file (raw) to output scaled signal to, if not provided will just visualize the output"
    )
    config = ap.parse_args()
    in_file = config.infile.strip()
    out_file = None if config.outfile is None else config.outfile.strip()
    bias = config.sum
    main(in_file, out_file, bias)