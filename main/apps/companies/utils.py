def company_dir_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/company_<id>/<filename>
    return 'company_{0}/{1}'.format(instance.id, filename)


def get_company_data_for_fakturoid(company):
    data = {
        'name': company.name,
        'street': "{} {}".format(company.street, company.street_number),
        'city': company.city,
        'zip': company.zip,
        'registration_no': company.reg_number,
        'vat_no': company.vat_number,
        'email': company.email,
        'phone': company.phone,
    }
    return data
