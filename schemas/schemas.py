from marshmallow import Schema, fields


class Itemschemas(Schema):
    id = fields.Str(dump_only= True)
    name = fields.Str(required= True)
    price = fields.Float(required= True)
    store_id = fields.Int(required= True)


class ItemUpdateSchemas(Schema):
    name = fields.Str(required= True)
    price = fields.Int(required= True)


class StoreSchema(Schema):
    id = fields.Str(dump_only= True)
    name = fields.Str(required= True)

