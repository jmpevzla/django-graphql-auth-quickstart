import graphene

from graphene_django.types import DjangoObjectType

from graphql_auth.schema import UserQuery, MeQuery
from graphql_auth import mutations
from users.models import Category
from graphql_jwt.decorators import login_required

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category

class CatQuery(object):
    all_categories = graphene.List(CategoryType)

    @login_required
    def resolve_all_categories(self, info, **kwargs):
        return Category.objects.all()

class AuthMutation(graphene.ObjectType):
   register = mutations.Register.Field()
   verify_account = mutations.VerifyAccount.Field()
   token_auth = mutations.ObtainJSONWebToken.Field()
   update_account = mutations.UpdateAccount.Field()

class Query(CatQuery, UserQuery, MeQuery, graphene.ObjectType):
    pass

class Mutation(AuthMutation, graphene.ObjectType):
   pass

schema = graphene.Schema(query=Query, mutation=Mutation)