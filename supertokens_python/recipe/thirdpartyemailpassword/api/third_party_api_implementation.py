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

from supertokens_python.recipe.thirdparty.interfaces import APIInterface, APIOptions
from supertokens_python.recipe.thirdparty.provider import Provider
from supertokens_python.recipe.thirdpartyemailpassword.interfaces import APIInterface as ThirdPartyEmailPasswordAPIInterface, \
    SignInUpAPIInput, SignInUpPostThirdPartyOkResponse, SignInUpPostThirdPartyNoEmailGivenByProviderResponse


async def get_interface_impl(api_implementation: ThirdPartyEmailPasswordAPIInterface) -> APIInterface:
    implementation = APIInterface()

    if api_implementation.disable_authorisation_url_get:
        implementation.disable_authorisation_url_get = True
    if api_implementation.disable_sign_in_up_post:
        implementation.disable_sign_in_up_post = True

    if not implementation.disable_sign_in_up_post:
        async def sign_in_up_post(provider: Provider, code: str, redirect_uri: str,
                                  api_options: APIOptions):
            result = await api_implementation.sign_in_up_post(
                SignInUpAPIInput('thirdparty', provider=provider, code=code, redirect_uri=redirect_uri,
                                 options=api_options))

            if result.is_ok:
                if result.user.third_party_info is None or result.type == 'emailpassword':
                    raise Exception('Should never come here')
                return SignInUpPostThirdPartyOkResponse(result.user, result.created_new_user, result.auth_code_response)

            elif result.status == 'NO_EMAIL_GIVEN_BY_PROVIDER':
                return SignInUpPostThirdPartyNoEmailGivenByProviderResponse()
            else:
                raise Exception('Should never come here')

        implementation.sign_in_up_post = sign_in_up_post

    implementation.authorisation_url_get = api_implementation.authorisation_url_get

    return implementation