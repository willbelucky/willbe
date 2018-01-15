# -*- coding: utf-8 -*-
"""
:Author: Jaekyoung Kim
:Date: 2018. 1. 10.
"""

stock_master_create_table_sql = """
    CREATE TABLE IF NOT EXISTS `stock_master` (
        `code` VARCHAR(12) NOT NULL DEFAULT '',
        `short_code` VARCHAR(7) DEFAULT NULL,
        `company_name` VARCHAR(255) DEFAULT NULL,
        `market_name` VARCHAR(16) DEFAULT NULL,
        PRIMARY KEY (`code`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""

stock_daily_price_create_table_sql = """
    CREATE TABLE IF NOT EXISTS `stock_daily_price` (
        `code` VARCHAR(12) NOT NULL,
        `date` DATETIME NOT NULL,
        `volume` INT(11) DEFAULT NULL,
        `open` INT(11) DEFAULT NULL,
        `high` INT(11) DEFAULT NULL,
        `low` INT(11) DEFAULT NULL,
        `close` INT(11) DEFAULT NULL,
        `market_capitalization` BIGINT(11) DEFAULT NULL,
        `listed_stocks_number` BIGINT(11) DEFAULT NULL,
        PRIMARY KEY (`code`,`date`),
        INDEX `date` (`date`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""

stock_trend_create_table_sql = """
    CREATE TABLE IF NOT EXISTS `stock_trend` (
        `date` DATETIME NOT NULL,
        `code` VARCHAR(16) NOT NULL,
        `bank_buy` BIGINT,
        `bank_sell` BIGINT,
        `foreigner_buy` BIGINT,
        `foreigner_sell` BIGINT,
        `government_buy` BIGINT,
        `government_sell` BIGINT,
        `individual_buy` BIGINT,
        `individual_sell` BIGINT,
        `insurance_buy` BIGINT,
        `insurance_sell` BIGINT,
        `investing_organization_buy` BIGINT,
        `investing_organization_sell` BIGINT,
        `investment_trust_buy` BIGINT,
        `investment_trust_sell` BIGINT,
        `other_corporation_buy` BIGINT,
        `other_corporation_sell` BIGINT,
        `other_finance_buy` BIGINT,
        `other_finance_sell` BIGINT,
        `other_foreigner_buy` BIGINT,
        `other_foreigner_sell` BIGINT,
        `pension_fund_buy` BIGINT,
        `pension_fund_sell` BIGINT,
        `private_equity_fund_buy` BIGINT,
        `private_equity_fund_sell` BIGINT,
        PRIMARY KEY (`code`, `date`),
        INDEX `date` (`date`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""
