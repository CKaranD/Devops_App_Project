# Deploying to Amazon ECR using GitHub Actions

This guide will walk you through the process of deploying a Docker image to an Amazon Elastic Container Registry (ECR) using GitHub Actions.

## Step-by-Step Instructions

### 1. Fork the Project

First, you need to fork the project in your GitHub account. Click on the fork button at the top right corner of the project's GitHub page to do this.

### 2. Clone the Forked Project

Next, clone the forked project to your local machine. You can do this by clicking on the code button and then clicking on the clipboard icon. Open your terminal and type `git clone` and then paste the URL you copied.

### 3. Configure AWS Credentials

Before configuring your AWS credentials, you need to create an AWS account if you don't have one already. Then, create an IAM user and make sure to grant it programmatic access and give it an appropriate IAM policy to be able to manage ECR.

After creating your IAM user, you should be able to retrieve the access key ID and secret access key. These will be used to allow GitHub actions to push images to your ECR.

### 4. Configure Secrets in GitHub

In your GitHub account, navigate to the forked project, and under settings, go to secrets. Create a new secret. Give it the name "AWS_ACCESS_KEY_ID" and under secret, provide the value of your access key ID you created earlier.

Follow the same procedure to create a secret for your secret access key, by giving it the name "AWS_SECRET_ACCESS_KEY".

### 5. Enable GitHub Actions

For this project, you may need to enable GitHub actions if you haven't already. This can be done by:

- Navigating to the forked project in your GitHub account.
- Clicking on Actions.
- Then clicking on "Enable GitHub Actions For This Project".

We are doing this for GitHub actions to run automatically anytime we push changes to our main branch.

### 6. Create an ECR Repository and Update the GitHub Action File

We need to create an ECR repository where GitHub actions will deploy our Docker image to. Make sure you are creating this repository in the "us-east-1" or "N. Virginia" region.

Once that is done, we have to update our GitHub actions file with the name of our ECR repository. This file can be found in the project we cloned, in the directory `.github/workflows/main.yml`. Inside the `main.yml` file, look for the key that says "ECR_REPOSITORY" and update its value with the name of your ECR repository.

### 7. Push and Deploy

Now, if everything was configured well, we should be able to push the current changes to our GitHub repository, and GitHub actions will run and deploy our image successfully.

You can go to the Actions tab in GitHub to make sure everything ran successfully, and also check your Amazon ECR Repository to make sure that you see the Docker image.

---
*Have fun Learning*
