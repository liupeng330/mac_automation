from sikuli import *
import helper

# Get width and heigth of screen by applescripts
width_of_screen = helper.get_bounds_of_screen()[0]
height_of_screen = helper.get_bounds_of_screen()[1]

# Height of top menu bar
height_of_top_menu_bar = 24

# Get height of dock by applescripts
height_of_dock = helper.get_height_of_dock()

# Region of screen, without top menu bar and dock
region = Region(0, height_of_top_menu_bar, width_of_screen,
                height_of_screen - height_of_top_menu_bar - height_of_dock)
print "region size is ({0}, {1}, {2}, {3})".format(region.x, region.y, region.w, region.h)

# Region for top menu bar region
top_menu_bar_region = Region(
    0, 0, helper.get_bounds_of_screen()[0], height_of_top_menu_bar)

# First launch realtimes
first_launch_warning_dialog = "first_launch_warning_dialog.png"
first_lannch_warning_dialog_open_button = "first_lannch_warning_dialog_open_button.png"

# Sign in panel
sign_in_button = "sign_in_button.png"
username_textbox = "username_textbox.png"
username_textbox_with_last_account = "username_textbox_with_last_account.png"
password_textbox = "password_textbox.png"
sign_in_button2 = "sign_in_button2.png"
sign_in_get_started = "sign_in_get_started.png"
welcome_page_recommended = "welcome_page_recommended.png"
welcome_page_get_started = "welcome_page_get_started.png"

# RT main window
# >>>Top bar:
account_setting_button_top_bar = "account_setting_button_top_bar.png"
has_signed_in_rt_top_bar = account_setting_button_top_bar
sign_out_button_in_account_setting_button_top_bar = "sign_out_button_in_account_setting_button_top_bar.png"
# >>>Top tab bar:
content_location_switcher_all_selected = "content_location_switcher_all_selected.png"
content_location_switcher_cloud_selected = "content_location_switcher_cloud_selected.png"
content_location_switcher_mymac_selected = "content_location_switcher_mymac_selected.png"
content_location_switcher_watched_selected = "content_location_switcher_watched_selected.png"
content_location_switcher_uploaded_selected = "content_location_switcher_uploaded_selected.png"
content_location_switcher_stories_suggested_selected = "content_location_switcher_stories_suggested_selected.png"
content_location_switcher_stories_saved_selected = "content_location_switcher_stories_saved_selected.png"
content_location_switcher_stories_cloud_selected = "content_location_switcher_stories_cloud_selected.png"
share_everyone_item = "share_everyone_item.png"
share_by_me_dropdown_list_item = "share_by_me_dropdown_list_item.png"
# >>>Navigation bar:
photos_and_videos_button_selected = "photos_and_videos_button_selected.png"
photos_and_videos_button_unselected = "photos_and_videos_button_unselected.png"
my_albums_button_selected = "my_albums_button_selected.png"
my_albums_button_unselected = "my_albums_button_unselected.png"
stories_button_selected = "stories_button_selected.png"
stories_button_unselected = "stories_button_unselected.png"
sharing_button_selected = Pattern("sharing_button_selected.png").similar(0.50)
sharing_button_unselected = "sharing_button_unselected.png"
recent_activity_selected = "recent_activity_selected.png"
recent_activity_unselected = "recent_activity_unselected.png"
# >>>Bottom bar:
transfers_button = "transfers_button.png"
transfers_button_in_progress = "transfers_button_in_progress.png"
plus_button = "plus_button.png"

# System tray
system_tray_icon = Pattern("system_tray_icon.png").similar(0.55)
system_tray_signout = "system_tray_signout.png"
system_tray_quit = "system_tray_quit.png"
system_tray_signin_10_9 = "system_tray_signin_10_9.png"
system_tray_signin_10_10 = "system_tray_signin_10_10.png"
system_tray_pause = "system_tray_pause.png"
system_tray_resume = "system_tray_resume.png"

# Items in view
# >>>Items in libary view:
no_photos_or_videos = "no_photos_or_videos.png"
download_video_item = "download_video_item.png"
upload_video_item = "upload_item.png"
upload_photo_item = "upload_photo_item.png"
rename_video_item = "rename_video_item.png"
rename_text_item = "rename_text_item.png"
rename_collection_item = "rename_collection_item.png"
rename_collection_title = "rename_collection_title.png"
newname_collection_title = "newname_collection_title.png"
share_video_item1 = "share_video_item1.png"
share_video_item2 = download_video_item
share_photo_item1 = "share_photo_item1.png"
share_photo_item2 = "share_photo_item2.png"
play_local_item = "play_local_item.png"
play_cloud_local_item = "play_cloud_local_item.png"
media_scan_item = "media_scan_item.png"
play_in_player_item = "play_in_player_item.png"

# >>>Stories
suggested_story_icon = "suggested_story_icon.png"
story_item = "story_item.png"
story_save_button = "story_save_button.png"
story_play_nums = ["pre_roll_story.png", "story_play_num_1.png", "story_play_num_2.png", "story_play_num_3.png", "post_roll_story.png"]
story_play_items = ["story_play_item_1.png", "story_play_item_2.png", "story_play_item_3.png"]

# >>>Play with slideshow 
slideshow_play_items = ["slideshow_play_item1.png", "slideshow_play_item2.png", "slideshow_play_item3.png"]
slideshow_left_arrows_button = "slideshow_left_arrows_button.png"
slideshow_album_item = "slideshow_album_item.png"

# >>>Items in gallery view:
upload_photo_item_in_gallery_view = "upload_photo_item_in_gallery_view.png"
rename_video_item_in_gallery_view = "rename_video_item_in_gallery_view.png"
newname_video_item_in_gallery_view = "newname_video_item_in_gallery_view.png"
# >>>Items in finder, icon view, default icon size:
upload_photo_item_in_finder_icon_view = "upload_photo_item_in_finder_icon_view.png"
upload_video_item_in_finder_icon_view = "upload_video_item_in_finder_icon_view.png"
upload_folder_item_in_finder_icon_view = "upload_folder_item_in_finder_icon_view.png"
# >>>Items in album view:
test_album_item = download_video_item
shared_album_item = "shared_album_item.png"
# >>>Items in sharing library view:
new_shared_media_item = shared_album_item
shared_media_item = download_video_item

# Playback mode
play_in_separate_window_button = "play_in_separate_window_button.png"
play_as_slideshow_button = "play_as_slideshow.png"
exit_gallery_button = "exit_gallery_button.png"
pause_button = "pause_button.png"
play_button = Pattern("play_button.png").similar(0.81)
# >>>Separate window:
play_item_title_in_separate_window = "play_item_title_in_separate_window.png"
share_button_in_separate_window = "share_button_in_separate_window.png"

# Player window
upload_button_in_player_window = "upload_button_in_player_window.png"
download_button_in_player_window = "download_button_in_player_window.png"

# Delete radio button
delete_from_this_mac_radio_button = Pattern(
    "delete_from_this_mac_radio_button.png").exact()

# Select current view
select_current_view = Pattern("select_current_view.png").targetOffset(0,46)

# Add to album dialog
new_album_dialog_button = "new_album_dialog_button.png"
album_item_dialog_icon = "album_item_dialog_icon.png"

# Share dialog
enter_names_text_box =  "enter_names_text_box.png"
write_something_text_box = "write_something_text_box.png"
share_button_of_share_dialog = "share_button_of_share_dialog.png"

share_success_text = "share_success_text.png"
close_button_of_share_dialog = "close_button_of_share_dialog.png"

# Folder upload to cloud dialog
folder_upload_to_cloud_dialog = Pattern("folder_upload_to_cloud_dialog.png").similar(0.56)

# Transfer dialog
transfer_dialog = "transfer_dialog.png"
transfer_dialog_clear_completed_button = "transfer_dialog_clear_completed_button.png"
transfer_dialog_resume_button = Pattern("transfer_dialog_resume_button.png").similar(0.73)
transfer_dialog_cancel_button = Pattern("transfer_dialog_cancel_button.png").similar(0.87)
transfer_dialog_pause_button = Pattern("transfer_dialog_pause_button.png").similar(0.85)
transfer_dialog_no_item = "transfer_dialog_no_item.png"

# Like/unlike button
like_button = "like_button.png"
unlike_button = "unlike_button.png"
one_like_message = "one_like_message.png"

share_group_button = "share_group_button.png"
share_group_item = "share_group_item.png"
back_button = "back_button.png"

# Notification
download_complete_notification_10_10 = "download_complete_notification_10_10.png"
download_complete_notification_10_9 = "download_complete_notification_10_9.png"
new_photo_found_notification_10_10 = "new_photo_found_notification_10_10.png"
new_photo_found_notification_10_9 = "new_photo_found_notification_10_9.png"
upload_complete_notification_10_10 = "upload_complete_notification_10_10.png"
upload_complete_notification_10_9 = "upload_complete_notification_10_9.png"
no_network_notification = Pattern("no_network_notification.png").similar(0.60)