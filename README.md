# next_buses_as
Alexa skill to tell me the when the next buses to work are arriving. 

# Standard utterance: Alexa, when are the next buses to work?

When Alexa hears this, 'next buses' is the retrieved 'intent' of the utterance. This in turn calls a custom AWS Lambda function running in the cloud called *next_buses*. This is private for my usage as the scope of the application is only for a particular set of buses which are compatible with my commute (i.e. it's not much use to anyone else).

# It's a mess...
The environnment for the lambda to execute in is included in the package, alone with a headless browser (chromedriver.exe) which takes the latest bus information.  The necessary structure is defined by the needs of the AWS lambda function requirements. It's not ideal but its necessary to be a self sufficient lambda.

# Finally
The deployment package is a .zip file containing your Lambda function code and dependencies.
