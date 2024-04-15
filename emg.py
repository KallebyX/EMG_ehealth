import serial
import numpy as np
from scipy.signal import butter, filtfilt, iirnotch
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler

# Configuração da porta serial
port = 'COM3'  # Substitua pela sua porta
baud_rate = 115200  # Deve corresponder ao configurado no Arduino
ser = serial.Serial(port, baudrate=baud_rate, timeout=1)

# Função para ler dados da porta serial
def read_serial_data(n_samples=1000):
    data = []
    while len(data) < n_samples:
        if ser.in_waiting:
            line = ser.readline().decode().strip()
            try:
                value = float(line)
                data.append(value)
            except ValueError:
                continue
    return np.array(data)

# Funções de Filtragem
def apply_filters(data, fs=1000):
    # Filtro passa-baixa para remover alta frequência de ruído
    low_cutoff = 20  # frequência de corte do filtro passa-baixa
    b, a = butter(6, low_cutoff / (0.5 * fs), btype='low')
    low_passed = filtfilt(b, a, data)
    
    # Filtro Notch para remover a frequência da rede elétrica (60 Hz no Brasil)
    notch_freq = 75  # frequência central do filtro notch
    quality_factor = 45  # fator de qualidade que define a largura da banda de rejeição
    b, a = iirnotch(notch_freq / (0.5 * fs), quality_factor)
    notch_filtered = filtfilt(b, a, low_passed)
    
    return notch_filtered

# Extração de características para várias amostras
def extract_features(data):
    features = []
    for sample in data:
        # Valor absoluto médio (MAV)
        mav = np.mean(np.abs(sample))
        # Valor quadrático médio (RMS)
        rms = np.sqrt(np.mean(np.square(sample)))
        features.append([mav, rms])
    return np.array(features)

# Coletar dados
raw_data = read_serial_data(n_samples=2000)  # Coleta de 2000 amostras
filtered_data = apply_filters(raw_data)

# Dividir dados em janelas
window_size = 100  # Tamanho da janela
windows = [filtered_data[i:i+window_size] for i in range(0, len(filtered_data), window_size)]

# Extração de características
features = extract_features(windows)
labels = np.zeros(len(features))  # Rótulos fictícios, substitua conforme necessário

# Escalação dos dados
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)

# Divisão dos dados para treinamento e teste
X_train, X_test, y_train, y_test = train_test_split(features_scaled, labels, test_size=0.25, random_state=42)

# Treinar um modelo de RandomForest
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# Avaliar o modelo
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print("Accuracy:", accuracy)

# Visualizar dados
plt.figure(figsize=(10, 5))
plt.plot(raw_data, label='Original Data')
plt.plot(filtered_data, label='Filtered Data', color='red')
plt.title("EMG Data Before and After Filtering")
plt.xlabel('Sample Number')
plt.ylabel('EMG Signal Amplitude')
plt.legend()
plt.show()
