# Chara


Chara enables developers to quickly create characterization tests.  Start by creating integration tests using whatever testing framework you prefer.  Using Chara you decorate those test functions to record interactions with specific dependencies.  Afterwards, you can replay the recording and those dependencies will behave as recorded.

## Usage

Create production code and passing integration test (test_scraper.py)::

    def scrape_headline(name):
        url, search = {
            'wired': (
                'http://www.wired.com', 
                '<div class="headline headline1">\s*'
                '<h5>[^<]*</h5>\s*'
                '<h2>\s*<a[^>]*>([^<]*?)</a>\s*</h2>\s*'
                '</div>'
            )
        }[name]

        matches = re.search(search, get_html(url))

        return matches.group(1) if matches else None


    def get_html(url):
        return urllib2.urlopen(url).read()


    class DemoTest(TestCase):
        def test_scraper(self):
            self.assertEqual(
                'This Is What Happens When You Hack and '
                'Extort the \'Bitcoin Jesus\'',
                scrape_headline('wired')
            )

Add chara.record decorator and run the test::

    class DemoTest(TestCase):
        @chara.record('test_scraper.get_html')
        def test_scraper(self):
            self.assertEqual(
                'This Is What Happens When You Hack and '
                'Extort the \'Bitcoin Jesus\'',
                scrape_headline('wired')
            )

Switch to using chara.replay and notice that even if you turn get_html() to a no-op function the test still passes, so you know that the function's normal functionality is being bypassed by Chara's replay functionality.::

    def get_html(url):
        pass # nothing even happening here, but the test passes!

    class DemoTest(TestCase):
        @chara.replay('test_scraper.get_html')
        def test_scraper(self):
            self.assertEqual(
                'This Is What Happens When You Hack and '
                'Extort the \'Bitcoin Jesus\'',
                scrape_headline('wired')
            )



## License

Uses the [MIT](http://opensource.org/licenses/MIT) license.