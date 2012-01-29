from string import Template

class Renderer(object):
    htmlForPage = Template('''
<html>
    <head>
        <title>Gio's little experiment for flat search</title>
        <link rel="shortcut icon" href="/resources/favicon.jpg" />
        <link rel="stylesheet" href="/resources/style.css" type="text/css" />
		<script type="text/javascript" src="/resources/jquery-1.6.4.min.js"></script>
        <script type="text/javascript" src="/resources/jquery.cookie.js"></script>
		<script type="text/javascript" src="/resources/rentscanner.js"></script>
    </head>

    <body>
        <div id="controls" class="navigation">
            <div class="name">Rentscanner</div>
            <div id="newProperties" class="clickable">new</div>
            <div id="saraLikes" class="clickable">she likes</div>
            <div id="gioLikes" class="clickable">he likes</div>
            <div id="bothLike" class="clickable">they like</div>
            <div id="discardedProperties" class="clickable">trashed</div>
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

    htmlForPropertyButtons = Template('''
                <div class="save"><button type="button" onclick="saveProperty('$key')">$user likes</button></div>
                <div class="remove"><button type="button" onclick="removeProperty('$key')">$user doesn't like</button></div>
    ''')

    def __init__(self, user=None):
        self.user = user

    def renderFullPage(self, properties, type):
        return self.renderPropertiesOnTemplate(self.htmlForPage, properties, type)

    def renderFragment(self, properties, type):
        return self.renderPropertiesOnTemplate(self.htmlForFragment, properties, type)

    def renderPropertiesOnTemplate(self, template, properties, type):
        return template.substitute({
            'properties': ''.join([self._renderProperty(p, type) for p in properties]) if properties else 'No properties found',
            'userwelcome' : 'Hi ' + self.user if self.user else 'Who are you?<input type="text" id="username" name="username" /><button type="button" onclick="setUser()">Set</button>'
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
