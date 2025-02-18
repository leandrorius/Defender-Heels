import os
import subprocess
import sys
RED = '\033[31m'
RESET = '\033[0m'
GREEN = '\033[32m'
YELLOW = '\033[33m'

header = """
  ___       __             _           _  _         _    
 |   \ ___ / _|___ _ _  __| |___ _ _  | || |___ ___| |___
 | |) / -_)  _/ -_) ' \/ _` / -_) '_| | __ / -_) -_) (_-<
 |___/\___|_| \___|_||_\__,_\___|_|   |_||_\___\___|_/__/
                                                         
By leandrorius

"""

print (header)

def check_permissions(directory):
    # Verificar permissão de leitura tentando listar o conteúdo do diretório
    try:
        os.listdir(directory)
        can_read = True
    except PermissionError:
        can_read = False
    
    # Verificar permissão de escrita tentando criar um arquivo temporário
    try:
        testfile = os.path.join(directory, 'tempfile.tmp')
        with open(testfile, 'w') as f:
            pass
        os.remove(testfile)
        can_write = True
    except (PermissionError, IOError):
        can_write = False
    
    return can_read, can_write


def run_defender_scan(directory, recursion_level, log_file):
    # Função para obter todos os subdiretórios até o nível de recursividade especificado
    def get_subdirectories(dir_path, level):
        subdirs = []
        for root, dirs, files in os.walk(dir_path):
            current_level = root[len(dir_path):].count(os.sep)
            if current_level < level:
                subdirs.extend([os.path.join(root, d) for d in dirs])
            elif current_level == level:
                subdirs.append(root)
        return subdirs

    # Obter todos os subdiretórios até o nível de recursividade especificado
    directories_to_scan = get_subdirectories(directory, recursion_level)
    directories_to_scan.append(directory)  # Incluir o diretório principal

    # Abrir o arquivo de log para escrita
    with open(log_file, 'w') as log:
        # Executar a verificação para cada diretório
        for dir_to_scan in directories_to_scan:
            command = f'\"C:\\\\Program Files\\\\Windows Defender\\\\MpCmdRun.exe\" -Scan -ScanType 3 -File \"{dir_to_scan}\\|*\"'
            result = subprocess.run(command, capture_output=True, text=True, shell=True)
            
            # Escrever a saída no arquivo de log e imprimir na tela
            log.write(f"Scanning directory: {dir_to_scan}\n")
            log.write(result.stdout)
            log.write(result.stderr)
            log.write("\n\n")
            
            print(f"Scanning directory: {dir_to_scan}", flush=True)
            sys.stdout.write("\033[F")
            sys.stdout.write('\033[2K\033[1G')
            if "was skipped" in result.stdout:
                can_read, can_write = check_permissions(dir_to_scan)
                if can_read:
                    readable = GREEN+"YES"+RESET
                else:
                    readable = RED+"NO"+RESET
                
                if can_write:
                    writable = GREEN+"YES"+RESET
                else:
                    writable = RED+"NO"+RESET
                                

                print (f"{YELLOW}Directory {dir_to_scan} is in Defender exceptions{RESET} (Readable: {readable} | Writable: {writable} )")


            #print(result.stdout)
            #print(result.stderr)
            #print("\n")

# Exemplo de uso
directory = input("Enter the directory to scan (e.g. C:\): ")
recursion_level = int(input("Enter the recursion level: "))
log_file = "defender_scan_log.txt"

run_defender_scan(directory, recursion_level, log_file)
