# Integration

A tool to provide integration between the three Stripe :left_right_arrow: Auth0 :left_right_arrow: Mailchimp services.

:warning: To use the given solution, API and authorization keys must be prepared, for each of the mentioned services. :warning:
___


## Get your API keys

:warning: Remember you can generate keys with minimal permissions :warning:

- [Mailchimp](https://mailchimp.com/help/about-api-keys/#:~:text=To%20generate%20an%20API%20key%2C%20follow%20these%20steps)
- [AudienceID](https://mailchimp.com/help/find-audience-id/)
- [Auth0](https://auth0.com/docs/secure/tokens/access-tokens/get-management-api-access-tokens-for-testing#get-access-tokens-manually) (read:users read:user_idp_tokens)
- [Stripe](https://dashboard.stripe.com/test/apikeys) (event_read  customer_read   customer.created)

Now open config.json file and fill all the empty spaces with the information you got. mailchimp_server is everything after "-" in mailchimp's API key eg. "us21".

Query url is already set, generator of such url can be found [here](https://auth0.com/docs/api/management/v2#!/Users/get_users)

## Running

Start STH :rocket:

```bash
sth
```
Later, deploy each of the sequences contained in the folder. Start with "ChimpInsert" directory.

Open terminal:

```bash
# Build sequence
npm run build

# Deploy sample to STH
si seq deploy dist -f ../config.json

```
:repeat: Repeat the process for the other two sequences. :repeat:
