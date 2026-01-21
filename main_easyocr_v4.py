import cv2
import os
import easyocr
import time
from ultralytics import YOLO

#Wersja z podzieleniem i zamiana pomylonych znakow
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

def is_flexible_match(detected, expected):
    if detected == expected:
        return True
    if not detected or not expected or len(detected) != len(expected):
        return False

    equiv_groups = [
        {'0', 'O', 'D', 'Q', 'U'},
        {'1', 'I', 'L', 'J', 'T'},
        {'2', 'Z'},
        {'3', 'B'},
        {'4', 'A'},
        {'5', 'S'},
        {'6', 'G'},
        {'8', 'B'},
        {'9', 'P'}
    ]

    for d, e in zip(detected, expected):
        if d == e: continue
        match_found = False
        for group in equiv_groups:
            if d in group and e in group:
                match_found = True
                break
        if not match_found:
            return False
    return True

def apply_polish_standards(text):
    if not text: return ""
    text = text.strip().upper()

    to_letter = {'0': 'O', '1': 'I', '2': 'Z', '4': 'A', '5': 'S', '8': 'B'}
    to_digit = {'O': '0', 'I': '1', 'Z': '2', 'S': '5', 'B': '8', 'D': '0', 'U': '0'}

    if " " in text:
        parts = text.split()
        prefix = list(parts[0])
        suffix = list("".join(parts[1:])[:5])
    else:
        chars = list(text[:8])
        check_range = 3 if (len(chars) >= 3 and not chars[2].isdigit()) else 2
        prefix = chars[:check_range]
        suffix = chars[check_range:]

    for i in range(len(prefix)):
        if prefix[i] in to_letter:
            prefix[i] = to_letter[prefix[i]]

    for i in range(len(suffix)):
        if i < 3 and suffix[i] in to_digit:
            suffix[i] = to_digit[suffix[i]]
        if i == len(suffix) - 1 and (suffix[i] == 'O' or suffix[i] == 'D'):
            suffix[i] = '0'

    return "".join(prefix) + "".join(suffix)

def calculate_final_grade(accuracy_percent: float, processing_time_sec: float) -> float:
    if accuracy_percent < 60 or processing_time_sec > 60:
        return 2.0
    accuracy_norm = max(0, min(1, (accuracy_percent - 60) / 40))
    time_norm = max(0, min(1, (60 - processing_time_sec) / 50))
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
        if img is None or img_name not in ground_truth: continue

        results = model(img, verbose=False)
        expected_text = ground_truth[img_name]['text']
        detected_text = ""

        if results and len(results[0].boxes) > 0:
            box = results[0].boxes[0]
            coords = box.xyxy[0].tolist()
            x1, y1, x2, y2 = int(coords[0]), int(coords[1]), int(coords[2]), int(coords[3])
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
                        raw_text = raw_text + res[1] + " "
                    raw_text = raw_text.strip().upper()
                    cleaned = ""
                    for c in raw_text:
                        if c.isalnum() or c.isspace():
                            cleaned = cleaned + c

                    processed = apply_polish_standards(cleaned)
                    detected_text = processed.replace(" ", "")

        is_correct = is_flexible_match(detected_text, expected_text)
        if is_correct:
            status = "OK"
        else:
            status = "BLAD"

        print("[" + str(i + 1).zfill(3) + "] " + img_name + " | OCR: " + detected_text + " | XML: " + expected_text + " | " + status)
        results_stats.append({'correct': is_correct})

    total_time = time.time() - start_time_total
    accuracy = (sum(1 for x in results_stats if x['correct']) / total_images) * 100 if total_images > 0 else 0
    final_grade = calculate_final_grade(accuracy, total_time)

    print("---------------------------")
    print("WYNIKI KONCOWE:")
    print("DOKLADNOSC: " + str(round(accuracy, 2)) + "%")
    print("CZAS LACZNY: " + str(round(total_time, 2)) + "s")
    print("OCENA KONCOWA: " + str(final_grade))

if __name__ == "__main__":
    folder_testowy = os.path.join("photos", "verify", "images")
    plik_xml = "annotations.xml"
    run_final_test(folder_testowy, plik_xml)