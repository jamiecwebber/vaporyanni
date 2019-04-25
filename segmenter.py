from matplotlib import pyplot as plt
import matplotlib.cm as cm
import fnmatch
import os
import numpy as np
import librosa
import matplotlib.pyplot as plt
import librosa.display
from sklearn.manifold import TSNE
import json

def get_features(y, sr):
    y = y[0:sr]  # analyze just first second
    S = librosa.feature.melspectrogram(y, sr=sr, n_mels=128)
    log_S = librosa.amplitude_to_db(S, ref=np.max)
    mfcc = librosa.feature.mfcc(S=log_S, n_mfcc=13)
    delta_mfcc = librosa.feature.delta(mfcc, mode='nearest')
    delta2_mfcc = librosa.feature.delta(mfcc, order=2, mode='nearest')
    feature_vector = np.concatenate((np.mean(mfcc,1), np.mean(delta_mfcc,1), np.mean(delta2_mfcc,1)))
    feature_vector = (feature_vector-np.mean(feature_vector)) / np.std(feature_vector)
    return feature_vector

source_audio = "D:/Yanni/YanniBestOf/Yanni - Nine.mp3"

hop_length = 512
y, sr = librosa.load(source_audio)

onset_strengths = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop_length)

onsets = [0]
local_min_index = 0
sensitivity = 30
min_length = 20
for index in range(sensitivity, len(onset_strengths) - sensitivity):
    local_max = np.amax(onset_strengths[index-sensitivity: index])
    
    if onset_strengths[index-1] > onset_strengths[index] < onset_strengths[index+1]:
        local_min_index = index
    if onset_strengths[index] > local_max and not onsets[-1] == local_min_index:
        onsets.append(local_min_index)
        if (onsets[-1] - onsets[-2]) < min_length:
            onsets.pop(-2)

times = [hop_length * onset / sr for onset in onsets]

plt.figure(figsize=(16,4))
plt.subplot(1, 1, 1)
librosa.display.waveplot(y, sr=sr)
plt.vlines(times, -1, 1, color='r', alpha=0.9, label='Onsets')
plt.title('Wavefile with %d onsets plotted' % len(times))
plt.show()