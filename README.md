# pulumi-aws
Example project playing around with Pulumi

### What is Pulumi?

In contrast to other Infrastructure-as-Code tools, Pulumi uses real programming languages instead of YAML to define infrastructure code:

> At the center of Pulumi is an open-source cloud object model & an evaluation runtime (https://www.pulumi.com/docs/intro/concepts/)

This cloud object model is language agnostic to support multiple programming languages at the same time (currently JavaScript, TypeScript, Python & Go). The evaluation runtime is knows about the cloud resources and how to plan, manage & execute them.

Pulumi Project is a folder with a `Pulumi.yaml` - create with `pulumi new`. 

Pulumi Stacks are like stages (dev, stage, production).


### Prerequisites

https://www.pulumi.com/docs/get-started/aws/

Install Pulumi SDK:

`brew install pulumi`


### HowTo

Let's create an Pulumi example project using Python and AWS. Therefore create an empty directory:

```
mkdir pulumi-aws-python-example
cd pulumi-aws-python-example
```

Now create a Pulumi project with: `pulumi new aws-python`. Then you're promted to login to Pulumi, if you run `pulumi new` for the first time:

```
Manage your Pulumi stacks by logging in.
Run `pulumi login --help` for alternative login options.
Enter your access token from https://app.pulumi.com/account/tokens
    or hit <ENTER> to log in using your browser                   :
```

I used GitHub to authorize Pulumi Cloud in my Browser:

![pulumi-cli-login](screenshots/pulumi-cli-login.png)

Now the console needs our attention again - Pulumi want's to know about project name, description, stack name

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

To run our first `pulumi up`: