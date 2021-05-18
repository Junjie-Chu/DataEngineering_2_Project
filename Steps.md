# Steps
## 1. login and download
login in the client via ssh (our client VM floating ip is 130.238.28.185):    
```
ssh -i /home/junjie-chu/Desktop/DEKEY/DE2_group11.pem ubuntu@130.238.28.185
ssh -i /Users/mac/Desktop/HU_2020/H20_Period4/DE2/Project/DE2_Project/DE2_group11.pem ubuntu@130.238.28.185
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
***change the user name in the RC file and enter your password after 'source'command!***
```
source 'UPPMAX 2020_1-3-openrc.sh'

then you need enter the password for s18228, the password is ******
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
# Next step is to enter these IP addresses in the Ansible hosts file. But we need to use cloud init to create and configure 3 VMs first! Change the configuration of clould init!

# 4. Add one cloud init file for Parameter tuning server VM.

# 5. Edit the start_instances.py
```
  flavor = "ssc.medium" 
  private_net = "UPPMAX 2020/1-3 Internal IPv4 Network"
  floating_ip_pool_name = None
  floating_ip = None
  image_name = "Ubuntu 20.04 - 2021.03.23" 
```  
  Add some basic setting for start the instance parameter tuning server.
# 6. python3 start_instances.py
```  
Instance: prod_server_group11_9473 is in ACTIVE state ip address: 192.168.2.166 130.238.29.82
Instance: dev_server_group11_9473 is in ACTIVE state ip address:  192.168.2.6
Instance: para_server_group11_9473 is in ACTIVE state ip address: 192.168.2.216
```  
   
# 7 Edit ansible   
ssh key
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCtSrktFxWmEw/q3queNQcNeGQ0XRHaXe4iWp/1H3WglNGq0UcUr94P97ToVJaMwM9FuCwcmyzdnc72EjtINvuu0TjxarPcaB+w1DXL0PHD59qkAd2eYkBRN3NXtDUnJBxLd0yYOS04k1kH2xGz8BFHTdMOcEfcMPOCnvGbZxB3USOIPWVPIDEts7F3FNkic2A5Es5JmZ0F5eH3UMurBn+UZS2AmvSH5r0h2X/oR+yuymNMBqL/mY7ryJmndSp2n0sPZpgQbFIZPnEgWD/f62l5IFIPX0tJ4QzlqBSybIqSy6W7ZHXPxQea7wJ4zhNrJIph2y1Kmo+8o7Ln2/lOr7b1CDBbkHfSyEF196qgpDJiwCU1FtPnF9WzFta0Xoox8PP3rLUabTPoNBGRXnoElt85uPwLIYsgIQrQsaedYAg00OuZdqglAIFdGgpX0FIf5KbYYF2B8UZAkcwRQ/1VIhanrh7NzlpUTK3vhwct81GvbBAJMGV5ludLN61QEPirIEc= ubuntu@de2-group11-client

change ansible hosts file
``` 
[servers]
prodserver ansible_host=192.168.2.50
devserver ansible_host=192.168.2.13
paraserver ansible_host=192.168.2.155

[all:vars]
ansible_python_interpreter=/usr/bin/python3

[prodserver]
prodserver ansible_connection=ssh ansible_user=appuser

[devserver]
devserver ansible_connection=ssh ansible_user=appuser
[paraserver]
paraserver ansible_connection=ssh ansible_user=appuser
``` 
``` 
ssh -i /home/ubuntu/cluster-keys/cluster-key appuser@130.238.29.250
ssh -i /home/ubuntu/cluster-keys/cluster-key appuser@130.238.28.39
ssh -i /home/ubuntu/cluster-keys/cluster-key appuser@130.238.28.225
``` 

# 8 Start the ansible configuration
``` 
export ANSIBLE_HOST_KEY_CHECKING=False
ansible-playbook configuration.yml --private-key=/home/ubuntu/cluster-keys/cluster-key
``` 
