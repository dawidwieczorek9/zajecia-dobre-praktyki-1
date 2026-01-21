import cv2
import os
import easyocr
import time
from ultralytics import YOLO

#Wersja z poprawą tylko znaku powiatowego (pierwszej czesci numeru)
model = YOLO('runs/detect/train2/weights/best.pt')
reader = easyocr.Reader(['en'], gpu=True)

def load_detailed_annotations(xml_path):
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
            data[name] = {
                'box': [xtl, ytl, xbr, ybr],
                'text': plate_number.strip().upper().replace(" ", "")
            }
    return data

def calculate_iou(box1, box2):
    x_left = max(box1[0], box2[0])
    y_top = max(box1[1], box2[1])
    x_right = min(box1[2], box2[2])
    y_bottom = min(box1[3], box2[3])
    if x_right < x_left or y_bottom < y_top:
        return 0.0
    intersection_area = (x_right - x_left) * (y_bottom - y_top)
    area1 = (box1[2] - box1[0]) * (box1[3] - box1[1])
    area2 = (box2[2] - box2[0]) * (box2[3] - box2[1])
    union_area = area1 + area2 - intersection_area
    return intersection_area / union_area

def apply_polish_standards(text):
    if not text:
        return ""
    if len(text) > 8:
        text = text[:8]

    digit_to_letter = {
        '0': 'O', '1': 'I', '2': 'Z', '3': 'B',
        '4': 'A', '5': 'S', '6': 'G', '7': 'T', '8': 'B'
    }
    chars = list(text)

    check_range = 2
    if len(chars) >= 3 and not chars[2].isdigit():
        check_range = 3

    for i in range(min(len(chars), check_range)):
        if chars[i] in digit_to_letter:
            chars[i] = digit_to_letter[chars[i]]
    return "".join(chars)

def calculate_final_grade(accuracy_percent: float, processing_time_sec: float) -> float:
    if accuracy_percent < 60 or processing_time_sec > 60:
        return 2.0

    accuracy_norm = (accuracy_percent - 60) / 40
    time_norm = (60 - processing_time_sec) / 50
    accuracy_norm = max(0, min(1, accuracy_norm))
    time_norm = max(0, min(1, time_norm))

    score = 0.7 * accuracy_norm + 0.3 * time_norm
    grade = 2.0 + 3.0 * score

    return round(grade * 2) / 2

def run_final_test(test_images_dir, annotations_xml):
    ground_truth = load_detailed_annotations(annotations_xml)
    results_stats = []
    test_images = sorted([f for f in os.listdir(test_images_dir) if f.endswith('.jpg')])
    total_images = len(test_images)

    start_time_total = time.time()

    for i in range(total_images):
        img_name = test_images[i]
        img = cv2.imread(os.path.join(test_images_dir, img_name))
        if img is None or img_name not in ground_truth:
            continue

        results = model(img, verbose=False)
        expected_text = ground_truth[img_name]['text']
        detected_text = ""
        coords = [0, 0, 0, 0]

        if results and len(results[0].boxes) > 0:
            box = results[0].boxes[0]
            coords = box.xyxy[0].tolist()
            x1, y1, x2, y2 = map(int, coords)
            w, h = x2 - x1, y2 - y1

            x1_c = int(x1 + w * 0.12)
            x2_c = int(x2 - w * 0.025)
            y2_c = int(y2 - h * 0.13)

            plate_crop = img[max(0, y1):min(img.shape[0], y2_c),
                             max(0, x1_c):min(img.shape[1], x2_c)]

            if plate_crop.size > 0:
                ocr_results = reader.readtext(plate_crop)
                if ocr_results:
                    raw_text = ""
                    for res in ocr_results:
                        raw_text = raw_text + res[1]
                    raw_text = raw_text.strip().upper()
                    cleaned_text = ""
                    for char in raw_text:
                        if char.isalnum():
                            cleaned_text = cleaned_text + char
                    detected_text = apply_polish_standards(cleaned_text)

        is_correct = (detected_text == expected_text)
        if is_correct:
            status = "OK"
        else:
            status = "BLAD"

        print("[" + str(i + 1).zfill(3) + "] " + img_name + " | OCR: " + detected_text + " | XML: " + expected_text + " | " + status)

        iou = calculate_iou(coords, ground_truth[img_name]['box'])
        results_stats.append({'correct': is_correct, 'iou': iou})

    total_time = time.time() - start_time_total
    accuracy = (sum(1 for x in results_stats if x['correct']) / total_images) * 100 if total_images > 0 else 0
    final_grade = calculate_final_grade(accuracy, total_time)

    print("---------------------------")
    print("Statystyki koncowe:")
    print("Osiagnieta dokladnosc: " + str(round(accuracy, 2)) + "%")
    print("Czas przetwarzania: " + str(round(total_time, 2)) + "s")
    print("OCENA KONCOWA: " + str(final_grade))

if __name__ == "__main__":
    folder_testowy = os.path.join("photos", "verify", "images")
    plik_xml = "annotations.xml"
    run_final_test(folder_testowy, plik_xml)