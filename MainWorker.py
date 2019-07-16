# from DB.Models import User
from Instagram import Instantiator, PostWorker
from Instagram.Util import Tag
from util import time as timeutil
import datetime
import time

THRESHOLD = 18

tagsBody = """#photography #photographylovers #photographysouls #photographyeveryday #photographyislife #photographylover #photographyislifee #photographylife #photographyart #photographyoftheday #photographyy #photographylove #photographyaddict #photographyskills #photographybook #photographyprops #photographydaily #photographyisart #photographyaccount #photographystudio #photographyday #photographynature #photographysoul #photographystudent #photographyworkshop #photographyindonesia #photographyblog #photographyig #photographybusiness #photography101"""

timings = []


def main():
    api = Instantiator.getApiInstance("your_instagram_username", "your_instagram_password")

    customCaptionContent = """
    Did you like this post? Tag the ones who should try this!
    """

    tags = Tag.parseTagsBodyToList(tagsBody)
    storageDir = "./storage/media"

    # user = User.get(User.username == "heyitsvaishnav")

    # PostWorker.worker(api, storageDir, customCaptionContent, tags, user)
    return PostWorker.worker(api, storageDir, customCaptionContent, tags)


def generate_timing_strings(date_time, threshold, hours_limit=23, minuites_limit=60, next_day_start_barricade=False):
    newdatetimes = sorted([timing for timing in
                           timeutil.generate_timings(date_time, threshold, hours_limit, minuites_limit,
                                                     next_day_start_barricade)])
    timings = [timeutil.get_string_time(iter) for iter in newdatetimes]
    return timings


def log_timings(timings, manual_start=False, date_time=datetime.datetime.now()):
    with open("./storage/logs/posts-timings-{}.txt".format(date_time.strftime("%d-%m-%y")), "a+") as posts_log:
        posts_log.write(
            "\nTimings of \"{}\" - {} ({})".format(datetime.datetime.now().strftime("%d/%m/%y"), str(timings),
                                                   "manual" if manual_start else "automatic"))
        posts_log.close()


def log_posted(date_time, post_id):
    with open("./storage/logs/posted-log-{}.txt".format(date_time.strftime("%d-%m-%y")), "a+") as post_log:
        post_log.write("\nPosted post-pk \"{}\" at: {}".format(post_id, str(date_time)))
        post_log.close()


def show_user_terminal_warning():
    print(
        """
        -------------------------------------------------    
        \"DO NOT CLOSE THIS WINDOW\"
        -------------------------------------------------
        \"DO NOT SHUT DOWN THE COMPUTER\"
        -------------------------------------------------
        \"CRITICAL TASKS ARE IN PROGRESS\"    
        -------------------------------------------------
        """)


if __name__ == '__main__':

    is_reset = False
    delta_hour = 0

    timings = generate_timing_strings(datetime.datetime.now(), THRESHOLD, next_day_start_barricade=True)
    log_timings(timings, True)

    while True:
        if datetime.datetime.now().hour == 0 and delta_hour != 0:
            timings = generate_timing_strings(datetime.datetime.now(), THRESHOLD, next_day_start_barricade=True)
            log_timings(timings)

        if datetime.datetime.now().hour != delta_hour:
            delta_hour = datetime.datetime.now().hour

        current_time_string = timeutil.get_string_time(datetime.datetime.now())

        if current_time_string in timings:
            post = main()
            log_posted(datetime.datetime.now(), post['id'])
            timings.remove(current_time_string)

        print("Checked at: {}".format(datetime.datetime.now()))
        show_user_terminal_warning()

        time.sleep(42)
