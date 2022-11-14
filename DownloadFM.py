from pathlib import Path, PurePath
import os, shutil


def findFolder(rutaHome):
    listaNames = [
        "Descargas",
        "Downloads",
    ]

    # crea lista con las posibles rutas a la carpeta de descargas
    posiblesRutas = [PurePath.joinpath(rutaHome, name) for name in listaNames]
    for folder in rutaHome.iterdir():
        # envia la ruta correcta
        if folder in posiblesRutas:
            return folder
    raise FileNotFoundError


def orderFiles(downloadPath):
    extensions = {
        "TextFiles": [".docx", ".doc", ".pdf", ".txt", ".xlsx", ".pptx"],
        "AudioFiles": [".mp3", ".wma", ".wav"],
        "VideoFiles": [".avi", ".mp4", ".mkv", ".wpl", ".mov"],
        "ImageFiles": [".jpeg", ".jpg", ".png", ".ico", ".gif", ".svg"],
        "ProgramFiles": [".exe", ".bin", ".msi", ".dll", ".iso"],
        "CompressedFiles": [".zip", ".rar", ".7z", ".gz"],
    }

    countFiles = {
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
    countFiles["DuplicateFiles"] = moveDuplicatefiles(downloadPath)

    # analiza cada archivo de la carpeta y la almacena en su carpeta correcta
    for file in downloadPath.iterdir():
        if file.is_dir():
            continue
        try:
            for fileName, extensionList in extensions.items():
                if file.suffix in extensionList:
                    destination = downloadPath / fileName
                    shutil.move(file, destination)
                    countFiles[fileName] += 1
                    break
            else:
                destination = downloadPath / "OtherFiles"
                shutil.move(file, destination)
                countFiles["OtherFiles"] += 1
        except:
            print("ya existe")
    makeReadMe(downloadPath, countFiles)


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


def makeReadMe(downloadPath, countFiles):
    # obtenemos el nombre de usuario
    user = str(Path.home()).split(os.sep)[2]
    with open(downloadPath / "README.txt", "a") as readMeFile:
        # escribe la plantilla del contenido del archivo
        readMeFile.write(
            f"Hola {user} acabo de ordenar tus archivos de la carpeta '{downloadPath.stem}':\n\n"
        )
        readMeFile.write("\t\tDatos de las carpetas creadas\n\n")

        # escribe la cantidad de archivos por cada carpeta
        for key, value in countFiles.items():
            readMeFile.write(f"La carpeta {key} contiene {value} archivos.\n")
        readMeFile.write("\nBy R3-D4N")


if __name__ == "__main__":
    try:
        downloadPath = findFolder(Path.home())
    except FileNotFoundError:
        exit(1)
    orderFiles(downloadPath)