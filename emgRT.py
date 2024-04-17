import sys
import serial
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.animation import FuncAnimation
from scipy.signal import butter, filtfilt, iirnotch
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler

# Configuração da porta serial
port = 'COM3'  # Substitua pela sua porta
baud_rate = 115200  # Deve corresponder ao configurado no Arduino
ser = serial.Serial(port, baudrate=baud_rate, timeout=1)

# Funções de Filtragem
def apply_filters(data, fs=1000):
    low_cutoff = 20  # frequência de corte do filtro passa-baixa
    b, a = butter(6, low_cutoff / (0.5 * fs), btype='low')
    low_passed = filtfilt(b, a, data)
    
    notch_freq = 60  # frequência central do filtro notch (ajuste conforme necessário)
    quality_factor = 30  # fator de qualidade que define a largura da banda de rejeição
    b, a = iirnotch(notch_freq / (0.5 * fs), quality_factor)
    notch_filtered = filtfilt(b, a, low_passed)
    
    return notch_filtered

class EMGApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Visualização de EMG em Tempo Real")
        self.setGeometry(100, 100, 800, 600)
        self.model = RandomForestClassifier(n_estimators=100)
        self.scaler = StandardScaler()
        
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        self.ax = self.figure.add_subplot(111)
        self.line, = self.ax.plot([], [], 'r-')
        self.ax.set_xlim(0, 100)
        self.ax.set_ylim(-1, 1)

        self.anim = FuncAnimation(self.figure, self.update_plot, init_func=self.plot_init, blit=True)

    def plot_init(self):
        self.line.set_data([], [])
        return self.line,

    def update_plot(self, frame):
        data = self.read_serial_data()
        if data.size == 0:
            return self.line,
        filtered_data = apply_filters(data)
        self.line.set_ydata(filtered_data)  # atualiza os dados do gráfico
        return self.line,

    def read_serial_data(self):
        data = []
        while ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            try:
                data.append(float(line))
            except ValueError:
                continue
        return np.array(data)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    emg_app = EMGApp()
    emg_app.show()
    sys.exit(app.exec_())

# pip install pyqt5 matplotlib numpy scipy scikit-learn pyserial
