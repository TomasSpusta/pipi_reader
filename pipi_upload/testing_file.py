import github_check
import log

log.open_sh("test")

local_repo = "/home/bluebox/pipi_reader"
github_check.ghub_check ("develop_cleaning")
