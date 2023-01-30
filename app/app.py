import os
import shutil
import glob
from flask import Flask, request
from pytube import YouTube
from ftplib import FTP
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/download')
def download():
    url = request.args.get('url', default = '', type = str)

    # Limpiar la carpeta de descargas
    shutil.rmtree('./downloads')

    # Descargar el archivo
    yt = YouTube(url)
    yt.streams.filter(only_audio=True).first().download('./downloads')

    # Obtener el nombre del archivo descargado
    file_name = glob.glob('./downloads/*')[0]  

    # Abrir la conexion a FTP server
    ftp_host = os.getenv('FTP_HOST')
    ftp_port = os.getenv('FTP_PORT')
    ftp_user = os.getenv('FTP_USER')
    ftp_pass = os.getenv('FTP_PASS')
    ftp_dir = os.getenv('FTP_DIR')

    ftp = FTP()
    ftp.connect(ftp_host, int(ftp_port))
    ftp.login(ftp_user, ftp_pass)

    # Abrir el archivo descargado
    with open(file_name, 'rb') as audio_file:
        # Copiar el archivo al servidor ftp
        ftp.storbinary('STOR ' + '/' + ftp_dir + '/' + file_name.replace('./downloads/', ''), audio_file)

    # Cerar la conexion a ftp 
    ftp.close()

    return files

@app.route('/files')
def files(): 
    # Obtener las variables de entorno
    ftp_host = os.getenv('FTP_HOST')
    ftp_port = os.getenv('FTP_PORT')
    ftp_user = os.getenv('FTP_USER')
    ftp_pass = os.getenv('FTP_PASS')
    ftp_dir = os.getenv('FTP_DIR')

     # Abrir la conexion a FTP server
    ftp = FTP()
    ftp.connect(ftp_host, int(ftp_port))
    ftp.login(ftp_user, ftp_pass)

     # Navegar al directorio compartido
    ftp.cwd('files')

    # Recuperar los archivos en ftp
    files = []
    ftp.dir(files.append)

    ftp.close()

    return files

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
