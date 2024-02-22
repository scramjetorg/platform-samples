# Integ-Master

A component of the tool that provides integration between the three Stripe :left_right_arrow: Auth0 :left_right_arrow: Mailchimp services. It manage two sources stripe and auth0.

:warning: To use the given solution, API and authorization keys must be prepared, for each of the mentioned services. :warning:

:warning: Remember, two sequences (Integ-Master, ChimpInsert) are required for proper operation. Start with "ChimpInsert" directory.:warning:

___


## Get your API keys

:warning: Remember you can generate keys with minimal permissions :warning:

- [Mailchimp](https://mailchimp.com/help/about-api-keys/#:~:text=To%20generate%20an%20API%20key%2C%20follow%20these%20steps)
- [AudienceID](https://mailchimp.com/help/find-audience-id/)
- [Auth0](https://auth0.com/docs/secure/tokens/access-tokens/get-access-tokens#:~:text=Get%20Access%20Tokens-,Get%20Access%20Tokens,-To%20access%20your) (read:users read:user_idp_tokens) \
The data collection process is easier if you create an application in the auth0 panel and then go to the "Quickstart" tab. Properly labeled data will be in the sample request.
- [Stripe](https://dashboard.stripe.com/test/apikeys) (event_read  customer_read   customer.created)

Now open config.json file and fill all the empty spaces with the information you got. mailchimp_server is everything after "-" in mailchimp's API key eg. "us21".

Query url is already set, generator of such url can be found [here](https://auth0.com/docs/api/management/v2#!/Users/get_users)

## Running

Start STH :rocket:

```bash
sth
```

Open terminal:

```bash

# Go into Integ-Master's sequence  directory
cd Integ-Master

# Build sequence
npm run build

# Deploy sample to STH
si seq deploy dist -f config.json

```
