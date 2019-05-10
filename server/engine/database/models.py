from datetime import datetime
from engine import db
from engine.helpers.service_helper import ServicesHelper
from engine.helpers.const.service_characteristics import TYPE, REGIONS, DEPLOYMENT_TIME, LEASING_PERIOD
import random
from sqlalchemy_imageattach.entity import Image, image_attachment
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_imageattach.context import store_context
from engine import store

Base = declarative_base()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'password': self.password
        }

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Provider(db.Model):
    """Provider model"""

    id = db.Column(db.Integer, primary_key=True)
    providerName = db.Column(db.String(100), nullable=False)
    serviceName = db.Column(db.String(100), nullable=False)
    image = image_attachment('ProviderImage')
    imageName = db.Column(db.String(30), default='default.png')
    description = db.Column(db.Text, nullable=False)
    type = db.Column(db.PickleType, nullable=False)
    features = db.Column(db.PickleType, nullable=False)
    region = db.Column(db.PickleType, nullable=False)
    deployment = db.Column(db.Text, nullable=False)
    leasingPeriod = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    currency = db.Column(db.Text, nullable=False)
    __tablename__ = 'provider'


    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'providerName': self.providerName,
            'serviceName': self.serviceName,
            'image': self.image.locate(),
            'description': self.description,
            'type': self.type,
            'features': self.features,
            'region': self.region,
            'deployment': self.deployment,
            'leasingPeriod': self.leasingPeriod,
            'price': self.price,
            'currency': self.currency,
        }

    def __repr__(self):
        return f"Provider('{self.serviceName}', '{self.type}', '{self.region}', '{self.price}', '{self.currency}')"


class ProviderImage(db.Model, Image):
    """Provider Image model"""
    provider_id = db.Column(db.Integer, db.ForeignKey('provider.id'), primary_key=True)
    provider = db.relationship('Provider')
    __tablename__ = 'provider_image'


class CustomerProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    region = db.Column(db.PickleType, nullable=False)
    serviceType = db.Column(db.PickleType, nullable=False)
    deploymentTime = db.Column(db.Text, nullable=False, default=datetime.utcnow)
    deploymentTimeWeight = db.Column(db.Integer, nullable=False)
    leasingPeriod = db.Column(db.PickleType, nullable=False)
    leasingPeriodWeight = db.Column(db.PickleType, nullable=False)
    budget = db.Column(db.Integer, nullable=False)
    budgetWeight = db.Column(db.Integer, nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'region': self.region,
            'serviceType': self.serviceType,
            'deploymentTime': self.deploymentTime,
            'deploymentTimeWeight': self.deploymentTimeWeight,
            'leasingPeriod': self.leasingPeriod,
            'leasingPeriodWeight': self.leasingPeriodWeight,
            'budget': self.budget,
            'budgetWeight': self.budgetWeight,
        }

    def __repr__(self):
        return f"CustomerProfile('{self.region}', '{self.serviceType}', '{self.deploymentTime}', '{self.leasingPeriod}', '{self.budget}')"

    def json_to_obj(self, json):
        self.region = json["region"]
        self.serviceType = json["serviceType"]
        self.deploymentTime = json["deploymentTime"]
        self.deploymentTimeWeight = json["deploymentTimeWeight"]
        self.leasingPeriod = json["leasingPeriod"]
        self.leasingPeriodWeight = json["leasingPeriodWeight"]
        self.budget = json["budget"]
        self.budgetWeight = json["budgetWeight"]
        return self


def load_data(app, db):
    service1 = Provider(providerName='Akamai', serviceName='Kona Site Defender',
                        imageName='akamai.png',
                        description='Kona Site Defender combines automated DDoS mitigation with a highly '
                                    'scalable and accurate WAF to protect websites from a wide range of online threats,'
                                    'including network- and application-layer DDoS, SQL injection and XSS attacks –'
                                    ' without compromising the user experience. Kona Site Defender can stop the largest'
                                    'attacks and leverages Akamai’s visibility into global web traffic to help '
                                    'organizations respond to the latest threats',
                        type=['PROACTIVE'], features=['VOLUMETRIC', 'PROTOCOL', 'APPLICATION LAYER', 'SSL', 'DNS'],
                        region=['NORTH AMERICA', 'SOUTH AMERICA', 'EUROPE'], deployment='SECONDS',
                        leasingPeriod='MINUTES', price=3500, currency='USD')


    service2 = Provider(providerName='CloudFlare', serviceName='Advanced DDoS Attack Protection',
                        imageName='cloudflare.png',
                        description='Cloudflare’s advanced DDoS protection, provisioned as a service at the network '
                                    'edge, matches the sophistication and scale of such threats, and can be used to '
                                    'mitigate DDoS attacks of all forms and sizes including those that target the UDP '
                                    'and ICMP protocols, as well as SYN/ACK, DNS amplification and Layer 7 attacks',
                        type=['PROACTIVE'], features=['VOLUMETRIC', 'PROTOCOL', 'APPLICATION', 'DNS'],
                        region=['NORTH AMERICA', 'SOUTH AMERICA', 'EUROPE'], deployment='SECONDS',
                        leasingPeriod='MONTHS', price=4900, currency='USD')

    service3 = Provider(providerName='Imperva', serviceName='Incapsula',
                        imageName='imperva.svg',
                        description='The Imperva Incapsula service delivers a multi-faceted approach to DDoS defense, '
                                    'providing blanket protection from all DDoS attacks to shield your critical '
                                    'online assets from these threats. Incapsula DDoS protection services are backed '
                                    'by a 24x7 security team, 99.999% uptime SLA, and a powerful, global network of '
                                    'data centers.',
                        type=['PROACTIVE'], features=['VOLUMETRIC', 'PROTOCOL', 'APPLICATION', 'SSL', 'DNS'],
                        region=['NORTH AMERICA', 'SOUTH AMERICA', 'EUROPE'], deployment='SECONDS',
                        leasingPeriod='DAYS', price=4500, currency='USD')

    service4 = Provider(providerName='Verisign', serviceName='Verisign DDoS Protection Service',
                        imageName='verisign.png',
                        description='Verisign DDoS Protection Services help organisations reduce the risk of '
                                    'catastrophic DDoS attacks by detecting and filtering malicious traffic aimed at '
                                    'disrupting or disabling their internet-based services. Unlike traditional security'
                                    ' solutions, Verisign DDoS Protection Services filter harmful traffic upstream of '
                                    'the organisational network or in the cloud',
                        type=['PROACTIVE'], features=['VOLUMETRIC', 'PROTOCOL', 'APPLICATION', 'SSL', 'DNS'],
                        region=['NORTH AMERICA', 'SOUTH AMERICA', 'EUROPE'], deployment='SECONDS',
                        leasingPeriod='MONTHS', price=3700, currency='USD')

    service5 = Provider(providerName='Arbor Networks', serviceName='Arbor Cloud',
                        imageName='arbor.png',
                        description='Arbor Cloud is a DDoS service powered by the world’s leading experts in DDoS '
                                    'mitigation, together with the most widely deployed DDoS protection technology',
                        type=['PROACTIVE'], features=['VOLUMETRIC', 'PROTOCOL', 'APPLICATION' 'SSL', 'DNS'],
                        region=['NORTH AMERICA', 'SOUTH AMERICA', 'EUROPE'], deployment='DAYS',
                        leasingPeriod='MONTHS', price=3000, currency='USD')

    service6 = Provider(providerName='Check Point Software Technologies', serviceName='DDos Protector',
                        imageName='checkPoint.png',
                        description='Check Point DDoS Protector™Appliances block Denial of Service attacks within '
                                    'seconds with multi-layered protection and up to 40 Gbps of performance. Modern '
                                    'DDoS attacks use new techniques to exploit areas where traditional security '
                                    'solutions are not equipped to protect. These attacks can cause serious network '
                                    'downtime to businesses who rely on networks and Web services to operate. DDoS '
                                    'Protectors extend company’s security perimeters to block destructive DDoS attacks '
                                    'before they cause damage.',
                        type=['REACTIVE'], features=['APPLICATION', 'DNS'],
                        region=['NORTH AMERICA', 'SOUTH AMERICA', 'EUROPE', 'ASIA'], deployment='SECONDS',
                        leasingPeriod='DAYS', price=2400, currency='USD')

    service7 = Provider(providerName='Corero Network Security, Inc.', serviceName='SmartWall® Threat Defense System',
                        imageName='corero.png',
                        description='The Corero SmartWall Threat Defense System (TDS) delivers comprehensive DDoS '
                                    'protection, eliminating attacks automatically and in real-time.The SmartWall '
                                    'Network Threat Defense (NTD) solutions include innovative technology for the '
                                    'mitigation of DDoS attacks of all sizes, including stealthy sub-saturating '
                                    'attacks, in seconds vs minutes (in contrast to legacy DDoS solutions), allowing '
                                    'good user traffic to flow uninterrupted and enabling applications and services to '
                                    'remain online, continuously, even whilst under attack',
                        type=['REACTIVE'], features=['APPLICATION', 'VOLUMETRIC'],
                        region=['NORTH AMERICA', 'SOUTH AMERICA', 'EUROPE', 'ASIA'], deployment='SECONDS',
                        leasingPeriod='MINUTES', price=3200, currency='USD')

    service8 = Provider(providerName='Flowmon Networks', serviceName='Flowmon DDoS Defender',
                        imageName='flowmon.png',
                        description='Flowmon DDoS Defender puts advanced artificial intelligence between your critical '
                                    'systems and criminals. Without any changes in infrastructure, in a matter of '
                                    'minutes, network and security engineers will have up-and-running active DDoS '
                                    'protection',
                        type=['REACTIVE'], features=['APPLICATION'],
                        region=['NORTH AMERICA', 'SOUTH AMERICA', 'EUROPE', 'ASIA'], deployment='SECONDS',
                        leasingPeriod='MONTHS', price=2345, currency='USD')

    service9 = Provider(providerName='Level 3 Communications', serviceName='Level 3 DDos Mitigation',
                        imageName='level3.png',
                        description='Level 3 provides layers of defense through enhanced network routing, rate '
                                    'limiting and filtering that can be paired with advanced network-based detection '
                                    'and mitigation scrubbing center solutions. Our mitigation approach is informed by '
                                    'threat intelligence derived from visibility across our global infrastructure and '
                                    'data correlation. Tailored for any business and IT/security budget, our flexible '
                                    'managed service can proactively detect and mitigate the threats of today to help '
                                    'ensure business-as-usual for employees, partners and customers',
                        type=['REACTIVE'], features=['APPLICATION', 'VOLUMETRIC'],
                        region=['EUROPE'], deployment='MINUTES',
                        leasingPeriod='DAYS', price=1090, currency='USD')

    service10 = Provider(providerName='F5 Networks', serviceName='F5 Silverline DDoS Protection',
                         imageName='f5silverline.png',
                         description=' F5’s DDoS Protection solution protects the fundamental elements of an application'
                                    ' (network, DNS, SSL, and HTTP) against distributed denial-of-service attacks. '
                                    'Leveraging the intrinsic security capabilities of intelligent traffic management '
                                    'and application delivery, F5 protects and ensures availability of an '
                                    'organization\'s network and application infrastructure under the most '
                                    'demanding conditions',
                         type=['REACTIVE'], features=['APPLICATION', 'VOLUMETRIC'],
                         region=['EUROPE'], deployment='HOURS',
                         leasingPeriod='DAYS', price=890, currency='USD')

    set_image(service1)
    set_image(service2)
    set_image(service3)
    set_image(service4)
    set_image(service5)
    set_image(service6)
    set_image(service7)
    set_image(service8)
    set_image(service9)
    set_image(service10)


def set_image(service):
    with store_context(store):
        with open(f"static/images/{service.imageName}", 'rb') as f:
            service.image.from_file(f)
        db.session.add(service)
        db.session.commit()


# For testing purposes
def mock_services():
    sh = ServicesHelper([])
    for i in range(0, 1000):
        s = Provider()
        s.id = i
        s.price = random.randint(0, 5000)
        s.type = "REACTIVE" if i % 2 == 0 else "PROACTIVE"
        s.region = [REGIONS[i % len(REGIONS)]]
        s.deployment = DEPLOYMENT_TIME[i % len(DEPLOYMENT_TIME)]
        s.leasingPeriod = LEASING_PERIOD[i % len(LEASING_PERIOD)]
        sh.services.append(s)
    return sh
