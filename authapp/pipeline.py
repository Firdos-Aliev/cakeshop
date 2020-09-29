import requests

def fill_user_model(backend, user, response, *args, **kwargs):
    if backend.name == "google-oauth2":
        if "picture" in response.keys():
            user.img = response["picture"]
            #url_img = response["picture"]
            #user.img = url_img
            #r = requests.get(url_img)
            #if r.status_code == requests.codes.ok:
                #img_path = '/media/user_img/1.png'
                #out = open(img_path, "wb")
                #out.write(r.content)
                #out.close()
            #user.img = '/user_img/' + url_img + '.png'

    user.save()
