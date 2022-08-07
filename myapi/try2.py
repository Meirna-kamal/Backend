import requests

url = 'http://127.0.0.1:8000/fileUploadApi/'
# link=r'C:\Users\10\Desktop\Squats'
link={'path':r'C:\Users\10\Desktop\Squats','name':'Anything.mp4'}
x = requests.post(url,params=link)

print(x.json())