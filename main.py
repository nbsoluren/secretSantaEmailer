import sys
sys.path.append(".")
import secretSanta as santa

# please modify as you see fit
participantsInputPath = "participants.csv"
ojSantaEmail = "natalie@natalienicole.dev"
smtpHost = "mail.gandi.net"
password = 'thisIsMySecretBro'


participants = santa.getMembers(participantsInputPath)
assignments = santa.assignChildren(participants)

# santa is a slave to traditions, he checksTwice but he knows everything is in order.
if santa.checksTwice(assignments) == False:
    print("Christmas is ruined! The Grinch has sabotaged Santa's mind!")
else:
    print("Sending~")
    santa.sendEmails(assignments, ojSantaEmail, smtpHost, password)
