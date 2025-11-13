from PIL import Image
import pytesseract

# 打开图片
file = r'D:\15.png'
image = Image.open(file)

# 识别文字（默认英文）
text = pytesseract.image_to_string(image)
print(text)