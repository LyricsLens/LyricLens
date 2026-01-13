<!-- Copyright (c) 2026 Cumulonimbus Crew. All rights reserved. -->

# Welcome to LyricLens

LyricLens is a full-stack web application that creates custom Spotify playlist cover art by leveraging AWS Comprehend for sentiment analysis and AWS Bedrock for AI image generation. The project integrates multiple AWS services and supports fully automated deployment and teardown using GitHub Actions and Terraform. Please feel free to give it a try!

## Getting Started

### Spinning LyricLens Up & Down

(Before doing this, make sure you complete the [Github Actions Setup](#github-actions-setup) section)

#### Spinning it Up:

In the Terraform Action, run the 'plan' workflow in the main branch. After that finished, run the 'apply' workflow in the main branch. Once that finishes, the `tf summary` will display the website URL.

#### Spinning it down.

In the Terraform action, run the 'destroy' workflow in the main branch. Once that's finished, you can confirm everything is destroyed by checking if the URL returns anything.

### Usage

1. Enter in a public spotify playlist URL with less than 50 songs into the search bar and press analyze.
   - Example: https://open.spotify.com/playlist/5RVat09qxvzmcwbS9Gzd1n?si=17500c5d3a804d79
   - _Please do not spam this button. Spotify has a rate limit so adding 15-20 seconds of buffer time would help!_
2. Enjoy the image!
3. View past generated images by pressing the Portfolio button on the top right part of the page.

### Github Actions Setup

Our repository leverages Github Actions to set up our service. To get started, please follow the instructions below.

1. Navigate to repository [settings](https://github.com/devinvasavong/2251-swen514-2-Cumulonimbus-Crew/settings)
2. Click on Secrets and variables > Actions
3. Add your `AWS_ACCESS_KEY_ID` to Repository secrets
4. Add your `AWS_SECRET_ACCESS_KEY` to Repository secrets

### Required Credentials

**AWS Credentials:**
You must set the following GitHub Action secrets for deployment to work:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`

**Spotify Credentials:**
You must add your Spotify API credentials in `modules/lambdas/spotify.py` by setting the `CLIENT_ID` and `CLIENT_SECRET` variables. Do not commit your real credentials to a public repository—use environment variables or a secure method for production.

---

Repository is now public. Please ensure you do not expose sensitive information in your commits or secrets.
