# pulumi-python-aws-ansible
[![Build Status](https://travis-ci.org/jonashackt/pulumi-python-aws-ansible.svg?branch=master)](https://travis-ci.org/jonashackt/pulumi-python-aws-ansible)
[![License](http://img.shields.io/:license-mit-blue.svg)](https://github.com/jonashackt/spring-boot-vuejs/blob/master/LICENSE)
[![renovateenabled](https://img.shields.io/badge/renovate-enabled-yellow)](https://renovatebot.com)
[![versionpulumi](https://img.shields.io/github/pipenv/locked/dependency-version/jonashackt/pulumi-python-aws-ansible/pulumi?color=brightgreen)](https://www.pulumi.com/)
[![versionawscli](https://img.shields.io/github/pipenv/locked/dependency-version/jonashackt/pulumi-python-aws-ansible/awscli?color=brightgreen)](https://aws.amazon.com/cli/)
[![versionansible](https://img.shields.io/github/pipenv/locked/dependency-version/jonashackt/pulumi-python-aws-ansible/ansible?color=brightgreen)](https://docs.ansible.com/ansible/latest/index.html)

Example project showing how to use Pulumi locally & with TravisCI to create Infrastructure on AWS 

[![asciicast](https://asciinema.org/a/273687.svg)](https://asciinema.org/a/273687)

See https://github.com/jonashackt/pulumi-talk#what-is-pulumi for more info on "What is Pulumi?".


## Prerequisites

#### Install Pulumi

https://www.pulumi.com/docs/get-started/install/

Install Pulumi SDK on MacOS:

`brew install pulumi`

or on Linux:

`curl -fsSL https://get.pulumi.com | sh`


If you choose to use Python as your preferred language for Pulumi, you should also install Python:

`brew install python`


#### Configure AWS credentials 

Like already described in https://github.com/jonashackt/molecule-ansible-docker-vagrant#install--configure-aws-cli, we need to do the following:


First we need to sure to have the [AWS CLI installed](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html). We can do this via Python pip package manager with (or any other system package manager):
 
```
pip3 install awscli
```
 
Now we should check, if AWS CLI was successfully installed. The `aws --version` command should print out sometime like:

```
$ aws --version
aws-cli/1.16.255 Python/3.7.4 Darwin/18.7.0 botocore/1.12.245
```

Now configure the AWS CLI to use the correct credentials. [According to the AWS docs](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html#cli-quick-configuration), the fastest way to accomplish that is to run `aws configure`:

```
$ aws configure
AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE
AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
Default region name [None]: eu-central-1
Default output format [None]: json
```


## An example Project with AWS & Python

Let's create an Pulumi example project using Python and AWS. Therefore create an empty directory:

```
mkdir pulumi-aws-python-example
cd pulumi-aws-python-example
```

Now create a Pulumi project with: `pulumi new aws-python`. Then you're promted to login to Pulumi (for more info about that, visit https://www.pulumi.com/docs/troubleshooting/faq/#how-does-pulumi-depend-on-pulumi-com), if you run `pulumi new` for the first time:

```
Manage your Pulumi stacks by logging in.
Run `pulumi login --help` for alternative login options.
Enter your access token from https://app.pulumi.com/account/tokens
    or hit <ENTER> to log in using your browser                   :
```

I used GitHub to authorize Pulumi Cloud in my Browser:

![pulumi-cli-login](screenshots/pulumi-cli-login.png)

Now the console needs our attention again - Pulumi want's to know about __project name__, __description__, __stack name__:

```
  Welcome to Pulumi!

  Pulumi  helps you create, deploy, and manage infrastructure on any cloud using
  your favorite language. You can get started today with Pulumi at:

      https://www.pulumi.com/docs/get-started/

This command will walk you through creating a new Pulumi project.

Enter a value or leave blank to accept the (default), and press <ENTER>.
Press ^C at any time to quit.

project name: (pulumi-aws) pulumi-example-aws-python
project description: (A minimal AWS Python Pulumi program)
Created project 'pulumi-example-aws-python'

Please enter your desired stack name.
To create a stack in an organization, use the format <org-name>/<stack-name> (e.g. `acmecorp/dev`).
stack name: (dev) jonashackt/dev
Created stack 'dev'
```

Then in case of AWS Pulumi needs a region to be used. For me I use `eu-central-1`:

```
aws:region: The AWS region to deploy into: (us-east-1) eu-central-1
Saved config
```

Now we're already finished:

```
Your new project is ready to go! ✨

To perform an initial deployment, run the following commands:

   1. virtualenv -p python3 venv
   2. source venv/bin/activate
   3. pip3 install -r requirements.txt

Then, run 'pulumi up'
```

Now you can also login to pulumi.com - I use `jonashackt` as the organisation, so you'll find my projects under: https://app.pulumi.com/jonashackt

![pulumi-com-project-overview](screenshots/pulumi-com-project-overview.png)



#### A clean Python environment with virtualenv

Before running `pulumi up`, you should install [virtualenv](https://virtualenv.pypa.io/en/latest/installation/), which is basically a project local dependency management for pip packages (this is also referred to as a good Python package dependency user style). If you're a Maven, Gradle, NPM user - think of a project local directory, where the all your dependecies are downloaded:

```
# On MacOS or Windows, simply do a
pip install virtualenv

# be more careful on Linux distros, e.g. use your distro's package manager for installation or use pip install --user virtualenv
```

Now we have to configure `virtualenv` to create the virtual pip environment - this will create a new directory `venv` inside your project folder:

```
virtualenv -p python3 venv
```

The `-p python3` option tells virtualenv to use the Python interpreter with version 3. Now we also need to `activate` the new isolated Python environment - and virtualenv provides us with a script to do so:

```
source venv/bin/activate
```

`source` is just a synonym for `.`, which simply [executes something on a shell](https://superuser.com/a/46146/497608). To run a check, if you're using the isolated virtualenv's Python now, run a `pip3 -V`. It should contain the correct path to your project:

```
$ pip3 -V
pip 19.2.3 from /Users/jonashecht/dev/pulumi-aws/venv/lib/python3.7/site-packages/pip (python 3.7)

# whereas the non-isolated Python would give something like this (on MacOS using brew):
pip 19.1.1 from /usr/local/lib/python3.7/site-packages/pip (python 3.7)
# then something would be missing - try some research on https://virtualenv.pypa.io/en/latest/userguide/
```

Finally we are now installing this Pulumi project's dependencies with:

```
pip3 install -r requirements.txt
```


#### Pulumi first run

Now we should have everything prepared to run Pulumi with `pulumi up`:

```
(venv)  jonashecht  ~/dev/pulumi-aws   master ●  pulumi up
Please choose a stack, or create a new one: dev
Previewing update (dev):

     Type                 Name                           Plan
 +   pulumi:pulumi:Stack  pulumi-example-aws-python-dev  create
 +   └─ aws:s3:Bucket     my-bucket                      create

Resources:
    + 2 to create

Do you want to perform this update? details
+ pulumi:pulumi:Stack: (create)
    [urn=urn:pulumi:dev::pulumi-example-aws-python::pulumi:pulumi:Stack::pulumi-example-aws-python-dev]
    + aws:s3/bucket:Bucket: (create)
        [urn=urn:pulumi:dev::pulumi-example-aws-python::aws:s3/bucket:Bucket::my-bucket]
        [provider=urn:pulumi:dev::pulumi-example-aws-python::pulumi:providers:aws::default_1_5_0::04da6b54-80e4-46f7-96ec-b56ff0331ba9]
        acl         : "private"
        bucket      : "my-bucket-58790f7"
        forceDestroy: false

Do you want to perform this update?
```

After choosing a stack to perform the action on, Pulumi outlines everything it will do when we choose `yes` to perform the update. Open the `details` to see everything in much more depth.

Then choose `yes` and Pulumi runs the update:

```
Updating (dev):

     Type                 Name                           Status
 +   pulumi:pulumi:Stack  pulumi-example-aws-python-dev  created
 +   └─ aws:s3:Bucket     my-bucket                      created

Outputs:
    bucket_name: "my-bucket-33cba3e"

Resources:
    + 2 created

Duration: 9s

Permalink: https://app.pulumi.com/jonashackt/pulumi-example-aws-python/dev/updates/1
```

You can have a look at the link provided and you'll see your Pulumi console:

![pulumi-first-run](screenshots/pulumi-first-run.png)

The example project creates a S3 bucket, which you could also check out by clicking onto the `Open in AWS console` button:

![aws-s3-console](screenshots/aws-s3-console.png)

That's it: this is our first Cloud resource created by Pulumi!



## A comparable Use Case

As we want to compare Pulumi (in terms of apples vs. bananas ;P ) with other Infrastructure-as-Code tools like Ansible. Therefore we should pick a use case like the one in https://github.com/jonashackt/molecule-ansible-docker-vagrant - which is "Installing Docker on an EC2 Ubuntu box".

Let's delete the initial stack and S3 bucket first. To destroy an existing stack and its resources, simply run:

```
pulumi destroy
```

#### Build a common ground: Create an EC2 instance with SSH access

Let's have a look into the tutorials: https://www.pulumi.com/docs/tutorials/aws/ec2-webserver/

and the Pulumi API reference -> https://www.pulumi.com/docs/reference/pkg/python/pulumi_aws/

Yeah, now we should be able to setup our first EC2 instance with Pulumi. Open [__main__.py](__main__.py) in your IDE and add some code:

```
import pulumi
import pulumi_aws as aws
from pulumi_aws import ec2

# AMI image configuration
ec2_image_id = 'ami-0cc0a36f626a4fdf5'
ec2_image_owner = '099720109477'
ec2_instance_size = 't2.micro'
ec2_instance_name = 'aws-ec2-ubuntu'

# Lets use Pulumi to get the AMI image
pulumi_ami = aws.get_ami(
                    filters = [{ "name": "image-id", "values": [ec2_image_id]}],
                    owners  = [ec2_image_owner])

# Create a EC2 security group
ssh_port = 22

pulumi_security_group = ec2.SecurityGroup(
                            'pulumi-secgrp',
                            description = 'Enable HTTP access',
                            ingress = [
                                { 'protocol': 'tcp', 'from_port': ssh_port, 'to_port': ssh_port, 'cidr_blocks': ['0.0.0.0/0'] }
                            ]
)

# Create EC2 instance
ec2_instance = ec2.Instance(
                    ec2_instance_name,
                    instance_type = ec2_instance_size,
                    security_groups = [pulumi_security_group.name],
                    ami = pulumi_ami.id
)

pulumi.export('publicIp', ec2_instance.public_ip)
pulumi.export('publicHostName', ec2_instance.public_dns)


```

> Maybe you find yourself lost in the Pulumi documentation like me: Many things are simply not available right now. E.g. the Pulumi AWS provider is derived from the Terraform AWS provider - so have a look there: https://www.terraform.io/docs/providers/aws/index.html!
> If you look for aws.get_ami special `owners` parameter, have a look at https://www.terraform.io/docs/providers/aws/d/ami.html

Let's first choose an AMI as described in [Choosing an Ubuntu 18.04 AMI](https://github.com/jonashackt/molecule-ansible-docker-vagrant#choosing-an-ubuntu-1804-ami) using the [ubuntu Amazon EC2 AMI Locator](https://cloud-images.ubuntu.com/locator/ec2/). Combine your AWS region and the desired Ubuntu version and type this into the search box:

```
eu-central-1 18.04 LTS
```

Now choose the latest AMI id with the Instance Type `hvm:ebs-ssd` like this: `ami-0cc0a36f626a4fdf5`

> Preventing the "Exception: invoke of aws:index/getAmi:getAmi failed: "owners": required field is not set ()"

If you're also just starting with Pulumi, you may also wonder if we __really need__ the `owners` parameter in the module `aws.get_ami`.

Well - this one is required - have a look at https://www.terraform.io/docs/providers/aws/d/ami.html#owners. So to prevent the mentioned Exception we need to also provide the valid `owners` id for the Ubuntu image. Having a look at the AWS docs, these ids could be found occasionally: https://docs.aws.amazon.com/de_de/AWSEC2/latest/UserGuide/finding-an-ami.html#finding-quick-start-ami

The Ubuntu owners id is `099720109477` for example, the RedHat AMIs need the `309956199498` and so on. Amazon images simply need `amazon` or `aws-marketplace`, Microsoft images have `microsoft` also.

Now give your Pulumi code a try and fire it up with `pulumi up`. This should give something like:

```
$ pulumi up
Previewing update (dev):

     Type                      Name                           Plan
 +   pulumi:pulumi:Stack       pulumi-example-aws-python-dev  create
 +   ├─ aws:ec2:SecurityGroup  pulumi-secgrp                  create
 +   └─ aws:ec2:Instance       aws-ec2-ubuntu                 create

Resources:
    + 3 to create

Do you want to perform this update? yes
Updating (dev):

     Type                      Name                           Status
 +   pulumi:pulumi:Stack       pulumi-example-aws-python-dev  created
 +   ├─ aws:ec2:SecurityGroup  pulumi-secgrp                  created
 +   └─ aws:ec2:Instance       aws-ec2-ubuntu                 created

Outputs:
    publicHostName: "ec2-3-120-32-194.eu-central-1.compute.amazonaws.com"
    publicIp      : "3.120.32.194"

Resources:
    + 3 created

Duration: 33s

Permalink: https://app.pulumi.com/jonashackt/pulumi-example-aws-python/dev/updates/3
```

Have a look into your AWS management console and you should see the new instance:

![first-ec2-instance-running](screenshots/first-ec2-instance-running.png)


On console you can also [access the variables exported](https://www.pulumi.com/docs/reference/pkg/python/pulumi/#stack-exports%C2%B6) with `pulumi.export` like:

```
$ pulumi stack output publicHostName
ec2-3-120-235-112.eu-central-1.compute.amazonaws.com

# or

$ pulumi stack output publicIp
3.120.235.112
```


## Run Pulumi with Travis

Now that we're able to run our Pulumi code against AWS, we should also configure Travis to do the job for us every time we push our code.

Most of the needed parts on how to execute a Python library on Travis to connect to AWS has been already described here: https://github.com/jonashackt/molecule-ansible-docker-vagrant#use-travisci-to-execute-molecule-with-ec2-infrastructure


#### Configure TravisCI to connect to AWS & app.pulumi.com

So let's create a [.travis.yml](.travis.yml), that doesn't contain so much in the first place:

```yaml
sudo: false
language: python

env:
- BOTO_CONFIG="/dev/null"
```

After that, we should activate TravisCI for our project at https://travis-ci.org/account/repositories. 

And we should already now think about the needed Pulumi login to `app.pulumi.com`, which could be done by defining the `PULUMI_ACCESS_TOKEN` variable, that needs to contain a correct access token. To create a Pulumi access token, head over to https://app.pulumi.com/yourUserNameHere/settings/tokens and click on `NEW ACCESS TOKEN`:

![app-pulumi-com-access-token](screenshots/app-pulumi-com-access-token.png)

Now we can switch over to the settings page of our Travis configuration at https://travis-ci.org/jonashackt/pulumi-example-aws-python/settings and create the needed environment variables `AWS_ACCESS_KEY` & `AWS_SECRET_KEY` for the `aws configure set` command and the `PULUMI_ACCESS_TOKEN` variable:

![travis-env-aws-pulumi-access-vars](screenshots/travis-env-aws-pulumi-access-vars.png)


Inside the `install` section of our `.travis.yml` we are now able to install and configure the boto packages & the AWS CLI, which Pulumi later uses to communicate with AWS:

```yaml
install:
# install AWS related packages
- pip install boto boto3
- pip install --upgrade awscli
# configure AWS CLI
- aws configure set aws_access_key_id $AWS_ACCESS_KEY
- aws configure set aws_secret_access_key $AWS_SECRET_KEY
- aws configure set default.region eu-central-1
# show AWS CLI config
- aws configure list
```

To avoid [the knows problems with boto (the AWS python client) on Travis](aus dem Weg gehen), we already defined `sudo: false` and configured the `BOTO_CONFIG="/dev/null"` environment variable directly inside our [.travis.yml](.travis.yml). With that our AWS communication should work like a charm.


#### Install & configure Pulumi on TravisCI

Now we should also install the Pulumi SDK - as we already did locally. This time, we use Python's pip to do that for us: 

```
script:
  # Install Pulumi SDK with the installation script from https://www.pulumi.com/docs/get-started/install/#installation-script
  - curl -fsSL https://get.pulumi.com | sh
  # Add Pulumi to Travis' PATH so the executable could be found
  - export PATH=$PATH:/home/travis/.pulumi/bin
  - pulumi version
  # login to app.pulumi.com with the predefined PULUMI_ACCESS_TOKEN
  - pulumi login
```

As you see, we add the Pulumi executable to the Travis build environments' PATH, otherwise we run into `pulumi: command not found` errors. We also log in to app.pulumi.com.


#### Fire up Pulumi on TravisCI

Now we're nearly there! But as we're running on TravisCI, we should skip the virtualenv usage - since TravisCI's Python environment is already based on a virtualenv configuration (see https://docs.travis-ci.com/user/languages/python/#travis-ci-uses-isolated-virtualenvs).
Therefore we only need to install the libraries needed via `pip install -r requirements.txt`:

```yaml
script:
...
  # skip virtualenv in virtualenv Travis inception (see https://docs.travis-ci.com/user/languages/python/#travis-ci-uses-isolated-virtualenvs)
  # and simply install pip libraries directly (otherwise pulumi: command not found error will come after us again)
  - pip install -r requirements.txt

  # Select your Pulumi projects' stack
  - pulumi stack select dev
```

Before running `pulumi up`, we have to select the stack Pulumi should use. Otherwise we'll run into `error: no stack selected;` errors. You can list your stacks on the command line with `pulumi stack ls` or have a look into the Pulumi online portal at https://app.pulumi.com/yourUserNameHere.

The final step then is to fire up Pulumi (and destroy the infrastructure again after it was created to prevent unnecessary costs):

```yaml
script:
...
  # Run Pulumi unattended
  - pulumi up --yes
  # After everything has been created, we should also destroy the infrastructure again
  - pulumi destroy --yes
```

Mind the `--yes` switch at the end of the commands to automatically approve and perform the update/destruction after previewing it 

You may now have a look into your TravisCI build ([like this](https://travis-ci.org/jonashackt/pulumi-example-aws-python/builds/596168913)). It should show an output similar to this at the end of the log:

```
$ 

The command "" exited with 0.

0.69s$ pulumi stack select dev

The command "pulumi stack select dev" exited with 0.

49.93s$ pulumi up --yes

Previewing update (dev):

 +  pulumi:pulumi:Stack pulumi-example-aws-python-dev create 

 +  aws:ec2:SecurityGroup pulumi-secgrp create 

 +  aws:ec2:Instance aws-ec2-ubuntu create 

 +  pulumi:pulumi:Stack pulumi-example-aws-python-dev create 

 

Resources:

    + 3 to create

Updating (dev):

 +  pulumi:pulumi:Stack pulumi-example-aws-python-dev creating 

 +  aws:ec2:SecurityGroup pulumi-secgrp creating 

 +  aws:ec2:SecurityGroup pulumi-secgrp created 

 +  aws:ec2:Instance aws-ec2-ubuntu creating 

@ Updating.....

 +  aws:ec2:Instance aws-ec2-ubuntu created 

 +  pulumi:pulumi:Stack pulumi-example-aws-python-dev created 

 

Outputs:

    publicHostName: "ec2-18-195-71-41.eu-central-1.compute.amazonaws.com"

    publicIp      : "18.195.71.41"

Resources:

    + 3 created

Duration: 45s

Permalink: https://app.pulumi.com/jonashackt/pulumi-example-aws-python/dev/updates/11

The command "pulumi up --yes" exited with 0.

58.06s$ pulumi destroy --yes

Previewing destroy (dev):

 -  aws:ec2:Instance aws-ec2-ubuntu delete 

 -  aws:ec2:SecurityGroup pulumi-secgrp delete 

 -  pulumi:pulumi:Stack pulumi-example-aws-python-dev delete 

 -  pulumi:pulumi:Stack pulumi-example-aws-python-dev delete 

 

Outputs:

  - publicHostName: "ec2-18-195-71-41.eu-central-1.compute.amazonaws.com"

  - publicIp      : "18.195.71.41"

Resources:

    - 3 to delete

Destroying (dev):

 -  aws:ec2:Instance aws-ec2-ubuntu deleting 

@ Destroying.....

 -  aws:ec2:Instance aws-ec2-ubuntu deleted 

 -  aws:ec2:SecurityGroup pulumi-secgrp deleting 

 -  aws:ec2:SecurityGroup pulumi-secgrp deleted 

 -  pulumi:pulumi:Stack pulumi-example-aws-python-dev deleting 

 -  pulumi:pulumi:Stack pulumi-example-aws-python-dev deleted 

 

Outputs:

  - publicHostName: "ec2-18-195-71-41.eu-central-1.compute.amazonaws.com"

  - publicIp      : "18.195.71.41"

Resources:

    - 3 deleted

Duration: 56s

Permalink: https://app.pulumi.com/jonashackt/pulumi-example-aws-python/dev/updates/12

The resources in the stack have been deleted, but the history and configuration associated with the stack are still maintained. 

If you want to remove the stack completely, run 'pulumi stack rm dev'.

The command "pulumi destroy --yes" exited with 0.

Done. Your build exited with 0.
```

You can also have a look into the AWS management console to see the EC2 instance beeing created and then destroyed again.



## Install Docker on EC2 instance

So EC2's running, now we want to install Docker on it. But is there a way on how to issue shell commands and the like with Pulumi?

The answer is: NO! There's currently no way to do this (see https://github.com/pulumi/pulumi/issues/99).  

If you want to know more about that topic, have a look into: https://github.com/jonashackt/pulumi-talk#provision-yes-configure-no

At the end, [Pulumi website tells us](https://www.pulumi.com/docs/intro/vs/chef_puppet_etc/) how to deal with such a problem:
 
> Simply use Chef, Puppet, Ansible or Salt here!

Ok, since Ansible leads the pack, we'll use that right away!


#### Creating an EC2 keypair with Ansible & firing up an EC2 instance with Pulumi

So let's use the Pulumi AWS documentation (sorry, we need to use the JavaScript docs here, since the Python docs aren't quite good right now): https://www.pulumi.com/docs/reference/pkg/nodejs/pulumi/aws/

And inside the [aws.ec2.Instance](https://www.pulumi.com/docs/reference/pkg/nodejs/pulumi/aws/ec2/#Instance) there's a parameter [keyName](https://www.pulumi.com/docs/reference/pkg/nodejs/pulumi/aws/ec2/#Instance-keyName) which uses the type [aws.ec2.KeyPair](https://www.pulumi.com/docs/reference/pkg/nodejs/pulumi/aws/ec2/#KeyPair), which is sadly not linked in the docs - but you can find it looking into the ec2 docs again searching for `keypair`: https://www.pulumi.com/docs/reference/pkg/nodejs/pulumi/aws/ec2/. But the docs also state, that

> Currently this resource requires an existing user-supplied key pair. This key pair’s public key will be registered with AWS to allow logging-in to EC2 instances.

So it seems that we have to provide our own keypair to use this module :(

Compared to the Ansible [ec2_key module](https://docs.ansible.com/ansible/latest/modules/ec2_key_module.html), __this is rather astonishing__. So we could only use the Pulumi [aws.ec2.KeyPair module](https://www.pulumi.com/docs/reference/pkg/nodejs/pulumi/aws/ec2/#KeyPair) as a wrapper around an EC2 keypair, that has to be generated elsewhere.

So let's do that also with Ansible. We simply create a [keypair.yml](keypair.yml), that creates a new EC2 keypair, if there's no local private key already. The generated private key is then saved to `.ec2ssh/pulumi_key` inside the projects directory:

```yaml
- name: Create EC2 Keypair
  hosts: localhost
  connection: local
  gather_facts: false
  vars:
    keypair_name: pulumi_key
    keypair_path: ".ec2ssh//{{ keypair_name }}"
  tasks:
    - name: Be sure to have .ec2ssh as local directory present
      file:
        path: ".ec2ssh"
        state: directory

    - name: Test for presence of local keypair
      stat:
        path: "{{ keypair_path }}"
      register: keypair_local

    - name: Delete remote keypair
      ec2_key:
        name: "{{ keypair_name }}"
        state: absent
      when: not keypair_local.stat.exists

    - name: Create keypair
      ec2_key:
        name: "{{ keypair_name }}"
      register: keypair

    - name: Persist the keypair
      copy:
        dest: "{{ keypair_path }}"
        content: "{{ keypair.key.private_key }}"
        mode: 0600
      when: keypair.changed
```

To run the playbook you should have Ansible installed on our system:

`pip install ansible`

Run the Ansible playbook now to generate the EC2 keypair:

```
ansible-playbook keypair.yml
```

Now a file called `pulumi_key` should be generated. This is the private key of our new EC2 key pair. You can find the key pair also in the AWS EC2 management console:

![aws-ec2-keypair](screenshots/aws-ec2-keypair.png)

The last part is to tell Pulumi, that this new key pair should be used at the EC2 instance creation time. Therefore we change our Pulumi Python code in [__main__.py](__main__.py) and add the `key_name` parameter to the `ec2.Instance()` call:

```python
...
ec2_keypair_name = 'pulumi_key'
...
# Create EC2 instance
ec2_instance = ec2.Instance(
                    ec2_instance_name,
                    key_name = ec2_keypair_name,
                    instance_type = ec2_instance_size,
                    security_groups = [pulumi_security_group.name],
                    ami = pulumi_ami.id
)
...
```

Now we should create a new Pulumi stack (and therefore destroy the old one first):

```
$ pulumi destroy --yes
$ pulumi up --yes
```


#### SSH connection to the Pulumi created EC2 instance

With that [the key pair's public key is configured inside our new EC2 instance](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html) and is ready to be used. Ansible should now be able to connect to that machine via SSH, so we need a playbook to read the `public IP` from the Pulumi stack and connect to the EC2 instance. Let's open our [playbook.yml](playbook.yml):

```yaml
- name: Connect to Pulumi created EC2 instance and install Docker
  hosts: localhost
  connection: local
  vars:
    keypair_name: pulumi_key
    keypair_path: ".ec2ssh//{{ keypair_name }}"
    # this is really important to configure, since Ansible will use this user for SSH connection
    ssh_user: ubuntu
  tasks:
    - name: Gather Pulumi created EC2 instance public IP
      shell: pulumi stack output publicIp
      register: pulumi_stack_output

    - set_fact:
        ec2_public_ip: "{{ pulumi_stack_output.stdout }}"

    - debug:
        msg: "The public IP of the Pulumi created EC2 instance is: {{ ec2_public_ip }}"

    - name: Wait 300 seconds for port 22 to become open and contain "SSH" - then the SSH connection should work afterwards
      wait_for:
        port: 22
        host: "{{ ec2_public_ip }}"
        search_regex: SSH
        delay: 10
        timeout: 320
```

To prevent waiting command prompts like this:

```
The authenticity of host '3.120.32.99 (3.120.32.99)' can't be established.
ECDSA key fingerprint is SHA256:+1Pb+VPlnUntX1E6bnegvpdU7qEPbxAsdXN6mFDgtZY.
Are you sure you want to continue connecting (yes/no)
```

We should also create a proper [ansible.cfg](ansible.cfg) containing `ssh_args = -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no`.

If nothing seems to work, you can debug the SSH connection with direct usage of Ansible ping module like this (insert the public IP retrieved by `pulumi stack output publicIp` and append a `,`):

```
ansible -i 3.120.32.99, -m ping all --user=ubuntu --private-key=.ec2ssh/pulumi_key -vvv
```

#### Configure outgoing traffic for apt with a second Security group rule ("egress")

Now we finally want to use the ansible-galaxy provided Ansible role 'docker' to install Docker on our Pulumic created EC2 instance!

First thing: we should prevent outgoing connection errors like this:

```bash
        "0% [Connecting to eu-central-1.ec2.archive.ubuntu.com (52.59.228.109)] [Connect\u001b[0m",
        "                                                                               ",
        "Err:2 http://eu-central-1.ec2.archive.ubuntu.com/ubuntu bionic InRelease",
        "  Could not connect to eu-central-1.ec2.archive.ubuntu.com:80 (52.59.244.233)
```

Therefore we need to create an EC2 __egress__ Security role also inside our Pulumi program [__main__.py](__main__.py) (have a look into the Pulumi [ec2.Security resource docs](https://www.pulumi.com/docs/reference/pkg/nodejs/pulumi/aws/ec2/#SecurityGroup)))

```python
# Create a EC2 security group
pulumi_security_group = ec2.SecurityGroup(
                            'pulumi-secgrp',
                            description = 'Enable HTTP access',
                            ingress = [
                                { 'protocol': 'tcp', 'from_port': ec2_ssh_port, 'to_port': ec2_ssh_port, 'cidr_blocks': ['0.0.0.0/0'] }
                            ],
                            egress = [
                                { 'protocol': '-1', 'from_port': 0, 'to_port': 0, 'cidr_blocks': ['0.0.0.0/0'] }
                            ]
)
```

A crucial point here is to set the __egress__ `protocol` to `-1`, since this is semantically equivalent to `"all"`, which is needed for successful outgoing communication of the package manager `apt-get` we need to use for the Docker installation. Inside the AWS EC2 management console, the `Outbound` configuration has to look like this:

![aws-security-group-egress-outgoing-all-traffic](screenshots/aws-security-group-egress-outgoing-all-traffic.png)
 
__Don't try to look that up inside the Pulumi docs, it's not there!__ But follow the link to [the Terraform docs, there you'll find this specific parameter configuration](https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/security_group.html.markdown#argument-reference).

Now apt should be able to talk to the outside world finally.


#### Reuse Ansible role 'docker' with ansible-galaxy CLI & requirements.yml

Now we need a Ansible role that installs Docker on Ubuntu for us. That problem is already solved for us (again) in https://github.com/jonashackt/molecule-ansible-docker-vagrant 
But since we don't want to copy the role, we use Ansible-Galaxy CLI to do that for us. [There's a nice not so much advertised feature](https://docs.ansible.com/ansible/latest/reference_appendices/galaxy.html#installing-multiple-roles-from-a-file) of `ansible-galaxy`, where you only have to provide a `requirements.yml` with the needed role with their git urls. So let's create our own [requirements.yml](requirements.yml):

```yaml
# dependency to docker role
- src: https://github.com/jonashackt/molecule-ansible-docker-vagrant
  name: docker
```

Now use `ansible-galaxy` CLI to download the role into the standard `/roles` directory, where your play/role could use it:

```
ansible-galaxy install -r requirements.yml -p roles/
```

Now the Ansible role should reside at [roles/docker/tasks/main.yml](roles/docker/tasks/main.yml) and is ready to be used!


##### Use our role to install Docker on Ubuntu

Now we finally want to use the ansible-galaxy provided Ansible role 'docker' to install Docker on our Pulumic created EC2 instance!

Let's open our [playbook.yml](playbook.yml) again:

```yaml
    # Since the docker role needs facts like ansible_distribution & ansible_lsb.codename, we need to gather those facts beforehand
    # from our delegate_to host (EC2 instance)
    - name: Gather facts of Pulumi created EC2 instance for later role execution
      setup:
      delegate_to: "{{ ec2_public_ip }}"
      vars:
        ansible_ssh_private_key_file: "{{ keypair_path }}"
        ansible_user: ubuntu

    - name: Now use the ansible-galaxy prepared docker role to install Docker on our EC2 instance
      import_role:
        name: docker
      delegate_to: "{{ ec2_public_ip }}"
      become: true
      vars:
        ansible_ssh_private_key_file: "{{ keypair_path }}"
        ansible_user: ubuntu
```

With the first usage of Ansible's [setup module](https://docs.ansible.com/ansible/latest/modules/setup_module.html) we're able to gather facts based dynamically on our Pulumi created host. In order to use this dynamic host, we use Ansible's [Delegation feature](https://docs.ansible.com/ansible/latest/user_guide/playbooks_delegation.html#delegation) with the keyword `delegate_to`.

We also need to set the `ansible_ssh_private_key_file` and `ansible_user` SSH connection properties correctly to the keypair we used to create our EC2 instance using Pulumi.

In the last step we finally use our role `docker` to install Docker on our Pulumi created EC2 instance. Simply run our playbook with: 

```
ansible-playbook playbook.yml
```

I also created a shell script [create_all.sh](create_all.sh) that contains all neccessary steps in the right order:

```shell script
#!/usr/bin/env bash
set -euo pipefail

echo "destroy pre-created Pulumi instances"
pulumi destroy --yes

echo "generate EC2 keypair and save private key locally (since Pulumi isn't able to do that now)"
ansible-playbook keypair.yml

echo "execute Pulumi to create EC2 instances"
pulumi up --yes

echo "Downloading the Ansible role 'docker' with ansible-galaxy"
ansible-galaxy install -r requirements.yml -p roles/

echo "run Ansible role to install Docker on Ubuntu"
ansible-playbook playbook.yml
```

Run it with `./create_all.sh`!

And here's also a recording of the whole thing:

[![asciicast](https://asciinema.org/a/273830.svg)](https://asciinema.org/a/273830)


##### Replace direct usage of virtualenv and pip with pipenv

While `virtualenv` does a great job to seperate Python build dependencies from different projects (and your system's pip packages), the `requirements.txt` doesn't lead to fully deterministic builds, because it doesn't manage transient dependencies - and Python packages tend to use unpinned dependencies -> so different environments could lead to different build outputs (see this article for more details: https://realpython.com/pipenv-guide/).

The solution for this is the use of [pipenv](https://github.com/pypa/pipenv), which effectively replaces the usage of pip and virtualenv and manages both for you. It also introduces two new files, which replace the requirements.txt: [Pipfile](https://github.com/pypa/pipfile) and `Pipfile.lock` to ensure deterministic builds.

To install `pipenv`, simply run

```
pip3 install pipenv
```

Now create a new virtual environment with

```
pipenv shell --python 3.7
```

Here, `--python 3.7` ensures a current Python 3 installation. 

Now we can use `pipenv` to install all required dependencies with 

```
pipenv install
```

We can now also add Ansible as a requirement, since our project depends on it (remember, we don't use `pip` command any more, only `pipenv` to install packages):

```
pipenv install ansible
```

##### Configure renovate and shields.io badges to use our pipenv managed versions

As this project is kept up-to-date by [renovate](https://github.com/renovatebot/renovate), we should configure the [renovate.json](renovate.json) configuration file to tell renovate about pipenv ([which is currently a beta feature](https://docs.renovatebot.com/configuration-options/#pipenv)):

```json
{
  "extends": [
    "config:base"
  ],
  "groupName": "all",
  "pipenv": {
    "enabled": true
  }
}
```

And as our project uses [shields.io badges](https://shields.io/category/platform-support) to show used dependency versions at the top of the [README.md](README.md), we should also configure them to be dynamically read from the [Pipfile](Pipfile).

There was a recent update to the dynamic shields.io endpoint (have a look into https://github.com/badges/shields/issues/2259#issuecomment-537699182 for more info), so we could upgrade our badges like that:

```
# old
[![versionansible](https://img.shields.io/badge/ansible-2.8.5-brightgreen.svg)](https://docs.ansible.com/ansible/latest/index.html)

# new
[![versionansible](https://img.shields.io/github/pipenv/locked/dependency-version/jonashackt/pulumi-python-aws-ansible/ansible?color=brightgreen)](https://docs.ansible.com/ansible/latest/index.html)
```

Now every badge stays up-to-date with every renovate update - like this one here: [![versionpulumi](https://img.shields.io/github/pipenv/locked/dependency-version/jonashackt/pulumi-python-aws-ansible/pulumi?color=brightgreen)](https://www.pulumi.com/)


##### Using pipenv on TravisCI

As we're now using `pipenv` for dependecy management, we could also rework our TravisCI configuration. [As this post states](https://medium.com/@dirk.avery/quirks-of-pipenv-on-travis-ci-and-appveyor-10d6adb6c55b) and we already learned, TravisCI uses `virtualenv` environment per default. Now `pipenv` is luckily smart enough to detect that, so all we have to do is the following inside our [.travis.yml](.travis.yml):

```yaml
sudo: false
language: python

env:
  - BOTO_CONFIG="/dev/null"

install:
  # Install pipenv dependency manager
  - pip install pipenv
  # Fire up pipenv shell
  - pipenv shell
  # Install required (and locked) dependecies from Pipfile.lock
  # skip virtualenv in virtualenv Travis inception (see https://docs.travis-ci.com/user/languages/python/#travis-ci-uses-isolated-virtualenvs)
  # and simply install pip libraries directly (otherwise pulumi: command not found error will come after us again)
  # pipenv is smart enough to recognise the existing virtualenv without a prior pipenv shell command (see https://medium.com/@dirk.avery/quirks-of-pipenv-on-travis-ci-and-appveyor-10d6adb6c55b)
  - pipenv install

  # configure AWS CLI
  - aws configure set aws_access_key_id $AWS_ACCESS_KEY
  - aws configure set aws_secret_access_key $AWS_SECRET_KEY
  - aws configure set default.region eu-central-1
  # show AWS CLI config
  - aws configure list
``` 



### Test-driven Development with Pulumi

https://www.pulumi.com/blog/testing-your-infrastructure-as-code-with-pulumi/


Testinfra??! Pytest


### Run a Dockerized application on AWS with Pulumi

Example app: https://github.com/jonashackt/spring-boot-vuejs

Pulumi API reference for the Pulumi Docker provider: https://www.pulumi.com/docs/reference/pkg/python/pulumi_docker/ (interestingly this Pulumi docker provider is derived from the [Terraform Docker provider](https://github.com/terraform-providers/terraform-provider-docker))

Second interesting point: The docs for the JavaScript/Typescript version of the Pulumi Docker provider are much nicer to view: https://www.pulumi.com/docs/reference/pkg/nodejs/pulumi/docker/



### Using AWS Fargate to run a Dockerized application



## Links

See example projects https://github.com/pulumi/examples

https://www.pulumi.com/docs/tutorials/aws/ec2-webserver/

https://blog.scottlowe.org/2019/05/05/a-sandbox-for-learning-pulumi/

Some also use Pulumi + Ansible already: https://blog.wallaroolabs.com/2018/10/spinning-up-a-wallaroo-cluster-is-easy/

