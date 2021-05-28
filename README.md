# DE2_Project_Group11

## 1. Login in the Orchestration VM
The detailed settings could be read in the Steps.md(step1-step3 are for Orchestration VM).  
git clone:  
```
https://github.com/Junjie-Chu/DE2_Project.git
```
Note: Be careful with the position of your key and authority of the key.(i.e. chmod 600 DE2_group11.pem)  

## 2. Create instances
![image](https://user-images.githubusercontent.com/53885509/119945734-6c85bb00-bfc8-11eb-9dee-c310e4776e7c.png)

Command:  
```
python3 DE2_Project/openstack-client/single_node_with_docker_ansible_client/start_instances.py
```
## 3. Revise the hosts IP
According to the IP of our instances, edit the file.  

```
sudo nano /etc/ansible/hosts
```

## 4. Start to deploy services with ansible.
Command:  
```
export ANSIBLE_HOST_KEY_CHECKING=False
ansible-playbook configuration.yml --private-key=/home/ubuntu/cluster-keys/cluster-key
```
![image](https://user-images.githubusercontent.com/53885509/119966894-5b47a900-bfde-11eb-9e55-6780081dec6c.png)

## 5. Start to train models in development node
Log in the development node:  
```
ssh -i /home/ubuntu/cluster-keys/cluster-key appuser@192.168.2.89
cd /home/DE2_Project/ci_cd/development_server/
sudo -s
docker build -t trainmodel .
```
According to the way you like, you could edit the .py file via vim/nano, or via jupyternotebook(floatingip:5100 and do not forget to start jupyternotebook service).  
Now we could run the scripts in the VM directly or run them in the containers.  
If in VM:  
```
python3 GDBT_train.py
python3 NN_train.py
python3 RF_train.py
```
If in containers:    
1. Build image    
```
docker build -t trainmodel .
```
2. Run models  
```
docker run -it imagename filename.py
```
3. After the .py is changed, copy the new modeltraining.py from the VM to the container   
```
docker cp /home/DE2_Project/ci_cd/development_server/trainmodel.py 10704c9eb7bb:/app
```
4. Log in the container and run new modeltraining.py  
```
docker exec -it imagename bash
python3 new modeltraining.py
```
5. Copy the result from containers to the VM   
```
docker cp 10704c9eb7bb:/app/model.name /home/DE2_Project/ci_cd/development_server/
```
## 6. Compare the models
Select the best one!  
## 7. Do parameter tuning
Tune the best one!
## 8. Push the best model to production cluster! 
The ci/cd is realized by githook. The setting of githook is realized via Ansible playbook.  
The part for dev server in Ansible playbook:  
![image](https://user-images.githubusercontent.com/65893273/119997600-77f5d800-c002-11eb-8337-9a674ca26cab.png)  
The part for prod server in Ansible playbook:  
![image](https://user-images.githubusercontent.com/65893273/119997693-922fb600-c002-11eb-8a90-39e252cec66b.png)  
Now push the first model:  
log in devserver:  
```
ssh -i cluster-key appuser@<DEVELOPMENT-SERVER-IP>
```
Go to the /home/appuser/my_project directory  
Add files for the commit and commit files   
```
git add .
git commit -m "test 1"
```
Connect development server's git to production server's git  
```
git remote add production appuser@<PRODUCTIONS-SERVER-IP>:/home/appuser/my_project
```
Push your commits to the production server  
```
git push production master
```
## 9. Set up the production cluster(docker swarm)
something!
## 10. Now visit the page: floatip:5100/accuracy
## 11. Test scalability
Note: all the tests should be run in the same environment.   
Run test.py and the start time(just example) will be recorded.  
![image](https://user-images.githubusercontent.com/65893273/119993769-84783180-bffe-11eb-80f0-4bfe7545116e.png)  
The end time(just example):  
![image](https://user-images.githubusercontent.com/65893273/119994699-6bbc4b80-bfff-11eb-9a65-5b100665caf4.png)  



