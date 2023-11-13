import os
from flask import Flask, request, send_file
from ImageGoNord import GoNord

go_nord = GoNord()
go_nord.reset_palette()
go_nord.add_color_to_palette('#282a36')
go_nord.add_color_to_palette('#44475a')
go_nord.add_color_to_palette('#F8F8F2')
go_nord.add_color_to_palette('#6272A4')
go_nord.add_color_to_palette('#BD93F9')
go_nord.add_color_to_palette('#8BE9FD')
go_nord.add_color_to_palette('#50FA7B')
go_nord.add_color_to_palette('#FFB86C')
go_nord.add_color_to_palette('#FF79C6')
go_nord.add_color_to_palette('#FF5555')
go_nord.add_color_to_palette('#F1FA8C')

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert_image():
    # Check if the post request has the file part
    if 'file' not in request.files:
        return {'message': 'No file part'}, 400

    file = request.files['file']

    # If user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return {'message': 'No selected file'}, 400

    # Save the uploaded file to disk
    filename = file.filename
    file.save(os.path.join(app.root_path, filename))

    # Load the image and convert it
    image = go_nord.open_image(os.path.join(app.root_path, filename))
    go_nord.convert_image(image, save_path=os.path.join(app.root_path, 'processed.jpg'))

    # Return the converted image
    return send_file(os.path.join(app.root_path, 'processed.jpg'), mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)