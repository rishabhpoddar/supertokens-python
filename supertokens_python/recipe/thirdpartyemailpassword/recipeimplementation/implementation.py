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
from __future__ import annotations

from typing import TYPE_CHECKING, Union, List

from ..types import User, UsersResponse, NextPaginationToken
from ..utils import extract_pagination_token, combine_pagination_results
from ...emailpassword.interfaces import UpdateEmailOrPasswordResult, ResetPasswordUsingTokenResult, \
    CreateResetPasswordResult, SignUpResult, SignInResult
from ...thirdparty.interfaces import SignInUpResult

if TYPE_CHECKING:
    from supertokens_python.querier import Querier
from ..interfaces import (
    RecipeInterface
)
from supertokens_python.recipe.emailpassword.recipe_implementation import RecipeImplementation as EmailPasswordImplementation
from supertokens_python.recipe.thirdparty.recipe_implementation import RecipeImplementation as ThirdPartyImplementation


class RecipeImplementation(RecipeInterface):
    def __init__(self, emailpassword_querier: Querier, thirdparty_querier: Union[Querier, None]):
        super().__init__()
        self.emailpassword_implementation = EmailPasswordImplementation(emailpassword_querier)
        self.thirdparty_implementation = None
        if thirdparty_querier is not None:
            self.thirdparty_implementation = ThirdPartyImplementation(thirdparty_querier)

    async def get_user_by_id(self, user_id: str) -> Union[User, None]:
        pass

    async def get_users_by_email(self, email: str) -> List[User]:
        pass

    async def get_user_by_thirdparty_info(self, third_party_id: str, third_party_user_id: str) -> Union[User, None]:
        pass

    async def sign_in_up(self, third_party_id: str, third_party_user_id: str, email: str,
                         email_verified: bool) -> SignInUpResult:
        pass

    async def sign_in(self, email: str, password: str) -> SignInResult:
        return await self.emailpassword_implementation.sign_in(email, password)

    async def sign_up(self, email: str, password: str) -> SignUpResult:
        return await self.emailpassword_implementation.sign_up(email, password)

    async def create_reset_password_token(self, user_id: str) -> CreateResetPasswordResult:
        return await self.emailpassword_implementation.create_reset_password_token(user_id)

    async def reset_password_using_token(self, token: str, new_password: str) -> ResetPasswordUsingTokenResult:
        return await self.emailpassword_implementation.reset_password_using_token(token, new_password)

    async def update_email_or_password(self, user_id: str, email: str = None,
                                       password: str = None) -> UpdateEmailOrPasswordResult:
        return await self.emailpassword_implementation.update_email_or_password(user_id, email, password)

    async def get_users_oldest_first(self, limit: int = None, next_pagination: str = None) -> UsersResponse:
        if limit is None:
            limit = 100
        next_pagination_tokens = NextPaginationToken('null', 'null')
        if next_pagination is not None:
            next_pagination_tokens = extract_pagination_token(next_pagination)
        email_password_result_promise = self.emailpassword_implementation.get_users_oldest_first(limit,
                                                                                                 next_pagination_tokens.email_password_pagination_token)
        third_party_result = UsersResponse([],
                                           None) if self.thirdparty_implementation is None else await self.thirdparty_implementation.get_users_oldest_first(
            limit, next_pagination_tokens.third_party_pagination_token)
        email_password_result = await email_password_result_promise
        return combine_pagination_results(third_party_result, email_password_result, limit, True)

    async def get_users_newest_first(self, limit: int = None, next_pagination: str = None) -> UsersResponse:
        if limit is None:
            limit = 100
        next_pagination_tokens = NextPaginationToken('null', 'null')
        if next_pagination is not None:
            next_pagination_tokens = extract_pagination_token(next_pagination)
        email_password_result_promise = self.emailpassword_implementation.get_users_newest_first(limit,
                                                                                                 next_pagination_tokens.email_password_pagination_token)
        third_party_result = UsersResponse([],
                                           None) if self.thirdparty_implementation is None else await self.thirdparty_implementation.get_users_newest_first(
            limit, next_pagination_tokens.third_party_pagination_token)
        email_password_result = await email_password_result_promise
        return combine_pagination_results(third_party_result, email_password_result, limit, True)

    async def get_user_count(self) -> int:
        emailpassword_count = await self.emailpassword_implementation.get_user_count()
        thirdparty_count = await self.thirdparty_implementation.get_user_count() if self.thirdparty_implementation is not None else 0
        return emailpassword_count + thirdparty_count