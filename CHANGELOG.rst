Changelog
============

v2.2.1 (2020-07-28)
---------------------

https://github.com/slackapi/python-slack-events-api/milestone/2?closed=1

- Better error handling for requests lacking required headers #75 #76 - thanks @SpamapS @seratch

v2.2.0 (2020-06-23)
---------------------

https://github.com/slackapi/python-slack-events-api/milestone/1?closed=1

- Add Blueprint (application factories) support #56 #69 - thanks @maryum375 @psykzz @seratch
- Add current_app (LocalProxy) support #66 #71 - thanks @tstoco @seratch
- Apply various improvement to the PyPI packaging #47 #70 #72 - thanks @seratch
- Drop Python 2.7.6 support #53 #68 - thanks @Roach @seratch
- Refactor duplicated code #59 - thanks @vvatelot
- Add more tests #37 #40 - thanks @datashaman

v2.1.0 (2018-12-12)
---------------------

- Updates request signing to work for any content-type (#44)
- Updated minimum Flask version to address security vulnerability (#45)

v2.0.0 (2018-08-15)
---------------------

- Added support for Request signing

v1.1.0 (2018-01-19)
---------------------

- Added the ability to pass an existing Flask instance into SlackEventAdapter
- Added server response headers for python, os and package versions

v1.1.0 (2018-01-19)
---------------------

- Added the ability to pass an existing Flask instance into SlackEventAdapter
- Added server response headers for python, os and package versions

v1.0.1 (2017-12-18)
---------------------

 - Added change log ✅
 - Decode byte stream into utf-8 - fixing Python 3 compatability issue (Thanks @navinpai!)
 - Added `host` argument, to bind to hosts other than `localhost` (Thanks @calvinhp!)
 - Improved verification token logic (Thanks @benoitlavigne!)


v1.0.0 (2017-02-22)
---------------------

 - Initial release 🎉
