"""
Copyright (c) 2021, VRAI Labs and/or its affiliates. All rights reserved.

This software is licensed under the Apache License, Version 2.0 (the
"License") as published by the Apache Software Foundation.

You may not use this file except in compliance with the License. You may
obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
License for the specific language governing permissions and limitations
under the License.
"""
from .recipe import ThirdPartyEmailPasswordRecipe
from . import exceptions


def init(config=None):
    return ThirdPartyEmailPasswordRecipe.init(config)


async def create_email_verification_token(user_id: str):
    return await ThirdPartyEmailPasswordRecipe.get_instance().email_verification_recipe.recipe_implementation.create_email_verification_token(user_id)


async def verify_email_using_token(token: str):
    return await ThirdPartyEmailPasswordRecipe.get_instance().email_verification_recipe.recipe_implementation.verify_email_using_token(token)


async def is_email_verified(user_id: str):
    return await ThirdPartyEmailPasswordRecipe.get_instance().email_verification_recipe.recipe_implementation.is_email_verified(user_id)


async def get_users_oldest_first(limit: int = None, next_pagination: str = None):
    return await ThirdPartyEmailPasswordRecipe.get_instance().recipe_implementation.get_users_oldest_first(limit, next_pagination)


async def get_users_newest_first(limit: int = None, next_pagination: str = None):
    return await ThirdPartyEmailPasswordRecipe.get_instance().recipe_implementation.get_users_newest_first(limit, next_pagination)


async def get_user_count():
    return await ThirdPartyEmailPasswordRecipe.get_instance().recipe_implementation.get_user_count()


async def get_user_by_id(user_id: str):
    return await ThirdPartyEmailPasswordRecipe.get_instance().recipe_implementation.get_user_by_id(user_id)


async def get_user_by_third_party_info(third_party_id: str, third_party_user_id: str):
    return await ThirdPartyEmailPasswordRecipe.get_instance().recipe_implementation.get_user_by_third_party_info(third_party_id, third_party_user_id)


async def sign_in_up(third_party_id: str, third_party_user_id: str, email: str, email_verified: bool):
    return await ThirdPartyEmailPasswordRecipe.get_instance().recipe_implementation.sign_in_up(third_party_id, third_party_user_id, email, email_verified)


async def create_reset_password_token(user_id: str):
    return await ThirdPartyEmailPasswordRecipe.get_instance().recipe_implementation.create_reset_password_token(user_id)


async def reset_password_using_token(token: str, new_password: str):
    return await ThirdPartyEmailPasswordRecipe.get_instance().recipe_implementation.reset_password_using_token(token, new_password)


async def sign_in(email: str, password: str):
    return await ThirdPartyEmailPasswordRecipe.get_instance().recipe_implementation.sign_in(email, password)


async def sign_up(email: str, password: str):
    return await ThirdPartyEmailPasswordRecipe.get_instance().recipe_implementation.sign_up(email, password)