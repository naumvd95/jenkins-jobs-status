import jenkins
import pprint
import csv
import os

PP = pprint.PrettyPrinter()

port = os.getenv('JENKINS_PORT', '8080')
host = os.getenv('JENKINS_HOST')
if not host:
    print ("JENKINS_HOST is undefined")
    exit(1)


def connect(host, port, username=None, password=None):
    return jenkins.Jenkins("http://{host}:{port}".format(host=host, port=port),
                           username=username, password=password)

def get_latest_build_number(server, name):
    return server.get_job_info(name)['lastCompletedBuild']['number']

def get_latest_result(server, name):
    return server.get_build_info(name, get_latest_build_number(server, name))['result']


def get_failed_jobs(server, name_filter=None, status='FAILED'):
    return get_jobs(server, name_filter, status)


def get_success_jobs(server, name_filter=None, status='SUCCESS'):
    return get_jobs(server, name_filter, status)


def get_aborted_jobs(server, name_filter=None, status='ABORTED'):
    return get_jobs(server, name_filter, status)


def get_jobs(server, name_filter=None, status=None):
    names = []
    if name_filter:
        if not isinstance(name_filter, list):
            name_filter = [name_filter]
        names = [job['name'] for job in server.get_jobs() if
                 any(item in job['name'] for item in name_filter)]
    else:
        names = [job['name'] for job in server.get_jobs()]

    return [name for name in names
            if status in get_latest_result(server, name)] if status else names  # all_jobs=none

#
# count = 0
# alljobs = 0
# csv_file = open('failedbuilds.csv', 'w')
# csvwriter = csv.writer(csv_file, delimiter='|', quoting=csv.QUOTE_MINIMAL)
# csvwriter.writerow(['count', 'name', 'url'])
#
# for job in all_jobs:
#    alljobs += 1
#    if job['color'] == 'red':
#        name = job['name']
#        for filtername in args:
#            if filtername in name:
#                count += 1
#                counter = '#' + str(count)
#                names = job['name']
#                print counter + ' ' + job['name']
#                if len(server.get_job_info(job['name'])['healthReport']) > 1:
#                    url = server.get_job_info(job['name'])['lastFailedBuild']['url'] + 'testReport'
#                    failed_number = server.get_job_info(job['name'])['lastFailedBuild']['number']
#                    output = (server.get_build_console_output(job['name'], failed_number)).encode('utf-8')
#                    print 'testreport\n' + url
#                    print '-' * 160
#                    print 'console output\n' + output
#                    print '=' * 160
#
#                else:
#                    url = server.get_job_info(job['name'])['lastFailedBuild']['url'] + 'console'
#                    failed_number = server.get_job_info(job['name'])['lastFailedBuild']['number']
#                    output = (server.get_build_console_output(job['name'], failed_number)).encode('utf-8')
#                    print ' testreport does not exist\n' + url
#                    print '-' * 160
#                    print 'console output\n' + output
#                    print '=' * 160
#                job_file = open(job['name'], 'w')
#                job_file.writelines(job['name'])
#                job_file.write('\n')
#                job_file.write(url)
#                job_file.write('\n')
#                job_file.write(output)
#                job_file.close()
#                csvwriter.writerow([counter, names, url])
# print "all checked jobs: " + str(alljobs)
