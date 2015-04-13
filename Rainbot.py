import time
import praw
import re
from math import ceil

owner_uname='healdb'
botusername="USERNAME"
banned_users = [owner_uname, 'bot' , 'Bot'] #TODO move to a file

# Login in to Reddit and the bot
r = praw.Reddit('DogecoinRainBot') # a curtosy to reddit to give them useful ideas about API use
r.login(botusername,"PASSWORD")    # change the password


tip_amount_pattern = re.compile("D?(\d+) ?(?:D|doge)?", re.IGNORECASE)
tipbbot = 'dogetipbot' # the coin tip bot name

#defines the summoning command
Name = ['+/u/' + str(tipbot), 'verify', '@randomactofdogebot', 'Rain!']
count = 0
deleted_comment = '[deleted]'
banned_users = [owner_uname, 'bot' , 'Bot']

def get_parent(com_id,com_permlink):
    submission = r.get_submission(url=com_permlink + com_id)
    submission = submission.comments
    for comment in submission:
        com_id =  comment.id
        oldstr = comment.permalink
        newstr = oldstr.replace(com_id, "")
        temp_id = comment.parent_id
        link_id = temp_id[3:]
        com_link = newstr + link_id
        submission = r.get_submission(url=com_link)
        submission = submission.comments
        for comment in submission:
            return comment

def find_summons():
    obj2 = open('dogerain_user.txt', 'ab+')
    #Searches for summoning command
    messages = r.get_unread('mentions')

    for comment in messages:
        print 'looking for summons'
        comment_text = comment.body
        origin_comment = comment
        com_id= comment.id
        oldstr = comment.permalink
        com_permlink = oldstr.replace(com_id, "")
        has_name = all(string in comment_text for string in Name)
        author = origin_comment.author
        op_name = author.name
        if origin_comment.id not in open("dogerain_user.txt").read() and op_name == tipbot:
            print 'Found comment! Getting ready to tip everyone in the thread with the dogecoin...'
            re1='.*?'                # Non-greedy match on filler
            re2='(?:[a-z][a-z]+)'    # Uninteresting: word
            re3='.*?'                # Non-greedy match on filler
            re4='(?:[a-z][a-z]+)'    # Uninteresting: word
            re5='.*?'                # Non-greedy match on filler
            re6='(?:[a-z][a-z]+)'    # Uninteresting: word
            re7='.*?'                # Non-greedy match on filler
            re8='((?:[a-z][a-z]+))'  # Word 1\
            re9='.*?'                # Non-greedy match on filler
            re10='((?:[a-z][a-z]+))' # Word 2 
            re11='.*?'               # Non-greedy match on filler
            re12='(\\d+)'            # Integer Number 1 tip ammount
            rg = re.compile(re1+re2+re3+re4+re5+re6+re7+re8+re9+re10+re11+re12,re.IGNORECASE|re.DOTALL)

            m = rg.search(comment_text)
            if m:
                amount=m.group(3)
            try:
                origin_comment = get_parent(com_id,com_permlink)
                print origin_comment
                author = origin_comment.author
                op_name = author.name
                total_amount = amount
                print total_amount
                temp_id = origin_comment.parent_id
                link_id = temp_id[3:]
                obj2.write(comment.id)
                comment.mark_as_read()
                return total_amount, link_id, origin_comment, op_name
            except IndexError:
                origin_comment.reply('Im sorry, I dont understand tips like that! Message /u/' + str(owner_uname) + ' and they will refund the dogecoin :)')
                print 'That wasnt right'
                obj2.write(origin_comment.id)
                obj2.close()
                time.sleep(5)

def comment_count(op_name, submission):
    global count
    print 'hey'
    print 'Counting the comments on the post...'
    submission = submission
    submission.replace_more_comments(limit=None, threshold=0)
    submission_comments = submission.comments
    for comment in submission_comments:
        objc = open('dogerain_dub.txt', 'ab+')
        objd = open('dogerain_com_count.txt', 'ab+')
        print comment.body
        if comment.id not in open("dogerain_com_count.txt").read():
            objc.write(op_name)
            com_text = comment.body
            is_deleted = all(string in com_text for string in deleted_comment)
            if is_deleted:
                print 'DELETED \n'
                objd.write(comment.id)
                objd.close()
            else:
                nam = comment.author
                comment_op = nam.name
                is_banned = any(string in comment_op for string in banned_users)
                if comment_op in open("dogerain_dub.txt").read():
                    print 'SEEN \n'
                    objd.write(comment.id)
                    objd.close()
                else:
                    if is_banned:
                        print 'BANNED \n'
                        objd.write(comment.id)
                        objd.close()
                    else:
                        count+=1
                        print count
                        global count
                        objd.write(comment.id)
                        objc.write(comment_op)
                        objc.close()
                        objd.close()
    return count, submission_comments, submission

def make_rain(total_amount, origin_comment, op_name, count, submission_comments, submission):
    try:
        tip_amount = int(total_amount)/int(count)
        pass
    except:
        print 'There were no comments in that thread. Starting again.'
        origin_comment.reply('There are no eligible comments in this thread. Please try again. +/u/' + str(tipbot) " " + str(total_amount) + ' doge verify')
        objt = open('dogerain_user.txt', 'ab+')
        objt.write(origin_comment.id)
        objt.close()
        print 'Done. Resetting variables...'
        open('dogerain_dub.txt', 'w').close()
        open('dogerain_dubs.txt', 'w').close()
        open('dogerain_users.txt', 'w').close()
        open('dogerain_com_count.txt', 'w').close()
        count = 0
        print 'Starting again in one minute'
        time.sleep(60)
        break
    print 'Checking to see if there is enough dogecoin for every one...'
    tip_amount = ceil(tip_amount * 10000) / 10000
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
                print '\n DELETED'
                obj.write(comment.id)
                obj.close()
                time.sleep(3)
            else:
                nam = comment.author
                comment_op = nam.name
                is_banned = any(string in comment_op for string in banned_users)
                if is_banned:
                    print '\n BANNED'
                    obj3.write(comment_op)
                    obj.write(comment.id)
                    obj.close()
                    obj3.close()
                    time.sleep(3)
                else:
                    if comment_op in open("dogerain_dubs.txt").read():
                        print '\n SEEN'
                        obj.write(comment.id)
                        obj.close()
                        time.sleep(3)
                    else:
                        if comment.id not in open("dogerain_users.txt").read():
                            print 'Found comment to tip, tipping them now'
                            comment.reply('/u/' + str(op_name) + ' has made it rain! Have some dogecoin! +/u/" + str(tipbot) + ' ' + str(tip_amount) + ' doge \n\n^I ^was ^initially ^made ^by ^/u/healdb ^through ^http://bots4doge.com')
                            obj3.write(comment_op)
                            obj.write(comment.id)
                            obj2.write(origin_comment.id)
                            obj.close()
                            obj2.close()
                            obj3.close()
                            print 'Dogecoin given! Starting again in 30 seconds...'
                            time.sleep(5)
    else:
        print 'They didnt have enough to make it rain'
        if origin_comment.id not in open("dogerain_user.txt").read():
            obj2 = open('dogerain_user.txt', 'ab+')  
            origin_comment.reply('Thats not enough dogecoin to tip everyone in this thread. Message /u/'+ str(owner_uname) +' and they will refund the dogecoin.')
            obj2.write(origin_comment.id)
            obj2.close()
            print 'Done. Resetting Variables...'
            open('dogerain_dub.txt', 'w').close()
            open('dogerain_dubs.txt', 'w').close()
            open('dogerain_users.txt', 'w').close()
            open('dogerain_com_count.txt', 'w').close()
            count = 0
            print 'Starting again in one minute'
            time.sleep(60)

while True:
    print 'Starting bot...'
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
                origin_comment.reply('Im sorry, I only work with replies to submissions, not replies to comments! Message /u/' + str(owner_uname) + " and they will refund the dogecoin.')
                objt.write(origin_comment.id)
                objt.close()
                time.sleep(10)
    count, submission_comments, submission = comment_count(op_name, submission)
    make_rain(total_amount, origin_comment, op_name, count, submission_comments, submission)
    print 'Done. Resetting Variables'
    open('dogerain_dub.txt', 'w').close()
    open('dogerain_dubs.txt', 'w').close()
    open('dogerain_users.txt', 'w').close()
    open('dogerain_com_count.txt', 'w').close()
    origin_comment.mark_as_read()
    count = 0
    print 'Starting again in one minute'
    time.sleep(60)
