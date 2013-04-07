tabular-predDB
==============

tabular predictive database

This package is configured to be installed as a StarCluster plugin.  Roughly, the following are prerequisites.

* An [Amazon EC2](http://aws.amazon.com/ec2/) account
    * [EC2 key pair](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/generating-a-keypair.html)
* [StarCluster](http://star.mit.edu/cluster/) installed on your local machine
    * ~/.starcluster/config file contains the information in [/path/to/tabular_predDB/starcluster.config](https://github.com/mit-probabilistic-computing-project/tabular-predDB/blob/master/starcluster.config) with information filled in
* tabular_predDB package available on your local machine and available on the PTYHONPATH
    * The package directory must be renamed to tabular\_predDB from tabular-predDB
    * if not on the PYTHONPATH, all starcluster commands must be run one level above the package directory

A starcluster_plugin.py file in included in this repo.  Assuming the above prerequisites are fulfilled,

    local> starcluster start -c tabular_predDB [CLUSTER_NAME]

should start a single c1.medium StarCluster server on EC2, install the necessary software, compile the engine, and start an engine listening on port 8007.

Everything will be set up for a user named 'sgeadmin'.  Required python packages will be installed in a virtualenv named tabular_predDB.  To access the environment necessary to build the software, you should be logged in as sgeadmin and run

    local> starcluster sshmaster [CLUSTER_NAME] -u sgeadmin
    sgeadmin> workon tabular_predDB


Starting the engine (Note: the engine is started on boot)
---------------------------
    local> starcluster sshmaster [CLUSTER_NAME] -u sgeadmin
    sgeadmin> pkill -f server_jsonrpc
    sgeadmin> workon tabular_predDB
    sgeadmin> make cython
    sgeadmin> cd jsonrpc_http
    sgeadmin> # capture stdout, stderr separately
    sgeadmin> python server_jsonrpc.py >server_jsonrpc.out 2>server_jsonrpc.err &
    sgeadmin> # test with 'python stub_client_jsonrpc.py'

Running tests
---------------------------
    local> starcluster sshmaster [CLUSTER_NAME] -u sgeadmin
    sgeadmin> workon tabular_predDB
    sgeadmin> # capture stdout, stderr separately
    sgeadmin> make runtests >tests.out 2>tests.err

Building local binary
-------------------------------------------------
    local> starcluster sshmaster [CLUSTER_NAME] -u sgeadmin
    sgeadmin> workon tabular_predDB
    sgeadmin> make bin

Setting up password login via ssh
---------------------------------
    local> starcluster sshmaster [CLUSTER_NAME]
    root> perl -pi.bak -e 's/PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config
    root> service ssh reload
    root> echo "sgeadmin:[PASSWORD]" | chpasswd

## [Creating an AMI](http://docs.aws.amazon.com/AWSEC2/latest/CommandLineReference/ApiReference-cmd-CreateImage.html) from booted instance

* Determine the instance id of the instance you want to create an AMI from.  You can list all instances with 'starcluster listinstances'
* make sure you have your private key and X.509 certificate

Note, this will temporarily shut down the instance

    local> nohup ec2cim [instance-id] --name [NAME] -d [DESCRIPTION] -K ~/.ssh/PRIVATE_KEY_FILE -C ~/.ssh/CERT_FILE >out 2> err


This will start the process of creating the AMI.  It will print 'IMAGE [AMI-NAME]' to the file 'out'.  Record AMI-NAME and modify ~/.starcluster/config to use that for the tabular_predDB cluster's NODE\_IMAGE\_ID.

<!---
Caching HTTPS password
----------------------
When a StarCluster machine is spun up, its .git origin is changed to the github https address.  You can perform git operations but github repo operations will require a password.  You can cache the password by performing the following operations (from the related github [help page](https://help.github.com/articles/set-up-git#password-caching))

     sgeadmin> git config --global credential.helper cache
     sgeadmin> git config --global credential.helper 'cache --timeout=3600'

This requires git 1.7.10 or higher.  To get on ubuntu, do
sudo add-apt-repository ppa:git-core/ppa
sudo apt-get update
sudo apt-get install git
--->