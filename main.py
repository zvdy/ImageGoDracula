import os
from flask import Flask, request, send_file
from ImageGoNord import GoNord

go_nord = GoNord()
go_nord.reset_palette()
go_nord.add_color_to_palette('#1a1b26')
go_nord.add_color_to_palette('#24283b')
go_nord.add_color_to_palette('#cfc9c2')
go_nord.add_color_to_palette('#565f89')
go_nord.add_color_to_palette('#bb9af7')
go_nord.add_color_to_palette('#7dcfff')
go_nord.add_color_to_palette('#9ece6a')
go_nord.add_color_to_palette('#e0af68')
go_nord.add_color_to_palette('#f7768e')
go_nord.add_color_to_palette('#8c4351')
go_nord.add_color_to_palette('#ff9e64')

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