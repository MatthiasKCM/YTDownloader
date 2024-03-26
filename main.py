from pytube import YouTube
from flask import Flask, render_template, request

app = Flask(__name__)

#Flask-dekorator, verwandelt Python-Funktion in Flask-Anzeigefunktion um, Rückgabe der Funktion ist HTTP Response
@app.route('/', methods=['GET', 'POST'])
def home():
    message = ''
    if request.method == 'POST': # POST, da download

        url = request.form.get('url') # URL holen aus Formular
        yt = YouTube(url) # YouTube-Objekt mit der Video-URL initialisieren
        resolution = request.form.get('resolution') # Auflösung holen aus Formular, 720p oder 1080p
        file_path = '/Users/matthiasp/Desktop/YT downloads' # Speicherort Streams

        try:
            if resolution == '720p':
                stream = yt.streams.filter(progressive=True, file_extension='mp4', resolution='720p').first()
                if stream:
                    stream.download(output_path=file_path)
                    message = '720p Download erfolgreich!'
                else:
                    message = 'Fehler: Kein passender 720p Stream gefunden.'

            elif resolution == '1080p':
                # Liste aller verfügbaren Streams für das spezielle Video
                for stream in yt.streams:
                    print(stream)
                # Prüfe zuerst auf progressive Streams für 1080p, diese sind selten, aber die beste Option
                stream = yt.streams.filter(progressive=True, file_extension='mp4', resolution='1080p').first()
                if stream:
                    stream.download(output_path=file_path)
                    message = '1080p Download erfolgreich!'
                else:
                    # Kein progressiver 1080p Stream, lade beste Video- und Audio-Streams separat
                    streamVideo = yt.streams.filter( progressive=False, resolution='1080p').first()
                    streamAudio = yt.streams.filter(only_audio=True).first()

                    if streamVideo and streamAudio:
                        streamVideo.download(output_path=file_path, filename_prefix="Video_")
                        streamAudio.download(output_path=file_path, filename_prefix="Audio_")
                        message = '1080p Video und Audio separat heruntergeladen. Bitte manuell kombinieren.'
                    else:
                        message = 'Fehler: Keine passenden 1080p Video- oder Audio-Streams gefunden.'
        except Exception as e:
            message = f'Fehler: {e}'

    return render_template('index.html', message=message)  # Ein einzelnes return-Statement


if __name__ == '__main__':
    app.run(debug=True) # Startet Anwendung in Debug-Modus -> automatisches Neuladen, bei Codeänderung, Fehlermeldungen etc.




