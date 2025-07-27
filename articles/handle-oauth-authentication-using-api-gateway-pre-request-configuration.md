# Handle OAuth Authentication using API Gateway Pre-request Configuration

### In this article, we will explain how to set up a Pre-request to retrieve an OAuth 2.0 access token for connecting to an API using an API Gateway.

OptiSigns API Gateway allows for OAuth authentication via Pre-request. This gives users the capability to consume API that requires OAuth authentication or similar.
To get started, you'll need to set up an API request. Hover over Account Name → More → Click DataSources:

From there, hit Add Request.

Create a GET Request and input your API endpoint, then click Pre-request:

Within the Pre-request field, input the following code:

```
const body = {  "grant_type": "client_credentials",  "client_id": "<CLIENT_ID>",  "client_secret": "<CLIENT_SECRET>"};const params = Object.keys(body || {}).map((key) => {        return key + '=' + body[key];      }).join('&');const {data, headers} = await os.postRequest("<OAUTH_AUTHENTICATION_URL>", params,{headers: {'content-type': 'application/x-www-form-urlencoded'}});const token = 'Bearer' + data.access_token;os.context.set("request.headers.authorization", token);
```

Notes:

"grant_type": Use "client_credentials" ., because "client_credentials" is the grant type in OAuth for server-side integration without user interaction.
<CLIENT_ID> and <CLIENT_SECRET> refers to the user's code for the API being accessed, this will need to be provided by the user.
<OAUTH_AUTHENTICATION_URL> refers to the URL the access token is being retrieved from. This URL will need to be provided by the user.

Now configure the Header:

With this and the rest of the required fields filled out, you've properly configured your Pre-request. Hitting Run Test should return a 200 OK Response.

If so, hit Save to finish your API Request.

### That's all!

If you have any additional questions, concerns, or any feedback about OptiSigns, feel free to reach out to our support team at [support@optisigns.com](mailto:support@optisigns.com).