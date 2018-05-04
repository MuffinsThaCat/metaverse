#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
from TestCase.MVSTestCase import *

class TestAssetBoundary(MVSTestCaseBase):
    def getExistAssetSymbol(self):
        # symbol is already used.
        ec, message = mvs_rpc.get_asset()
        self.assertEqual(ec, 0, message)

        exist_assets = message["assets"]
        if not exist_assets:
            return None
        # pickup existing asset symbol by random
        i = random.randint(0, len(exist_assets) - 1)
        return exist_assets[i]

    def test_0_check_asset_symbol(self):
        spec_char_lst = "`~!@#$%^&*()-_=+[{]}\\|;:'\",<>/?"
        for char in spec_char_lst:
            ec, message = mvs_rpc.create_asset(Zac.name, Zac.password, Zac.asset_symbol + char, 100)
            self.assertEqual(ec, 1000, message)
            self.assertEqual(message, "symbol must be alpha or number or dot", message)

    def test_1_create_asset(self):
        #account password match error
        ec, message = mvs_rpc.create_asset(Zac.name, Zac.password + '1', Zac.asset_symbol, 100)
        self.assertEqual(ec, 1000, message)

        #aasset symbol can not be empty.
        ec, message = mvs_rpc.create_asset(Zac.name, Zac.password, "", 100)
        self.assertEqual(ec, 5011, message)

        #asset symbol length must be less than 64.
        ec, message = mvs_rpc.create_asset(Zac.name, Zac.password, "x" * 65, 100)
        self.assertEqual(ec, 5011, message)

        #asset description length must be less than 64.
        ec, message = mvs_rpc.create_asset(Zac.name, Zac.password, "x" * 64, 100, "x"*65)
        self.assertEqual(ec, 5007, message)

        #secondaryissue threshold value error, is must be -1 or in range of 0 to 100.
        ec, message = mvs_rpc.create_asset(Zac.name, Zac.password, "x" * 64, 100, "x" * 64, rate=-2)
        self.assertEqual(ec, 5016, message)

        ec, message = mvs_rpc.create_asset(Zac.name, Zac.password, "x" * 64, 100, "x" * 64, rate=101)
        self.assertEqual(ec, 5016, message)

        #asset decimal number must less than 20.
        ec, message = mvs_rpc.create_asset(Zac.name, Zac.password, "x" * 64, 100, "x" * 64, rate=0, decimalnumber=-1)
        self.assertEqual(ec, 5002, message)
        ec, message = mvs_rpc.create_asset(Zac.name, Zac.password, "x" * 64, 100, "x" * 64, rate=0, decimalnumber=20)
        self.assertEqual(ec, 5002, message)

        #volume must not be zero.
        ec, message = mvs_rpc.create_asset(Zac.name, Zac.password, "x" * 64, 0, "x" * 64, rate=0, decimalnumber=19)
        self.assertEqual(ec, 2003, message)
        #contain sensitive words

        ec, message = mvs_rpc.create_asset(Zac.name, Zac.password, "JZM.xxx", 10, "x" * 64, rate=0, decimalnumber=19)
        self.assertEqual(ec, 5012, message)

        exist_symbol = self.getExistAssetSymbol()
        if exist_symbol:
            ec, message = mvs_rpc.create_asset(Zac.name, Zac.password, exist_symbol, 10, "x" * 64, rate=0, decimalnumber=19)
            self.assertEqual(ec, 5009, message)

    def test_2_issue_asset(self):
        ten_etp = 10 * (10 ** 8)
        # account password match error
        ec, message = mvs_rpc.issue_asset(Zac.name, Zac.password + '2', Zac.asset_symbol, 1)
        self.assertEqual(ec, 1000, message)

        #issue asset fee less than 10 etp
        ec, message = mvs_rpc.issue_asset(Zac.name, Zac.password, Zac.asset_symbol, ten_etp - 1)
        self.assertEqual(ec, 5006, message)

        #asset symbol length must be less than 64
        ec, message = mvs_rpc.issue_asset(Zac.name, Zac.password, "x"*65, ten_etp)
        self.assertEqual(ec, 5011, message)

        #asset symbol is already exist in blockchain
        exist_symbol = self.getExistAssetSymbol()
        if exist_symbol:
            ec, message = mvs_rpc.issue_asset(Zac.name, Zac.password, exist_symbol, ten_etp)
            self.assertEqual(ec, 5009, message)

        #asset not in local database
        ec, message = mvs_rpc.issue_asset(Zac.name, Zac.password, Zac.asset_symbol, ten_etp)
        self.assertEqual(ec, 5010, message)

        def isDomainExist(domain):
            ec, message = mvs_rpc.get_asset()
            self.assertEqual(ec, 0, message)

            exist_assets = message["assets"]
            if not exist_assets:
                return False
            for i in exist_assets:
                if i.startswith(domain):
                    return True

        if isDomainExist("ALICE."):
            asset_symbol = Zac.asset_symbol.replace("ZAC.", "ALICE.")
            # domain cert not belong to current account
            ec, message = mvs_rpc.create_asset(Zac.name, Zac.password, asset_symbol, 100)
            self.assertEqual(ec, 0, message)

            ec, message = mvs_rpc.issue_asset(Zac.name, Zac.password, asset_symbol, ten_etp)
            self.assertEqual(ec, 5017, message)

    def test_3_list_assets(self):
        # account password match error
        ec, message = mvs_rpc.list_assets(Zac.name, Zac.password + '3')
        self.assertEqual(ec, 1000, message)

    def test_4_get_asset(self):
        #Illegal asset symbol length.
        ec, message = mvs_rpc.get_asset("x"*65)
        self.assertEqual(ec, 5011, message)

        #asset not exist
        ec, message = mvs_rpc.get_asset("JZM.xxx")
        self.assertEqual(ec, 0, message)
        self.assertEqual(message['assets'], None, message)

    def test_5_deletelocalasset(self):
        # account password match error
        ec, message = mvs_rpc.delete_localasset(Zac.name, Zac.password + '4', Zac.asset_symbol)
        self.assertEqual(ec, 1000, message)

        # asset not exist
        ec, message = mvs_rpc.delete_localasset(Zac.name, Zac.password, Zac.asset_symbol)
        self.assertEqual(ec, 5003, message)

        # asset not belong to Zac
        Frank.create_asset(False)
        ec, message = mvs_rpc.delete_localasset(Zac.name, Zac.password, Frank.asset_symbol)
        self.assertEqual(ec, 5003, message)

        Zac.create_asset(False)
        ec, message = mvs_rpc.delete_localasset(Zac.name, Zac.password, Zac.asset_symbol)
        self.assertEqual(ec, 0, message)

    def test_6_getaccountasset(self):
        # account password match error
        ec, message = mvs_rpc.get_accountasset(Zac.name, Zac.password + '5', Zac.asset_symbol)
        self.assertEqual(ec, 1000, message)

        # no asset
        ec, message = mvs_rpc.get_accountasset(Zac.name, Zac.password, Zac.asset_symbol)
        self.assertEqual(ec, 0, message)
        self.assertEqual({u'assets': None}, message)

        # with 1 asset
        Zac.create_asset(False)
        ec, message = mvs_rpc.get_accountasset(Zac.name, Zac.password)
        self.assertEqual(ec, 0, message)
        self.assertEqual(len(message["assets"]), 1, message)

        # with 2 assets
        ec, message = mvs_rpc.create_asset(Zac.name, Zac.password, Zac.asset_symbol + '1', 100)
        self.assertEqual(ec, 0, message)

        ec, message = mvs_rpc.get_accountasset(Zac.name, Zac.password)
        self.assertEqual(ec, 0, message)
        self.assertEqual(len(message["assets"]), 2, message)

        # asset_symbol sepecified
        ec, message = mvs_rpc.get_accountasset(Zac.name, Zac.password, Zac.asset_symbol)
        self.assertEqual(ec, 0, message)
        self.assertEqual(len(message["assets"]), 1, message)

        # --cert specified
        ec, message = mvs_rpc.get_accountasset(Zac.name, Zac.password, cert=True)
        self.assertEqual(ec, 0, message)
        self.assertEqual(message["assetcerts"], None, message)

    def test_7_getaddressasset(self):
        # invalid address
        ec, message = mvs_rpc.get_addressasset(Zac.mainaddress()+'1')
        self.assertEqual(ec, 4010, message)

        # no asset
        ec, message = mvs_rpc.get_addressasset(Zac.mainaddress())
        self.assertEqual(ec, 0, message)
        self.assertEqual({u'assets': None}, message)

        # --cert specified
        ec, message = mvs_rpc.get_addressasset(Zac.mainaddress(), cert=True)
        self.assertEqual(ec, 0, message)

    def test_8_sendasset(self):
        # account password match error
        ec, message = mvs_rpc.send_asset(Zac.name, Zac.password + '6', "", Zac.asset_symbol, 1)
        self.assertEqual(ec, 1000, message)

        # invalid to address parameter
        ec, message = mvs_rpc.send_asset(Zac.name, Zac.password, "111", Zac.asset_symbol, 1)
        self.assertEqual(ec, 4010, message)

        # invalid amount parameter
        ec, message = mvs_rpc.send_asset(Zac.name, Zac.password, Zac.mainaddress(), Zac.asset_symbol, 0)
        self.assertEqual(ec, 5002, message)

    def test_9_sendassetfrom(self):
        # account password match error
        ec, message = mvs_rpc.send_asset_from(Zac.name, Zac.password + '6', "", "", Zac.asset_symbol, 1)
        self.assertEqual(ec, 1000, message)

        # invalid from address
        ec, message = mvs_rpc.send_asset_from(Zac.name, Zac.password, "111", "222", Zac.asset_symbol, 1)
        self.assertEqual(ec, 4015, message)

        # invalid to address
        ec, message = mvs_rpc.send_asset_from(Zac.name, Zac.password, Zac.mainaddress(), "", Zac.asset_symbol, 1)
        self.assertEqual(ec, 4012, message)

        # invalid amount parameter
        ec, message = mvs_rpc.send_asset_from(Zac.name, Zac.password, Zac.mainaddress(), Frank.mainaddress(), Zac.asset_symbol, 0)
        self.assertEqual(ec, 5002, message)

    def test_A_burn(self):
        # account password match error
        ec, message = mvs_rpc.burn(Zac.name, Zac.password + '1', Zac.asset_symbol, 100)
        self.assertEqual(ec, 1000, message)

        # amount = 0
        ec, message = mvs_rpc.create_asset(Zac.name, Zac.password, Zac.asset_symbol, 0)
        self.assertEqual(ec, 2003, message)