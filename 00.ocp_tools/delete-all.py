#!/usr/bin/python3

#######################################################################
# Python program to delete objects on OCP cluster
#
# WARNING: you must uncomment final command to execute deletions
# Prerequisites: You must be logged in a OCP Cluster (oc login ..)
#
#######################################################################

import yaml, os, subprocess

print('Starting...')
to_delete = []

os.system('oc get pods -o yaml > tmpPods')
os.system('oc get svc -o yaml > tmpSvc')
os.system('oc get bc -o yaml > tmpBC')
os.system('oc get route -o yaml > tmpRoute')
os.system('oc get is -o yaml > tmpImage')
os.system('oc get build -o yaml > tmpBuild')

#print(open('tmpRoute', 'r').read())
# ImageStream
with open('tmpImage', 'r') as f:
    parsed = yaml.safe_load(f)

print("ImageStreams:")
for item in parsed['items']:
    if item['metadata']['name'] != ['']:
        to_delete.append('is/'+item['metadata']['name'])
        #print('\t', item['metadata']['name'])
        continue 

# Builds
with open('tmpBuild', 'r') as f:
    parsed = yaml.safe_load(f)

print("Builds:")
for item in parsed['items']:
    if item['metadata']['name'] != ['']:
        to_delete.append('build/'+item['metadata']['name'])
        #print('\t', item['metadata']['name'])
        continue 

# Pods
with open('tmpPods', 'r') as f:
    parsed = yaml.safe_load(f)

print("Pods:")
for item in parsed['items']:
    if item['metadata']['name'] != ['']:
        to_delete.append('pod/'+item['metadata']['name'])
        #print('\t', item['metadata']['name'])
        continue 

#Services
with open('tmpSvc', 'r') as f:
    parsed = yaml.safe_load(f)

print("Services:")
for item in parsed['items']:
    if item['metadata']['name'] != ['']:
        to_delete.append('service/'+item['metadata']['name'])
        #print('\t', item['metadata']['name'])
        continue 

#BC
with open('tmpBC', 'r') as f:
    parsed = yaml.safe_load(f)

print("BuildConfig:")
for item in parsed['items']:
    if item['metadata']['name'] != ['']:
        to_delete.append('bc/'+ item['metadata']['name'])
        #print('\t', item['metadata']['name'])
        continue 

#Routes
with open('tmpRoute', 'r') as f:
    parsed = yaml.safe_load(f)

print("Routes:")
for item in parsed['items']:
    if item['metadata']['name'] != ['']:
        to_delete.append('route/'+ item['metadata']['name'])
        #print('\t', item['metadata']['name'])
        continue 

print("\nObjetos a eliminar:")
for item in to_delete:
    deleteCommand = 'oc delete '+ item
    print('Running: ' + deleteCommand)
    #######################################################
    # UNCOMMENT THE FOLLOWING COMMAND TO EXECUTE DELETIONS:
    # os.system(deleteCommand)
    #######################################################
    

print('\nRemember to delete temporary files created!!')
os.system('ls -la tmp*')

print('\nEnd!')
