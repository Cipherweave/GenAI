import unittest
import web_suggester
import cohere
import json
import os
from dotenv import load_dotenv
from duckduckgo_search import DDGS
import unittest
from unittest.mock import patch
import web_suggester
from privacy_policy_score import main


class Test_code(unittest.TestCase):


    def test_web_suggester(self):

        names = ['tiktok', 'google', 'youtube', 'facebook']

        for name in names:
            result = web_suggester.get_related_websites(name)

            self.assertIsInstance(result, list)
            self.assertEqual(len(result), 3)

            for item in result:
                self.assertIsInstance(item, str)
                print(item)
                self.assertTrue(len(item) > 0, "Empty string found in the list")


    @patch("web_suggester.DDGS.text")  # Mock DDGS.text to avoid real API calls
    def test_get_official_urls_valid(self, mock_ddgs):
        # Mock response for different companies
        mock_ddgs.side_effect = lambda query, max_results: [
            {"href": f"https://www.{query.split()[0]}.com"}
        ]

        companies = ["tiktok", "google", "youtube"]
        result = web_suggester.get_official_urls(companies)

        expected = {
            "tiktok": "https://www.tiktok.com",
            "google": "https://www.google.com",
            "youtube": "https://www.youtube.com"
        }

        self.assertEqual(result, expected)

    @patch("web_suggester.DDGS.text")
    def test_get_official_urls_no_results(self, mock_ddgs):
        # Mock case where no search results are found
        mock_ddgs.side_effect = lambda query, max_results: []

        companies = ["unknowncompany"]
        result = web_suggester.get_official_urls(companies)

        self.assertEqual(result, {})  # Should return an empty dictionary

    @patch("web_suggester.DDGS.text")
    def test_get_official_urls_mixed_results(self, mock_ddgs):
        # Mock different responses: one with results, one without
        def mock_response(query, max_results):
            if "google" in query:
                return [{"href": "https://www.google.com"}]
            return []  # No results for other queries

        mock_ddgs.side_effect = mock_response

        companies = ["google", "unknowncompany"]
        result = web_suggester.get_official_urls(companies)

        expected = {"google": "https://www.google.com"}
        self.assertEqual(result, expected)

    @patch("web_suggester.get_related_websites")  # Mock related websites
    @patch("web_suggester.get_official_urls")  # Mock official URLs
    def test_search_related_websites_valid(self, mock_get_official_urls, mock_get_related_websites):
        # Mock related websites response
        mock_get_related_websites.return_value = ["weheartit", "fotophound", "jolty"]

        # Mock official URLs response
        mock_get_official_urls.return_value = {
            "weheartit": "https://www.weheartit.com",
            "fotophound": "https://www.fotophound.com",
            "jolty": "https://www.jolty.com"
        }

        result = web_suggester.search_related_websites("pinterest")

        expected = {
            "company": "pinterest",
            "related_companies": {
                "weheartit": "https://www.weheartit.com",
                "fotophound": "https://www.fotophound.com",
                "jolty": "https://www.jolty.com"
            }
        }

        self.assertEqual(result, expected)

        # Ensure JSON file is correctly written
        with open("related_companies_urls.json", "r") as json_file:
            saved_data = json.load(json_file)
            self.assertEqual(saved_data, expected)

    @patch("web_suggester.get_related_websites")
    @patch("web_suggester.get_official_urls")
    def test_search_related_websites_no_results(self, mock_get_official_urls, mock_get_related_websites):
        # No related websites found
        mock_get_related_websites.return_value = []

        # No official URLs since no websites were found
        mock_get_official_urls.return_value = {}

        result = web_suggester.search_related_websites("unknowncompany")

        expected = {
            "company": "unknowncompany",
            "related_companies": {}
        }

        self.assertEqual(result, expected)

    @patch("web_suggester.get_related_websites")
    @patch("web_suggester.get_official_urls")
    def test_search_related_websites_partial_results(self, mock_get_official_urls, mock_get_related_websites):
        # One valid website, one without a URL
        mock_get_related_websites.return_value = ["google", "nonexistent"]

        # Only Google has a result
        mock_get_official_urls.return_value = {
            "google": "https://www.google.com"
        }

        result = web_suggester.search_related_websites("bing")

        expected = {
            "company": "bing",
            "related_companies": {
                "google": "https://www.google.com"
            }
        }

        self.assertEqual(result, expected)



