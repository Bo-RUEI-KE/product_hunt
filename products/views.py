from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required #登入權限監視
from .models import Animal
from django.utils import timezone #django抓時間的東西
from django.utils import timezone as datetime 
from django.core.files.storage import FileSystemStorage #可以把上船的檔案拿到一個地方存起來
#以下兩個import為json要用的
import json, os, sys
import requests
# Create your views here.


def product_list(request):
	try:
		animal =  Animal.objects
		#.values_list('animal_id','animal_variety','animal_sex','animal_old','animal_size','animal_color')
		return render(request, 'product_list.html',{'animal' :  animal} ) 

	except:
		return render(request, 'product_list.html',{'查詢錯誤' : '讀取錯誤'} ) 
	return render(request, 'product_list.html') 

@login_required    #只有登入才可以啟動這頁面，輸入網址也來不了
def publish(request):
	if request.method == 'GET':
		return render(request, 'publish.html') 
	elif request.method == 'POST':
		animal_id = request.POST['編號']
		animal_variety = request.POST['品種']
		animal_sex = request.POST['性別']
		animal_old = request.POST['歲數']
		animal_size = request.POST['大小']
		animal_color = request.POST['毛色']
		animal_from = request.POST['來源地']
		animal_health = request.POST['健康情況']
		animal_remark = request.POST['備註']
		try:
			animal_image = request.FILES['圖片']  #不知道為啥總是為空值 => 解決 : 在html form表單加入enctype="multipart/form-data"
				#以下可以存入檔案到mdeia裏頭 不過這邊我已經可以存了就不用這個了
			#FileStorage = FileSystemStorage()
			#FileStorage.save(animal_image.name, animal_image)
				#以下寫入資料庫
			DBanimal = Animal() #需要import
			DBanimal.animal_id = animal_id   #資料庫的animal_id = 使用者輸入的animal
			DBanimal.animal_variety = animal_variety
			DBanimal.animal_sex = animal_sex
			DBanimal.animal_old = animal_old
			DBanimal.animal_size = animal_size
			DBanimal.animal_color = animal_color
			DBanimal.animal_from = animal_from
			DBanimal.animal_health = animal_health	
			DBanimal.animal_remark = animal_remark
			DBanimal.animal_image = animal_image

			DBanimal.pub_data = timezone.datetime.now()     #datetime好像要拿掉比較好!?!?!!?
			DBanimal.animal_owner = request.user

			DBanimal.save()
			return redirect('主頁面')
		except Exception as err:
			return render(request, 'publish.html', {'錯誤':'請上傳圖片'})


def update_Json_To_DB(request):
	#以下為json塞入DB
	animal =  Animal.objects
	url = "http://163.29.157.32:8080/dataset/6a3e862a-e1cb-4e44-b989-d35609559463/resource/f4a75ba9-7721-4363-884d-c3820b0b917c/download/363b8cdd1d2742768af9e47ae54a09c2.json"
	data = requests.get(url).json()
	
	count = 0;
	for item in data:
		DBanimal = Animal() #需要import
		if count  ==10 :
			break
		DBanimal.animal_id = count +1   #=> 我的ID要用我們自己的? 還是用opendata的?
		DBanimal.animal_variety = item['Variety']
		DBanimal.animal_sex = item['Sex']
		DBanimal.animal_old = item['Age']
		DBanimal.animal_size = item['Build']
		DBanimal.animal_color = item['HairType']
		DBanimal.animal_from = item['Resettlement']
		DBanimal.animal_health = item['IsSterilization']
		DBanimal.animal_remark = item['Note'] 
		DBanimal.animal_image = item['ImageName']
		DBanimal.pub_data = timezone.now()
		DBanimal.animal_owner = request.user
		test = item['AcceptNum']
		if check_id(DBanimal.animal_id):
			DBanimal.save()
		count+=1
	return render(request, 'update.html',{'message' :  "成功"} )

def check_id(input_id):
	try:
		get_id =  Animal.objects.get(input_id)
		print(input_id,"可以存!")
		return False #有get的到代表已經有資料了
	except:
		print(input_id,"已經有了")
		return True
