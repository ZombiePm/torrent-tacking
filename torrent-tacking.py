
import os
import bencodepy

# Указываем путь до папки с торрент-файлами
folder_path = "E:/Downloads"
file_content_name = ".torrent"

# Создаем пустой список трекеров
trackers = set()

# Читаем все файлы *.torrent в указанной папке
for file_name in os.listdir(folder_path):
    if file_content_name in file_name:
        # Открываем файл и декодируем его содержимое в словарь
        with open(os.path.join(folder_path, file_name), "rb") as f:
            torrent_dict = bencodepy.decode(f.read())

        # Извлекаем список трекеров из словаря
        if b'announce-list' in torrent_dict:
            tracker_list = torrent_dict[b'announce-list']
            for sublist in tracker_list:
                for tracker in sublist:
                    trackers.add(tracker.decode())  # добавляем в множество
        elif b'announce' in torrent_dict:
            trackers.add(torrent_dict[b'announce'].decode())  # добавляем в множество

# Прописываем уникальные трекеры во все торрент-файлы
for file_name in os.listdir(folder_path):
    if file_content_name in file_name:
        # Открываем файл и декодируем его содержимое в словарь
        with open(os.path.join(folder_path, file_name), "rb") as f:
            torrent_dict = bencodepy.decode(f.read())

        # Заменяем трекеры в словаре
        if b'announce-list' in torrent_dict:
            torrent_dict[b'announce-list'] = [[tracker] for tracker in set(trackers)]  # создаем список уникальных трекеров
        elif b'announce' in torrent_dict:
            torrent_dict[b'announce'] = list(set(trackers))[0]  # берем первый уникальный трекер

        # Записываем измененный словарь в тот же файл
        with open(os.path.join(folder_path, file_name), "wb") as f:
            f.write(bencodepy.encode(torrent_dict))
