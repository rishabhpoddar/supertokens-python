# Copyright (c) 2021, VRAI Labs and/or its affiliates. All rights reserved.
#
# This software is licensed under the Apache License, Version 2.0 (the
# "License") as published by the Apache Software Foundation.
#
# You may not use this file except in compliance with the License. You may
# obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
from __future__ import annotations

from typing import Any, Dict, Union

from supertokens_python.recipe.passwordless.interfaces import (
    APIInterface, APIOptions, ConsumeCodePostExpiredUserInputCodeErrorResponse,
    ConsumeCodePostGeneralErrorResponse,
    ConsumeCodePostIncorrectUserInputCodeErrorResponse,
    ConsumeCodePostOkResponse, ConsumeCodePostResponse,
    ConsumeCodePostRestartFlowErrorResponse)

from ...passwordless.types import User
from ..interfaces import APIInterface as ThirdPartyPasswordlessAPIInterface


def get_interface_impl(
        api_implementation: ThirdPartyPasswordlessAPIInterface) -> APIInterface:
    implementation = APIInterface()

    implementation.disable_email_exists_get = api_implementation.disable_passwordless_user_email_exists_get
    implementation.disable_resend_code_post = api_implementation.disable_resend_code_post
    implementation.disable_create_code_post = api_implementation.disable_create_code_post
    implementation.disable_consume_code_post = api_implementation.disable_consume_code_post
    implementation.disable_phone_number_exists_get = api_implementation.disable_passwordless_user_phone_number_exists_get

    implementation.email_exists_get = api_implementation.passwordless_user_email_exists_get
    if not implementation.disable_consume_code_post:
        async def consume_code_post(pre_auth_session_id: str,
                                    user_input_code: Union[str, None],
                                    device_id: Union[str, None],
                                    link_code: Union[str, None],
                                    api_options: APIOptions,
                                    user_context: Dict[str, Any]) -> ConsumeCodePostResponse:
            otherType = await api_implementation.consume_code_post(pre_auth_session_id, user_input_code, device_id, link_code, api_options, user_context)

            if otherType.is_ok:
                if otherType.created_new_user is None or otherType.user is None or otherType.session is None:
                    raise Exception("Should never come here")
                return ConsumeCodePostOkResponse(otherType.created_new_user, User(otherType.user.user_id, otherType.user.email, otherType.user.phone_number, otherType.user.time_joined), otherType.session)
            if otherType.is_expired_user_input_code_error:
                if otherType.failed_code_input_attempt_count is None or otherType.maximum_code_input_attempts is None:
                    raise Exception("Should never come here")
                return ConsumeCodePostExpiredUserInputCodeErrorResponse(otherType.failed_code_input_attempt_count, otherType.maximum_code_input_attempts)
            if otherType.is_general_error:
                if otherType.message is None:
                    raise Exception("Should never come here")
                return ConsumeCodePostGeneralErrorResponse(otherType.message)
            if otherType.is_incorrect_user_input_code_error:
                if otherType.failed_code_input_attempt_count is None or otherType.maximum_code_input_attempts is None:
                    raise Exception("Should never come here")
                return ConsumeCodePostIncorrectUserInputCodeErrorResponse(otherType.failed_code_input_attempt_count, otherType.maximum_code_input_attempts)

            # restart flow error
            return ConsumeCodePostRestartFlowErrorResponse()

        implementation.consume_code_post = consume_code_post

    implementation.create_code_post = api_implementation.create_code_post
    implementation.phone_number_exists_get = api_implementation.passwordless_user_phone_number_exists_get
    implementation.resend_code_post = api_implementation.resend_code_post

    return implementation
