deploy:
	gcloud functions deploy nba-recap-bot \
	--gen2 \
	--region=us-west1 \
	--runtime=python311 \
	--source=. \
  --memory=512M \
	--entry-point=run_bot \
	--trigger-http --env-vars-file=env.yml 
