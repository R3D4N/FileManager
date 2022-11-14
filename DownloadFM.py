from pathlib import Path, PurePath
import os, shutil


def findFolder(rutaHome):
    listaNames = ["Descargas", "Downloads"]

    # crea lista con las posibles rutas a la carpeta de descargas
    posiblesRutas = [PurePath.joinpath(rutaHome, name) for name in listaNames]
    for folder in rutaHome.iterdir():
        # envia la ruta correcta
        if folder in posiblesRutas:
            return folder
    raise FileNotFoundError


def orderFiles(downloadPath):
    textExtensions = [".docx", ".doc", ".pdf", ".txt", ".xlsx", ".pptx"]
    audioExtensions = [".mp3", ".wma", ".wav"]
    videoExtensions = [".avi", ".mp4", ".mkv", ".wpl", ".mov"]
    imageExtensions = [".jpeg", ".jpg", ".png", ".ico", ".gif", ".svg"]
    windowsExtensions = [".exe", ".bin", ".msi", ".dll", ".iso"]
    compressedExtensions = [".zip", ".rar", ".7z", ".gz"]
    nameFolders = {
        "TextFiles": 0,
        "AudioFiles": 0,
        "VideoFiles": 0,
        "ImageFiles": 0,
        "ProgramFiles": 0,
        "CompressedFiles": 0,
        "OtherFiles": 0,
        "DuplicateFiles": 0,
    }

    makeFiles(downloadPath)
    # mueve los archivos duplicados y obtiene la cantidad de estos
    nameFolders["DuplicateFiles"] = moveDuplicatefiles(downloadPath)
    KeyFolders = list(nameFolders.keys())

    # analiza cada archivo de la carpeta y la almacena en su carpeta correcta
    for file in downloadPath.iterdir():
        if file.is_dir():
            continue
        try:
            if file.suffix in textExtensions:
                destination = downloadPath / KeyFolders[0]
                shutil.move(file, destination)
                nameFolders[KeyFolders[0]] += 1
            elif file.suffix in audioExtensions:
                destination = downloadPath / KeyFolders[1]
                shutil.move(file, destination)
                nameFolders[KeyFolders[1]] += 1
            elif file.suffix in videoExtensions:
                destination = downloadPath / KeyFolders[2]
                shutil.move(file, destination)
                nameFolders[KeyFolders[2]] += 1
            elif file.suffix in imageExtensions:
                destination = downloadPath / KeyFolders[3]
                shutil.move(file, destination)
                nameFolders[KeyFolders[3]] += 1
            elif file.suffix in windowsExtensions:
                destination = downloadPath / KeyFolders[4]
                shutil.move(file, destination)
                nameFolders[KeyFolders[4]] += 1
            elif file.suffix in compressedExtensions:
                destination = downloadPath / KeyFolders[5]
                shutil.move(file, destination)
                nameFolders[KeyFolders[5]] += 1
            else:
                destination = downloadPath / KeyFolders[6]
                shutil.move(file, destination)
                nameFolders[KeyFolders[6]] += 1
        except:
            print("ya existe")
    makeReadMe(downloadPath, nameFolders)


def makeFiles(downloadPath):
    nameFolders = [
        "TextFiles",
        "AudioFiles",
        "VideoFiles",
        "ImageFiles",
        "ProgramFiles",
        "CompressedFiles",
        "OtherFiles",
        "DuplicateFiles",
    ]
    # crea carpetas con los items de la lista
    for name in nameFolders:
        Path(downloadPath / name).mkdir(exist_ok=True)


def moveDuplicatefiles(downloadPath):
    countDupliFiles = 0
    # se plantea el patron del nombre que tendra posiblemente un archivo duplicado
    for file in downloadPath.glob("*(*).*"):
        nameFile, extFile = file.stem, file.suffix
        nameFile = nameFile[:-4]
        # verifica si realmente es un duplicado, si lo es lo envia a la carpeta DuplicateFiles
        if Path(downloadPath / f"{nameFile}{extFile}").exists():
            countDupliFiles += 1
            shutil.move(file, Path(downloadPath / "DuplicateFiles"))
    #  retorna cantidad de archivos duplicados
    return countDupliFiles


def makeReadMe(downloadPath, nameFolders):
    # obtenemos el nombre de usuario
    user = str(Path.home()).split(os.sep)[2]
    readMeFile = open(downloadPath / "Readme.txt", "w")

    # escribe la plantilla del contenido del archivo
    readMeFile.write(
        f"Hola {user} acabo de ordenar tus archivos de la carpeta '{downloadPath.stem}':\n\n"
    )
    readMeFile.write("\t\tDatos de las carpetas creadas\n\n")

    # escribe la cantidad de archivos por cada carpeta
    for key,value in nameFolders.items():
        readMeFile.write(f"La carpeta {key} contiene {value} archivos.\n")
    readMeFile.write("\nCreado por R3-D4N")
    readMeFile.close()

if __name__=="__main__":
    try:
        downloadPath = findFolder(Path.home())
    except FileNotFoundError:
        exit(1)
    orderFiles(downloadPath)