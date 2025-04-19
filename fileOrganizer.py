import os
from pathlib import Path
from sys import argv

from getTargetDir import get_target_dir, extensions_dict

PATH = None
# Diretórios que não serão movidos para a pasta Directories
EXCLUDED_DIRS = set(["Other","Directories", ".git", "__pycache__", "venv"] + [v.split("/")[0] for v in extensions_dict.values()])


def main():
    global PATH

    if len(argv) < 2:
        print("Uso do comando: <caminho para o diretório a ser organizado> <exclusões(opcional)>")
        print("A flag --move-dirs pode ser adicionada para mover os diretórios para a pasta Directories")
        exit()

    PATH = Path(argv[1])

    if not PATH.exists():
        print(f"O caminho {PATH} não existe")
        exit()

    move_dirs = "--move-dirs" in argv
        
    for x in PATH.iterdir():
        try:
            if x.name in argv[2:]:
                continue

            if x.is_file():
                organize_file(x)
            elif x.is_dir() and move_dirs:
                organize_dir(x)

        except Exception as e:
            print(f"Error: {e}")
            return
        
    print("Arquivos organizados com sucesso")

def organize_file(file):
    file_extension = file.name.rsplit(".", 1)[1].lower()
    target_dir = get_target_dir(file_extension)

    Path(PATH / target_dir).mkdir(parents=True, exist_ok=True)

    new_path = os.path.join(PATH, target_dir, file.name)
    file.rename(new_path)

# Move os diretórios para a pasta Directories
def organize_dir(dir):
    # Garante que nenhum diretório padrão seja movido
    if dir.name in EXCLUDED_DIRS:
        return
    
    target = PATH / "Directories"
    Path(target).mkdir(exist_ok=True)

    new_path = target / dir.name

    if new_path.exists():
        print(f"O Diretório {dir.name} ja existe dentro da pasta Directories")
        return

    dir.rename(new_path)

if __name__ == "__main__":
    main()