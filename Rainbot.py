import time
import praw
import re
# Login in to Reddit and the bot
r = praw.Reddit('DogecoinRainBot')
r.login("USERNAME","PASSWORD")

# regex pattern that finds how much the bot is tipped.

tip_amount_pattern = re.compile("D?(\d+) ?(?:D|doge)?", re.IGNORECASE)

#defines the summoning command
Name = ['+/u/dogetipbot', 'verify', '@dogerainbot', 'rain']

deleted_comment = '[deleted]'
banned_users = ['bot', 'Healdb']

def find_summons():
    obj2 = open('dogerain_user.txt', 'ab+')
    #Searches for summoning command
    subreddit_comment = r.get_comments('bots4dogetesting', limit=25)
    for comment in subreddit_comment:
        print 'looking for summons'
        comment_text = comment.body
        origin_comment = comment
        author = comment.author
        op_name = author.name
        has_name = all(string in comment_text for string in Name)
        time.sleep(2)
        if origin_comment.id not in open("dogerain_user.txt").read() and has_name:
            print 'Found comment! Getting ready to tip everyone in the thread with the dogecoin...'
            amount = tip_amount_pattern.findall(comment_text)
            total_amount = float(amount[0])
            temp_id = comment.parent_id
            link_id = temp_id[3:]
            time.sleep(5)
            return total_amount, link_id, origin_comment, op_name
total_amount, link_id, origin_comment, op_name = find_summons()

def comment_count(total_amount, link_id, op_name):
    objd = open('dogerain_com_count.txt', 'ab+')
    count = 0
    submission = r.get_submission(submission_id=link_id)
    print 'Counting the comments on the post...'
    submission_comments = submission.comments
    for comment in submission_comments:
        if comment.id not in open("dogerain_com_count.txt").read():
            objc = open('dogerain_dubs.txt', 'ab+')
            objd = open('dogerain_com_count.txt', 'ab+')
            objc.write(op_name)
            com_text = comment.body
            is_deleted = all(string in com_text for string in deleted_comment)
            if is_deleted:
                objd.write(comment.id)
                objd.close()
                time.sleep(5)
            else:
                nam = comment.author
                comment_op = nam.name
                is_banned = all(string in comment_op for string in banned_users)
                if comment_op not in open("dogerain_dubs.txt").read():
                    if is_banned:
                        objd.write(comment.id)
                        objd.close()
                        time.sleep(5)
                    else:
                        count+=1
                        print count
                        objd.write(comment.id)
                        objc.write(comment_op)
                        objc.close()
                        objd.close()
                        time.sleep(5)
    return count, submission_comments, submission
count, submission_comments, submission = comment_count(total_amount, link_id, op_name)      

def make_rain(total_amount, origin_comment, op_name, count, submission_comments, submission):
    tip_amount = total_amount/count
    print 'Checking to see if there is enough dogecoin for every one...'
    if tip_amount>=4:
        print 'There is enough!'
        time.sleep(5)
        origin_comment.reply('Starting to make it rain! Each user in this thread will get... ' + str(tip_amount) + ' Dogecoin')
        submission_comments = submission.comments
        for comment in submission_comments:
            obj = open('dogerain_users.txt', 'ab+')
            obj2 = open('dogerain_user.txt', 'ab+')
            obj3 = open('dogerain_dubs.txt', 'ab+')
            obj3.write(op_name)
            com_text = comment.body
            is_deleted = all(string in com_text for string in deleted_comment)
            if is_deleted:
                obj.write(comment.id)
                obj.close()
                time.sleep(3)
            else:
                nam = comment.author
                comment_op = nam.name
                is_banned = all(string in comment_op for string in banned_users)
                if is_banned:
                    obj3.write(comment_op)
                    obj.write(comment.id)
                    time.sleep(3)
                else:
                    if comment.id not in open("dogerain_users.txt").read() and comment_op not in open("dogerain_dubs.txt").read():
                        print 'Found comment to tip, tipping them now'
                        comment.reply('/u/' + str(op_name) + ' has made it rain! Have some dogecoin! +/u/dogetipbot ' + str(tip_amount) + ' doge')
                        obj3.write(comment_op)
                        obj.write(comment.id)
                        obj2.write(origin_comment.id)
                        obj.close()
                        obj2.close()
                        obj3.close()
                        print 'Dogecoin given! Starting again in 5 seconds...'
                        time.sleep(5)
    else:
        print 'They didnt have enough to make it rain'
        if origin_comment.id not in open("dogerain_user.txt").read():
            origin_comment.reply('Thats not enough dogecoin to tip everyone in this thread. +/u/dogetipbot ' + str(total_amount) + ' doge verify')
            obj2.write(origin_comment.id)
            obj2.close()
            time.sleep(5)
            find_summons()
            total_amount, link_id, origin_comment, op_name = find_summons()
            comment_count(total_amount, link_id, op_name)
            count, submission_comments, submission = comment_count(total_amount, link_id, op_name)
            make_rain(total_amount, origin_comment, op_name, submission, count, submission_comments)

while True:
    print 'Starting bot...'
    make_rain(total_amount, origin_comment, op_name, count, submission_comments, submission)
    print 'Done'
    open('dogerain_dubs.txt', 'w').close()
    time.sleep(5)
    find_summons()
    total_amount, link_id, origin_comment, op_name = find_summons()
    comment_count(total_amount, link_id, op_name)
    count, submission_comments, submission = comment_count(total_amount, link_id, op_name)
    make_rain(total_amount, origin_comment, op_name, count, submission_comments, submission)
                
            
    
    
