import xml.etree.ElementTree as ET
import os


def convert_annotations(xml_file, output_folder):
    # Tworzymy folder na etykiety, jeśli nie istnieje
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    tree = ET.parse(xml_file)
    root = tree.getroot()

    count = 0
    for img_tag in root.findall('image'):
        file_name = img_tag.get('name')
        # Zmieniamy .jpg na .txt
        txt_name = os.path.splitext(file_name)[0] + ".txt"

        # Pobieramy wymiary obrazu do normalizacji
        w = float(img_tag.get('width'))
        h = float(img_tag.get('height'))

        box = img_tag.find('box')
        if box is not None:
            # Pobieramy współrzędne pikselowe
            xtl = float(box.get('xtl'))
            ytl = float(box.get('ytl'))
            xbr = float(box.get('xbr'))
            ybr = float(box.get('ybr'))

            # Konwersja na format YOLO: środek_x, środek_y, szerokość, wysokość
            # Wszystko w skali 0.0 - 1.0
            box_width = xbr - xtl
            box_height = ybr - ytl
            x_center = xtl + (box_width / 2)
            y_center = ytl + (box_height / 2)

            # Normalizacja
            norm_x = x_center / w
            norm_y = y_center / h
            norm_w = box_width / w
            norm_h = box_height / h

            # Zapis do pliku: klasa 0 (plate) + współrzędne
            with open(os.path.join(output_folder, txt_name), "w") as f:
                f.write(f"0 {norm_x:.6f} {norm_y:.6f} {norm_w:.6f} {norm_h:.6f}")
            count += 1

    print(f"Przetworzono {count} plików adnotacji do folderu: {output_folder}")

