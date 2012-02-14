import datetime
from main.domain.configuration import Configuration
from main.houses.model import Property, Price, Address
from main.houses.persistence import Librarian

#properties = [Property('AGENT', Price(9999, 'PERIOD'), Address('ADDRESS', 'POSTCODE'), 'LINK', 'ID', datetime.datetime.now(), 'No description, manual load', 'resources/sorry_no_image.jpeg')]

properties = [
    Property('ZachKnightons',
        Price(475, 'week'),
        Address('Pond House, Pond Place', 'SW3'),
        'http://www.zachknightons.co.uk/SW3/London/Pond-House/2-bed/property.vtx?p=5FB944C9-A37B-41FC-8DF4-3AE374062DFC',
        '5FB944C9-A37B-41FC-8DF4-3AE374062DFC',
        datetime.datetime.now(),
        'No description, manual load',
        'resources/sorry_no_image.jpeg'),
    Property('Remax',
        Price(499, 'week'),
        Address('St George\'s Square', 'SW1V'),
        'http://www.remax-londoncentral.co.uk/Property/Residential/for-rent/LONDON/Pimlico/St-Georges-Square/1633045.aspx',
        '1633045',
        datetime.datetime.now(),
        'No description, manual load',
        'http://media.estateweb.com/PhotoServ/Default.aspx?a=657&i=1.jpg&r=1633045&l=4&h=235&w=351&st=&rt=1.2&ds=1&lt=6&t=0&resinfo=&ct=3'),
    Property('Remax',
        Price(475, 'week'),
        Address('Emperor\'s Gate', 'SW7'),
        'http://www.remax-londoncentral.co.uk/Property/Residential/for-rent/London/Kensignton/Emperors-Gate/2424712.aspx',
        '2424712',
        datetime.datetime.now(),
        'No description, manual load',
        'resources/sorry_no_image.jpeg'),
    Property('LondonLivingHomes',
        Price(1738, 'month'),
        Address('Dawes Road, Fulham', 'SW6'),
        'http://www.londonlivinghomes.co.uk/index.php?url=property&wci=xml&db=dezrez&wce=002419885',
        '002419885',
        datetime.datetime.now(),
        'No description, manual load',
        'http://data.dezrez.com/PictureResizer.ASP?PropertyID=2419885&PhotoID=1&AgentID=982&BranchID=1602&width=485&rotation=0'),
    Property('JohnDWood',
        Price(460, 'week'),
        Address('Ifield Road', 'SW10'),
        'http://www.johndwood.co.uk/property-to-let/London-SW10-LON093109',
        'LON093109',
        datetime.datetime.now(),
        'No description, manual load',
        'http://www.johndwood.co.uk/index.php?action=getthumbnail&filepath=aspasia/pictures/3728_000093109_IMG_00.jpg&width=230&height=150&quality=75&crop=0'),
    ]

Librarian(Configuration.prod()).archiveProperties(properties)
