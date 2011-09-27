from string import Template

class Renderer:
    htmlForPage = Template('''
<html>
    <head>
        <title>Gio's little experiment for flat search</title>
    </head>

    <body>
        <div>Properties</div>
        <table>
            $properties
        </table>
    </body>
</html>''')

    htmlForItem = Template('''
            <tr>
                <td>$agent</td>
                <td>$price</td>
                <td><a href="$link">$address</a></td>
            </tr>
    ''')

    def render(self, properties):
        return self.htmlForPage.substitute({'properties' : ''.join([self._renderProperty(p) for p in properties])})

    def _renderProperty(self, property):
        return self.htmlForItem.substitute({
            'agent' : property.agent,
            'price' : property.price.monthlyPrice(),
            'address' : property.address,
            'link' : property.link
        })
