from PIL import Image, ImageDraw, ImageFont

# Создаем новое изображение
image = Image.new('RGB', (800, 600), color = (255, 255, 255))

# Добавляем текст на изображение
draw = ImageDraw.Draw(image)
font = ImageFont.truetype('arial.ttf', 36)
draw.text((10, 10), "Ваш текст здесь", fill=(0, 0, 0), font=font)

# Сохраняем изображение
image.save('чек.jpg')
