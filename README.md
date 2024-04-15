Projeto de Análise de Sinais EMG

Este projeto desenvolve um sistema completo para a coleta, filtragem e análise de sinais eletromiográficos (EMG) usando Arduino, a eHealth Sensor Platform V2.0, e processamento em Python. O objetivo é facilitar a aplicação destes sinais em contextos clínicos e de pesquisa, como no controle de próteses e na avaliação da atividade muscular.

Funcionalidades

Coleta de Sinais EMG: Utiliza Arduino e eHealth Sensor Platform para capturar sinais EMG diretamente dos músculos do usuário.
Filtragem Digital de Sinais: Implementa filtros digitais em Python para limpar o sinal de ruídos indesejáveis.
Análise de Machine Learning: Utiliza modelos de aprendizado de máquina para classificar ou interpretar os sinais EMG.
Visualização de Dados: Fornece scripts para visualizar os sinais EMG antes e depois da filtragem.
Hardware Necessário

Arduino (Uno, Mega, etc.)
eHealth Sensor Platform V2.0 com módulo de EMG
Cabos e conexões adequadas
Computador com uma porta serial disponível
Software Necessário

Python 3.6+
Bibliotecas Python: pyserial, numpy, scipy, matplotlib, scikit-learn
Instale as bibliotecas usando pip:
bash: pip install pyserial numpy scipy matplotlib scikit-learn
Configuração

Montagem do Hardware
Conecte os eletrodos de EMG à eHealth Sensor Platform seguindo o manual do usuário fornecido com a plataforma.
Conecte a eHealth Sensor Platform ao Arduino.
Conecte o Arduino ao computador via cabo USB.
Preparação do Software
Carregue o script de coleta de dados no Arduino (verifique o diretório arduino para o código-fonte).
Certifique-se de que o Arduino está configurado para transmitir dados para a porta COM correta no seu computador.
Uso

Para iniciar a coleta e análise de dados, execute o script Python emg.py:

bash: python emg.py
Este script irá inicializar a coleta de dados do Arduino, aplicar a filtragem e a análise, e exibir os resultados visualmente.
