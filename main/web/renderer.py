from string import Template

class Renderer(object):
    htmlForPage = Template('''
<html>
    <head>
        <title>Gio's little experiment for flat search</title>
        <link rel="shortcut icon" href="/resources/favicon.jpg" />
        <link rel="stylesheet" href="/resources/style.css" type="text/css" />
		<script type="text/javascript" src="/resources/jquery-1.6.4.min.js"></script>
		<script type="text/javascript" src="/resources/rentscanner.js"></script>
    </head>

    <body>
        <div id="controls" class="navigation">
            <div id="newProperties" class="clickable">View New</div>
            <div id="savedProperties" class="clickable">View Saved</div>
        </div>
        <div id="properties" class="content">
            $properties
        </div>
        <script>
            $$('#newProperties').click(showNewProperties);
            $$('#savedProperties').click(showSavedProperties);
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
                <div class="save"><button type="button" onclick="saveProperty('$key')">interested</button></div>
                <div class="remove"><button type="button" onclick="removeProperty('$key')">not interested</button></div>
            </div>
    ''')

    def renderFullPage(self, properties, type):
        return self.renderPropertiesOnTemplate(self.htmlForPage, properties, type)

    def renderFragment(self, properties, type):
        return self.renderPropertiesOnTemplate(self.htmlForFragment, properties, type)

    def renderPropertiesOnTemplate(self, template, properties, type):
        if not len(properties):
            return template.substitute({'properties': 'No properties found'})
        else:
            return template.substitute({'properties': ''.join([self._renderProperty(p, type) for p in properties])})

    def _renderProperty(self, property, type):
        return self.htmlForItem.substitute({
            'key' : property.key(),
            'agentimage' : self.imageFor(property.agent),
            'agent' : property.agent,
            'price' : property.price.monthlyPrice(),
            'address' : property.address,
            'agentlink' : property.link,
            'description' : property.description,
            'imagelink' : property.image,
            'type' : type
        })

    def imageFor(self, agent):
        return '/resources/' + agent.lower() + '.jpeg'
