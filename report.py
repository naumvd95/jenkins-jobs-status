import jenkins
import pprint
import csv
PP=pprint.PrettyPrinter()
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
        if name.startswith('9.0.build') or name.startswith('9.0.regression') or name.startswith('8.0.contrail') or name.startswith('7.0'):
            count+=1
            counter = '#'+str(count)
            names = job['name']
            print counter+' '+job['name']
            if len(server.get_job_info(job['name'])['healthReport'])>1:
                url = server.get_job_info(job['name'])['lastFailedBuild']['url']+'testReport'
                print 'testReport\n'+url

                print '================================================================================================'
            else:
                url = server.get_job_info(job['name'])['lastFailedBuild']['url']+ 'console'
                print 'Console output,  testReport does not exist\n'+url
                print '================================================================================================'
            csvwriter.writerow([counter, names, url])
print alljobs
