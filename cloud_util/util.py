import requests
import json
import base64
import os
from media import *


class CloudAPI(object):
    BASE_MEDIA_URL = "http://media.{0}.real.com"
    BASE_USER_URL = "https://users.{0}.real.com"
    BASE_EVENT_URL = "http://events.{0}.real.com"

    def __init__(self, env, token=None):
        self.env = env
        self.token = token

    @property
    def base_media_URL(self):
        return CloudAPI.BASE_MEDIA_URL.format(self.env)

    @property
    def base_user_URL(self):
        return CloudAPI.BASE_USER_URL.format(self.env)

    @property
    def base_event_URL(self):
        return CloudAPI.BASE_EVENT_URL.format(self.env)

    @property
    def base_upload_V2_URL(self):
        return self.base_media_URL + "/v2/{0}"

    @property
    def get_all_V1_URL(self):
        return self.base_media_URL + "/v1/media_info"

    @property
    def get_all_V2_URL(self):
        return self.base_media_URL + "/v2/media_info"

    @property
    def get_all_share_to_me_V2_URL(self):
        return self.get_all_V2_URL + "?results=shared_to_me"

    @property
    def get_all_file_V2_URL(self):
        return self.get_all_V2_URL + "?type=file"

    @property
    def get_all_collection_V2_URL(self):
        return self.get_all_V2_URL + "?type=collection"

    @property
    def login_user_V1_URL(self):
        return self.base_user_URL + "/v1/users/login"

    @property
    def upload_init_V2_URL(self):
        return self.base_upload_V2_URL + "/init"

    def upload_chunk_V2_URL(self, offset, upload_id):
        return self.base_upload_V2_URL + "?offset=" + str(offset) + "&upload_id=" + upload_id

    def upload_commit_V2_URL(self, upload_id):
        return self.base_upload_V2_URL + "/commit?upload_id=" + upload_id

    def default_headers(self):
        headers = {
            "Authorization": "RPCToken " + self.token,
            "X-RPC-AUTHORIZATION": "test:c2VjcmV0"
        }
        return headers

    def login(self, username, password):
        """ Return user token """

        userpass = username + ":" + password
        userpass_b64 = base64.encodestring(userpass).rstrip()
        user_auth = 'authorization:basic {0}'.format(userpass_b64.lower())
        user_auth_token = "Basic {0}".format(userpass_b64)
        headers = {
            "Authorization": "Basic " + userpass_b64,
            "X-RPC-AUTHORIZATION": "test:c2VjcmV0",
            "Content-Type": "application/json"
        }
        data = {
            "device_id": "1234567890",
            "device_user_agent": "your_device/your_app",
            "device_name": "RPC Mac test code",
            "tos_agree": True
        }

        response = requests.post(
            self.login_user_V1_URL, json=data, headers=headers)
        response.raise_for_status()
        self.token = response.json()['user_token']
        return self.token

    def get_all_file_V2(self):
        """ Return a media list """

        response = requests.get(
            self.get_all_file_V2_URL, headers=self.default_headers())
        response.raise_for_status()
        results = response.json()["results"]
        medias = []
        for i in results:
            title = i.get("title")
            file_name = i.get("file_name")
            media_id = i.get("media_id", "")
            media_type = i.get("media_type", "")
            media_owner_id = i.get("media_owner_id", "")
            source_id = i.get("source_id", "")
            m = Media(
                title, file_name, media_id, media_type, media_owner_id, source_id)
            medias.append(m)
        return medias

    def get_all_collection_V2(self):
        """ Return a collection list """

        response = requests.get(
            self.get_all_collection_V2_URL, headers=self.default_headers())
        response.raise_for_status()
        results = response.json()["results"]
        collects = []
        for i in results:
            title = i.get("title")
            media_id = i.get("media_id", "")
            media_owner_id = i.get("media_owner_id", "")
            default_video = i.get("default_video", False)
            c = Collection(title, media_id, media_owner_id, default_video)
            collects.append(c)
        return collects

    def get_title_of_shared_to_me_by_sender_V2(self, sender):
        """ Return shared video's title """

        response = requests.get(
            self.get_all_share_to_me_V2_URL, headers=self.default_headers())
        response.raise_for_status()
        results = response.json()["results"]
        media_id_filter_by_sender = [
            i.get("media_id") for i in results if i.get("sender").get("email") == sender]
        return [self.get_title_V1(i) for i in media_id_filter_by_sender]

    def get_title_V1(self, media_id):
        """ Return file's title by media id """

        response = requests.get(
            self.get_all_V1_URL + "/" + media_id, headers=self.default_headers())
        response.raise_for_status()
        return response.json()["title"]
    
    def get_media_id_V1(self, title):
        """ Return media id by title """
        return [i.media_id for i in self.get_all_file_V2() if i.title == title][0]

    def del_file_V1(self, media_id):
        """ Delete a media file from cloud by media id """

        response = requests.delete(self.get_all_V1_URL + "/root/items/" +
                                   media_id + "?action=delete_from_all", headers=self.default_headers())
        response.raise_for_status()

    def del_collection_V1(self, collection_id):
        """ Delete a collection from cloud by collection id """

        response = requests.delete(
            self.get_all_V1_URL + "/" + collection_id, headers=self.default_headers())
        response.raise_for_status()

    def del_all_file_V1(self):
        """ Delete all media files, including video and photo, from cloud """

        for i in self.get_all_file_V2():
            print "Deleting media file '%s'" % i.title
            self.del_file_V1(i.media_id)

    def del_all_collection_V1(self):
        """ Delete all collection from cloud """

        for i in self.get_all_collection_V2():
            print "Deleting collection '%s'" % i.title
            self.del_collection_V1(i.media_id)

    def del_all_V1(self):
        """ Delete all media and collection from cloud """

        self.del_all_file_V1()
        self.del_all_collection_V1()

    def upload_video_V2(self, file_fullpath):
        title = os.path.splitext(os.path.basename(file_fullpath))[0]
        self.upload_media_V2("media_files", file_fullpath, title)

    def upload_photo_V2(self, file_fullpath):
        title = os.path.splitext(os.path.basename(file_fullpath))[0]
        self.upload_media_V2("media_photos", file_fullpath, title)

    def upload_media_V2(self, media_type, file_fullpath, title):
        """ Upload a media file into cloud """

        file_name = os.path.basename(file_fullpath)
        headers = self.default_headers()
        headers["Content-Type"] = "application/json"
        data = {"file_name": file_name}

        # Get init upload id
        print "Uploading init"
        response = requests.post(
            self.upload_init_V2_URL.format(media_type), json=data, headers=headers)
        response.raise_for_status()
        upload_id = response.json()["upload_id"]

        # Chunk upload
        upload_file = open(file_fullpath, 'rb')
        offset = 0
        headers["Content-Type"] = "application/octet-stream"
        block_size = 1024000
        data = upload_file.read(block_size)
        while data:
            response = requests.post(self.upload_chunk_V2_URL(
                offset, upload_id).format(media_type), data=data, headers=headers)
            response.raise_for_status()
            offset = response.json()["offset"]
            upload_id = response.json()["upload_id"]
            print "Uploading chunk %d" % offset
            data = upload_file.read(block_size)

        # Commit
        print "Commit"
        headers["Content-Type"] = "application/json"
        data = {"file_name": file_name, "title": title}
        response = requests.post(self.upload_commit_V2_URL(
            upload_id).format(media_type), json=data, headers=headers)
        response.raise_for_status()

        print 'Uploading Done'

    def create_collection(self, title):
        """ Create a collection into cloud """

        headers = self.default_headers()
        headers["Content-Type"] = "application/json"
        data = {"title": title, "collection_ids": [], "type": "collection"}
        response = requests.post(
            self.get_all_V1_URL, json=data, headers=headers)
        response.raise_for_status()
        return response.json()["id"]

    def add_to_collection(self, collection_title, *media_titles):
        collection_id = [
            i.media_id for i in self.get_all_collection_V2() if i.title == collection_title]
        all_medias = self.get_all_file_V2()
        media_ids = []
        for i in media_titles:
            for media in all_medias:
                if i == media.title:
                    media_ids.append(media.media_id)

        headers = self.default_headers()
        headers["Content-Type"] = "application/json"
        data = {"ids": media_ids}
        response = requests.post(
            self.get_all_V1_URL + "/" + collection_id[0] + "/items", json=data, headers=headers)
        response.raise_for_status()
        
    def share_file_V1(self, title, share_to, share_note):
        share_url = self.get_all_V1_URL + "/" + self.get_media_id_V1(title) + "/share"
        data = {"recipients": [{"email": share_to }], "group_count": 1, "group_index": 1, "note": share_note}
        headers = self.default_headers()
        headers["Content-Type"] = "application/json"
        response = requests.post(share_url, json=data, headers=headers)
        response.raise_for_status()


if __name__ == "__main__":
    test = CloudAPI("macauto7@real.com", "123456", "int2")
    test.login()
    for i in test.get_all_file_V2():
        print str(i)