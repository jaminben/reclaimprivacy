import os
import logging
import urlparse
from google.appengine.api import memcache
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

VERSION = '13'


class NewsletterEntry(db.Model):
    email_address = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add=True)


class Newsletter(webapp.RequestHandler):
    def get(self):
        email = self.request.get('email')
        if email:
            try:
                num_previous_entries = NewsletterEntry.gql('WHERE email_address = :1 LIMIT 1', email).count()
                if num_previous_entries != 0:
                    logging.error("already have email addres: %(email)s" % locals())
                else:
                    entry = NewsletterEntry()
                    entry.email_address = email
                    entry.put()
            except Exception, e:
                logging.error('error adding email: ', e)
        else:
            logging.error('email not given')
        self.redirect('/')

class DesktopApplication(webapp.RequestHandler):
    def get(self):
        self.redirect("https://www.facebook.com")

class Facebook(webapp.RequestHandler):
    def get(self):
        # detect MSIE
        if 'MSIE' in os.environ['HTTP_USER_AGENT']:
            is_iebrowser = 1
        else:
            is_iebrowser = 0

        # build the memcache key we will use
        version = VERSION
        memcache_key = 'page_content:facebook:%(version)s:%(is_iebrowser)s' % locals()

        # try to get a cached page, and otherwise build the page
        page_content = memcache.get(memcache_key)
        if not page_content:

            # figure out the host name of this server (for serving the proper
            # javascript bookmarklet)
            parts = urlparse.urlparse(self.request.url)
            if parts.port:
                bookmarklet_host = parts.hostname + ':' + str(parts.port)
            else:
                bookmarklet_host = parts.hostname

            # we need to serve a different bookmarklet Javascript for MSIE
            if is_iebrowser:
                step_one_instructions = "Right-click this link and 'Add to Favorites'"
                step_two_instructions = "<a href='http://www.facebook.com/settings/?tab=privacy&ref=mb'>Go to your Facebook privacy settings</a>, open your Favorites, and click the link called 'Scan for Privacy' once you are on Facebook"
            else:
                step_one_instructions = "Drag this link to your web browser bookmarks bar"
                step_two_instructions = "<a href='http://www.facebook.com/settings/?tab=privacy&ref=mb'>Go to your Facebook privacy settings</a> and then click that bookmark once you are on Facebook."

            # build the page HTML
            bookmarklet_host = bookmarklet_host.replace('www.reclaimprivacy.org', 'static.reclaimprivacy.org')
            page_content = '''
<html>
<head>
    <title>ReclaimPrivacy.org | Facebook Privacy Scanner</title>
    <link rel="stylesheet" href="/stylesheets/main.css" type="text/css" media="screen" title="no title" charset="utf-8">
    
</head>
<body>

    <div id='logo'>
        <a href="http://www.reclaimprivacy.org"><img src='/images/logo.png' /></a>
        <div>
            <strong>ReclaimPrivacy</strong><span class='soft'>.org</span>
        </div>
        <div class='donation-box'>
            <a href='http://www.pledgie.com/campaigns/10721'><img alt='Click here to lend your support to: reclaimprivacy and make a donation at www.pledgie.com !' src='http://www.pledgie.com/campaigns/10721.png?skin_name=chrome' border='0' /></a>
            <br/>
            donations help us cover bandwidth costs,
            <br/>even $5 or $10 helps
        </div>
    </div>

    <div id='content'>
        <h1>Get Informed</h1>
        <p>
            Keep up with the latest news about privacy policies on Facebook.
            <ul>
                <li>
                    <a href='http://www.eff.org/deeplinks/2010/04/facebook-further-reduces-control-over-personal-information'>The Erosion of Facebook Privacy</a>
                    <span class='soft'>eff.org</span>
                </li>
                <li>
                    <a href='http://www.eff.org/deeplinks/2009/12/facebooks-new-privacy-changes-good-bad-and-ugly'>Facebook Privacy Changes</a>
                    <span class='soft'>eff.org</span>
                </li>
                <li>
                    <a href='http://finance.yahoo.com/family-home/article/109538/7-things-to-stop-doing-now-on-facebook'>7 Things to Stop Doing Now on Facebook</a>
                    <span class='soft'>yahoo.com</span>
                </li>
                <li>
                    <a href='http://www.wired.com/epicenter/2010/05/facebook-rogue/'>Facebook's Gone Rogue</a>
                    <span class='soft'>wired.com</span>
                </li>
            </ul>
        </p>

        <h1>Get Protected</h1>
        <p>
            This website provides an <strong>independent</strong> and <strong>open</strong> tool for scanning
            your Facebook privacy settings.  <em>The <a href='http://github.com/mjpizz/reclaimprivacy'>source code</a> and its development will always remain open and transparent.</em>
            <ol class='instructions'>
                <li>
                    %(step_one_instructions)s:
                    <strong>
                        <a class='bookmarklet' title="Scan for Privacy" href="javascript:(function(){var%%20script=document.createElement('script');script.src='http://%(bookmarklet_host)s/javascripts/privacyscanner.js';document.getElementsByTagName('head')[0].appendChild(script);})()">Scan for Privacy</a>
                    </strong>
                </li>
                <li>
                    %(step_two_instructions)s
                </li>
                <li>
                    You will see a series of privacy scans that inspect your privacy settings and warn you about
                    settings that might be unexpectedly public.
                </li>
                <li>
                    <a href="http://www.facebook.com/pages/Reclaim-Privacy/121897834504447">Follow us on Facebook</a>
                    to hear about the latest updates.
                </li>
            </ol>
            <p class='need-help'>
                <em>
                    Having trouble? <a href='/help'>Check our help page</a> for tips and video walkthroughs.</a>
                </em>
            </p
        </p>

        <h1>Get Involved</h1>
        <p>
            Our mission is to promote privacy awareness on Facebook and elsewhere.
            Spread awareness to your friends on Facebook by sharing this website with them:
            <p>
                <a name="fb_share" type="button_count" share_url="http://www.reclaimprivacy.org/facebook" href="http://www.facebook.com/sharer.php">Share</a><script src="http://static.ak.fbcdn.net/connect.php/js/FB.Share" type="text/javascript"></script>
            </p>
            <p>
                You can <a href='http://twitter.com/reclaimprivacy'>follow us on Twitter</a> too!
            </p>
            <p>
                <form class='newsletter' action='/newsletter'>
                    <div class='message'>
                        If you prefer email, you can also sign up for the newsletter to get informed of privacy updates:
                    </div>
                    <label for='email'>email:</label>
                    <input type='text' name='email' />
                    <input type='submit' value='sign me up for the newsletter' />
                </form>
            </p>
            <p>
                    <em>Are you a coder?</em> Contribute to the <a href='http://github.com/mjpizz/reclaimprivacy'>source code</a> and help to
                    keep the privacy scanner up-to-date.
            </p>
        </p>

        <h1>Read Our Own Privacy Policy</h1>
        <p>
            Our privacy policy is not long:
            <ul>
                <li>we <strong>never see</strong> your Facebook data</li>
                <li>we <strong>never share</strong> your personal information</li>
            </ul>
            Simple.  The scanner operates entirely within your own browser.
        </p>
        <p>
            <em>Statement of limitation of liability:</em>
            <strong>you use this tool at your own risk</strong>, and by using this tool you agree
            to hold neither ReclaimPrivacy.org (nor its contributors) liable for
            damage to your Facebook account.
            <strong>However, we do strive to reduce that risk
            by keeping the source code open and transparent</strong>, so that
            we can identify bugs and quickly fix any functionality.
        </p>

        <div class='about-section'>
            <h2>about the author</h2>
            <p>
                I am an avid Javascript developer and co-founder at <a href='http://www.olark.com/'>Olark</a> (check it out!).  You
                can chat with me about ReclaimPrivacy.org on my <a href='http://www.mjpizz.com'>website</a>. 
            </p>
        </div>
    </div>

</body>
</html>
            ''' % locals()

            # cache the page in memcache (only on the production servers)
            if 'reclaimprivacy.org' in parts.hostname:
                memcache.set(memcache_key, page_content)

        # write the response
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(page_content)


class Help(webapp.RequestHandler):
    def get(self):

        # build the memcache key we will use
        version = VERSION
        memcache_key = 'page_content:help:%(version)s' % locals()

        # try to get a cached page, and otherwise build the page
        page_content = memcache.get(memcache_key)
        if not page_content:

            # figure out the host name of this server (for serving the proper
            # javascript bookmarklet)
            parts = urlparse.urlparse(self.request.url)
            if parts.port:
                bookmarklet_host = parts.hostname + ':' + str(parts.port)
            else:
                bookmarklet_host = parts.hostname

            # render the page
            page_content = '''
<html>
<head>
    <title>ReclaimPrivacy.org | Facebook Privacy Scanner</title>
    <link rel="stylesheet" href="/stylesheets/main.css" type="text/css" media="screen" title="no title" charset="utf-8">

</head>
<body>

    <div id='logo'>
        <a href="http://www.reclaimprivacy.org"><img src='/images/logo.png' /></a>
        <div>
            <strong>ReclaimPrivacy</strong><span class='soft'>.org</span>
        </div>
        <div class='donation-box'>
            <a href='http://www.pledgie.com/campaigns/10721'><img alt='Click here to lend your support to: reclaimprivacy and make a donation at www.pledgie.com !' src='http://www.pledgie.com/campaigns/10721.png?skin_name=chrome' border='0' /></a>
            <br/>
            donations help us cover bandwidth costs,
            <br/>even $5 or $10 helps
        </div>
    </div>

    <div id='content'>
        <h1>Video Walkthroughs</h1>
        <p>
            If you are having trouble setting up the privacy scanner, watch the video
            walkthrough for your browser.
            <ul class='browser-walkthrough'>
                <li class='enabled for-windows'>
                    <a href='http://www.youtube.com/watch?v=lVQga-m4aRk' title='Google Chrome Privacy Walkthrough Video' target='_blank'>
                        <img src='/images/google-chrome-logo.png' width='90' height='87' /><span class='label'>Chrome (Windows)</span>
                        <span class='volunteers-needed'>volunteers needed!</span>
                    </a>
                </li>
                <li class='enabled for-mac'>
                    <a href='http://www.youtube.com/watch?v=lVQga-m4aRk' title='Google Chrome Privacy Walkthrough Video' target='_blank'>
                        <img src='/images/google-chrome-logo.png' width='90' height='87' /><span class='label'>Chrome (Mac)</span>
                        <span class='volunteers-needed'>volunteers needed!</span>
                    </a>
                </li>
                <li class='enabled for-mac'>
                    <a href='http://www.youtube.com/watch?v=BsTF8vbi3ns' title='Safari Privacy Walkthrough Video' target='_blank'>
                        <img src='/images/safari-logo.png' width='90' height='90' /><span class='label'>Safari</span>
                        <span class='volunteers-needed'>volunteers needed!</span>
                    </a>
                </li>
                <li class='disabled for-windows'>
                    <a href='#' title='Internet Explorer Privacy Walkthrough Video' onclick='return false;'>
                        <img src='/images/ie-logo.png' width='90' height='90' /><span class='label'>Internet Explorer</span>
                        <span class='volunteers-needed'>volunteers needed!</span>
                    </a>
                </li>
                <li class='disabled for-mac'>
                    <a href='#' title='Firefox (Mac) Explorer Privacy Walkthrough Video' onclick='return false;'>
                        <img src='/images/ff-logo.png' width='90' height='89' /><span class='label'>Firefox (Mac)</span>
                        <span class='volunteers-needed'>volunteers needed!</span>
                    </a>
                </li>
                <li class='disabled for-windows'>
                    <a href='#' title='Firefox (Windows) Explorer Privacy Walkthrough Video' onclick='return false;'>
                        <img src='/images/ff-logo.png' width='90' height='89' /><span class='label'>Firefox (Windows)</span>
                        <span class='volunteers-needed'>volunteers needed!</span>
                    </a>
                </li>
            </ul>
        </p>
        <div class='clearfix'></div>
        <h1>Frequently Asked Questions</h1>
        <p>
            <em>Here are some of the questions that many people like you have asked...</em>
        </p>
        <p>
            <h3>How do I add the "Scan for Privacy" bookmark?</h3>
            <p class='answer'>
                You can either <strong>drag</strong> it to your bookmarks bar or <strong>right click it</strong> and
                add it to your bookmarks/favorites.
            </p>
            <p class='answer'>
                <em class='soft'>this grey box is the bookmark:</em>
                <strong>
                    <a class='bookmarklet' title="Scan for Privacy" href="javascript:(function(){var%%20script=document.createElement('script');script.src='http://%(bookmarklet_host)s/javascripts/privacyscanner.js';document.getElementsByTagName('head')[0].appendChild(script);})()">Scan for Privacy</a>
                </strong>
            </p>
            <p class='answer'>
                <strong>After you have added that grey box bookmark</strong> you need to
                <a href='http://www.facebook.com/settings/?tab=privacy&ref=mb'>go to your Facebook privacy settings</a>.
                <strong>Once you are on Facebook</strong>, you should click that bookmark.
            </p>
        </p>
        <p>
            <h3>I can't drag the "Scan for Privacy" bookmark, what can I do?</h3>
            <p class='answer'>
                <strong>If you are using Safari or Chrome</strong>: click "View...Show Bookmarks Bar", and then you will be able to drag the link into it.
            </p>
            <p class='answer'>
                <strong>If you are using Internet Explorer</strong>: right-click the grey bookmark button, and click "Add to Favorites".
            </p>
        </p>
        <p>
            <h3>Why does the bookmark take me back to ReclaimPrivacy.org?</h3>
            <p class='answer'>
                You probably bookmarked the homepage, instead of bookmarking the
                grey "Scan for Privacy" button. Make sure that you bookmark (or favorite) the grey button,
                instead of the page.
            </p>
            <p class='answer'>
                <em class='soft'>this grey box is the bookmark:</em>
                <strong>
                    <a class='bookmarklet' title="Scan for Privacy" href="javascript:(function(){var%%20script=document.createElement('script');script.src='http://%(bookmarklet_host)s/javascripts/privacyscanner.js';document.getElementsByTagName('head')[0].appendChild(script);})()">Scan for Privacy</a>
                </strong>
            </p>
        </p>
        <p>
            <h3>Some of the settings never get fixed, what can I do?</h3>
            <p class='answer'>
                Sometimes the automatic fixes have trouble working, but the scan
                will <strong>always have a link</strong> to the right page in your privacy settings.  That
                way you can always go and fix that privacy setting yourself, even
                when the scanner cannot automatically fix it.
            </p>
        </p>
        <p>
            <h3>Why is the scanner stuck on the 2nd and 4th lines?</h3>
            <p class='answer'>
                We are currently working on fixing <a href='http://github.com/mjpizz/reclaimprivacy/issues#issue/2'>this bug</a> (if you are a programmer
                and can help, let me know).  The easiest thing to do in the
                meantime is to use Chrome, Internet Explorer, or Safari (those browsers work a bit better).
            </p>
        </p>

        <div class='go-to-discussions'>
            <em>
                If you still have trouble, you should
                <a href='http://www.facebook.com/pages/Reclaim-Privacy/121897834504447?v=app_2373072738'>
                    check out the discussion forums
                </a> on our Facebook Fan page, there are lots of
                other people there trying to help each other out.
            </em>
        </div>
    </div>

<!-- begin olark code -->
<script type='text/javascript'>
(function(d,u){var h=d.location.protocol=='https:'?'https://':'http://';d.write(
unescape("%%3Cscript src='"+h+u+"' type='text/javascript'%%3E%%3C/script%%3E"));
})(document,'static.olark.com/javascript/olark.js');
</script>
<a href='http://olark.com/about' id='olark-key' class='site-9122-608-10-8698' style='display:none' rel='nofollow'>
Powered by Olark
</a>
<!-- end olark code-->

<script type='text/javascript'>
olark.extend(function(api){
    api.chat.updateVisitorNickname({snippet: 'reclaimprivacy'})
});
</script>

</body>
</html>
            ''' % locals()

            # cache the page in memcache (only on the production servers)
            if 'reclaimprivacy.org' in parts.hostname:
                memcache.set(memcache_key, page_content)

        # write the response
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(page_content)


application = webapp.WSGIApplication([
    ('/application', DesktopApplication),
    ('/newsletter', Newsletter),
    ('/facebook', Facebook),
    ('/help', Help),
    ('/', Facebook),
], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()


