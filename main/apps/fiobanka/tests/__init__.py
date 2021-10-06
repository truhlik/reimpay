import datetime

test_data = [{
  'transaction_id': '22978121284',
  'date': datetime.date(2020, 3, 6),
  'amount': -511.0,
  'currency': 'CZK',
  'account_number': '2701191435',
  'bank_code': '2010',
  'bank_name': 'Fio banka, a.s.',
  'user_identification': 'Vrácení přeplatku braingames - poslali naši provozi ještě extra mimo zápočet',
  'recipient_message': 'Vrácení přeplatku',
  'type': 'Platba převodem uvnitř banky',
  'executor': 'Nguyen, Marko',
  'comment': 'Vrácení přeplatku braingames - poslali naši provozi ještě extra mimo zápočet',
  'instruction_id': '26961313481',
  'constant_symbol': None,
  'variable_symbol': None,
  'specific_symbol': None,
  'account_name': None,
  'specification': None,
  'bic': None,
  'original_amount': None,
  'original_currency': None,
  'account_number_full': '2701191435/2010'
}, {
  'transaction_id': '22978140346',
  'date': datetime.date(2020, 3, 6),
  'amount': -149.0,
  'currency': 'CZK',
  'account_number': '2600285563',
  'bank_code': '2010',
  'bank_name': 'Fio banka, a.s.',
  'user_identification': 'provozo platební brány - email pohledávky z 24.2.2020',
  'recipient_message': 'provozo platební brány',
  'type': 'Platba převodem uvnitř banky',
  'executor': 'Nguyen, Marko',
  'comment': 'provozo platební brány - email pohledávky z 24.2.2020',
  'instruction_id': '26961424888',
  'constant_symbol': None,
  'variable_symbol': None,
  'specific_symbol': None,
  'account_name': None,
  'specification': None,
  'bic': None,
  'original_amount': None,
  'original_currency': None,
  'account_number_full': '2600285563/2010'
}, {
  'transaction_id': '22979163706',
  'date': datetime.date(2020, 3, 9),
  'amount': 2536.19,
  'currency': 'CZK',
  'account_number': '2108550230',
  'account_name': 'BENEFITY a.s.',
  'bank_code': '2700',
  'bank_name': 'UniCredit Bank Czech Republic and Slovakia, a.s.',
  'constant_symbol': '0308',
  'variable_symbol': '2002466739',
  'user_identification': 'BENEFITY a.s.',
  'type': 'Bezhotovostní příjem',
  'comment': 'BENEFITY a.s.',
  'instruction_id': '26965447505',
  'specific_symbol': None,
  'executor': None,
  'recipient_message': None,
  'specification': None,
  'bic': None,
  'original_amount': None,
  'original_currency': None,
  'account_number_full': '2108550230/2700'
}, {
  'transaction_id': '22979856685',
  'date': datetime.date(2020, 3, 9),
  'amount': 149.0,
  'currency': 'CZK',
  'account_number': '2600285563',
  'account_name': 'ComGate Payments, a.s.',
  'bank_code': '2010',
  'bank_name': 'Fio banka, a.s.',
  'variable_symbol': '0',
  'recipient_message': 'unknown',
  'type': 'Příjem převodem uvnitř banky',
  'comment': 'unknown',
  'instruction_id': '26968491047',
  'constant_symbol': None,
  'specific_symbol': None,
  'user_identification': None,
  'executor': None,
  'specification': None,
  'bic': None,
  'original_amount': None,
  'original_currency': None,
  'account_number_full': '2600285563/2010'
}, {
  'transaction_id': '22981539183',
  'date': datetime.date(2020, 3, 11),
  'amount': 1287.13,
  'currency': 'CZK',
  'account_number': '4631352',
  'account_name': 'ComGate Payments, a.',
  'bank_code': '0800',
  'bank_name': 'Česká spořitelna, a.s.',
  'constant_symbol': '0000',
  'variable_symbol': '119977892',
  'specific_symbol': '0',
  'user_identification': 'ComGate Payments, a.',
  'type': 'Bezhotovostní příjem',
  'comment': 'ComGate Payments, a.',
  'instruction_id': '26975924167',
  'executor': None,
  'recipient_message': None,
  'specification': None,
  'bic': None,
  'original_amount': None,
  'original_currency': None,
  'account_number_full': '4631352/0800'
}, {
  'transaction_id': '22982561474',
  'date': datetime.date(2020, 3, 12),
  'amount': 1068.77,
  'currency': 'CZK',
  'account_number': '43-1680820217',
  'account_name': 'EDENRED CZ S.R.O. -',
  'bank_code': '0100',
  'bank_name': 'Komerční banka a.s.',
  'constant_symbol': '0308',
  'variable_symbol': '563000299',
  'specific_symbol': '0',
  'user_identification': 'EDENRED CZ S.R.O. -',
  'recipient_message': '563-000299',
  'type': 'Bezhotovostní příjem',
  'comment': 'EDENRED CZ S.R.O. -',
  'instruction_id': '26980289851',
  'executor': None,
  'specification': None,
  'bic': None,
  'original_amount': None,
  'original_currency': None,
  'account_number_full': '43-1680820217/0100'
}, {
  'transaction_id': '22983100338',
  'date': datetime.date(2020, 3, 12),
  'amount': -1260.0,
  'currency': 'CZK',
  'account_number': '670100-2208571266',
  'bank_code': '6210',
  'bank_name': 'mBank S.A., organizační složka',
  'variable_symbol': '4183',
  'user_identification': 'Refundace objednávky escapemania Č. 4183',
  'recipient_message': 'Refundace objednávky escapemania Č. 4183',
  'type': 'Bezhotovostní platba',
  'executor': 'Nguyen, Marko',
  'comment': 'Refundace objednávky escapemania Č. 4183',
  'instruction_id': '26982713169',
  'constant_symbol': None,
  'specific_symbol': None,
  'account_name': None,
  'specification': None,
  'bic': None,
  'original_amount': None,
  'original_currency': None,
  'account_number_full': '670100-2208571266/6210'
}, {
  'transaction_id': '22987127187',
  'date': datetime.date(2020, 3, 17),
  'amount': -1129.5,
  'currency': 'CZK',
  'account_number': '0-1270003011',
  'bank_code': '3030',
  'bank_name': 'Air Bank a.s.',
  'constant_symbol': '0000',
  'variable_symbol': '0000020002',
  'specific_symbol': '0000000000',
  'recipient_message': 'Escape mania',
  'type': 'Okamžitá odchozí platba',
  'comment': 'Escape mania',
  'instruction_id': '27000100158',
  'user_identification': None,
  'executor': None,
  'account_name': None,
  'specification': None,
  'bic': None,
  'original_amount': None,
  'original_currency': None,
  'account_number_full': '0-1270003011/3030'
}, {
  'transaction_id': '22989162296',
  'date': datetime.date(2020, 3, 20),
  'amount': -236.78,
  'currency': 'CZK',
  'variable_symbol': '2605',
  'user_identification': 'Nákup: BALSAMIQ TRID1181024,  PO Box 1138, 4153673531, 95812, USA, dne 19.3.2020, částka  9.00 USD',
  'recipient_message': 'Nákup: BALSAMIQ TRID1181024,  PO Box 1138, 4153673531, 95812, USA, dne 19.3.2020, částka  9.00 USD',
  'type': 'Platba kartou',
  'executor': 'Černý, Martin',
  'comment': 'Nákup: BALSAMIQ TRID1181024,  PO Box 1138, 4153673531, 95812, USA, dne 19.3.2020, částka  9.00 USD',
  'instruction_id': '27008800214',
  'account_number': None,
  'bank_code': None,
  'constant_symbol': None,
  'specific_symbol': None,
  'account_name': None,
  'bank_name': None,
  'specification': None,
  'bic': None,
  'original_amount': None,
  'original_currency': None,
  'account_number_full': None
}, {
  'transaction_id': '22991208377',
  'date': datetime.date(2020, 3, 23),
  'amount': -14000.0,
  'currency': 'CZK',
  'account_number': '43-4551330207',
  'bank_code': '0100',
  'bank_name': 'Komerční banka a.s.',
  'variable_symbol': '2020006',
  'user_identification': 'endorfin napojení escapemania',
  'recipient_message': 'endorfin napojení escapemania',
  'type': 'Okamžitá odchozí platba',
  'executor': 'Nguyen, Marko',
  'comment': 'endorfin napojení escapemania',
  'instruction_id': '27017374763',
  'constant_symbol': None,
  'specific_symbol': None,
  'account_name': None,
  'specification': None,
  'bic': None,
  'original_amount': None,
  'original_currency': None,
  'account_number_full': '43-4551330207/0100'
}, {
  'transaction_id': '22999516242',
  'date': datetime.date(2020, 4, 2),
  'amount': 2527.0,
  'currency': 'CZK',
  'account_number': '2102143052',
  'account_name': 'Benefit Management s',
  'bank_code': '2700',
  'bank_name': 'UniCredit Bank Czech Republic and Slovakia, a.s.',
  'specific_symbol': '682688',
  'user_identification': 'Benefit Management s',
  'type': 'Bezhotovostní příjem',
  'comment': 'Benefit Management s',
  'instruction_id': '27048934804',
  'constant_symbol': None,
  'variable_symbol': None,
  'executor': None,
  'recipient_message': None,
  'specification': None,
  'bic': None,
  'original_amount': None,
  'original_currency': None,
  'account_number_full': '2102143052/2700'
}, {
  'transaction_id': '23001888105',
  'date': datetime.date(2020, 4, 6),
  'amount': -1300.5,
  'currency': 'CZK',
  'account_number': '2501264820',
  'bank_code': '2010',
  'bank_name': 'Fio banka, a.s.',
  'constant_symbol': '0000',
  'variable_symbol': '0000203001',
  'specific_symbol': '0000000000',
  'recipient_message': 'Escape mania',
  'type': 'Platba převodem uvnitř banky',
  'comment': 'Escape mania',
  'instruction_id': '27059283674',
  'user_identification': None,
  'executor': None,
  'account_name': None,
  'specification': None,
  'bic': None,
  'original_amount': None,
  'original_currency': None,
  'account_number_full': '2501264820/2010'
}, {
  'transaction_id': '23001888106',
  'date': datetime.date(2020, 4, 6),
  'amount': -2421.0,
  'currency': 'CZK',
  'account_number': '2501264820',
  'bank_code': '2010',
  'bank_name': 'Fio banka, a.s.',
  'constant_symbol': '0000',
  'variable_symbol': '0002030002',
  'specific_symbol': '0000000000',
  'recipient_message': 'Escape mania',
  'type': 'Platba převodem uvnitř banky',
  'comment': 'Escape mania',
  'instruction_id': '27059283675',
  'user_identification': None,
  'executor': None,
  'account_name': None,
  'specification': None,
  'bic': None,
  'original_amount': None,
  'original_currency': None,
  'account_number_full': '2501264820/2010'
}, {
  'transaction_id': '23001888107',
  'date': datetime.date(2020, 4, 6),
  'amount': -1309.5,
  'currency': 'CZK',
  'account_number': '2400681852',
  'bank_code': '2010',
  'bank_name': 'Fio banka, a.s.',
  'constant_symbol': '0000',
  'variable_symbol': '0000020018',
  'specific_symbol': '0000000000',
  'recipient_message': 'Escape mania',
  'type': 'Platba převodem uvnitř banky',
  'comment': 'Escape mania',
  'instruction_id': '27059283678',
  'user_identification': None,
  'executor': None,
  'account_name': None,
  'specification': None,
  'bic': None,
  'original_amount': None,
  'original_currency': None,
  'account_number_full': '2400681852/2010'
}, {
  'transaction_id': '23001888108',
  'date': datetime.date(2020, 4, 6),
  'amount': -1174.5,
  'currency': 'CZK',
  'account_number': '2600791474',
  'bank_code': '2010',
  'bank_name': 'Fio banka, a.s.',
  'constant_symbol': '0000',
  'variable_symbol': '0002020009',
  'specific_symbol': '0000000000',
  'recipient_message': 'Escape mania',
  'type': 'Platba převodem uvnitř banky',
  'comment': 'Escape mania',
  'instruction_id': '27059283679',
  'user_identification': None,
  'executor': None,
  'account_name': None,
  'specification': None,
  'bic': None,
  'original_amount': None,
  'original_currency': None,
  'account_number_full': '2600791474/2010'
}, {
  'transaction_id': '23009811893',
  'date': datetime.date(2020, 4, 16),
  'amount': -1309.5,
  'currency': 'CZK',
  'account_number': '2400681852',
  'bank_code': '2010',
  'bank_name': 'Fio banka, a.s.',
  'constant_symbol': '0000',
  'variable_symbol': '0000020028',
  'specific_symbol': '0000000000',
  'recipient_message': 'Escape mania',
  'type': 'Platba převodem uvnitř banky',
  'comment': 'Escape mania',
  'instruction_id': '27095285808',
  'user_identification': None,
  'executor': None,
  'account_name': None,
  'specification': None,
  'bic': None,
  'original_amount': None,
  'original_currency': None,
  'account_number_full': '2400681852/2010'
}, {
  'transaction_id': '23009811894',
  'date': datetime.date(2020, 4, 16),
  'amount': -1129.5,
  'currency': 'CZK',
  'account_number': '0-264610347',
  'bank_code': '0300',
  'bank_name': 'ČSOB, a.s.',
  'constant_symbol': '0000',
  'variable_symbol': '0200100444',
  'specific_symbol': '0000000000',
  'recipient_message': 'Escape mania',
  'type': 'Bezhotovostní platba',
  'comment': 'Escape mania',
  'instruction_id': '27095285809',
  'user_identification': None,
  'executor': None,
  'account_name': None,
  'specification': None,
  'bic': None,
  'original_amount': None,
  'original_currency': None,
  'account_number_full': '0-264610347/0300'
}, {
  'transaction_id': '23009811895',
  'date': datetime.date(2020, 4, 16),
  'amount': -9778.5,
  'currency': 'CZK',
  'account_number': '0-9763796001',
  'bank_code': '5500',
  'bank_name': 'Raiffeisenbank a.s.',
  'constant_symbol': '0000',
  'variable_symbol': '0020200003',
  'specific_symbol': '0000000000',
  'recipient_message': 'Escape mania',
  'type': 'Bezhotovostní platba',
  'comment': 'Escape mania',
  'instruction_id': '27095285810',
  'user_identification': None,
  'executor': None,
  'account_name': None,
  'specification': None,
  'bic': None,
  'original_amount': None,
  'original_currency': None,
  'account_number_full': '0-9763796001/5500'
}, {
  'transaction_id': '23009811896',
  'date': datetime.date(2020, 4, 16),
  'amount': -5598.0,
  'currency': 'CZK',
  'account_number': '0-9763796001',
  'bank_code': '5500',
  'bank_name': 'Raiffeisenbank a.s.',
  'constant_symbol': '0000',
  'variable_symbol': '0020200002',
  'specific_symbol': '0000000000',
  'recipient_message': 'Escape mania',
  'type': 'Bezhotovostní platba',
  'comment': 'Escape mania',
  'instruction_id': '27095285811',
  'user_identification': None,
  'executor': None,
  'account_name': None,
  'specification': None,
  'bic': None,
  'original_amount': None,
  'original_currency': None,
  'account_number_full': '0-9763796001/5500'
}, {
  'transaction_id': '23009811897',
  'date': datetime.date(2020, 4, 16),
  'amount': -1129.5,
  'currency': 'CZK',
  'account_number': '0-264610347',
  'bank_code': '0300',
  'bank_name': 'ČSOB, a.s.',
  'constant_symbol': '0000',
  'variable_symbol': '0200100439',
  'specific_symbol': '0000000000',
  'recipient_message': 'Escape mania',
  'type': 'Bezhotovostní platba',
  'comment': 'Escape mania',
  'instruction_id': '27095285814',
  'user_identification': None,
  'executor': None,
  'account_name': None,
  'specification': None,
  'bic': None,
  'original_amount': None,
  'original_currency': None,
  'account_number_full': '0-264610347/0300'
}, {
  'transaction_id': '23009811898',
  'date': datetime.date(2020, 4, 16),
  'amount': -1039.5,
  'currency': 'CZK',
  'account_number': '0-1384470013',
  'bank_code': '3030',
  'bank_name': 'Air Bank a.s.',
  'constant_symbol': '0000',
  'variable_symbol': '0000201004',
  'specific_symbol': '0000000000',
  'recipient_message': 'Escape mania',
  'type': 'Bezhotovostní platba',
  'comment': 'Escape mania',
  'instruction_id': '27095285816',
  'user_identification': None,
  'executor': None,
  'account_name': None,
  'specification': None,
  'bic': None,
  'original_amount': None,
  'original_currency': None,
  'account_number_full': '0-1384470013/3030'
}, {
  'transaction_id': '23009811899',
  'date': datetime.date(2020, 4, 16),
  'amount': -1300.5,
  'currency': 'CZK',
  'account_number': '2501264820',
  'bank_code': '2010',
  'bank_name': 'Fio banka, a.s.',
  'constant_symbol': '0000',
  'variable_symbol': '0000203001',
  'specific_symbol': '0000000000',
  'recipient_message': 'Escape mania',
  'type': 'Platba převodem uvnitř banky',
  'comment': 'Escape mania',
  'instruction_id': '27095285817',
  'user_identification': None,
  'executor': None,
  'account_name': None,
  'specification': None,
  'bic': None,
  'original_amount': None,
  'original_currency': None,
  'account_number_full': '2501264820/2010'
}, {
  'transaction_id': '23011630199',
  'date': datetime.date(2020, 4, 20),
  'amount': -231.73,
  'currency': 'CZK',
  'variable_symbol': '2605',
  'user_identification': 'Nákup: BALSAMIQ TRID1193835,  PO Box 1138, 4153673531, 95812, USA, dne 19.4.2020, částka  9.00 USD',
  'recipient_message': 'Nákup: BALSAMIQ TRID1193835,  PO Box 1138, 4153673531, 95812, USA, dne 19.4.2020, částka  9.00 USD',
  'type': 'Platba kartou',
  'executor': 'Černý, Martin',
  'comment': 'Nákup: BALSAMIQ TRID1193835,  PO Box 1138, 4153673531, 95812, USA, dne 19.4.2020, částka  9.00 USD',
  'instruction_id': '27103005261',
  'account_number': None,
  'bank_code': None,
  'constant_symbol': None,
  'specific_symbol': None,
  'account_name': None,
  'bank_name': None,
  'specification': None,
  'bic': None,
  'original_amount': None,
  'original_currency': None,
  'account_number_full': None
}, {
  'transaction_id': '23013520309',
  'date': datetime.date(2020, 4, 21),
  'amount': 2501.87,
  'currency': 'CZK',
  'account_number': '59942',
  'account_name': 'Up Česká republika s',
  'bank_code': '0800',
  'bank_name': 'Česká spořitelna, a.s.',
  'constant_symbol': '0308',
  'variable_symbol': '20045608',
  'specific_symbol': '81429',
  'user_identification': 'Up Česká republika s',
  'type': 'Bezhotovostní příjem',
  'comment': 'Up Česká republika s',
  'instruction_id': '27111097935',
  'executor': None,
  'recipient_message': None,
  'specification': None,
  'bic': None,
  'original_amount': None,
  'original_currency': None,
  'account_number_full': '59942/0800'
}, {
  'transaction_id': '23015639737',
  'date': datetime.date(2020, 4, 24),
  'amount': 1138.13,
  'currency': 'CZK',
  'account_number': '4631352',
  'account_name': 'ComGate Payments, a.',
  'bank_code': '0800',
  'bank_name': 'Česká spořitelna, a.s.',
  'constant_symbol': '0000',
  'variable_symbol': '129092165',
  'specific_symbol': '0',
  'user_identification': 'ComGate Payments, a.',
  'type': 'Bezhotovostní příjem',
  'comment': 'ComGate Payments, a.',
  'instruction_id': '27120100272',
  'executor': None,
  'recipient_message': None,
  'specification': None,
  'bic': None,
  'original_amount': None,
  'original_currency': None,
  'account_number_full': '4631352/0800'
}]
