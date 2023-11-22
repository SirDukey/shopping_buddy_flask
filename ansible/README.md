## Ansible

The playbook `webservices.yml` can be used to configure the following
on the destination server:
1. Ensure package for python virtual environment is installed
2. Create Python virtual environment
3. Install Python packages from a requirements File
4. Install gunicorn as a systemd service
5. Start gunicorn service
6. Install Nginx
7. Start Nginx
8. Configure the nginx site
9. Restart nginx service

## How to use
Install ansible on a host
```
python3 -m pip install --user ansible
```
Copy the `ansible` directory from this repository to a 
directory on the host

Create the following directory and hosts file (change `1.2.3.4` to your destination server ip address)
```
mkdir inventory
printf '[webservers]\n1.2.3.4\n' > inventory/hosts
```
Run the playbook
```commandline
ansible-playbook -i inventory/hosts webservice.yml
```
