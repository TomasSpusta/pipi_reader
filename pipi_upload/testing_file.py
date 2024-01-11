import github_check
import log
import network_check

log.open_sh("test")

local_repo = "/home/bluebox/pipi_reader"
github_check.ghub_check ("develop_cleaning")

network_check.connection_check()
