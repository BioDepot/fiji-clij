# [CLIJ](https://clij.github.io/) Benchmarking Workflow in [Bwb](https://github.com/BioDepot/BioDepot-workflow-builder)

This repository contains a workflow for the Biodepot-workflow-builder
(Bwb) implementing a benchmarking workflow for CLIJ, a library and
extension for the Fiji image processing suite allowing the use of GPUs
for accelerated processing (using OpenCL).

The workflow implemented is the one described in the Supplementary
Materials section of the original CLIJ paper (see
[References](#References) below), with some modifications to adapt it
to the Bwb platform. Like all Bwb workflows, the benchmarking workflow
is containerized, which means it can be deployed on a more powerful
cloud server with minimal effort, and does not require installation of
anything besides Docker (and video drivers).

## Requirements

The workflow should be run on a machine with an NVIDIA GPU and
appropriate drivers installed. (Note that AMD GPUs are not currently
supported, as Bwb uses the `--gpus` option in Docker, which does not
support AMD GPUs at time of writing (this is an open issue, see
https://github.com/docker/cli/issues/2063 ). Use of a cloud server is
recommended; the workflow has been tested on Amazon Web Services'
`g4dn.*` instances, which have an NVIDIA Tesla V100 GPU. See [AWS
Setup](#aws-setup) below.

If using an AWS cloud server, the use of our Amazon Machine Image
(AMI) is recommended; this contains an installation of Ubuntu with all
the necessary GPU drivers and scripts to run the workflows
preinstalled. See [Using the AMI](#using-the-ami) below.

If you are not using an AWS cloud server or you do not wish to use the
AMI, see [Manual Installation](#manual-installation) below.

Bwb requires that Docker be installed ([instructions
here](https://github.com/BioDepot/BioDepot-workflow-builder#installing-and-starting-docker)). Additionally,
you will need to have the [NVIDIA Container Toolkit
installed](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html)
to make the GPU available to Docker containers.

## AWS Setup

The following are instructions for launching a virtual machine
instance on AWS to run the workflow. You will need to log in to the
[AWS console](https://aws.amazon.com) before continuing; additionally,
if you wish to use the AMI, you must make sure your region (found in
the top-right corner next to your username) is set to `us-east-2`
(Ohio), since the AMI is stored in that region.

If you are using the AMI, you may skip the steps [Launch
instance](#launch-instance) and [Choose an OS image](#choose-an-os-image)
below by using [this
link](https://console.aws.amazon.com/ec2/v2/home?region=us-east-2#LaunchInstanceWizard:ami=ami-0ae86208aad96a06e). Otherwise,
continue reading below.

### Launch instance

Go to the [EC2
Console](https://us-east-2.console.aws.amazon.com/ec2/home?region=us-east-2#Home:)
(can also be found by searching "EC2" from the main AWS console), and
press the orange "Launch Instance" button.

![A screenshot of the EC2 console, with the orange "Launch Instance"
button indicated.](readme-images/launch-instance.png)

The "Launch an instance" form will come up; first, give your instance
a name in the box at the top of the screen.

![A screenshot of the instance name field in the "Launch an instance"
form.](readme-images/instance-name.png)

### Choose an OS image

Next, you will need to choose an operating system image to be
installed on the instance. Scroll down to the "Application and OS Images"
section on the form, and make sure the "Quick Start" tab is selected.

![A screenshot of the "Application and OS Images" section on the form,
with the "Quick Start" tab selected.](readme-images/choose-image.png)

#### Option 1: If You Are Using the AMI

To select the AMI, click the "Browse more AMIs" button to the
right. Then, once the "Choose an Amazon Machine Image" page comes up,
select the "Community AMIs" tab, and search for
`bwb-clij-benchmarking-latest` to find the latest version of the
AMI. (Alternatively, you can search `bwb-clij-benchmarking` to bring
up specific versions to use.) 

Available versions are:
* `bwb-clij-benchmarking-latest` (AMI ID: `ami-0ae86208aad96a06e`) 
  * _NOTE_: The "latest" AMI is just a copy of the latest version of
    the AMI, but under a name that is easier to search; when a new
    version is released, the "latest" AMI is deleted and replaced with
    a copy of the new latest version.
* `bwb-clij-benchmarking_v0.4_20220926` (AMI ID: `ami-0a86efe9d0f29abf6`)
* `clij-benchmarking_v0.3_2022-07-05` (AMI ID: `ami-0e4eb88d9cacd5be9`)


![A screenshot of the "Choose an Amazon Machine Image" form, with the
latest version of the Bwb CLIJ AMI
shown.](readme-images/choose-ami.png)

When you have found the version of the AMI you want to use, click the
orange "Select" button on the right.

#### Option 2: If You Are Doing Manual Setup

If you are doing manual setup, click the "Ubuntu" button in the list
of operating systems and then choose Ubuntu Server 20.04 LTS from the
drop-down menu.

![A screenshot of the "Application and OS Images" section on the form,
with Ubuntu Server 20.04 LTS
selected.](readme-images/choose-image-manual.png)

### Choose an instance type

Next, you will need to choose the type of instance you wish to launch;
this will configure the hardware installed on the instance (CPU cores,
memory, etc.). Scroll down to the "Instance type" section of the
form. Then, click the drop-down menu and search for `g4dn`; the [G4dn
instances](https://aws.amazon.com/ec2/instance-types/g4/#Amazon_EC2_G4dn_Instances)
have NVIDIA GPUs installed, which are currently required for the
workflow. You can choose any of the G4dn instance types; they have
varying CPU core counts and memory/storage sizes (but larger ones may
also cost more per hour). We have tested the workflow on
`g4dn.2xlarge` instances, so we recommend this instance type.

![A screenshot of the "Instance Type" section on the form, with
`g4dn.2xlarge` selected.](readme-images/instance-type.png)

### Create or choose a key pair

Next, you will need to create an SSH key pair (or choose one that you
have previously created) to be installed onto the instance. A key pair
consists of a private key, which will be downloaded onto your computer
and used to access the instance, and a public key, which will be
installed onto the instance. Scroll down to the "Key pair (login)"
section in the form.

![A screenshot of the "Key pair (login)" section on the
form.](readme-images/key-pair.png)

If you have already done this before (unlikely for new users), and
still have access to the key file, select the key pair you previously
created from the drop-down menu, and continue to the next step. 

Otherwise, click the "Create new key pair" link. A window will pop up
where you can give the key pair a name and optionally choose what key
type you would like to create. You can leave the key pair type as
"RSA"; then, for the private key format, choose ".pem" (unless you
wish to use PuTTY; see [Connecting](#connecting) below).

![A screenshot of the "Create key pair" dialog, with "RSA" selected
for the key pair type, and ".pem" selected for the private key file
format.](readme-images/create-key-pair.png)

Then, click the orange "Create key pair" button when you are
finished. The private key file will download in your web browser; for
security reasons, _**you will not be able to download it again**_, so hold
onto it! If you lose access to your private key, you may be unable to
access your instance.

### Set up a security group

Next, you will need to set up a firewall security group, to allow
access to the Bwb server that will run on your instance. Scroll down
to the "Network settings" section of the form, and press the "Edit"
button in the top right.

![A screenshot of the "Network settings" section of the form, with the
"Edit" button indicated.](readme-images/edit-network-settings.png)

After doing so, you can optionally give the security group your own
name and description (or just use the one already generated for you);
then, press "Add security group rule" until there are three security
group rules (the form starts with one).

For each of the rules, you will be able to choose whether you would
like to allow incoming traffic from any computer ("Anywhere") or only
from the public IP address of your network ("My IP"). Anywhere will
allow access if your computer changes networks, **but will allow
_anyone_ with the address to access your Bwb virtual desktop, and
possibly files on the instance** that are mapped to data volumes in
Bwb.

Set up the security group rules like so:
1. **Description**: "SSH access"
  * **Type**: "ssh"
  * **Source Type**: "Anywhere" or "My IP" (see above)
2. **Description**: "HTTP access for Bwb"
  * **Type**: "Custom TCP"
  * **Port Range**: 6080
  * **Source Type**: "Anywhere" or "My IP" (see above)
3. **Description**: "VNC access for Bwb"
  * **Type**: "Custom TCP"
  * **Port Range**: 5900
  * **Source Type**: "Anywhere" or "My IP" (see above)
  
![A screenshot of the security group rules form, with the above
settings entered. The author's IP address is
obscured.](readme-images/security-group-rules.png)

### Final steps

### Connecting

## Manual Installation

### Installing GPU Drivers
The following instructions should work for an Ubuntu 20.04 system.

```bash
# Update software repositories and perform any necessary upgrades:
sudo apt update && sudo apt upgrade
# Install NVIDIA server driver 510:
sudo apt install nvidia-driver-510-server
# Hold the nvidia driver at the current version to prevent unintentional updates
sudo apt-mark hold nvidia-driver-510-server
```
You may need to **reboot your system** to finalize installation of the drivers.
Afterwards, check if your GPU is recognized by running
```bash
nvidia-smi
```

### Choose a working directory
When it is run, the workflow will create a directory called `benchmark` in your
current working directory, which will contain all data generated or downloaded
by the workflow (including ~40GB of images). Before cloning the workflow
repository, choose an appropriate working directory, and navigate to it with
`cd`. For example, if we wanted to store the workflow and all its data in
`Documents`, we would use
```bash
cd Documents
```

On Linux, you may also be able to use the file browser to find an appropriate
directory, right-click it, and then select "Open in Terminal" to launch a
terminal already pointed to that working directory.

### Cloning repository
Clone this repository with
```bash
git clone https://github.com/biodepot/fiji-clij
```

Navigate into the repository with
```bash
cd fiji-clij
```

### Building Docker Images
*TODO*: Remove this section if images are uploaded to DockerHub.

The widgets in this workflow use several custom Docker images that are not
available on the central Docker Hub repository, and need to be built on the host
machine; the most notable is the `fijiOCL` widget which contains GPU drivers and
OpenCL libraries for running Fiji with CLIJ. To build the Docker images, simply
navigate to the *root directory of the repository* and run
```bash
sudo ./build_docker_images.sh
```
Note that you will need root access on the host machine.

**NOTE:** It is important that this script is run from the root directory, as it
uses this assumption to navigate into directories containing relevant
`Dockerfile`s. The script will pause for 5 seconds to allow the user to confirm
that they are indeed in the root directory; to bypass this, run
```bash
sudo NOSLEEP=1 ./build_docker_images.sh
```

### Start the Bwb server
Run the command

```bash
sudo docker run --rm \
 -p 5900:5900 -p 6080:6080 \
 -v ${PWD}/:/data \
 -v /var/run/docker.sock:/var/run/docker.sock \
 -v /tmp/.X11-unix:/tmp/.X11-unix \
 --privileged --group-add root \
 biodepot/bwb:imaging__latest
```

This will forward ports 5900 (for VNC access) and 6080 (for HTTP access) on your
local machine to those same ports within the container, "pass through" access to
your machine's Docker daemon and display server, and map your current working
directory to the `/data` directory inside the container. As mentioned earlier, a
directory called `benchmark` will be created inside your current working
directory (or `/data/benchmark` inside the container), containing all data
generated by the workflow.

See ["Overview: Running
Bwb"](https://github.com/biodepot/biodepot-workflow-builder#overview-running-bwb)
in the Bwb documentation for more details.

## Usage

### Connect to Bwb with a browser or VNC client

To use Bwb, the user can use a browser (Chrome/Firefox/Safari) or a VNC client
(e.g. RealVNC). Instructions are given in [the Bwb documentation](https://github.com/biodepot/biodepot-workflow-builder#overview-running-bwb). In
most cases, the browser should be set to http://localhost:6080 if the Bwb server is
started on a laptop or the https://\<ip of the remote machine>:6080 if started on a
remote or cloud server. In addition, to connect to Bwb on the cloud, a port must
be opened and forwarded to allow browser and client to communicate with Bwb. The
exact methodology will depend on the cloud provider.  Some instructions for
Amazon web services are provided
[here](https://github.com/BioDepot/BioDepot-workflow-builder#how-do-i-run-bwb-on-the-cloud)

### Loading the workflow
1. From the Bwb menu bar, select `File > Load Workflow`
2. Navigate to `/data`, and select `clij_benchmarking_workflow`, then press
   "Choose".
3. Double click on the "Start" widget and press the blue "Start" button to start
   the workflow. 
   
The workflow will download images and benchmarking macros, and then perform the
same sequence of image processing operations on the dataset using both the
GPU and the CPU, and then compare the runtime and results of the two analyses.

Please note that the CPU benchmark may take a very long time to complete
depending on how many images are used - the runtime scales linearly with the
number of images used, since images are sequentially processed.
   
### Modifying parameters
By default, the workflow uses 300 images from the [dataset used in the
CLIJ paper](https://doi.org/10.17617/1.8J) for benchmarking; this can
be adjusted by double clicking on the "Download Images" widget and
modifying the parameters. Each image is ~127MB, so 300 images will
occupy ~38GB.

The entire dataset consists of 607 images, numbered `000000` through `000606`;
the "Pattern" field of the "Download Images" widget contains a [`printf`-style format
string](https://en.wikipedia.org/wiki/Printf_format_string); by default it is
the URL of one of these images, with a `%06d` placeholder that will be replaced
by an image number, zero-padded to be 6 digits long. The number will range from
the value in the "Minimum Value" field to the value in the "Maximum Value"
field, inclusively, and files will be placed in the directory specified in the
"Output directory" field. Additionally, the "Replace Existing Files" checkbox
can be used to control whether existing files should be replaced; since the
dataset is very large, the user may choose to only download missing files and
skip existing ones.

Note that for simplicity, the benchmarking workflows will use **all** the images
in the chosen output directory; if you have already downloaded images once, and
wish to re-run the workflow with a smaller subset of images, either delete the
images you do not wish to use, or move them to another directory.

## More on the AMI

The AMI contains an installation of Ubuntu 20.04 with Docker and
NVIDIA graphics driver packages preinstalled, as well as several
utility scripts for using the workflow, in the home directory of the
`ubuntu` user.

If you are using a `g4dn` instance (recommended, since an NVIDIA GPU
is required for the workflow) then your instance will have an
ephemeral "instance store" drive physically attached to the machine;
this is where the workflow, image data, and results will be
stored. This drive will be mounted at `/mnt/data`, which is
symbolically linked to `data` in the home directory. You can simply do
`cd data` to access the drive. If you are using an instance that
doesn't have an instance store drive, `/mnt/data` will simply be a
regular directory, and is still usable for storing data.

### General/setup scripts

* `./start_all.sh` - **Recommended for a quick start.** Runs all the
  setup scripts in order, and then starts the Bwb server.

The individual setup scripts are (in recommended execution order):

* `./mount_disks.sh` - Formats the instance store drive(s) and then
  mounts them to `/mnt/data` (if any). If multiple instance store
  drives are present, they will be formatted into a RAID-0 array and
  presented as one large disk. **Must be done before any other
  operations if you wish to use the instance store drive** -
  otherwise, the root volume will be used.
* `./download_workflow.sh` - Downloads the latest version of this
  workflow to `/mnt/data` via `git clone`. If another version of the
  workflow already exists, it will be updated via `git pull`.
* `./update_bwb.sh` - Downloads the latest version of the Bwb Docker
  image available on DockerHub.
* `./start_bwb.sh` - Starts the Bwb server.

### S3 backup scripts (optional)

These scripts are intended to allow you to store a backup of your
data/analysis results on Amazon S3, since the instance store drive on
which they are stored is deleted when the instance shuts down. 

These scripts will not work out of the box, and require AWS
credentials to be set up first. If you have not already, you will need
to generate an access key for the AWS Command-Line Interface by
logging in to the AWS console, clicking on your username at the
top-right, and selecting "Security Credentials". Once on that page,
click "Create access key" and make sure to save the credentials that
you are given, since you *won't be able to access them through the
console again.*

Once you have an access key and an access key secret, run the command
```bash
aws configure
```
and enter the access key and secret when prompted. Afterwards, you
should be able to use the scripts.

* `./create_bucket.sh` - This script will create an S3 bucket for the
  backup data (if one does not already exist).
* `./pull_backup1.sh` - This script will download the contents of
  `backup1` (i.e. the most recent backup) on S3 to the instance store
  drive.
* `./sync_data.sh` - This script will create a new backup by moving
  `backup1` to `backup2` on S3, and then copying the contents of the
  instance store drive to `backup1` on S3.
* `./sync_start_bwb.sh` - This script will create a new backup (by
  calling `./sync_data.sh`) first, and then start Bwb (by calling
  `./start_bwb.sh`).

## Licensing

This workflow is free software, under the BSD license; see
[`LICENSE.txt`](LICENSE.txt) for more information.

The ImageJ macros and Jupyter notebooks in `clij_files` are adapted
from those in the original [CLIJ benchmarking
repository](https://github.com/clij/clij-benchmarking) by the authors
of CLIJ, and are licensed under the BSD license as well. See
[`clij_files/LICENSE.txt`](clij_files/LICENSE.txt) for more
information.

## References

* CLIJ

    > Robert Haase, Loic Alain Royer, Peter Steinbach, Deborah Schmidt,
	>     Alexandr Dibrov, Uwe Schmidt, Martin Weigert, Nicola Maghelli,
	>     Pavel Tomancak, Florian Jug, Eugene W Myers. CLIJ: GPU-accelerated
	>     image processing for everyone. Nat Methods 17, 5-6 (2020)
	>     doi:10.1038/s41592-019-0650-1
 
	 Workflow is taken from the Supplementary Materials section of this paper.
 
* Dataset used is the one given in the Supplementary Materials section of the
  CLIJ paper:
  
    > Haase, R. (2019). Workflow benchmarking data, drosophila
	>	  lightsheet. doi:10.17617/1.8J

* Fiji:
  
    > Schindelin, J., Arganda-Carreras, I., Frise, E., Kaynig, V.,
	>   Longair, M., Pietzsch, T., … Cardona, A. (2012). Fiji: an
	>   open-source platform for biological-image analysis. Nature Methods,
	>   9(7), 676–682. doi:10.1038/nmeth.2019
