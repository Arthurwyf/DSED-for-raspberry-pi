from nnet.CRNN import CRNN
import torch
import yaml
from utils.scaler import TorchScaler
from torchaudio.transforms import AmplitudeToDB, MelSpectrogram
import torchaudio
import random
from utils.model_audio import take_log, read_audio
import librosa


if __name__ == '__main__':
    with open('./confs/freesound_only_weak.yaml', "r") as f:
        configs = yaml.safe_load(f)
    model = CRNN(**configs["net"])

    checkpoint = torch.load("./checkpoints/epoch=146-step=12053.ckpt", map_location='cpu')
    new_state_dict = {}
    for key, value in checkpoint['state_dict'].items():
        if 'sed_student.' in key:
            key = key.replace('sed_student.', '')
            new_state_dict[key] = value
    checkpoint['state_dict'] = new_state_dict
    model.load_state_dict(checkpoint['state_dict'])
    scaler = TorchScaler(
        "instance",
        "minmax",
        [1, 2],
    )

    # eval
    mel_spec = MelSpectrogram(
        sample_rate=16000,
        n_fft=2048,
        win_length=2048,
        hop_length=256,
        f_min=0,
        f_max=8000,
        n_mels=128,
        window_fn=torch.hamming_window,
        wkwargs={"periodic": False},
        power=1,
    )
    model.eval()
    
    audio, *_ = read_audio("./records/587_0_10.wav", 10 * 16000)  # Audio file should be in 16,000Hz
    features = mel_spec(audio)
    features = features.unsqueeze(0)
    result1 = model(scaler(take_log(features)))
    predictions = '[' + ','.join(["{:.4f}".format(x) for x in result1[1][0].tolist()]) + ']'
    print(predictions)
