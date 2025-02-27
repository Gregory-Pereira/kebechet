#!/usr/bin/env python3
# Kebechet
# Copyright(C) 2021 Kevin Postlethwait
#
# This program is free software: you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Report information about repository and Kebechet itself."""

import logging
import typing
import importlib.resources as pkg_resources

from kebechet.managers.manager import ManagerBase
from kebechet.utils import cloned_repo
from . import resources

_INFO_ISSUE_NAME = "Kebechet info"

_LOGGER = logging.getLogger(__name__)
# Github and Gitlab events on which the manager acts upon.
_EVENTS_SUPPORTED = ["issues", "issue"]


_PR_BODY = """## Automatic configuration initialization
The Kebechet app was installed on this repository but no configuration was
found.  This PR contains basic configuration of runtime environments and
managers."""

_BRANCH_NAME = "initial_thoth_config"


class ConfigInitializer(ManagerBase):
    """Manager for submitting information about running Kebechet instance."""

    def run(self) -> typing.Optional[dict]:  # type: ignore
        """Check for info issue and close it with a report."""
        thoth_config = pkg_resources.read_text(resources, "simple.thoth.yaml")

        with cloned_repo(self, depth=1, branch=self.project.default_branch) as repo:
            prs = self.get_prs_by_branch(_BRANCH_NAME)
            if len(prs) > 0:
                _LOGGER.debug("PR initializing .thoth.yaml already exists skipping...")
                return None
            repo.git.checkout("HEAD", b=_BRANCH_NAME)
            with open(".thoth.yaml", "w+") as f:
                f.write(thoth_config)
            repo.index.add([".thoth.yaml"])
            repo.index.commit("Initialize .thoth.yaml with basic configuration")
            repo.remote().push(_BRANCH_NAME)
            self.project.create_pr(
                title="Thoth Configuration Initialization",
                body=_PR_BODY,
                target_branch=self.project.default_branch,
                source_branch=_BRANCH_NAME,
            )
