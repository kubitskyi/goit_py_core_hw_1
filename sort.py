from pathlib import Path
import shutil
import sys


#  Translation
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANS = {}
INVALI_CHAR = set('!@#$%^&*()-+=`~:;}{\/?')

for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()
    

#  Folders and category 
FILE_CATEGORY={
    'images': ['jpeg', 'png', 'jpg', 'svg'],
    'video': ['avi', 'mp4', 'mov', 'mkv'],
    'documents': ['doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx'],
    'audio':  ['mp3', 'ogg', 'wav', 'amr'],
    'archives': ['zip', 'gz', 'tar']
}
# TARGET_FOLDER = '/home/yaroslav/Projects/goit_py_hw/tets'
TARGET_FOLDER = sys.argv[1]
PATH = Path(TARGET_FOLDER +'/')

FOLDERS =[ Path(TARGET_FOLDER + '/' + x) for x in FILE_CATEGORY.keys()]+[Path(TARGET_FOLDER + '/' +'unknown')]


# Нормалізація імен
def normalize(name: str) -> str:
    name = name.translate(TRANS)
    for i in name:
        if i in INVALI_CHAR:
            name = name.replace(i, '_')    
    return name


    for ctg in FOLDERS:
        try:
            ctg.mkdir()
        except FileExistsError as exc:
            continue


# Сортування файлів
def sort_file(file: Path) -> None:
    sufix = str(file.suffix)[1:]

    try:
        if sufix in FILE_CATEGORY['images']:
            shutil.move(file, PATH / 'images')
        elif sufix in FILE_CATEGORY['video']:
            shutil.move(file, PATH / 'video')
        elif sufix in FILE_CATEGORY['documents']:
            shutil.move(file, PATH / 'documents')
        elif sufix in FILE_CATEGORY['audio']:
            shutil.move(file, PATH / 'audio')
        elif sufix in FILE_CATEGORY['archives']:
            shutil.move(file, PATH / 'archives')
        else:
            shutil.move(file, PATH / 'unknown')
    except shutil.Error:
        name = str(file.stem + '_copy' + file.suffix)
        file = file.rename(file.parent/name)
        sort_file(file)

# Вивід результатів
def print_result(path: Path):
    result = {}
    for item in path.iterdir():
        count = 0
        for j in item.iterdir():
            count +=1
        result.update({item.name:count})

    print('Відсортовано :')
    print(f"      {result['images']} - зображень")
    print(f"      {result['video']} - відео")
    print(f"      {result['audio']} - аудіо")
    print(f"      {result['documents']} - документів")
    print(f"      {result['archives']} - архівів розпаковано")
    print(f"      {result['unknown']} - невідомих файлів.")


def main(path: Path, first_round = True):
    #Провірка на перший прохід
    if first_round:
        try:
            p = path / 'tmp_dir'
            p.mkdir()
        except FileExistsError:
            pass
            
        for item in path.iterdir():
            if item in FOLDERS:
                try:
                    shutil.move(item, PATH / 'tmp_dir')
                except shutil.Error:
                    name = str(item.stem + '_copy' + item.suffix)
                    item = item.rename(item.parent/name)

        for ctg in FOLDERS:
            try:
                ctg.mkdir()
            except FileExistsError as exc:
                continue

    # Прохід по папках
    for item in path.iterdir():
        if item in FOLDERS:
            continue
        elif item.is_dir():
            main(item, first_round=False)
            item.rmdir()
        elif item.is_file():
            
            new_name = normalize(item.stem)+item.suffix
            item = item.rename(item.parent/new_name)

            if item.suffix[1:] in FILE_CATEGORY['archives']:      
                shutil.unpack_archive(item, PATH/'archives'/item.stem)
                item.unlink()

            sort_file(item)

    # return path.rmdir() if path != PATH else main(item, first_round=False)
    

if __name__ == '__main__':
    main(PATH)
    print_result(PATH)
