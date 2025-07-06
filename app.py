from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import glob

app = Flask(__name__)

DOWNLOAD_DIR = 'downloads'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']

    # Clean previous downloads
    for f in glob.glob(f"{DOWNLOAD_DIR}/*"):
        os.remove(f)

    ydl_opts = {
        'format': 'best',
        'outtmpl': f'{DOWNLOAD_DIR}/%(title)s.%(ext)s'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info_dict)

        return send_file(file_path, as_attachment=True)

    except Exception as e:
        return f"<h2>❌ Error: {e}</h2>"

if __name__ == '__main__':
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    app.run(debug=True)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
