#!/usr/bin/env python2.7
"""
Written by Lucas Ou-Yang. MIT licensed. Copyright 2014.
"""
import re
from settings import google_username, google_password
from gdata.youtube import service

def comments_generator(client, video_id):
    """
    Directly uses google youtube api to build a generator of comments
    for a particular video. We traverse the comments list via the
    next_link calls. We stop after the first failure.
    """
    try:
        comment_feed = client.GetYouTubeVideoCommentFeed(video_id=video_id)
    except Exception, e:
        print str(e)
        return

    while comment_feed is not None:
        for comment in comment_feed.entry:
             yield comment

        next_link = comment_feed.GetNextLink()

        if next_link is None:
             comment_feed = None
        else:
            try:
                comment_feed = client.GetYouTubeVideoCommentFeed(next_link.href)
            except Exception, e:
                print 'Custom exception', str(e)
                comment_feed = None
                break

def get_yt_comments(video_id):
    """
    Extracts out the youtube comments for a particular video in an
    array form. We only note the comment body, not author name, etc.

    There is a start_token glitch in the youtube api which only allows
    us to ge to around comment #600 per video so we stop at 550.

    Also, the standard google api restriction is 1000 most recent comments
    per video anyways. We auth with a custom google application key.
    """
    API_LIMIT = 550

    client = service.YouTubeService()
    client.ClientLogin(google_username, google_password)

    # import codecs
    # f = codecs.open('comments.txt', 'w', 'utf8')
    count = 1
    ret_comments = []

    for comment in comments_generator(client, video_id):
        if not comment.content.text:
            continue
        # author_name = comment.author[0].name.text
        text = comment.content.text.decode('utf8')
        ret_comments.append(text)

        count += 1
        if count == API_LIMIT:
            break
    return ret_comments

def trim_str_num(s):
    """
    Takes a string in the form of a yt timestamp, \d\d:\d\d, and
    chunks out the whitepace or un-wanted words surrounding it.
    """
    timestamp_arr = [c for c in s if c.isdigit() or c == ':']
    return ''.join(timestamp_arr)

def get_timestamp_list(video_id):
    """
    Returns a sorted list of all timestamps present in any comment
    of this selected youtube video.
    """
    vtime_regex = re.compile(u'[\d\s\w]{0,1}\d:\d\d')
    comments = get_yt_comments(video_id=video_id)
    times = []
    for comment in comments:
        cur_times = vtime_regex.findall(comment)
        clean_times = [trim_str_num(t) for t in cur_times]
        print 'clean_times', clean_times
        times += clean_times # More pythonic than .extends(..)

    print 'The times are:', times
    return times

if __name__ == '__main__':
    timestamps = get_timestamp_list(video_id='p5HXQ1HFDgA')
