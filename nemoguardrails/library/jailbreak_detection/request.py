# SPDX-FileCopyrightText: Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import aiohttp
from typing import Optional

from nemoguardrails.actions import action

log = logging.getLogger(__name__)


@action(name="jailbreak heuristics")
async def jailbreak_heuristics(
    prompt: str,
    api_url: str = "http://localhost:1337/heuristics",
    lp_threshold: Optional[float] = None,
):
    payload = {"prompt": prompt, "lp_threshold": lp_threshold}

    async with aiohttp.ClientSession() as session:
        async with session.post(api_url, json=payload) as resp:
            if resp.status != 200:
                log.error(
                    f"Jailbreak check API request failed with status {resp.status}"
                )
                return None

            result = await resp.json()

            log.info(f"Prompt jailbreak check: {result}.")
            try:
                result = result["jailbreak"]
            except Exception:
                result = None
            return result
