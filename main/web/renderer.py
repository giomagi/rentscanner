from string import Template

class Renderer(object):
    htmlForPage = Template('''
<html>
    <head>
        <title>Gio's little experiment for flat search</title>
        <link rel="shortcut icon" href="/resources/favicon.jpg" />
		<script type="text/javascript" src="/resources/jquery-1.6.4.min.js"></script>
		<script type="text/javascript" src="/resources/rentscanner.js"></script>
    </head>

    <body>
        <div>
            <button type="button" onclick="showNewProperties()">show new</button>
            <button type="button" onclick="showSavedProperties()">show saved</button>
        </div>
        <table id="properties">
            $properties
        </table>
    </body>
</html>''')

    htmlForFragment = Template('''
        <table id="properties">
            $properties
        </table>''')

    htmlForItem = Template('''
            <tr id=$key>
                <td><img width="100" src="$agentimage" alt="$agent" /></td>
                <td>$price</td>
                <td><a href="$agentlink">$address</a></td>
                <td><img width="200" src="$imagelink" /></td>
                <td>$description</td>
                <td><button type="button" onclick="saveProperty('$key')">interested</button></td>
                <td><button type="button" onclick="removeProperty('$key')">not interested</button></td>
            </tr>
    ''')

    def renderFullPage(self, properties):
        return self.renderPropertiesOnTemplate(self.htmlForPage, properties)

    def renderFragment(self, properties):
        return self.renderPropertiesOnTemplate(self.htmlForFragment, properties)

    def renderPropertiesOnTemplate(self, template, properties):
        if not len(properties):
            return template.substitute({'properties': 'No properties found'})
        else:
            return template.substitute({'properties': ''.join([self._renderProperty(p) for p in properties])})

    def _renderProperty(self, property):
        return self.htmlForItem.substitute({
            'key' : property.key(),
            'agentimage' : self.imageFor(property.agent),
            'agent' : property.agent,
            'price' : property.price.monthlyPrice(),
            'address' : property.address,
            'agentlink' : property.link,
            'description' : property.description,
            'imagelink' : property.image
        })

    def imageFor(self, agent):
        return '/resources/' + agent.lower() + '.jpeg'
