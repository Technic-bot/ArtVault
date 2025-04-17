import webbrowser 
import httpx
import sys

patreon_url = ( 
    "https://www.patreon.com/api/posts?"
      "include=campaign,"
          "access_rules,"
          "attachments,"
          "audio,"
          "audio_preview.null,"
          "images,"
          "media,"
          "native_video_insights,"
          "poll.choices,"
          "poll.current_user_responses.user,"
          "poll.current_user_responses.choice,"
          "poll.current_user_responses.poll,"
          "user,"
          "user_defined_tags,"
          "ti_checks"
      "&fields[campaign]=currency,"
          "show_audio_post_download_links,"
          "avatar_photo_url,"
          "avatar_photo_image_urls,"
          "earnings_visibility,"
          "is_nsfw,"
          "is_monthly,"
          "name,"
          "url"
      "&fields[post]=change_visibility_at,"
          "content,"
          # "comment_count,"
          # "commenter_count,"
          # "current_user_can_comment,"
          # "current_user_can_delete,"
          # "current_user_can_report,"
          # "current_user_can_view,"
          # "current_user_comment_disallowed_reason,"
          # "like_count,"
          # "current_user_has_liked,"
          # "embed,"
          # "impression_count,"
          # "insights_last_updated_at,"
          # "pledge_url,"
          # "thumbnail,"
          # "thumbnail_url,"
          # "is_paid,"
          # "upgrade_url,"
          # "was_posted_by_campaign_owner,"
          # "meta_image_url,"
          # "min_cents_pledged_to_view,"
          # "post_metadata,"
          "image,"
          "post_file,"
          "post_metadata,"
          "published_at,"
          "patreon_url,"
          "title,"
          "url,"
          "post_type,"
          # "preview_asset_type,"
          # "pls_one_liners_by_category,"
          # "teaser_text,"
          # "has_ti_violation,"
          # "moderation_status,"
          # "post_level_suspension_removal_date,"
          # "video_preview,"
          # "view_count"
      "&fields[post_tag]=tag_type%2Cvalue"
      "&fields[user]=image_url%2Cfull_name%2Curl"
      "&fields[access_rule]=access_rule_type%2Camount_cents"
      "&fields[media]=id%2Cimage_urls%2Cdownload_url%2Cmetadata%2Cfile_name"
      "&fields[native_video_insights]=average_view_duration%2Caverage_view_pct%2Chas_preview%2Cid%2Clast_updated_at%2Cnum_views%2Cpreview_views%2Cvideo_duration"
      "&filter[campaign_id]=145535"
      "&filter[contains_exclusive_posts]=true&filter[is_draft]=false"
      "&sort=-published_at&json-api-version=1.0"
      "&json-api-use-default-includes=false" )

print(patreon_url)
webbrowser.open_new_tab(patreon_url)

sys.exit(0)
r = httpx.get(patreon_url)
print(r.status_code)
if r.status_code == 200:
    data = r.json()
    print(data['data'][1]['attributes'])
else:
    print("denied")

