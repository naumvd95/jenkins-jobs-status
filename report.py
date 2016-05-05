import jenkins
import pprint
import csv
PP=pprint.PrettyPrinter()

# should be passed into through an env variable
# e.g. JENKINS_HOST=...

# jenkins_url should be splitted to JENKINS_HOST and JENKINS_PORT
# remove the addr from code
jenkins_url = 'http://172.18.170.69:8080/'
server = jenkins.Jenkins(jenkins_url)
job_instance = server.get_all_jobs()
count=0
alljobs=0
csv_file = open('failedbuilds.csv', 'w')
csvwriter = csv.writer(csv_file, delimiter='|',quoting=csv.QUOTE_MINIMAL)
csvwriter.writerow(['count', 'name', 'url'])
for job in job_instance:
    alljobs+=1
    if job['color'] == 'red':
        name = job['name']
        # "startwith" should be replaced by "in" (what about the ".regression" case ?)
        # filter should be passed by script's args
        if name.startswith('9.0.build') or name.startswith('9.0.regression') or name.startswith('8.0.contrail') or name.startswith('7.0'):
            count+=1
            counter = '#'+str(count)
            names = job['name']
            print counter+' '+job['name']
            if len(server.get_job_info(job['name'])['healthReport'])>1:
                # all string concatenation should be replaced by .format 
                url = server.get_job_info(job['name'])['lastFailedBuild']['url']+'testReport'
                print 'testReport\n'+url
                # use .format to generate lines line that  
                print '================================================================================================'
            else:
                url = server.get_job_info(job['name'])['lastFailedBuild']['url']+ 'console'
                print 'Console output,  testReport does not exist\n'+url
                print '================================================================================================'
            csvwriter.writerow([counter, names, url])
print alljobs
