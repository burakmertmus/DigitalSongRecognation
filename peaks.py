#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Burak Mert Muş
#
# Created:     21.12.2018
# Copyright:   (c) Burak Mert Muş 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------


import pylab
import numpy as np
import matplotlib.pyplot as plt
import wave
import scipy
from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.morphology import (generate_binary_structure,
                                      iterate_structure, binary_erosion)
import os
DEFAULT_AMP_MIN = 10
PEAK_NEIGHBORHOOD_SIZE = 15
DEFAULT_WINDOW_SIZE = 4096
DEFAULT_OVERLAP_RATIO = 0.5
DEFAULT_BUDAMA_DEGERİ = 1000.0

def get_wav_info(wav_file):
    wav = wave.open(wav_file)
    frames = wav.readframes(-1)
    sound_info = pylab.fromstring(frames, 'int16')
    frame_rate = wav.getframerate()
    wav.close()
    print(wav_file)
    print("Dosya Açıldı")
    return sound_info, frame_rate

def specGraph(wav_file):
    wsize=DEFAULT_WINDOW_SIZE,
    wratio=DEFAULT_OVERLAP_RATIO,
    sound_info, frame_rate = get_wav_info(wav_file)
    NFFT=1024
    print("Spec Basladı")
    fig, (ax1,ax2) = plt.subplots(nrows=2)
    ##f,t,Sxx=ax1.specgram(sound_info,Fs=frame_rate)
    from scipy import signal
    freqs, times, Sx = signal.spectrogram(sound_info, fs=frame_rate)
    ##print(arr2D)
    Sx=10 * np.log10(Sx)
    im=ax2.pcolormesh(times, freqs, Sx, cmap='viridis')
    fig.colorbar(im,ax=ax2)
    ax2.set_xlabel("Times")
    ax2.set_ylabel("freqs/10")
    indexF,indexT=getPeaks(Sx)
    degerFreqs=[]
    degerTimes=[]
    for i in range(len(indexF)):
        degerFreqs.append(freqs[indexF[i]])
    for j in range(len(indexT)):
        degerTimes.append(times[indexT[j]])
    x=np.linspace(0,frame_rate,len(sound_info))
    ax1.plot(x,sound_info)
    ax2.plot(degerTimes,degerFreqs,'x',color='red')
    ##ax2.plot(nFreqs,nTimes,'x')
    ##plt.show()
    print("Spectogram bitti")
    return indexF,indexT,degerFreqs,degerTimes
    # The `specgram` method returns 4 objects. They are:
    # - Pxx: the periodogram
    # - freqs: the frequency vector
    # - bins: the centers of the time bins
    # - im: the matplotlib.image.AxesImage instance representing the data in the plot
def getPeaks(arr2D, amp_min=DEFAULT_AMP_MIN):
    # http://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.morphology.iterate_structure.html#scipy.ndimage.morphology.iterate_structure
    struct = generate_binary_structure(2, 1)
    neighborhood = iterate_structure(struct,PEAK_NEIGHBORHOOD_SIZE)
    # find local maxima using our fliter shape
    local_max = maximum_filter(arr2D, footprint=neighborhood) == arr2D
    background = (arr2D == 0)
    eroded_background = binary_erosion(background,structure=neighborhood,border_value=1)
    # Boolean mask of arr2D with True at peaks
    # ^ 8 bittte toplama işlemi
    ##detected_peaks = np.logical_xor(local_max,eroded_background)
    detected_peaks = local_max ^ eroded_background
    # extract peaks
    amps = arr2D[detected_peaks]
    j, i = np.where(detected_peaks)
    # filter peaks
    amps = amps.flatten()
    peaks = zip(i, j, amps)
    peaks_filtered = [x for x in peaks if x[2] > amp_min]  # freq, time, amp
    # get indices for frequency and time
    frequency_idx = [x[1] for x in peaks_filtered]
    time_idx = [x[0] for x in peaks_filtered]
    print("Peakler bulundu")
    return frequency_idx, time_idx

def arraySort(matris):
    sayacSira=len(matris)-1
    while sayacSira > 0:
        maxIndis=0
        max = 0.0
        for i in range(0,sayacSira+1,1):
            if(matris[i][1]>=max):
                max=matris[i][1]
                maxIndis=i
        if sayacSira != maxIndis:
            tmpF=matris[sayacSira][0]
            tmpT=matris[sayacSira][1]
            matris[sayacSira][0]=matris[maxIndis][0]
            matris[sayacSira][1]=matris[maxIndis][1]
            matris[maxIndis][0]=tmpF
            matris[maxIndis][1]=tmpT
        sayacSira=sayacSira-1
    return matris
def peakMatris(music):
    indexMF,indexMT,degerMF,degerMT=specGraph(music)
    ## Matrisin Boytunu bulma
    boyutM=0
    for i in range(0,len(degerMF),1):
        if degerMF[i] > DEFAULT_BUDAMA_DEGERİ:
            boyutM=boyutM+1
    k=0
    matrixM=np.array([[0]*2]*boyutM,dtype = float)
    for i in range(0,len(degerMF),1):
        ##degerMF[i] > DEFAULT_BUDAMA_DEGERİ
        if degerMF[i] > DEFAULT_BUDAMA_DEGERİ:
            matrixM[k][0]=degerMF[i]
            matrixM[k][1]=degerMT[i]
            k=k+1
    matrixSM=arraySort(matrixM)
    return matrixSM
