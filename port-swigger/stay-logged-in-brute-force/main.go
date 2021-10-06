package main

import (
	"log"
	"io/ioutil"
	"strings"
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
	candidatePasswords, err := readFromFile("assets/candidate-passwords.txt")

	if err != nil {
		log.Printf("Error reading the file %s", err)
		return
	}

	log.Printf("Found %d candidates passwords", len(candidatePasswords))
}


func readFromFile(filePath string) ([]string, error) {
	fileBytes, err := ioutil.ReadFile(filePath)

	if err != nil {
		return []string{}, err
	}

	return strings.Split(string(fileBytes), "\n"), nil
}


func main() {
	log.SetFlags(log.LstdFlags | log.Lmicroseconds)

	hardcodedHostname := "https://ac8e1f801fbb4814c0091036004300a6.web-security-academy.net"
	solve(hardcodedHostname)
}
