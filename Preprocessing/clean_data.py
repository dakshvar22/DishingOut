import json
from dishingOut.NPChunking.NPChunker import NPChunker

with open('result.json','r') as f:
	data = json.load(f)
	
for restaurant in data:
	dishes = restaurant['dishes']
	for dish in dishes:
		for i in xrange(len(dishes[dish])):
			comment = dishes[dish][i]
			comment = comment.replace('&amp;','and')
			comment = comment.replace('&nbsp;',' ')
			comment = comment.replace('&rsquo;',"'")
			comment = comment.replace('&ndash;',"-")
			comment = comment.replace('&hellip;',".")
			comment = comment.replace('&quot;','"')
			comment = comment.replace('&lsquo;',"'")
			comment = comment.replace('&eacute;',"e")
			dishes[dish][i]=comment

with open('final_data.json','w') as f:
	data = json.dump(data, f, indent = 2)
