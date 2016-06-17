import jenkins
import pprint
import csv
PP=pprint.PrettyPrinter()
JENKINS_HOST='172.18.170.69'
JENKINS_PORT='8080'
args=['9.0.','9.0.regression','.regression','8.0.contrail','7.0']
jenkins_url = 'http://'+JENKINS_HOST+':'+JENKINS_PORT
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
        for filtername in args:
            if filtername in name:
                count+=1
                counter = '#'+str(count)
                names = job['name']
                print(counter+' '+job['name'])
                if len(server.get_job_info(job['name'])['healthReport'])>1:
                    url = server.get_job_info(job['name'])['lastFailedBuild']['url']+'testReport'
                    failed_number = server.get_job_info(job['name'])['lastFailedBuild']['number']
                    output = server.get_build_console_output(job['name'], failed_number)
                    print('testReport\n'+url)
                    print ('-'*160)
                    print ('console output\n'+output)
                    print ('=' * 160)


                else:
                    url = server.get_job_info(job['name'])['lastFailedBuild']['url']+ 'console'
                    failed_number=server.get_job_info(job['name'])['lastFailedBuild']['number']
                    output = server.get_build_console_output(job['name'],failed_number)
                    print (' testReport does not exist\n'+url)
                    print ('-'*160)
                    print ('console output\n'+output)
                    print ('='*160)
                job_file = open(job['name'],'w')
                info = (job['name'] + '\n'+('-'*80)+'\n'+ url+'\n'+('-'*80)+ '\n' + output).encode('utf-8')
                job_file.write(info)
                job_file.close()
                csvwriter.writerow([counter, names, url])
print ("all checked jobs: " + str(alljobs))
