import math
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror

import numpy as np
import pandas as pd
from scipy.signal import butter, filtfilt
import pywt
#import sklearn
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

def load_data(file_path):
    with open(file_path, 'r') as file:
        data = file.read().replace('\n', '').split('|')[:-1]
        return np.array(data, dtype=float)

# Load datasets
lbbb_train = load_data('Normal&LBBB/LBBB_Train.txt')
lbbb_test = load_data('Normal&LBBB/LBBB_Test.txt')
normal_train = load_data('Normal&LBBB/Normal_Train.txt')
normal_test = load_data('Normal&LBBB/Normal_Test.txt')

def preprocess_signal(signal, fs=360, lowcut=0.5, highcut=40):
    # Mean removal
    signal = signal - np.mean(signal)

    # Bandpass Butterworth filter
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(4, [low, high], btype='band')
    filtered_signal = filtfilt(b, a, signal)


    # Normalization
    # Normalize to range 0 to 1
    normalized_signal = (filtered_signal - np.min(filtered_signal)) / (np.max(filtered_signal) - np.min(filtered_signal))
    return normalized_signal



# Preprocess signals
lbbb_train = preprocess_signal(lbbb_train)
lbbb_test = preprocess_signal(lbbb_test)
normal_train = preprocess_signal(normal_train)
normal_test = preprocess_signal(normal_test)
print(lbbb_train)
print("")
print(lbbb_test)
print("")
print(normal_train)
print("")
print(normal_test)

def extract_wavelet_features(signal, wavelet='db4'):


    coeffs = pywt.wavedec(signal, wavelet, level=9) #level =9

    # Extract coefficients
    approximation = coeffs[0]  # cA_9
    details = coeffs[1:]  # [cD_9, cD_8, cD_7,cD_6, cD_5, cD_4,cD_3, cD_2, cD_1]
    print(f"approximation :{approximation}")
    print(f"details :{details}")
   
    features_extraction = coeffs[1:8]
    return features_extraction


# Extract features
lbbb_train_features = extract_wavelet_features(lbbb_train)
lbbb_test_features = extract_wavelet_features(lbbb_test)
normal_train = extract_wavelet_features(normal_train)
normal_test_features = extract_wavelet_features(normal_test)

