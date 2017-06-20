# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from json import loads
from eth.event_receiver import (
    CentralizedOracleFactoryReceiver, UltimateOracleFactoryReceiver, EventFactoryReceiver, MarketFactoryReceiver,
    EventInstanceReceiver
)

from relationaldb.models import (
    CentralizedOracle, UltimateOracle, ScalarEvent, CategoricalEvent, Market, OutcomeToken
)

from relationaldb.factories import (
    UltimateOracleFactory, CentralizedOracleFactory,
    OracleFactory, EventFactory, MarketFactory, OutcomeTokenFactory
)
from datetime import datetime
from time import mktime
from ipfs.ipfs import Ipfs


class TestEventReceiver(TestCase):

    def setUp(self):
        self.ipfs_api = Ipfs()

    def to_timestamp(self, datetime_instance):
        return mktime(datetime_instance.timetuple())

    def test_centralized_oracle_receiver(self):
        oracle = CentralizedOracleFactory()
        # saving event_description to IPFS
        event_description_json = {
            'title':'Test title',
            'description': 'test long description',
            'resolution_date': datetime.now().isoformat(),
            'outcomes': ['YES', 'NO']
        }

        ipfs_hash = self.ipfs_api.post(event_description_json)

        block = {
            'number': oracle.creation_block,
            'timestamp': self.to_timestamp(oracle.creation_date_time)
        }

        oracle_address = oracle.address[1:-7] + 'GIACOMO'

        oracle_event = {
            'address': oracle.factory[1:-7] + 'GIACOMO',
            'params': [
                {
                    'name': 'creator',
                    'value': oracle.creator
                },
                {
                    'name': 'centralizedOracle',
                    'value': oracle_address,
                },
                {
                    'name': 'ipfsHash',
                    'value': ipfs_hash
                }
            ]
        }

        CentralizedOracleFactoryReceiver().save(oracle_event, block)
        created_oracle = CentralizedOracle.objects.get(address=oracle_address)
        self.assertIsNotNone(created_oracle.pk)

    def test_ultimate_oracle_receiver(self):
        forwarded_oracle = CentralizedOracleFactory()
        ultimate_oracle = UltimateOracleFactory()

        block = {
            'number': ultimate_oracle.creation_block,
            'timestamp': mktime(ultimate_oracle.creation_date_time.timetuple())
        }

        oracle_address = ultimate_oracle.address[0:7] + 'another'

        oracle_event = {
            'address': ultimate_oracle.factory[0:7] + 'another',
            'params': [
                {
                    'name': 'creator',
                    'value': ultimate_oracle.creator
                },
                {
                    'name': 'ultimateOracle',
                    'value': oracle_address,
                },
                {
                    'name': 'oracle',
                    'value': forwarded_oracle.address
                },
                {
                    'name': 'collateralToken',
                    'value': ultimate_oracle.collateral_token
                },
                {
                    'name': 'spreadMultiplier',
                    'value': ultimate_oracle.spread_multiplier
                },
                {
                    'name': 'challengePeriod',
                    'value': ultimate_oracle.challenge_period
                },
                {
                    'name': 'challengeAmount',
                    'value': ultimate_oracle.challenge_amount
                },
                {
                    'name': 'frontRunnerPeriod',
                    'value': ultimate_oracle.front_runner_period
                }
            ]
        }

        UltimateOracleFactoryReceiver().save(oracle_event, block)
        created_oracle = UltimateOracle.objects.get(address=oracle_address)
        self.assertIsNotNone(created_oracle.pk)

    def test_scalar_event_receiver(self):
        oracle = OracleFactory()
        event = EventFactory()
        event_address = event.address[0:33] + 'GIACOMO'

        block = {
            'number': oracle.creation_block,
            'timestamp': self.to_timestamp(oracle.creation_date_time)
        }

        scalar_event = {
            'address': oracle.factory[0:33] + 'GIACOMO',
            'name': 'ScalarEventCreation',
            'params': [
                {
                    'name': 'creator',
                    'value': oracle.creator
                },
                {
                    'name': 'collateralToken',
                    'value': event.collateral_token
                },
                {
                    'name': 'oracle',
                    'value': oracle.address
                },
                {
                    'name': 'outcomeCount',
                    'value': 1
                },
                {
                    'name': 'upperBound',
                    'value': 1
                },
                {
                    'name': 'lowerBound',
                    'value': 0
                },
                {
                    'name': 'scalarEvent',
                    'value': event_address
                }
            ]
        }

        EventFactoryReceiver().save(scalar_event, block)
        event = ScalarEvent.objects.get(address=event_address)
        self.assertIsNotNone(event.pk)

    def test_categorical_event_receiver(self):
        event = EventFactory()
        oracle = OracleFactory()
        event_address = event.address[0:33] + 'GIACOMO'

        block = {
            'number': oracle.creation_block,
            'timestamp': self.to_timestamp(oracle.creation_date_time)
        }

        categorical_event = {
            'address': oracle.factory[0:33] + 'GIACOMO',
            'name': 'CategoricalEventCreation',
            'params': [
                {
                    'name': 'creator',
                    'value': oracle.creator
                },
                {
                    'name': 'collateralToken',
                    'value': event.collateral_token
                },
                {
                    'name': 'oracle',
                    'value': oracle.address
                },
                {
                    'name': 'outcomeCount',
                    'value': 1
                },
                {
                    'name': 'categoricalEvent',
                    'value': event_address
                }
            ]
        }

        EventFactoryReceiver().save(categorical_event, block)
        event = CategoricalEvent.objects.get(address=event_address)
        self.assertIsNotNone(event.pk)

    def test_market_receiver(self):
        event = EventFactory()
        market = MarketFactory()
        oracle = OracleFactory()
        event_address = event.address

        block = {
            'number': oracle.creation_block,
            'timestamp': self.to_timestamp(oracle.creation_date_time)
        }

        market_dict = {
            'address': oracle.factory[1:-7] + 'GIACOMO',
            'params': [
                {
                    'name': 'creator',
                    'value': oracle.creator
                },
                {
                    'name': 'centralizedOracle',
                    'value': oracle.address[1:-7] + 'GIACOMO',
                },
                {
                    'name': 'marketMaker',
                    'value': market.market_maker
                },
                {
                    'name': 'fee',
                    'value': market.fee
                },
                {
                    'name': 'eventContract',
                    'value': event_address
                },
                {
                    'name': 'fee',
                    'value': market.fee
                },
                {
                    'name': 'market',
                    'value': market.address[0:7] + 'another'
                }
            ]
        }

        MarketFactoryReceiver().save(market_dict, block)
        market = Market.objects.get(event=event_address)
        self.assertIsNotNone(market.pk)

    #
    # contract instances
    #

    # def test_centralized_oracle_instance_receiver(self):
    #     oracle_factory = CentralizedOracleFactory()
    #     oracle_address = oracle_factory.address[1:-7] + 'GIACOMO'
    #     # oracle.event_description
    #     event_description_json = {
    #         'title': oracle_factory.event_description.title,
    #         'description': oracle_factory.event_description.description,
    #         'resolution_date': oracle_factory.event_description.resolution_date.isoformat(),
    #         'outcomes': ['Yes', 'No']
    #     }
    #
    #     # save event_description to IPFS
    #     ipfs_hash = self.ipfs_api.post(event_description_json)
    #
    #     block = {
    #         'number': oracle_factory.creation_block,
    #         'timestamp': mktime(oracle_factory.creation_date_time.timetuple())
    #     }
    #
    #     oracle_event = {
    #         'address': oracle_factory.factory[0:-7] + 'GIACOMO',
    #         'params': [
    #             {
    #                 'name': 'creator',
    #                 'value': oracle_factory.address
    #             },
    #             {
    #                 'name': 'centralizedOracle',
    #                 'value': oracle_factory.address[1:-8] + 'INSTANCE',
    #             },
    #             {
    #                 'name': 'ipfsHash',
    #                 'value': ipfs_hash
    #             }
    #         ]
    #     }
    #
    #     CentralizedOracleInstanceReceiver().save(oracle_event, block)
    #     created_oracle = CentralizedOracle.objects.get(address=oracle_address)
    #     self.assertIsNotNone(created_oracle.pk)

    def test_event_instance_receiver(self):
        outcome_token_factory = OutcomeTokenFactory()
        oracle_factory = OracleFactory()
        event_factory = EventFactory()
        event_address = event_factory.address[0:-7] + 'GIACOMO'

        block = {
            'number': oracle_factory.creation_block,
            'timestamp': mktime(oracle_factory.creation_date_time.timetuple())
        }

        scalar_event = {
            'name': 'ScalarEventCreation',
            'address': oracle_factory.factory[1:-12] + 'TESTINSTANCE',
            'params': [
                {
                    'name': 'creator',
                    'value': oracle_factory.creator
                },
                {
                    'name': 'collateralToken',
                    'value': event_factory.collateral_token
                },
                {
                    'name': 'oracle',
                    'value': oracle_factory.address
                },
                {
                    'name': 'outcomeCount',
                    'value': 1
                },
                {
                    'name': 'upperBound',
                    'value': 1
                },
                {
                    'name': 'lowerBound',
                    'value': 0
                },
                {
                    'name': 'scalarEvent',
                    'value': event_address
                }
            ]
        }

        EventFactoryReceiver().save(scalar_event, block)
        event = ScalarEvent.objects.get(address=event_address)

        block = {
            'number': oracle_factory.creation_block,
            'timestamp': mktime(oracle_factory.creation_date_time.timetuple())
        }
        outcome_token_address = oracle_factory.address[1:-8] + 'INSTANCE'
        outcome_event = {
            'name': 'OutcomeTokenCreation',
            'address': oracle_factory.factory[0:-7] + 'GIACOMO',
            'params': [
                {
                    'name': 'creator',
                    'value': event.creator
                },
                {
                    'name': 'address',
                    'value': event.address
                },
                {
                    'name': 'outcomeToken',
                    'value': outcome_token_address,
                },
                {
                    'name': 'index',
                    'value': outcome_token_factory.index
                }
            ]
        }
        EventInstanceReceiver().save(outcome_event, block)
        self.assertIsNotNone(OutcomeToken.objects.get(address=outcome_token_address))
