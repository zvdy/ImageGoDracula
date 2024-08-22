import os
from flask import Flask, request, send_file
from ImageGoNord import GoNord

go_nord = GoNord()
go_nord.reset_palette()
go_nord.add_color_to_palette('#1f2335')  # Background
go_nord.add_color_to_palette('#24283b')  # Current Line
go_nord.add_color_to_palette('#292e42')  # Foreground
go_nord.add_color_to_palette('#3b4261')  # Comment
go_nord.add_color_to_palette('#414868')  # Darker Comment
go_nord.add_color_to_palette('#545c7e')  # Darker Foreground
go_nord.add_color_to_palette('#565f89')  # Lighter Comment
go_nord.add_color_to_palette('#737aa2')  # Lighter Foreground
go_nord.add_color_to_palette('#a9b1d6')  # Light Blue
go_nord.add_color_to_palette('#c0caf5')  # Lightest Blue
go_nord.add_color_to_palette('#394b70')  # Dark Blue
go_nord.add_color_to_palette('#3d59a1')  # Blue
go_nord.add_color_to_palette('#7aa2f7')  # Light Blue
go_nord.add_color_to_palette('#7dcfff')  # Cyan
go_nord.add_color_to_palette('#b4f9f8')  # Light Cyan
go_nord.add_color_to_palette('#bb9af7')  # Magenta
go_nord.add_color_to_palette('#9d7cd8')  # Light Magenta
go_nord.add_color_to_palette('#ff9e64')  # Orange
go_nord.add_color_to_palette('#ffc777')  # Light Orange
go_nord.add_color_to_palette('#c3e88d')  # Green
go_nord.add_color_to_palette('#4fd6be')  # Light Green
go_nord.add_color_to_palette('#41a6b5')  # Dark Cyan
go_nord.add_color_to_palette('#ff757f')  # Red
go_nord.add_color_to_palette('#c53b53')  # Dark Red
go_nord.add_color_to_palette('#ff007c')  # Pink

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert_image():
    # Check if the post request has the file part
    if 'file' not in request.files:
        return {'message': 'No file part in the request'}, 400

    file = request.files['file']

    # If user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return {'message': 'No selected file'}, 400

    try:
        # Save the uploaded file to disk
        filename = file.filename
        file_path = os.path.join(app.root_path, filename)
        file.save(file_path)
    except Exception as e:
        return {'message': f'Failed to save the file: {str(e)}'}, 500

    try:
        # Load the image and convert it
        image = go_nord.open_image(file_path)
        go_nord.convert_image(image, save_path=os.path.join(app.root_path, 'processed.jpg'))
    except Exception as e:
        return {'message': f'Failed to process the image: {str(e)}'}, 500

    try:
        # Return the converted image
        return send_file(os.path.join(app.root_path, 'processed.jpg'), mimetype='image/jpeg')
    except Exception as e:
        return {'message': f'Failed to send the processed image: {str(e)}'}, 500

if __name__ == '__main__':
    app.run(debug=True)