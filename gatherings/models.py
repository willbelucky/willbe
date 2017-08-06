# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from willbe.models import BaseModel


class Item(BaseModel):
    item_code = models.CharField(max_length=8)
    item_name = models.CharField(max_length=128)
    item_type = models.CharField(max_length=16)


class Currency(BaseModel):
    abbreviation = models.CharField(max_length=3)
    original_word = models.CharField(max_length=128)

    def __str__(self):
        return self.abbreviation


class ExchangeRate(BaseModel):
    from_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='%(class)s_from')
    to_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='%(class)s_to')
    exchange_rate = models.DecimalField(max_digits=20, decimal_places=4)

    def __str__(self):
        return self.from_currency.__str__() + '/' + self.to_currency.__str__()


class Price(BaseModel):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=20, decimal_places=4)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class ClosingPrice(Price):
    date = models.DateField()


class RealTimePrice(Price):
    time = models.DateTimeField()


# class FinancialStatement(BaseModel):
#     d = 0
    # 매출액	2,062,060	2,006,535	2,018,667	2,384,935	478,156	533,317	505,475	583,351
    # 영업이익	250,251	264,134	292,407	526,073	52,001	92,208	98,984	131,252
    # 세전계속사업이익	278,750	259,610	307,137	537,273	59,707	95,485	101,646	135,412
    # 당기순이익	233,944	190,601	227,261	404,454	45,379	70,880	76,844	102,126
    # 당기순이익(지배)	230,825	186,946	224,157	396,954	44,088	69,172	74,885	98,175
    # 당기순이익(비지배)	3,119	3,655	3,104		1,291	1,709	1,958
    # 자산총계	2,304,230	2,421,795	2,621,743	2,973,518	2,444,715	2,621,743	2,642,174	2,765,315
    # 부채총계	623,348	631,197	692,113	761,778	649,351	692,113	743,994	703,190
    # 자본총계	1,680,882	1,790,598	1,929,630	2,211,742	1,795,364	1,929,630	1,898,180	2,062,125
    # 자본총계(지배)	1,621,817	1,728,768	1,864,243	2,141,488	1,732,697	1,864,243	1,831,196	1,991,331
    # 자본총계(비지배)	59,065	61,830	65,387		62,667	65,387	66,983
    # 자본금	8,975	8,975	8,975	8,859	8,975	8,975	8,975	8,975
    # 영업활동현금흐름	369,754	400,618	473,856	567,236	143,366	109,859	105,973	152,104
    # 투자활동현금흐름	-328,064	-271,678	-296,587	-405,879	-121,809	-73,008	-81,651	-63,790
    # 재무활동현금흐름	-30,571	-65,735	-86,695	-110,601	-14,919	15,909	-51,889	-38,426
    # CAPEX	220,429	258,802	241,430	348,510	53,999	99,993	89,017	65,000
    # FCF	149,324	141,815	232,427	221,056	89,367	9,866	16,956	72,966
    # 이자발생부채	112,655	128,740	152,824		129,573	152,824	132,493
    # 영업이익률	12.14	13.16	14.49	22.06	10.88	17.29	19.58	22.50
    # 순이익률	11.34	9.50	11.26	16.96	9.49	13.29	15.20	17.51
    # ROE(%)	15.06	11.16	12.48	19.82	10.78	12.48	13.87
    # ROA(%)	10.53	8.07	9.01	14.46	7.68	9.01	9.95
    # 부채비율	37.09	35.25	35.87	34.44	36.17	35.87	39.20	34.10
    # 자본유보율	19,379.47	21,117.88	22,004.14		21,233.43	22,004.14	22,409.50
    # EPS(원)	135,673	109,883	136,760	259,983	27,099	42,912	46,457	64,133
    # PER(배)	9.78	11.47	13.18	9.19	14.17	13.18	13.58
    # BPS(원)	1,083,205	1,185,738	1,331,779	1,569,357	1,237,805	1,331,779	1,318,741	1,444,397
    # PBR(배)	1.23	1.06	1.35	1.52	1.29	1.35	1.56	1.65
    # 현금DPS(원)	20,000	21,000	28,500	35,925	0	27,500	7,000
    # 현금배당수익률	1.51	1.67	1.58	1.50
    # 현금배당성향(%)	13.00	16.42	17.81	0.14	0.00	55.66	12.98
    # 발행주식수(보통주)	147,299,337	147,299,337	140,679,337		140,679,337	140,679,337	140,679,337
