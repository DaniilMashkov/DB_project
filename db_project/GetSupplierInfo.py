class GetSupplierInfo:
    id = 0
    products_list = {}

    @classmethod
    def init(cls, supplier: dict):
        GetSupplierInfo.id += 1
        splitted_cont = supplier.get('contact').split(', ')
        splitted_address = supplier.get('address').split(';')

        cls.comp_name = supplier.get('company_name')
        cls.phone = supplier.get('phone')
        cls.fax = supplier.get('fax')
        cls.homepage = supplier.get('homepage')
        cls.cont_name = splitted_cont[0]
        cls.cont_title = splitted_cont[1]
        cls.country = splitted_address[0]
        cls.region = splitted_address[1]
        cls.postal_code = splitted_address[2]
        cls.city = splitted_address[3]
        cls.address = splitted_address[4]
        cls.products = supplier.get('products')

        for prod in cls.products:
            cls.products_list.update({prod: cls.id})

    @classmethod
    def to_tuple(cls):
        return tuple([cls.id, cls.comp_name, cls.cont_name, cls.cont_title, cls.address, cls.city,
                      cls.region, cls.postal_code, cls.country, cls.phone, cls.fax, cls.homepage])


