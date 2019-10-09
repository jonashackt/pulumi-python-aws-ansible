# pulumi-example-aws-python
Example project playing around with Pulumi

### What is Pulumi?

In contrast to other Infrastructure-as-Code tools, Pulumi uses real programming languages instead of YAML to define infrastructure code:

> At the center of Pulumi is an open-source cloud object model & an evaluation runtime (https://www.pulumi.com/docs/intro/concepts/)

This cloud object model is language agnostic to support multiple programming languages at the same time ([currently Node.js/JavaScript & Python. And there's a Preview for Go and the possibility to implement your own Language](https://www.pulumi.com/docs/intro/languages/)). The evaluation runtime is knows about the cloud resources and how to plan, manage & execute them.

Pulumi Project is a folder with a `Pulumi.yaml` - create with `pulumi new`. 

Pulumi Stacks are like stages (dev, stage, production).


## Prerequisites

#### Install Pulumi

https://www.pulumi.com/docs/get-started/aws/

Install Pulumi SDK:

`brew install pulumi`


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



### A clean Python environment with virtualenv

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
# OR .venv/bin/activate
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


### Pulumi first run

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



### A comparable Use Case

As we want to compare Pulumi (in terms of apples vs. bananas ;P ) with other Infrastructure-as-Code tools like Ansible. Therefore we should pick a use case like the one in https://github.com/jonashackt/molecule-ansible-docker-vagrant - which is "Installing Docker on an EC2 Ubuntu box".

Let's delete the initial stack and S3 bucket first. To destroy an existing stack and its resources, simply run:

```
pulumi destroy
```

##### Build a common ground: Create an EC2 instance with SSH access

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


##### Install Docker on EC2 instance

So EC2's running, now we want to install Docker on it. But is there a way on how to issue shell commands and the like with Pulumi?

There's this issue: https://github.com/pulumi/pulumi/issues/99 (still open...)



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


