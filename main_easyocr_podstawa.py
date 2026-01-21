import cv2
import os
import easyocr
import time
from ultralytics import YOLO

#Inicjalizacja modeli - YOLO do detekcji i EasyOCR do tekstu
model = YOLO('runs/detect/train2/weights/best.pt')
reader = easyocr.Reader(['en'], gpu=True)


def load_detailed_annotations(xml_path):
    #Funkcja wczytuje dane z pliku XML i zwraca slownik z nazwa zdjecia i tekstem
    import xml.etree.ElementTree as ET
    tree = ET.parse(xml_path)
    root = tree.getroot()
    data = {}
    for image in root.findall('image'):
        name = image.get('name')
        box = image.find('box')
        if box is not None:
            xtl = float(box.get('xtl'))
            ytl = float(box.get('ytl'))
            xbr = float(box.get('xbr'))
            ybr = float(box.get('ybr'))
            attr = box.find(".//attribute[@name='plate number']")
            plate_number = attr.text if attr is not None else ""
            #Usuwamy spacje i zamieniamy na wielkie litery dla porownania
            data[name] = {
                'box': [xtl, ytl, xbr, ybr],
                'text': plate_number.strip().upper().replace(" ", "")
            }
    return data


def calculate_final_grade(accuracy_percent: float, processing_time_sec: float) -> float:
    """
    Calculates the final grade based on license plate OCR accuracy and processing time.
    """
    if accuracy_percent < 60 or processing_time_sec > 60:
        return 2.0

    # Normalize accuracy: 60% → 0.0, 100% → 1.0
    accuracy_norm = (accuracy_percent - 60) / 40
    # Normalize time: 60s → 0.0, 10s → 1.0
    time_norm = (60 - processing_time_sec) / 50
    # Clip norms to range [0, 1] in case of values exceeding limits
    accuracy_norm = max(0, min(1, accuracy_norm))
    time_norm = max(0, min(1, time_norm))

    # Compute weighted score
    score = 0.7 * accuracy_norm + 0.3 * time_norm
    grade = 2.0 + 3.0 * score

    # Round to the nearest 0.5
    return round(grade * 2) / 2


def run_final_test(test_images_dir, annotations_xml):
    #Glowna funkcja testujaca caly zbior zdjec
    ground_truth = load_detailed_annotations(annotations_xml)
    correct_count = 0
    test_images = sorted([f for f in os.listdir(test_images_dir) if f.endswith('.jpg')])
    total_images = len(test_images)

    #Zmienna startowa do mierzenia czasu calego procesu
    start_time_total = time.time()

    for i in range(total_images):
        img_name = test_images[i]
        img = cv2.imread(os.path.join(test_images_dir, img_name))
        if img is None or img_name not in ground_truth:
            continue

        #Detekcja tablicy przy uzyciu modelu YOLO
        results = model(img, verbose=False)
        expected_text = ground_truth[img_name]['text']
        detected_text = ""

        if results and len(results[0].boxes) > 0:
            box = results[0].boxes[0]
            coords = box.xyxy[0].tolist()
            x1, y1, x2, y2 = map(int, coords)
            w, h = x2 - x1, y2 - y1

            #Parametry przycinania dla uzyskania najlepszego rezultatu
            x1_c = int(x1 + w * 0.12)
            x2_c = int(x2 - w * 0.025)
            y2_c = int(y2 - h * 0.13)

            #Wycinanie obszaru tablicy z oryginalnego zdjecia
            plate_crop = img[max(0, y1):min(img.shape[0], y2_c),
            max(0, x1_c):min(img.shape[1], x2_c)]

            if plate_crop.size > 0:
                #Odczyt tekstu za pomoca biblioteki easyocr
                ocr_results = reader.readtext(plate_crop)
                if ocr_results:
                    #Laczenie wykrytych fragmentow tekstu w jeden ciag
                    raw_text = ""
                    for res in ocr_results:
                        raw_text = raw_text + res[1]

                    raw_text = raw_text.strip().upper()

                    #Filtrowanie ciagu - pozostawienie tylko liter i cyfr
                    cleaned = ""
                    for char in raw_text:
                        if char.isalnum():
                            cleaned = cleaned + char

                    #Ucinanie wyniku do dlugosci zdefiniowanej w XML (standard tablic rejestracyjnych w polsce)
                    target_len = len(expected_text)
                    detected_text = cleaned[0:target_len]

        #Porownanie wyniku detekcji z tekstem wzorcowym
        is_correct = (detected_text == expected_text)
        if is_correct:
            correct_count = correct_count + 1
            status = "OK"
        else:
            status = "BLAD"

        #Wyswietlanie linii wyniku
        print("[" + str(i + 1).zfill(
            3) + "] " + img_name + " | OCR: " + detected_text + " | XML: " + expected_text + " | " + status)

    #Obliczanie koncowych statystyk po zakonczeniu petli
    total_time = time.time() - start_time_total
    accuracy = (correct_count / total_images) * 100 if total_images > 0 else 0
    final_grade = calculate_final_grade(accuracy, total_time)

    #Wyswietlanie podsumowania
    print("---------------------------")
    print("Statystyki koncowe:")
    print("Dokladnosc: " + str(round(accuracy, 2)) + "%")
    print("Czas przetwarzania: " + str(round(total_time, 2)) + "s")
    print("OCENA KONCOWA: " + str(final_grade))


if __name__ == "__main__":
    folder_testowy = os.path.join("photos", "verify", "images")
    plik_xml = "annotations.xml"
    run_final_test(folder_testowy, plik_xml)