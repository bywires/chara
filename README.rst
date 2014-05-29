Chara
======================

Chara enables developers to quickly create characterization tests.  Start by creating integration tests using whatever testing framework you prefer.  Using Chara you decorate those test functions to record interactions with specific dependencies.  Afterwards, you can replay the recording and those dependencies will behave as recorded.

Usage
-----

Example::

    # test_scraper.py

    def scrape_headline(name):
        """ Code under test """

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
        """ Dependency we want to eliminate """

        return urllib2.urlopen(url).read()


    class DemoTest(TestCase):
        @chara.replay('test_scraper.get_html')
        def test_scraper(self):
            """ Should get Wired.com headline as recorded on
            May 28, 2014.  The recorded content, which includes
            the full HTML payload, are in
            examples/.chara/test_scraper.py.test_scraper.pickle. """

            self.assertEqual(
                'This Is What Happens When You Hack and '
                'Extort the \'Bitcoin Jesus\'',
                scrape_headline('wired')
            )


License
-------

Uses the `MIT`_ license.


.. _MIT: http://opensource.org/licenses/MIT
