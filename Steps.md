# Steps
## 1. login and download
login in the client via ssh (our client VM floating ip is 130.238.28.185):    
```
ssh -i /home/junjie-chu/Desktop/DEKEY/DE2_group11.pem ubuntu@130.238.28.185
```
git clone:
```
https://github.com/Junjie-Chu/DE2_Project.git
```
Note: Be careful with the position of your key and authority of the key.(i.e. chmod 600 DE2_group11.pem)

## 2. install openstack api
1.Enable the repository for Ubuntu Cloud Archive  
OpenStack Victoria for Ubuntu 20.04 LTS:
```
add-apt-repository cloud-archive:victoria
```
2.Finalize the installation  
 -1 Upgrade packages on all nodes:  
 ```
 apt update && apt dist-upgrade
 ```  
 -2 Install the OpenStack client:  
 ```
 apt install python3-openstackclient
 ```
Note: May need sudo or using a root  
The following 2 commands are also run after the 2 steps above.  
But nothing happens I think this is because they are included in the above steps.  
```
apt install python3-novaclient
apt install python3-keystoneclient
```
3.Set your API password and download the RC file  
The RC file is included in the git folder. Just change the user name.  
Confirm that your RC file have following environment variables(The RC file should contain, but double check!):  
```
export OS_USER_DOMAIN_NAME="snic"
export OS_IDENTITY_API_VERSION="3"
export OS_PROJECT_DOMAIN_NAME="snic"
export OS_PROJECT_NAME="UPPMAX 2020/1-3"
```
Set the environment variables by sourcing the RC-file in the client VM.  
```
source 'UPPMAX 2020_1-3-openrc.sh'
```
The successful execution of the following commands will confirm that you have the correct 
packages available on your client VM:  
```
openstack server list
openstack image list
```
![image](https://user-images.githubusercontent.com/65893273/118350121-a6e26780-b587-11eb-97cd-d153329c0d05.png)
# 3. install Ansible on the client machine.
Install Ansible packages on the client machine.  
```
# apt update; apt upgrade
# apt-add-repository ppa:ansible/ansible
# apt update
# apt install ansible
```
# Next step is to enter these IP addresses in the Ansible hosts file. But we need to use cloud init to create and configure 3 VMs first!

