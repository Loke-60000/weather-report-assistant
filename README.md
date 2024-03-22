# Setting up a Cron Job

## Follow these steps to set up a cron job to run your script at regular intervals:

### Step 1: Get your conda environment name

To begin, find the name of your conda environment by running the following command:

`crontab -e`

## Step 3: Add the following line to the end of the crontab file

### This schedules your script to run every 30 minutes

```
*/30 * * * * /home/lokman/anaconda3/envs/YOUR_ENV_NAME/bin/python /home/lokman/simplon/00.briefs/17.weather/my_script.py

```

## Step 4: Verify the cron job has been added

`crontab -l`
