from string import Template

class Renderer(object):
    htmlForPage = Template('''
<html>
    <head>
        <title>Sara and Gio magical home finder</title>
        <link rel="shortcut icon" href="/resources/favicon.jpg" />
        <link rel="stylesheet" href="/resources/style.css" type="text/css" />
		<script type="text/javascript" src="/resources/jquery-1.6.4.min.js"></script>
        <script type="text/javascript" src="/resources/jquery.cookie.js"></script>
		<script type="text/javascript" src="/resources/rentscanner.js"></script>
    </head>

    <body>
        <div id="controls" class="navigation">
            <div class="name">Rentscanner</div>
            <div id="newProperties" class="clickable selected">new</div>
            <div id="saraLikes" class="clickable">she likes</div>
            <div id="gioLikes" class="clickable">he likes</div>
            <div id="bothLike" class="clickable">they like</div>
            <div id="seen" class="clickable">they've seen</div>
            <div id="discardedProperties" class="clickable">no one likes</div>
            <div id="user">$userwelcome</div>
        </div>
        <div id="properties" class="content">
            $properties
        </div>
        <script>
            $$('#newProperties').click(showNewProperties);
            $$('#saraLikes').click(showSaraLikesProperties);
            $$('#gioLikes').click(showGioLikesProperties);
            $$('#bothLike').click(showBothLikeProperties);
            $$('#seen').click(showSeenProperties);
            $$('#discardedProperties').click(showDiscardedProperties);
        </script>
    </body>
</html>''')

    htmlForFragment = Template('''
        <div id="properties" class="content">
            $properties
        </div>''')

    htmlForItem = Template('''
            <div id="$key" class="property $type">
                <div class="agent"><img src="$agentimage" width="100" alt="$agent" /></div>
                <div class="price">$price</div>
                <div class="address"><a href="$agentlink">$address</a></div>
                <div class="image"><img src="$imagelink" width="200" /></div>
                <div class="description">$description</div>
                <div class="buttons">$buttons</div>
            </div>
    ''')

    def __init__(self, user=None):
        self.user = user

    htmlForPropertyButtons = Template('''
                <div class="saveButton"><button type="button" onclick="saveProperty('$key')">$user likes</button></div>
                <div class="seenButton" style="display:none"><button type="button" onclick="archiveProperty('$key')">seen</button></div>
                <div class="removeButton"><button type="button" onclick="removeProperty('$key')">$user doesn't like</button></div>
    ''')

    def renderFullPage(self, properties, type):
        return self.renderPropertiesOnTemplate(self.htmlForPage, properties, type)

    def renderFragment(self, properties, type):
        return self.renderPropertiesOnTemplate(self.htmlForFragment, properties, type)

    def renderPropertiesOnTemplate(self, template, properties, type):
        return template.substitute({
            'properties': ''.join([self._renderProperty(p, type) for p in properties]) if properties else 'No properties found',
            'userwelcome' : 'Ciao ' + self.user if self.user else 'Who are you?<input type="text" id="username" name="username" /><button type="button" onclick="setUser()">Set</button>'
        })

    def _renderProperty(self, property, type):
        return self.htmlForItem.substitute({
            'key': property.key(),
            'agentimage': self.imageFor(property.agent),
            'agent': property.agent,
            'price': property.price.monthlyPrice(),
            'address': property.address,
            'agentlink': property.link,
            'description': property.description,
            'imagelink': property.image,
            'buttons': self.htmlForPropertyButtons.substitute({'key': property.key(), 'user': self.user}) if self.user in ['gio', 'sara'] else '&nbsp;',
            'type': type
        })

    def imageFor(self, agent):
        return '/resources/' + agent.lower() + '.jpeg'


class LogRenderer(object):
    htmlForLogPage = Template('''
<html>
    <head>
        <title>The crappy load logger for Sara and Gio magical home finder</title>
        <link rel="stylesheet" href="/resources/style.css" type="text/css" />
    </head>
    <body>
        <pre>$stats</pre>
    </body>
</html>''')

    def renderLogPage(self, loadStats):
        return self.htmlForLogPage.substitute({'stats' : self.niceTextFrom(loadStats)})

    def niceTextFrom(self, stats):
        return 'started   @ ' + stats['startTime'] + '\n' + 'completed @ ' + stats['endTime'] + '\n\n' + self.formatAgentStats(stats['agents'])

    def formatAgentStats(self, dictAsString):
        # in a nicer way with a regex
        return dictAsString.replace('\'', '').replace(':', '\t').replace('{', '').replace('}', '').replace(',', '').replace('"', '') + '\n'
