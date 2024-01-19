from torchaudio.transforms import AmplitudeToDB
import torchaudio
import torch
import random


def to_mono(mixture, random_ch=False):

    if mixture.ndim > 1:  # multi channel
        if not random_ch:
            mixture = torch.mean(mixture, 0)
        else:  # randomly select one channel
            indx = np.random.randint(0, mixture.shape[0] - 1)
            mixture = mixture[indx]
    return mixture
    
    
def pad_audio(audio, target_len, fs):
    
    if audio.shape[-1] < target_len:
        audio = torch.nn.functional.pad(
            audio, (0, target_len - audio.shape[-1]), mode="constant"
        )

        padded_indx = [target_len / len(audio)]
        onset_s = 0.000
    
    elif len(audio) > target_len:
        
        rand_onset = random.randint(0, len(audio) - target_len)
        audio = audio[rand_onset:rand_onset + target_len]
        onset_s = round(rand_onset / fs, 3)

        padded_indx = [target_len / len(audio)] 
    else:

        onset_s = 0.000
        padded_indx = [1.0]

    offset_s = round(onset_s + (target_len / fs), 3)
    return audio, onset_s, offset_s, padded_indx


def read_audio(file, pad_to):
    mixture, fs = torchaudio.load(file)
    mixture = to_mono(mixture)

    if pad_to is not None:
        mixture, onset_s, offset_s, padded_index = pad_audio(mixture, pad_to, fs)
    else:
        padded_index = [1.0]
        onset_s = None
        offset_s = None

    mixture = mixture.float()
    return mixture, onset_s, offset_s, padded_index


def take_log(mels):
    """ Apply the log transformation to mel spectrograms.
    Args:
        mels: torch.Tensor, mel spectrograms for which to apply log.

    Returns:
        Tensor: logarithmic mel spectrogram of the mel spectrogram given as input
    """

    amp_to_db = AmplitudeToDB(stype="amplitude")
    amp_to_db.amin = 1e-5  # amin= 1e-5 as in librosa
    return amp_to_db(mels).clamp(min=-50, max=80)  # clamp to reproduce old code

