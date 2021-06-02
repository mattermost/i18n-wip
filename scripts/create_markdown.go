package main

import (
	"fmt"
	"log"
	"os"
	"sort"
)

func main() {
	weblateURL := "https://translate.mattermost.com"
	shippedURL := fmt.Sprintf("%v/projects/mattermost", weblateURL)
	widgetURL := fmt.Sprintf("%v/widgets/mattermost", weblateURL)
	server := "mattermost-server"
	webapp := "mattermost-webapp"
	mobile := "mattermost-mobile"
	shippedLs := map[string]string{
		"Bulgarian":             "bg",
		"Chinese (Simplified)":  "zh_Hans",
		"Chinese (Traditional)": "zh_Hant",
		"Dutch":                 "nl",
		"French":                "fr",
		"German":                "de",
		"Hungarian": 		 "hu",
		"Italian":               "it",
		"Japanese":              "ja",
		"Korean":                "ko",
		"Polish":                "pl",
		"Portuguese (Brazil)":   "pt_BR",
		"Romanian":              "ro",
		"Russian":               "ru",
		"Spanish":               "es",
		"Turkish":               "tr",
		"Ukrainian":             "uk",
		"Swedish":               "sv",

	}
	sortedL := getSortedLanguages(shippedLs)

	n, err := createMD(server, shippedURL, webapp, mobile, sortedL, shippedLs, widgetURL)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Print(*n)
}

func createMD(server string, shippedURL string, webapp string, mobile string, sortedL []string, shippedLs map[string]string, widgetURL string) (*int, error) {
	f, err := os.Create("shipped.md")
	if err != nil {
		return nil, err
	}

	tHeader := fmt.Sprintf(
		"|  | [%v](%v%v_master/) | [%v](%v%v_master/) | [%v](%v%v_master/) |\n | ------------- | ------------- | ------------- | ------------- |\n",
		server, shippedURL, server, webapp, shippedURL, webapp, mobile, shippedURL, mobile,
	)

	var tCellL string
	var tCellServer string
	var tCellWebapp string
	var tCellMobile string
	var tRow string
	var tBody string
	var lCode string
	for _, l := range sortedL {
		lCode = shippedLs[l]
		tCellL = fmt.Sprintf("| %v [%v] | ", l, lCode)
		tCellServer = fmt.Sprintf("[![mattermost](%v/%v/%v_master/svg-badge.svg)](%v/%v_master/%v/) | ", widgetURL, lCode, server, shippedURL, server, lCode)
		tCellWebapp = fmt.Sprintf("[![mattermost](%v/%v/%v_master/svg-badge.svg)](%v/%v_master/%v/) | ", widgetURL, lCode, webapp, shippedURL, webapp, lCode)
		tCellMobile = fmt.Sprintf("[![mattermost](%v/%v/%v_master/svg-badge.svg)](%v/%v_master/%v/) |\n", widgetURL, lCode, mobile, shippedURL, mobile, lCode)
		tRow = tCellL + tCellServer + tCellWebapp + tCellMobile
		tBody += tRow
	}

	t := tHeader + tBody

	n, err := f.WriteString(t)
	if err != nil {
		_ = f.Close()
		return nil, err
	}
	return &n, nil
}

func getSortedLanguages(shippedLs map[string]string) []string {
	sortedL := make([]string, 0, len(shippedLs))
	for key := range shippedLs {
		sortedL = append(sortedL, key)
	}
	sort.Strings(sortedL)
	return sortedL
}
