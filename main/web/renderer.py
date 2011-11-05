from string import Template

class Renderer:
    htmlForPage = Template('''
<html>
    <head>
        <title>Gio's little experiment for flat search</title>
		<script type="text/javascript" src="resources/jquery-1.6.4.min.js"></script>
		<script type="text/javascript" src="resources/rentscanner.js"></script>
    </head>

    <body>
        <h1>Properties</h1>
        <table>
            $properties
        </table>
    </body>
</html>''')

    htmlForItem = Template('''
            <tr id=$key>
                <td>$agent</td>
                <td>$price</td>
                <td><a href="$agentlink">$address</a></td>
                <td><img width="200" src="$imagelink" /></td>
                <td>$description</td>
                <td><button type="button" onclick="removeProperty('$key')">not interested</button></td>
            </tr>
    ''')

    def render(self, properties):
        return self.htmlForPage.substitute({'properties' : ''.join([self._renderProperty(p) for p in properties])})

    def _renderProperty(self, property):
        return self.htmlForItem.substitute({
            'key' : property.key(),
            'agent' : property.agent,
            'price' : property.price.monthlyPrice(),
            'address' : property.address,
            'agentlink' : property.link,
            'description' : property.description,
            'imagelink' : property.image
        })
