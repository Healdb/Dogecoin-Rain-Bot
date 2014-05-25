import time
import praw
import re
from math import ceil
# Login in to Reddit and the bot
r = praw.Reddit('DogecoinRainBot')
r.login("USERNAME","PASSWORD")

# creates file where the posts it has already counted are stored.

tip_amount_pattern = re.compile("D?(\d+) ?(?:D|doge)?", re.IGNORECASE)

#defines the summoning command
Name = ['+/u/dogetipbot', 'verify', '@randomactofdogebot', 'Rain!']
count = 0
deleted_comment = '[deleted]'
banned_users = ['bot', 'Healdb', 'Bot']
def find_summons():
    obj2 = open('dogerain_user.txt', 'ab+')
    #Searches for summoning command
    messages = r.get_unread('mentions')
    for comment in messages:
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
            try:
                total_amount = float(amount[0])
                temp_id = comment.parent_id
                link_id = temp_id[3:]
                time.sleep(5)
                return total_amount, link_id, origin_comment, op_name
            except IndexError:
                origin_comment.reply('Im sorry, I dont understand tips like that! Message /u/healdb and he will refund the dogecoin :)')
                print 'That wasnt right'
                time.sleep(5)
while True:
    try:
        total_amount, link_id, origin_comment, op_name = find_summons()
        submission = r.get_submission(submission_id=link_id)
        break
    except TypeError:
        print 'Found no new summons, trying again in 10 seconds.'
        time.sleep(10)
    except:
        objt = open('dogerain_user.txt', 'ab+')
        if origin_comment.id not in open("dogerain_user.txt").read():
            print 'they got it wrong'
            origin_comment.reply('Im sorry, I only work with replies to submissions, not replies to comments! +/u/dogetipbot ' + str(total_amount) + ' doge verify')
            objt.write(origin_comment.id)
            objt.close()
            time.sleep(10)
def comment_count(total_amount, link_id, op_name, submission):
    global count
    objd = open('dogerain_com_count.txt', 'ab+')
    obj2 = open('dogerain_user.txt', 'ab+')
    print 'Counting the comments on the post...'
    submission = submission
    submission_comments = submission.comments
    for comment in submission_comments:
        if comment.id not in open("dogerain_com_count.txt").read():
            objc = open('dogerain_dub.txt', 'ab+')
            objd = open('dogerain_com_count.txt', 'ab+')
            obje = open('dogerain_dubs.txt', 'ab+')
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
                is_banned = any(string in comment_op for string in banned_users)
                if comment_op in open("dogerain_dub.txt").read():
                    objd.write(comment.id)
                    objd.close()
                    time.sleep(5)
                else:
                    if is_banned:
                        objd.write(comment.id)
                        objd.close()
                        time.sleep(5)
                    else:
                        count+=1
                        print count
                        global count
                        objd.write(comment.id)
                        objc.write(comment_op)
                        objc.close()
                        objd.close()
                        time.sleep(5)
    return count, submission_comments, submission
count, submission_comments, submission = comment_count(total_amount, link_id, op_name, submission)      

def make_rain(total_amount, origin_comment, op_name, count, submission_comments, submission):
    try:
        tip_amount = total_amount/count
        pass
    except:
        print 'There were no comments in that thread. Starting again.'
        origin_comment.reply('There are no eligible comments in this thread. Please try again. +/u/dogetipbot ' + str(total_amount) + ' doge verify')
        objt = open('dogerain_user.txt', 'ab+')
        objt.write(origin_comment.id)
        objt.close()
        time.sleep(10)
        print 'done'
        open('dogerain_dub.txt', 'w').close()
        open('dogerain_dubs.txt', 'w').close()
        open('dogerain_users.txt', 'w').close()
        open('dogerain_com_count.txt', 'w').close()
        count = 0
        find_summons()
        while True:
            try:
                total_amount, link_id, origin_comment, op_name = find_summons()
                submission = r.get_submission(submission_id=link_id)
                break
            except TypeError:
                print 'Found no new summons, trying again in 10 seconds.'
                time.sleep(10)
            except:
                objt = open('dogerain_user.txt', 'ab+')
                if origin_comment.id not in open("dogerain_user.txt").read():
                    print 'they got it wrong'
                    origin_comment.reply('Im sorry, I only work with replies to submissions, not replies to comments! +/u/dogetipbot ' + str(total_amount) + ' doge verify')
                    objt.write(origin_comment.id)
                    objt.close()
                    time.sleep(10)
        comment_count(total_amount, link_id, op_name, submission)
        count, submission_comments, submission = comment_count(total_amount, link_id, op_name, submission)
        make_rain(total_amount, origin_comment, op_name, count, submission_comments, submission)
        
    print 'Checking to see if there is enough dogecoin for every one...'
    tip_amount = ceil(tip_amount * 10000) / 10000
    if tip_amount!=0 and tip_amount>=4:
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
                is_banned = any(string in comment_op for string in banned_users)
                if is_banned:
                    obj3.write(comment_op)
                    obj.write(comment.id)
                    time.sleep(3)
                else:
                    if comment_op in open("dogerain_dubs.txt").read():
                        obj.write(comment.id)
                        time.sleep(3)
                    else:
                        if comment.id not in open("dogerain_users.txt").read():
                            print 'Found comment to tip, tipping them now'
                            comment.reply('/u/' + str(op_name) + ' has made it rain! Have some dogecoin! +/u/dogetipbot ' + str(tip_amount) + ' doge')
                            obj3.write(comment_op)
                            obj.write(comment.id)
                            obj2.write(origin_comment.id)
                            obj.close()
                            obj2.close()
                            obj3.close()
                            print 'Dogecoin given! Starting again in 10 seconds...'
                            time.sleep(10)
    else:
        print 'They didnt have enough to make it rain'
        if origin_comment.id not in open("dogerain_user.txt").read():
            origin_comment.reply('Thats not enough dogecoin to tip everyone in this thread. +/u/dogetipbot ' + str(total_amount) + ' doge verify')
            obj2.write(origin_comment.id)
            obj2.close()
            time.sleep(5)

while True:
    print 'Starting bot...'
    find_summons()
    while True:
        try:
            total_amount, link_id, origin_comment, op_name = find_summons()
            submission = r.get_submission(submission_id=link_id)
            break
        except TypeError:
            print 'Found no new summons, trying again in 10 seconds.'
            time.sleep(10)
        except:
            objt = open('dogerain_user.txt', 'ab+')
            if origin_comment.id not in open("dogerain_user.txt").read():
                print 'they got it wrong'
                origin_comment.reply('Im sorry, I only work with replies to submissions, not replies to comments! +/u/dogetipbot ' + str(total_amount) + ' doge verify')
                objt.write(origin_comment.id)
                objt.close()
                time.sleep(10)
    comment_count(total_amount, link_id, op_name, submission)
    count, submission_comments, submission = comment_count(total_amount, link_id, op_name, submission)
    make_rain(total_amount, origin_comment, op_name, count, submission_comments, submission)
    print 'Done'
    open('dogerain_dub.txt', 'w').close()
    open('dogerain_dubs.txt', 'w').close()
    open('dogerain_users.txt', 'w').close()
    open('dogerain_com_count.txt', 'w').close()
    count = 0
    time.sleep(10)
                
            
    
    
