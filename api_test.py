import http.client

conn = http.client.HTTPSConnection("translateai.p.rapidapi.com")

payload = """{ "origin_language":"en","target_language":"bn","words_not_to_translate":"Earbuds; New York","paths_to_exclude":"product.media.img_desc","common_keys_to_exclude":"name; price","json_content":{"product":{"productName":"Wireless Earbuds","price":"$79 (Seventy Nine)","productDesc":"Wireless Earbuds from SoundTech, offering high-quality sound and a seamless connection experience. Perfect for on-the-go use, available for $79.","manufacturer":{"name":"SoundTech"},"supplier":{"name":"FastTech"},"media":{"img_url":"https://example.com/images/earbuds1.jpg","img_desc":"Not to translate"},"customer":{"name":"Alice Johnson","location":"New York, USA","feedback":"Great quality, easy to connect! Also the shop is inside to the New York city, which is great."}}}}"""

headers = {
    'x-rapidapi-key': "13de082c03mshbc25a4de77df86ep1f88efjsn0699b1f9175d",
    'x-rapidapi-host': "translateai.p.rapidapi.com",
    'Content-Type': "application/json"
}

conn.request("POST", "/google/translate/json", payload, headers)
res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))