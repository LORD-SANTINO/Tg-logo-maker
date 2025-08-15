from flask import Flask, request, send_file, render_template_string
from PIL import Image, ImageDraw
import io

app = Flask(__name__)

HTML_FORM = '''
    <h2>Telegram Logo Maker</h2>
    <form method="post">
        Logo Color (hex: #0088cc): <input type="text" name="color" value="#0088cc"><br>
        Image Size (px): <input type="number" name="size" value="256"><br>
        <input type="submit" value="Generate Logo">
    </form>
    {% if img_url %}
        <h3>Result:</h3>
        <img src="{{ img_url }}" />
    {% endif %}
'''

@app.route("/", methods=["GET", "POST"])
def home():
    img_url = None
    if request.method == "POST":
        color = request.form.get("color", "#0088cc")
        size = int(request.form.get("size", 256))
        
        # Create Telegram-like circle logo
        img = Image.new("RGBA", (size, size), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse([(0,0), (size,size)], fill=color)
        
        # Draw paper plane (stylized)
        plane_size = size // 2
        plane_points = [
            (size//2, size//4),
            (size//4, size*3//4),
            (size//2, size//2),
            (size*3//4, size*3//4)
        ]
        draw.polygon(plane_points, fill="white")

        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        img_bytes = buf.read()
        img_url = "data:image/png;base64," + img_bytes.encode("base64").decode()
        return render_template_string(HTML_FORM, img_url=img_url)
    return render_template_string(HTML_FORM, img_url=None)

@app.route("/generate", methods=["POST"])
def generate_logo():
    color = request.form.get("color", "#0088cc")
    size = int(request.form.get("size", 256))
    img = Image.new("RGBA", (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([(0,0), (size,size)], fill=color)
    plane_size = size // 2
    plane_points = [
        (size//2, size//4),
        (size//4, size*3//4),
        (size//2, size//2),
        (size*3//4, size*3//4)
    ]
    draw.polygon(plane_points, fill="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return send_file(buf, mimetype="image/png")

if __name__ == "__main__":
    app.run(debug=True)
  
