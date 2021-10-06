def addTrailingSpaces(text, number):
    """Function that adds extra spaces after text."""
    text += number * " "
    return text


def createSMV(createPDS, data):
    """Function that creates a SMV(Sumační věta)"""
    output = ""
    # 1
    # Sumacni veta musi mit vzdy na zacatku 0

    output += "0"
    # 2
    output += data['DateVDS']
    # 3
    output += " "
    # 4
    output += data['SerialNumber'].zfill(2)
    # 5
    output += data['SenderNumber']
    # 6
    output += data['BankNumber']
    # 7
    output += 3 * " "
    # 8
    output += data['AccountPrefix'].zfill(6)
    # 9
    output += data['AccountNumber'].zfill(10)
    # 10
    output += data['VariableSymbol'].zfill(10)
    # 11
    output += data['ConstantSymbol'].zfill(4)
    # 12
    output += data['SpecificSymbol'].zfill(10)
    # 13
    output += data['AmountSM'].zfill(12)
    # 14
    output += data['PriceSM'].zfill(12)
    # 15
    output += data['SentenceNumber'].zfill(5)
    if not createPDS:
        # 16
        output += 1 * " "
        # 17
        output += data['Validity']
        # 18
        output += 10 * " "
    else:
        # 16
        output += data['ListNumber'].zfill(3)
        # 17
        output += 16 * " "
    # 19
    output += data['PaymentType']
    # 20
    output += data['BankCodeSender'].zfill(4)
    # 21
    output += data['AccountPrefixSender'].zfill(6)
    # 22
    output += data['AccountNumberSender'].zfill(10)
    # 23
    output += data['ConstantSymbolSender'].zfill(4)
    # 24
    if not createPDS:
        output += 139 * " " + "\n"
    else:
        output += 99 * " " + "\n"

    return output


def createPLV(createPDS, data_array, ID):
    """Function that creates PLV(Položková věta)."""
    output = ""
    """Forloop ktery prochazi vsechny polozkove
     vety a hleda ty, ktere maji stejne id jako sumacni veta"""
    for data in data_array['polozkove_vety']:
        if data['ID'] == ID:
            # Polozkova veta musi mit vzdy na zacatku 1
            # 1
            output += "1"
            # 2
            output += data['SerialNumberPV'].zfill(5)
            # 3
            SpecificationSender = data['SpecificationSender']
            output += "*" + addTrailingSpaces(
                SpecificationSender, 15 - len(SpecificationSender) - 1)
            # 4
            SenderInfo = data['SenderInfo']
            output += addTrailingSpaces(SenderInfo, 40 - len(SenderInfo))
            # 5
            Street = data['Street']
            output += addTrailingSpaces(Street, 40 - len(Street))
            # 6
            HouseNumber = data['HouseNumber']
            output += addTrailingSpaces(HouseNumber, 8 - len(HouseNumber))
            # 7
            PartOfCity = data['PartOfCity']
            output += addTrailingSpaces(PartOfCity, 40 - len(PartOfCity))
            # 8
            City = data['City']
            output += addTrailingSpaces(City, 40 - len(City))
            # 9
            output += data['ZipCode']
            if not createPDS:
                # 10
                Message = data['Message']
                output += addTrailingSpaces(Message, 60 - len(Message))
                # 11
                output += data['Services']
                # 12
                output += data['PaymentDeadline']
            # 13
            output += data['AmountPV'].zfill(10)

            if createPDS:
                output += data['PricePV'].zfill(10)

                output += data['PodaciCislo'].zfill(5)

                output += data['DistrictStamp']

                output += data['SubmissionDate']

            output += "\n"

    return output


def create_vstupni_datovy_soubor(data) -> str:
    """Function that creates VDS(Vstupní datový soubor)"""
    file_data = ""
    for sm_data in data['sumacni_vety']:
        smv = createSMV(False, sm_data)
        plv = createPLV(False, data, sm_data['ID'])
        file_data += smv + plv

    # text_file = open(path, "w+")
    # text_file.write(file_data)
    # text_file.close()
    return file_data


def create_podaci_stvrzenka(data) -> str:
    """Function that creates PDS(Podací stvrzenka)"""
    file_data = ""
    for sm_data in data['sumacni_vety']:
        smv = createSMV(True, sm_data)
        plv = createPLV(True, data, sm_data['ID'])
        file_data += smv + plv

    # text_file = open(path, "w+")
    # text_file.write(file_data)
    # text_file.close()
    return file_data
