import sys
import util
import time
from requests.exceptions import HTTPError


def print_help_info():
    print "--Help for cloud_util.py--"
    print "Usage: python cloud_util.py -t token [options]"
    print "Options:"
    print "--login -u username -p password -e env: Return token"
    print "--cleanup: Cleanup all contents and collections from cloud"
    print "--uploadvideo file_path: Upload videos to cloud"
    print "--uploadimage image_path: Upload images to cloud"
    print "--check title: Check if a media file exist in cloud"
    print "--createcollection name: Create a collection to cloud"
    print ""
    print "--Examples--"
    print "Login and return token"
    print "python cloud_util.py --login -u testaccount@real.com -p 123456 -e int"
    print "Cleanup all contents and collections from cloud:"
    print "python cloud_util.py -t token -e env --cleanup\n"
    print "Upload videos to cloud:"
    print "python cloud_util.py -t token -e env --uploadvideo \"/Users/real/testcontent/test1.mp4,/Users/real/testcontent/test2.mp4\"\n"
    print "Upload images to cloud:"
    print "python cloud_util.py -t token -e env --uploadimage /Users/real/testcontent/test2.png\n"
    print "Create a collection to cloud:"
    print "python cloud_util.py -t token -e env --createcollection mycollection\n"
    print "Check if video or photo exist in cloud:"
    print "python cloud_util.py -t token -e env --check test1\n"
    print "Check if a collection exist in cloud:"
    print "python cloud_util.py -t token -e env --checkcollection test1\n"
    print "Add a media into collection:"
    print "python cloud_util.py -t token -e env --addtocollection collection_name media_title1 media_title2\n"


if len(sys.argv) < 6:
    print_help_info()
    sys.exit(0)

if len(sys.argv) == 8:
    if sys.argv[1] == "--login":
        username = sys.argv[3]
        password = sys.argv[5]
        env = sys.argv[7]
        cloud_api = util.CloudAPI(env)
        print cloud_api.login(username, password)
        sys.exit(0)

if sys.argv[1] != "-t" or sys.argv[3] != "-e":
    print_help_info()
    sys.exit(0)

token = sys.argv[2]
env = sys.argv[4]

cloud_api = util.CloudAPI(env, token)

def upload_video_clips_with_request_control(*videos):
    video_wait_time_dic = {}
    for v in videos:
        # default wait time for uploading video clip is 10 sec
        video_wait_time_dic[v] = 10
    i = 0
    while(i < len(video_wait_time_dic)):
        video_path = video_wait_time_dic.keys()[i]
        sleep_time = video_wait_time_dic.values()[i]
        print "Uploading video '%s'" % video_path
        try:
            time.sleep(sleep_time)
            cloud_api.upload_video_V2(video_path)
            i += 1
        except HTTPError as ex:
            if ex.response.status_code == 429:
                if sleep_time > 30:
                    raise
                print "Get 429 too many requests error, will retry"
                video_wait_time_dic[video_path] += 10
            else:
                raise


if sys.argv[-1] == "--cleanup":
    print "Start to cleanup all contents"
    try:
        cloud_api.del_all_V1()
        sys.exit(0)
    except HTTPError as ex:
        print ex, ex.args
        sys.exit(1)

if sys.argv[5] == "--uploadvideo":
    print "Start to upload videos to cloud"
    try:
        videos = sys.argv[-1].split(",")
        upload_video_clips_with_request_control(*videos)
        sys.exit(0)
    except Exception as ex:
        print ex
        sys.exit(1)

if sys.argv[5] == "--uploadimage":
    print "Start to upload images to cloud"
    try:
        photos = sys.argv[-1].split(",")
        for p in photos:
            print "Uploading image '%s'" % p
            cloud_api.upload_photo_V2(p)
            time.sleep(10)
        sys.exit(0)
    except HTTPError as ex:
        print ex, ex.args
        sys.exit(1)

if sys.argv[5] == "--createcollection":
    print "Create a collection to cloud"
    try:
        collection_id = cloud_api.create_collection(sys.argv[6])
        print "Collection id is '%s'" % collection_id
        sys.exit(0)
    except HTTPError as ex:
        print ex, ex.args
        sys.exit(1)

if sys.argv[5] == "--check":
    print "Check if file '%s' exist in cloud" % sys.argv[6]
    try:
        medias = cloud_api.get_all_file_V2()
        ret = [i for i in medias if i.title == sys.argv[6]]
        if len(ret) >= 1:
            print "Found '%s' in cloud" % sys.argv[6]
            sys.exit(0)
        else:
            print "Doesn't exist"
            sys.exit(1)
    except HTTPError as ex:
        print ex, ex.args
        sys.exit(1)

if sys.argv[5] == "--checkcollection":
    print "Check if collection '%s' exist in cloud" % sys.argv[6]
    try:
        albums = cloud_api.get_all_collection_V2()
        ret = [i for i in albums if i.title == sys.argv[6]]
        if len(ret) >= 1:
            print "Found '%s' in cloud" % sys.argv[6]
            sys.exit(0)
        else:
            print "Doesn't exist"
            sys.exit(1)
    except HTTPError as ex:
        print ex, ex.args
        sys.exit(1)

if sys.argv[5] == "--addtocollection":
    print "Add media into collection '%s'" % sys.argv[6]
    try:
        media_titles = sys.argv[7:]
        cloud_api.add_to_collection(sys.argv[6], *media_titles)
    except HTTPError as ex:
        print ex, ex.args
        sys.exit(1)
