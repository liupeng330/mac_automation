
class Media(object):

    def __init__(self, title, file_name, media_id, media_type, media_owner_id="", source_id=""):
        self.title = title
        self.file_name = file_name
        self.media_id = media_id
        self.media_type = media_type
        self.media_owner_id = media_owner_id
        self.source_id = source_id

    def __str__(self):
        return "\
title: %s\n\
file_name: %s\n\
media_id: %s\n\
media_type: %s\n\
media_owner_id: %s\n\
source_id: %s\n" \
            % (self.title,
               self.file_name,
               self.media_id,
               self.media_type,
               self.media_owner_id,
               self.source_id)


class Collection(object):

    def __init__(self, title, media_id, media_owner_id="", default_video=False):
        self.title = title
        self.media_id = media_id
        self.media_owner_id = media_owner_id
        self.default_video = default_video

    def __str__(self):
        return "\
title: %s\n\
media_id: %s\n\
media_owner_id: %s\n\
default_video: %s\n" \
            % (self.title,
               self.media_id,
               self.media_owner_id,
               self.default_video)
