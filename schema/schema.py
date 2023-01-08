import strawberry
from model import password_info
from resolver.verify import validadePass
from strawberry.fastapi import GraphQLRouter

# Graphql Schema in strawberry format 
@strawberry.type
class Query:
    verify: password_info.PasswordInfo = strawberry.field(resolver=validadePass)

schema = strawberry.Schema(
    query=Query,
)

# using a GraphQLRouter object to integrate with fastAPI 
graphql_app = GraphQLRouter(schema)