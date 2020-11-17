import subprocess, re

# function create_tempEmail():
# returns created temporary email
def create_tempEmail():
	result = subprocess.run(['./tmpmail', '--generate'], stdout=subprocess.PIPE)
	email = result.stdout.decode('ascii')

	return email

# function read_tempEmail()
# Reads most recent email of ballot sent by user
# Parses file to a dictionary ballot send to mongoDB
def read_tempEmail():
	result = subprocess.run(['./tmpmail', '-r', '-t'], stdout=subprocess.PIPE)
	# remove the header and footer of the message; leaving just the ballot
	body, email = result.stdout.split(b'\n\n\n', 1)[1].split(b'This message was sent to')
	
	email = email.split(b' from Voter Guide')[0].decode('utf-8').strip()
	body = re.split(b'\d+\.', body)

	ballot = {}
	curRace = None
	for line in body:
		delim = re.search(b'\n\n', line)
		# race
		if(delim!=None and line!=body[-1]):
			curRace = line.strip().decode('utf-8')
			ballot[curRace] = {"race":curRace, "candidate": [], "vote": ""}
		# candidate for that race
		else:
			if(line==b' '):
				continue
			candidate = line.strip().decode('utf-8')
			# determine if the candidate is the vote choise for the user
			if(re.search(b'\xe2\x86\x92',line)!=None):
				candidate = candidate.split(b'\xe2\x86\x92'.decode('utf-8'))[1].strip()
				ballot[curRace]['vote'] = candidate
			ballot[curRace]['candidate'].append(candidate)

	return email, ballot

print(read_tempEmail())
	
	
