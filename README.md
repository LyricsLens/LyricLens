## Getting Started

### Spinning LyricLens Up & Down

(Before doing this, make sure you complete the [Github Actions Setup](#github-actions-setup) section)

#### Spinning it Up:

In the Terraform Action, run the 'plan' workflow in the main branch. After that finished, run the 'apply' workflow in the main branch. Once that finishes, the `tf summary` will display the website URL.

#### Spinning it down.

In the Terraform action, run the 'destroy' workflow in the main branch. Once that's finished, you can confirm everything is destroyed by checking if the URL returns anything.

### Usage

1. Enter in any public spotify playlist URL into the search bar and press analyze
   - Example: https://open.spotify.com/playlist/5RVat09qxvzmcwbS9Gzd1n?si=17500c5d3a804d79 
2. Enjoy the image


### Github Actions Setup

Our repository leverages Github Actions to set up our service. To get started, please follow the instructions below.

1. Navigate to repository [settings](https://github.com/devinvasavong/2251-swen514-2-Cumulonimbus-Crew/settings)
2. Click on Secrets and variables > Actions
3. Add your `AWS_ACCESS_KEY_ID` to Repository secrets
4. Add your `AWS_SECRET_ACCESS_KEY` to Repository secrets
5. All set!