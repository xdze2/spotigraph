import requests
import base64

r = requests.get("https://i.scdn.co/image/ec1fb7127168dbaa962404031409c5a293b95ec6")

# print(r.content)


base64_encoded_data = base64.b64encode(r.content)
base64_message = base64_encoded_data.decode('utf-8')

print(base64_message)



html = f'<img src="data:image/jpg;base64,{base64_message}">'

with open('yo.html', 'w') as f:
    f.write(html)
