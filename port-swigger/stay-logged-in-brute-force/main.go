package main

import (
	"log"
)

func solve(hostname string) {
	/*
		What is known?
		- The cookie stay-logged-in is a base64 encoded value of user:md5hash(password), where
		md5hash is the md5 hash function.
		- Using the cookie, we can access the /my-account page without a redirect


		Steps to solve:
		- Read candidate passwords into array
		- For each candidate password:
			- Create a cookie based on base64(user:md5hash(password))
			- Use created cookie to access page /my-account
			- If redirect (302 http status), try again
			- Otherwise (200 http status), the password is known!
	*/

}

func main() {
	log.SetFlags(log.LstdFlags | log.Lmicroseconds)

	hardcodedHostname := "https://ac8e1f801fbb4814c0091036004300a6.web-security-academy.net"
	solve(hardcodedHostname)
}
