# Lab: Stealing OAuth access tokens via a proxy page

- [Link](https://portswigger.net/web-security/oauth/lab-oauth-stealing-oauth-access-tokens-via-a-proxy-page)

## Tips

Maybe you can divide this lab in two or three parts. The first one is to manipulate the `redirect_uri` which is quite similar to how is done in the [Stealing OAuth access tokens via open redirect](../stealing-access-token-via-open-redirect).

The second part is to find where is the other vulnerability in the client app. That is the most important part, since you will exploit this vulnerability to steal the access tokens.