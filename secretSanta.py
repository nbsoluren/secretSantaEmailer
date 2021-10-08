import sys, csv, copy, random, smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders

sys.path.append(".")
from caseClasses import Participant, Assignment

def getMembers(participantsCsv):
    participants = []
    with open(participantsCsv) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                participants.append(Participant(row[0], row[1]))

    return participants

def assignChildren(participants):
    assignments = []
    random.shuffle(participants)
    lastIndex = len(participants)-1

    for i in range(lastIndex):
        santa = participants[i]
        child = participants[i+1]
        assignments.append(Assignment(santa, child))

    #let's not forget the last person~
    santa = participants[lastIndex]
    child = participants[0]
    assignments.append(Assignment(santa, child))

    return assignments

def checksTwice(assignments):
    for assignment in assignments:
        santa = assignment.santa.name
        child = assignment.child.name
        if santa == child:
            return False

    return True

def sendEmails(assignments, organizerEmail, smtpHost, password):
    for assignment in assignments:
        # Assignments(santa, child) = assignment deconstructors don't work
        # this makes me cry 😢
        santa = assignment.santa
        child = assignment.child
        santaEmail = santa.email

        msg = MIMEMultipart('related')
        msg['From'] = organizerEmail
        msg['To'] = santaEmail
        msg['Subject'] = "OJ SANTA HAS ASSIGNED YOU YOUR CHILD!!!!"

        html = """\
        <html>
          <head></head>
            <body>
                <img src="cid:image1" alt="Header"><br>
                <h1>Santa %s, you have been assigned a child! Congratulations!</h1>

                <h3>Your Child is: </h3> <h2>%s!!!!</h2>

            </body>
        </html>
        """ % (santa.name, child.name)

        part2 = MIMEText(html, 'html')
        msg.attach(part2)

        fp = open('images/headerPic.png', 'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()

        msgImage.add_header('Content-ID', '<image1>')
        msg.attach(msgImage)

        smtp = smtplib.SMTP(smtpHost,587)
        smtp.starttls()
        smtp.login(organizerEmail,password)
        smtp.sendmail(organizerEmail, santaEmail, msg.as_string())
        smtp.quit()
        print("Email sent to: %s" % (santaEmail))
