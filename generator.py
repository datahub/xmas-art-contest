from glob import glob
from PIL import Image, ExifTags
from jinja2 import Template, Environment, FileSystemLoader

def main():

	env = Environment(loader=FileSystemLoader('templates'))
	image_template = env.get_template('gallery.html')
	
	images = glob("dist/media/*.JPG")
	image_list = []

	for image in images:

		img = Image.open(image)
		width, height = img.size
		tags = {
		    ExifTags.TAGS[k]: v
		    for k, v in img._getexif().items()
		    if k in ExifTags.TAGS
		}
		img.close()

		if (width / height) >= .8:
			orientation = 'landscape'
		else:
			orientation = 'portrait'

		image_list.append({
			"path": image,
			"desc": tags['ImageDescription'],
			"artist": tags['Artist'],
			"orientation": orientation
		})

	output = image_template.render(images=image_list)

	with open("dist/index.html", "wb") as f:
		f.write(output)


if __name__ == "__main__":
	main()