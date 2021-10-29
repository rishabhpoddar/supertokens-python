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

from pytest import mark

from supertokens_python import init
from supertokens_python.recipe import session
from supertokens_python.recipe.session import SessionRecipe
from supertokens_python.recipe.session.asyncio import create_new_session
from tests.utils import (
    reset, setup_st, clean_st, start_st
)


def setup_function(f):
    reset()
    clean_st()
    setup_st()


def teardown_function(f):
    reset()
    clean_st()


@mark.asyncio
async def test_that_once_the_info_is_loaded_it_doesnt_query_again():
    init({
        'supertokens': {
            'connection_uri': "http://localhost:3567",
        },
        'framework': 'fastapi',
        'app_info': {
            'app_name': "SuperTokens Demo",
            'api_domain': "http://api.supertokens.io",
            'website_domain': "supertokens.io",
        },
        'recipe_list': [session.init({
            'anti_csrf': 'VIA_TOKEN'
        })
        ],
    })
    start_st()

    s = SessionRecipe.get_instance()

    response = await create_new_session(s.recipe_implementation, "", {}, {})

    assert response.get_session_data() is not None
    assert response.get_access_token() is not None
    assert response.new_refresh_token_info is not None
    assert response.new_id_refresh_token_info is not None
    assert response.new_anti_csrf_token is not None

    await create_new_session(s.recipe_implementation, response.get_access_token())
