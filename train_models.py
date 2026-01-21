from ultralytics import YOLO

def start_training():
    # 1. Ładujemy bazowy, "pusty" model
    model = YOLO('yolov8n.pt')

    # 2. Rozpoczynamy proces uczenia
    model.train(
        data='data.yaml',    # ścieżka do pliku konfiguracyjnego
        epochs=50,           # 50 "okrążeń" uczenia wystarczy na tablice
        imgsz=640,           # rozmiar obrazów treningowych
        plots=True,          # wygeneruje wykresy pokazujące postępy
        device='cpu'             # zmień na device=0 jeśli masz kartę graficzną NVIDIA
    )

if __name__ == '__main__':
    start_training()