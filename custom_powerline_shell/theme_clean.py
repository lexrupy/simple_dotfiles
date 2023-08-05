from powerline_shell.themes.default import DefaultColor


class Color(DefaultColor):
    """Basic theme which only uses colors in 0-15 range"""

    USERNAME_FG = 8
    USERNAME_BG = 15
    USERNAME_ROOT_BG = 1

    HOSTNAME_FG = 8
    HOSTNAME_BG = 7

    HOME_SPECIAL_DISPLAY = False
    # PATH_BG = 8  # dark grey
    PATH_BG = 0
    PATH_FG = 10
    CWD_FG = 10
    SEPARATOR_FG = 0

    READONLY_BG = 1
    READONLY_FG = 15

    # REPO_CLEAN_BG = 11
    # REPO_CLEAN_FG = 0
    # REPO_DIRTY_BG = 9
    # REPO_DIRTY_FG = 255

    REPO_CLEAN_BG = 0
    REPO_CLEAN_FG = 11
    REPO_DIRTY_BG = 0
    REPO_DIRTY_FG = 9  # white
    GIT_STASH_BG = 0
    GIT_STASH_FG = 15

    GIT_AHEAD_BG = 0

    GIT_BEHIND_BG = 0

    GIT_STAGED_BG = 0

    GIT_NOTSTAGED_BG = 0

    GIT_UNTRACKED_BG = 0

    GIT_CONFLICTED_BG = 0

    JOBS_FG = 14
    JOBS_BG = 8

    CMD_PASSED_BG = 0
    CMD_PASSED_FG = 15
    CMD_FAILED_BG = 0
    CMD_FAILED_FG = 11

    SVN_CHANGES_BG = REPO_DIRTY_BG
    SVN_CHANGES_FG = REPO_DIRTY_FG

    VIRTUAL_ENV_FG = 200
    VIRTUAL_ENV_BG = 0
    # VIRTUAL_ENV_FG = 200
    # VIRTUAL_ENV_BG = 240

    AWS_PROFILE_FG = 14
    AWS_PROFILE_BG = 8

    # TIME_FG = 255
    # TIME_BG = 39
    TIME_FG = 39
    TIME_BG = 0
