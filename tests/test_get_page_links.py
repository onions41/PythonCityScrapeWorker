import unittest
from time import sleep
from modules.get_page_links import get_page_links


class TestGetPageLinks(unittest.TestCase):
    def test_basic(self):
        get_page_links("abcde")

    # def test_no_results(self):
    #     search_string = "site:council.vancouver.ca/20230511"
    #     search_gen = google_search(search_string)
    #     with self.assertLogs(level="INFO") as log_context, self.assertRaises(
    #         StopIteration
    #     ) as exception_context:
    #         next(search_gen)

    #     self.assertEqual(
    #         ["INFO:root:No results found for " + search_string], log_context.output
    #     )
    #     self.assertEqual(exception_context.exception.value, "no results")

    # def test_yes_results(self):
    #     sleep(5)
    #     search_string = "site:council.vancouver.ca/20230509"
    #     search_gen = google_search(search_string)

    #     for result_dict in search_gen:
    #         self.assertTrue(
    #             type(result_dict) is dict,
    #             msg=f"result_dict was not a dictionary, it was: {type(result_dict)}",
    #         )
    #         self.assertTrue(type(result_dict["link_url"]) is str)
    #         self.assertTrue(type(result_dict["link_title"]) is str)
    #         self.assertTrue(type(result_dict["link_description"]) is str)
    #         print(result_dict)


if __name__ == "__main__":
    unittest.main()
